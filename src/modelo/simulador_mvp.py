"""Alternativas C4/C1/C3 e horizonte automático. Legado: simulador.py intacto.

[DEC] Reparos são serviços FIFO elegíveis após o fim original, com demanda
original e um agente. Não geram novos defeitos. TR mede esforço efetivamente
pago; ocupação é ceil(esforço), explicitada separadamente. Não retroagimos
precedências já liberadas nem apagamos omissões históricas. Ver PLANO_MVP.md.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, replace
import numpy as np
from simulador import Simulacao, v


def risco_porta(p0, p_heu, heuristico, rho):
    """C4: excesso no complemento apenas em P1 e acima do limiar de sobrecarga."""
    q=max(0.,2*p_heu-1.)
    if not heuristico or rho==0. or q==0.:
        return p0  # identidade exata para o controle, sem cancelamento numérico
    return 1.-(1.-p0)*(1.-rho*q)


@dataclass(frozen=True)
class OpcoesMVP:
    fator_omissao: float = .75
    rho_omissao: float | None = None
    retrabalho_fila: bool = True
    canal_erro_direto: str = 'ativo'
    lei_confianca: str = 'constante'
    lei_tempo_aprendizado: str = 'unitario'
    comunicacao_crowder: bool = False
    reset_competencia: bool = False
    instrumentar_tarefas: bool = True
    horizonte_automatico: bool = True
    limite_horizonte_fator: int = 256
    politica_porta2: str = 'nominal'
    tau_portao: float | None = None
    tau_rede: float | None = None

    def __post_init__(self):
        if self.canal_erro_direto not in {'ativo','desligado'}:
            raise ValueError('canal de erro direto desconhecido')
        if self.rho_omissao is not None and not 0<=self.rho_omissao<=1:
            raise ValueError('rho_omissao fora de [0,1]')
        if self.lei_tempo_aprendizado not in {'unitario','crowder_eq3'}:
            raise ValueError('lei de tempo de aprendizado desconhecida')
        if self.lei_confianca not in {'constante','crowder'}:
            raise ValueError('lei de confiança desconhecida')
        if self.politica_porta2 not in {'nominal','sem_assistencia','assistencia_universal','sem_filtro_competencia'}:
            raise ValueError('política Porta 2 desconhecida')
        if not 0 < self.fator_omissao <= 1 or self.limite_horizonte_fator < 1:
            raise ValueError('fator de duração/horizonte inválido')
        for x in [self.tau_portao,self.tau_rede]:
            if x is not None and not 0 <= x <= 1: raise ValueError('confiança fora de [0,1]')


class SimulacaoMVP(Simulacao):
    def __init__(self,*args,opcoes=None,**kwargs):
        self.opcoes=opcoes or OpcoesMVP()
        super().__init__(*args,**kwargs)
        if self.opcoes.rho_omissao is None:
            self.opcoes=replace(self.opcoes,rho_omissao=float(v(self.par['risco']['rho_omissao'])))
        if self.ablacoes: raise ValueError('use politica_porta2 na alternativa MVP')
        if self.makespan_cpm <= 0 or not self.agentes:
            raise ValueError('CPM e número de agentes devem ser positivos')
        for tar in self.tarefas.values():
            if any(d<0 or d>cap for d,cap in zip(tar.demanda,self.disponibilidade)):
                raise ValueError(f'recurso inviável na tarefa {tar.ident}')
        self.competencias_iniciais={a.ident:a.competencia for a in self.agentes}
        self.subtarefas_aprendizado={}
        self.confiancas_rede={a.ident:(a.confianca if self.opcoes.tau_rede is None
                                      else self.opcoes.tau_rede) for a in self.agentes}
        if self.opcoes.lei_confianca=='crowder' and self.opcoes.tau_portao is not None:
            for a in self.agentes:a.confianca=self.opcoes.tau_portao
        self.cnt.update(N_req=0,N_fail=0,N_blocked=0,N_success=0)
        self.reparos=[]
        self.eventos=[]
        self.registros_tarefas=[]
        self.gerado=0.
        self.ocupacao_retrabalho=0
        self.extensoes=0
        self.traj.update({k:[] for k in ['uso_recursos','confianca_media','retrabalho_pendente']})

    def multiplicadores(self,agente,P):
        separados=self.opcoes.lei_confianca=='crowder' and self.opcoes.tau_portao is not None
        if self.opcoes.tau_rede is None and not separados:
            return super().multiplicadores(agente,P)
        anterior=agente.confianca
        try:
            agente.confianca=(self.confiancas_rede[agente.ident] if self.opcoes.lei_confianca=='crowder'
                              else self.opcoes.tau_rede)
            return super().multiplicadores(agente,P)
        finally:
            agente.confianca=anterior

    def decidir_porta(self,p_heu,sorteio):
        """Ponto de intervenção contrafactual; nominal mantém o mesmo sorteio."""
        return sorteio<p_heu

    def atualizar_confianca(self,agente,sucesso,dC=0.):
        """Eq.4: dC está na escala original; τ está normalizada em [0,1]."""
        if self.opcoes.lei_confianca!='crowder':return
        dC=float(np.clip(dC,0.,.30))
        def atualizar(tau):
            return float(np.clip(tau*(1.+dC) if sucesso else tau-.01,0.,1.))
        agente.confianca=atualizar(agente.confianca)
        if self.opcoes.tau_rede is not None or self.opcoes.tau_portao is not None:
            self.confiancas_rede[agente.ident]=atualizar(self.confiancas_rede[agente.ident])

    def preparar_subtarefa(self,agente,j):
        if self.opcoes.reset_competencia and self.subtarefas_aprendizado.get(agente.ident)!=j:
            agente.competencia=self.competencias_iniciais[agente.ident]
            self.subtarefas_aprendizado[agente.ident]=j

    def contabilizar_tempo_aprendizado(self,sucesso,dC_original=0.):
        """Eq3 usa ΔC na escala original 0–5; altera só a contagem de TL."""
        if self.opcoes.lei_tempo_aprendizado=='unitario':
            if sucesso:self.TL+=1.
        else:
            self.TL+=.5*dC_original if sucesso else .05

    def comunicar(self,a,tar,t,tm):
        """Um destinatário por tentativa (política legada), antes de disponibilidade.

        [DEC] Preserva escolha do melhor disponível; se todos ocupados, envia ao
        mais competente elegível e registra insucesso real. Não é broadcast.
        """
        o=self.opcoes
        livres=[k for k in self.agentes if k.ident!=a.ident and k.tarefa_atual is None]
        capazes=[k for k in self.agentes if k.ident!=a.ident and
                 (o.politica_porta2=='sem_filtro_competencia' or k.competencia>a.competencia)]
        self.cnt['hiato_sem_colega_livre']+=int(not livres)
        def confianca(k):
            return k.confianca if o.lei_confianca=='crowder' or o.tau_portao is None else o.tau_portao
        elegiveis=[k for k in capazes if o.politica_porta2=='assistencia_universal' or confianca(k)>tm]
        if o.politica_porta2=='sem_assistencia':elegiveis=[]
        if not elegiveis:
            if capazes and o.politica_porta2!='sem_assistencia':self.cnt['N_blocked']+=1
            self.cnt['p2_bloqueio']+=1;self.TU+=1.
            self.cnt['hiato_colega_capaz_sem_confianca' if capazes else 'hiato_sem_colega_capaz']+=1
            return
        disponiveis=[k for k in elegiveis if k.tarefa_atual is None]
        k=max(disponiveis or elegiveis,key=lambda x:x.competencia)
        self.cnt['N_req']+=1
        if not disponiveis:
            self.cnt['N_fail']+=1
            self.contabilizar_tempo_aprendizado(False)
            self.cnt['p2_bloqueio']+=1;self.TU+=1.
            self.atualizar_confianca(k,False)
            self.eventos.append(dict(tipo='comunicacao',t=t,tarefa=tar.ident,
                solicitante=a.ident,respondente=k.ident,sucesso=False,dC=0.))
            return
        # Crowder C em [0,5]: converter antes de calcular Eq.1; incremento/5 em C normalizada.
        dC=float(np.clip((15.+3.*(5.*k.competencia-5.*a.competencia))/100.,0.,.30))
        a.competencia=min(tar.dificuldade,a.competencia+dC/5.)
        self.cnt['N_success']+=1;self.cnt['p2_ajuda']+=1
        self.contabilizar_tempo_aprendizado(True,dC)
        k.tarefa_atual=-1;k.livre_em=t+1
        self.atualizar_confianca(k,True,dC)
        self.eventos.append(dict(tipo='comunicacao',t=t,tarefa=tar.ident,
            solicitante=a.ident,respondente=k.ident,sucesso=True,dC=dC))

    def _pendente(self):
        return sum(e for _,e in self.divida_pendente)+sum(q['restante'] for q in self.reparos)

    def _terminal(self):
        return (all(x.estado.startswith('concluida') for x in self.tarefas.values())
                and not self.divida_pendente and not any(q['restante']>1e-12 for q in self.reparos)
                and all(a.tarefa_atual is None for a in self.agentes))

    def _reparo(self,j,esforco,disponivel):
        self.reparos.append(dict(j=j,restante=esforco,pronto=disponivel,agente=None))

    def executar(self):
        p,c,o=self.par,self.cen,self.opcoes
        ag,ret=p['agentes'],p['retrabalho']
        tau=float(v(ag['tau_sat'])); s=float(v(ag['s_transicao']))
        bmin=float(v(ag['b_min'])); ka=float(v(ag['k_analitico'])); kh=float(v(ag['k_heuristico']))
        rec=float(v(ag['r_recuperacao']))
        omega=float(v(p['gestor']['omega'])); limite=float(v(p['gestor']['limite_aversao_perda']))
        fc=float(v(ret['f_corrup'])); fr=float(v(ret['f_retrabalho']))
        re=float(v(p['risco']['R_error'])) if o.canal_erro_direto=='ativo' else 0.
        pr=float(v(c['p_reporte'])); pd=float(v(c['p_deteccao'])); tm=float(v(c['tau_min']))
        horizonte=int(v(p['execucao']['horizonte_maximo_fator']))*self.makespan_cpm
        if o.horizonte_automatico:
            horizonte=max(1,horizonte)
            cap=o.limite_horizonte_fator*self.makespan_cpm
        else:
            # O teto de extensão só pertence ao horizonte automático.
            cap=horizonte
        if kh<=ka: self.violacoes.append('k_heuristico deve exceder k_analitico (TCC I)')
        t=0; motivo='limite_seguranca'
        while True:
            if t>=cap: break
            for a in self.agentes:
                if a.tarefa_atual is not None and a.livre_em<=t:
                    if o.reset_competencia and a.tarefa_atual>=0:
                        a.competencia=self.competencias_iniciais[a.ident]
                        self.subtarefas_aprendizado.pop(a.ident,None)
                    a.tarefa_atual=None
            if self._terminal(): motivo='terminal'; break
            if t>=cap: break
            if t>=horizonte:
                horizonte=min(cap,max(horizonte+1,2*horizonte)); self.extensoes+=1
            P=self.pressao(t)
            uso=[0]*len(self.disponibilidade)
            for x in self.tarefas.values():
                if x.estado=='em_execucao':
                    uso=[u+d for u,d in zip(uso,x.demanda)]
            for q in self.reparos:
                if q['agente'] is not None and q['restante']>1e-12:
                    uso=[u+d for u,d in zip(uso,self.tarefas[q['j']].demanda)]
            ainda=[]
            for j,e in self.divida_pendente:
                if self.rng.random()<pd:
                    self.S_UR=max(0.,self.S_UR-e)
                    if o.retrabalho_fila: self._reparo(j,e,max(t,self.tarefas[j].fim or t))
                    else: self.TR+=e
                else: ainda.append((j,e))
            self.divida_pendente=ainda
            disponiveis=[a for a in self.agentes if a.tarefa_atual is None]
            for a in sorted(disponiveis,key=lambda a:-a.competencia):
                if (o.comunicacao_crowder or o.lei_confianca=='crowder') and a.tarefa_atual is not None:
                    continue
                reparo=next((q for q in self.reparos if q['agente'] is None and q['restante']>1e-12
                            and q['pronto']<=t and all(u+d<=capr for u,d,capr in
                            zip(uso,self.tarefas[q['j']].demanda,self.disponibilidade))),None)
                if reparo is not None:
                    tar=self.tarefas[reparo['j']]
                    reparo['agente']=a.ident
                    a.tarefa_atual=-2; a.livre_em=t+int(math.ceil(reparo['restante']))
                    a.esforco_corrente=tar.dificuldade*P/max(a.bateria,bmin); a.modo_corrente='analitico'
                    uso=[u+d for u,d in zip(uso,tar.demanda)]
                    self.eventos.append(dict(tipo='inicio_retrabalho',t=t,tarefa=tar.ident,agente=a.ident))
                    continue
                prontas=self.elegiveis(t,uso)
                if not prontas: continue
                j=max(prontas,key=lambda j:self.tarefas[j].dificuldade); tar=self.tarefas[j]
                self.preparar_subtarefa(a,j)
                E=tar.dificuldade*P/max(a.bateria,bmin)
                mc,mr=self.multiplicadores(a,P)
                logit=float(np.clip((E-tau)/max(s,1e-9),-700,700))
                p_heu=1/(1+math.exp(-logit))
                sorteio_porta=self.rng.random()
                heu=self.decidir_porta(p_heu,sorteio_porta)
                registro=dict(t=t,tarefa=j,agente=a.ident,E=E,E_menos_tau_sat=E-tau,
                    p_heu=p_heu,q=max(0.,2*p_heu-1.),Di=tar.dificuldade,P=P,B=a.bateria,
                    mu_cog=mc,mu_rede=mr,porta=None,p0=None,p_fail=None,excesso=None,
                    duracao_nominal=tar.duracao,duracao_efetiva=None,
                    duracao_analitica=max(1,int(math.ceil(tar.duracao/max(1e-6,mc*mr)))),
                    sorteio_porta=sorteio_porta,sorteio_falha=None,falhou=None,
                    executada=False,selecionou_p1=bool(heu),competencia=a.competencia)
                if o.instrumentar_tarefas:self.registros_tarefas.append(registro)
                if heu and omega>limite:
                    registro['porta']='P1_fuga'
                    self.cnt['p1_fuga']+=1; self.TU+=1.; self.n_adiamentos+=1
                    a.bateria=max(0.,a.bateria-kh*E)
                    continue
                if not heu and tar.dificuldade>a.competencia:
                    registro['porta']='P2'
                    self.cnt['hiato_encontrado']+=1
                    if o.comunicacao_crowder or o.lei_confianca=='crowder':
                        self.comunicar(a,tar,t,tm)
                        continue
                    livres=[k for k in self.agentes if k.ident!=a.ident and k.tarefa_atual is None]
                    capazes=[k for k in livres if o.politica_porta2=='sem_filtro_competencia' or k.competencia>a.competencia]
                    self.cnt['hiato_sem_colega_livre']+=int(not livres)
                    if o.politica_porta2=='sem_assistencia': apoio=[]
                    elif o.politica_porta2=='assistencia_universal': apoio=capazes
                    else: apoio=[k for k in capazes if (k.confianca if o.tau_portao is None else o.tau_portao)>tm]
                    if apoio:
                        k=max(apoio,key=lambda k:k.competencia)
                        dC_tl=float(np.clip((15.+3.*(5.*k.competencia-5.*a.competencia))/100.,0.,.30))
                        a.competencia=min(.98,a.competencia+(15+3*(k.competencia-a.competencia))/100)
                        self.cnt['p2_ajuda']+=1
                        self.contabilizar_tempo_aprendizado(True,dC_tl)
                        # Sem reserva adicional do solicitante: compatibilidade
                        # com a política de ajuda legada, medida por controle exato.
                        k.tarefa_atual=-1; k.livre_em=t+1
                        self.cnt['N_req']+=1;self.cnt['N_success']+=1
                    else:
                        self.cnt['p2_bloqueio']+=1; self.TU+=1.
                        self.cnt['hiato_colega_capaz_sem_confianca' if capazes else 'hiato_sem_colega_capaz']+=1
                        if capazes and o.politica_porta2!='sem_assistencia':self.cnt['N_blocked']+=1
                    continue
                fator=o.fator_omissao if heu else 1.
                dur=max(1,int(math.ceil(tar.duracao*fator/max(1e-6,mc*mr))))
                p0=float(np.clip(self.F_base(tar.nivel)+re*(1-mc),0,1))
                p_falha=risco_porta(p0,p_heu,heu,o.rho_omissao)
                sorteio_falha=self.rng.random()
                falhou=sorteio_falha<p_falha
                registro.update(porta='P1_omissao' if heu else 'P3_analitica',p0=p0,
                    p_fail=p_falha,excesso=p_falha-p0,duracao_efetiva=dur,
                    sorteio_falha=sorteio_falha,falhou=bool(falhou),executada=True)
                tar.estado='em_execucao'; tar.inicio=t; tar.fim=t+dur
                tar.porta='P1_omissao' if heu else 'P3_analitica'
                self.cnt['p1_omissao' if heu else 'p3_analitica']+=1
                a.tarefa_atual=j; a.livre_em=t+dur
                a.esforco_corrente=E; a.modo_corrente='heuristico' if heu else 'analitico'
                uso=[u+d for u,d in zip(uso,tar.demanda)]
                if not o.retrabalho_fila:
                    self.TW+=dur
                    if heu:a.periodos_heuristicos+=dur
                    else:a.periodos_analiticos+=dur
                if falhou:
                    e=fr*tar.duracao*(1+fc*max(E-tau,0.)); self.gerado+=e
                    if self.rng.random()<pr:
                        self.n_reportadas+=1
                        tar.estado_final='reportada'
                        if o.retrabalho_fila and e>1e-12: self._reparo(j,e,t+dur)
                        else: self.TR+=e
                    else:
                        self.S_UR+=e
                        if e>1e-12 or not o.retrabalho_fila: self.divida_pendente.append((j,e))
                        tar.defeito_oculto=True
            if any(u>capa for u,capa in zip(uso,self.disponibilidade)):
                self.violacoes.append(f'recurso excedido em t={t}')
            for q in self.reparos:
                if q['agente'] is not None and q['restante']>1e-12:
                    pago=min(1.,q['restante']); self.TR+=pago; q['restante']-=pago
                    self.ocupacao_retrabalho+=1
            for x in self.tarefas.values():
                if x.estado=='em_execucao' and x.fim<=t+1:
                    x.estado='concluida_com_erro' if x.defeito_oculto else 'concluida_limpa'
                    self.S_PV+=x.duracao if not x.defeito_oculto else 0.
                    if o.reset_competencia:
                        for agente in self.agentes:
                            if self.subtarefas_aprendizado.get(agente.ident)==x.ident:
                                agente.competencia=self.competencias_iniciais[agente.ident]
                                self.subtarefas_aprendizado.pop(agente.ident,None)
            for a in self.agentes:
                if a.tarefa_atual is not None and a.tarefa_atual!=-1:
                    if o.retrabalho_fila and a.tarefa_atual>=0:
                        self.TW+=1.
                        if a.modo_corrente=='heuristico': a.periodos_heuristicos+=1
                        else: a.periodos_analiticos+=1
                    dr=(kh if a.modo_corrente=='heuristico' else ka)*a.esforco_corrente
                    a.bateria=max(0.,a.bateria-dr); self.S_DC+=dr
                else: a.bateria=min(1.,a.bateria+rec)
                if a.tarefa_atual==-1 and a.livre_em<=t+1: a.tarefa_atual=None
            valores=dict(t=t,P=P,bateria_media=float(np.mean([a.bateria for a in self.agentes])),
                         mu_cog=float(np.mean([self.multiplicadores(a,P)[0] for a in self.agentes])),
                         mu_rede=float(np.mean([self.multiplicadores(a,P)[1] for a in self.agentes])),
                         S_PV=self.S_PV,S_UR=self.S_UR,concluidas=sum(x.estado.startswith('concluida') for x in self.tarefas.values()),
                         uso_recursos=list(uso),confianca_media=float(np.mean([a.confianca for a in self.agentes])),
                         retrabalho_pendente=self._pendente())
            for k,x in valores.items(): self.traj[k].append(x)
            t+=1
        r=self._resultado(t)
        if o.retrabalho_fila or o.horizonte_automatico: r.concluiu=self._terminal()
        r.contadores.update(retrabalho_gerado=self.gerado,retrabalho_pendente=self._pendente(),
                             ocupacao_retrabalho=self.ocupacao_retrabalho,extensoes_horizonte=self.extensoes,
                             motivo_termino=motivo,confianca_media_final=float(np.mean([a.confianca for a in self.agentes])))
        erro=abs(self.gerado-self.TR-self._pendente())
        if erro>1e-8: r.violacoes.append(f'conservação retrabalho: {erro}')
        return r
