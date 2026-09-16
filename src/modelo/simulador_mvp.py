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
    lei_confianca: str = 'constante'
    taxa_aprendizado: float = .05
    incremento_sucesso: float = .02
    decremento_recusa: float = .01
    horizonte_automatico: bool = True
    limite_horizonte_fator: int = 256
    politica_porta2: str = 'nominal'
    tau_portao: float | None = None
    tau_rede: float | None = None

    def __post_init__(self):
        if self.rho_omissao is not None and not 0<=self.rho_omissao<=1:
            raise ValueError('rho_omissao fora de [0,1]')
        if self.lei_confianca not in {'constante','media_eventos','saldo_eventos'}:
            raise ValueError('lei de confiança desconhecida')
        if self.politica_porta2 not in {'nominal','sem_assistencia','assistencia_universal','sem_filtro_competencia'}:
            raise ValueError('política Porta 2 desconhecida')
        if not 0 < self.fator_omissao <= 1 or self.limite_horizonte_fator < 1:
            raise ValueError('fator de duração/horizonte inválido')
        for x in [self.taxa_aprendizado,self.incremento_sucesso,self.decremento_recusa]:
            if not 0 <= x <= 1: raise ValueError('taxa fora de [0,1]')
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
        self.reparos=[]
        self.eventos=[]
        self.gerado=0.
        self.ocupacao_retrabalho=0
        self.extensoes=0
        self.traj.update({k:[] for k in ['uso_recursos','confianca_media','retrabalho_pendente']})

    def multiplicadores(self,agente,P):
        if self.opcoes.tau_rede is None:
            return super().multiplicadores(agente,P)
        anterior=agente.confianca
        try:
            agente.confianca=self.opcoes.tau_rede
            return super().multiplicadores(agente,P)
        finally:
            agente.confianca=anterior

    def atualizar_confianca(self,agente,sucesso):
        o=self.opcoes
        if o.lei_confianca=='media_eventos':
            agente.confianca += o.taxa_aprendizado*(float(sucesso)-agente.confianca)
        elif o.lei_confianca=='saldo_eventos':
            agente.confianca += o.incremento_sucesso if sucesso else -o.decremento_recusa
        agente.confianca=float(np.clip(agente.confianca,0.,1.))

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
        re=float(v(p['risco']['R_error']))
        pr=float(v(c['p_reporte'])); pd=float(v(c['p_deteccao'])); tm=float(v(c['tau_min']))
        horizonte=max(1,int(v(p['execucao']['horizonte_maximo_fator']))*self.makespan_cpm)
        cap=o.limite_horizonte_fator*self.makespan_cpm
        if not o.horizonte_automatico: cap=min(cap,horizonte)
        if kh<=ka: self.violacoes.append('k_heuristico deve exceder k_analitico (TCC I)')
        t=0; motivo='limite_seguranca'
        while True:
            if t>=cap: break
            for a in self.agentes:
                if a.tarefa_atual is not None and a.livre_em<=t: a.tarefa_atual=None
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
            eventos_tau=[]
            disponiveis=[a for a in self.agentes if a.tarefa_atual is None]
            for a in sorted(disponiveis,key=lambda a:-a.competencia):
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
                E=tar.dificuldade*P/max(a.bateria,bmin)
                mc,mr=self.multiplicadores(a,P)
                logit=float(np.clip((E-tau)/max(s,1e-9),-700,700))
                p_heu=1/(1+math.exp(-logit))
                heu=self.rng.random()<p_heu
                if heu and omega>limite:
                    self.cnt['p1_fuga']+=1; self.TU+=1.; self.n_adiamentos+=1
                    a.bateria=max(0.,a.bateria-kh*E)
                    continue
                if not heu and tar.dificuldade>a.competencia:
                    self.cnt['hiato_encontrado']+=1
                    livres=[k for k in self.agentes if k.ident!=a.ident and k.tarefa_atual is None]
                    capazes=[k for k in livres if o.politica_porta2=='sem_filtro_competencia' or k.competencia>a.competencia]
                    self.cnt['hiato_sem_colega_livre']+=int(not livres)
                    if o.politica_porta2=='sem_assistencia': apoio=[]
                    elif o.politica_porta2=='assistencia_universal': apoio=capazes
                    else: apoio=[k for k in capazes if (k.confianca if o.tau_portao is None else o.tau_portao)>tm]
                    if apoio:
                        k=max(apoio,key=lambda k:k.competencia)
                        a.competencia=min(.98,a.competencia+(15+3*(k.competencia-a.competencia))/100)
                        self.cnt['p2_ajuda']+=1; self.TL+=1.
                        # Sem reserva adicional do solicitante: compatibilidade
                        # com a política de ajuda legada, medida por controle exato.
                        k.tarefa_atual=-1; k.livre_em=t+1
                        eventos_tau.extend([(a,True),(k,True)])
                    else:
                        self.cnt['p2_bloqueio']+=1; self.TU+=1.
                        self.cnt['hiato_colega_capaz_sem_confianca' if capazes else 'hiato_sem_colega_capaz']+=1
                        if capazes: eventos_tau.append((a,False))
                    continue
                fator=o.fator_omissao if heu else 1.
                dur=max(1,int(math.ceil(tar.duracao*fator/max(1e-6,mc*mr))))
                p0=float(np.clip(self.F_base(tar.nivel)+re*(1-mc),0,1))
                p_falha=risco_porta(p0,p_heu,heu,o.rho_omissao)
                falhou=self.rng.random()<p_falha
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
            for a,sucesso in eventos_tau: self.atualizar_confianca(a,sucesso)
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
