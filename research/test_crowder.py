"""Contratos de eventos reais, respondente e normalização de Crowder."""
import unittest
from test_mvp import caso
from simulador_mvp import SimulacaoMVP, OpcoesMVP

class Crowder(unittest.TestCase):
    def sim(self, **opts):
        g,p=caso(n=2)
        s=SimulacaoMVP(g,[1],8,p,'centralizada',0,
            opcoes=OpcoesMVP(lei_confianca='crowder',**opts))
        a,b=s.agentes
        a.competencia=.4;b.competencia=.8
        a.confianca=b.confianca=.5
        s.tarefas[1].dificuldade=.9
        return s,a,b

    def test_sucesso_credita_respondente_e_converte_competencia(self):
        s,a,b=self.sim()
        s.comunicar(a,s.tarefas[1],0,.2)
        self.assertAlmostEqual(a.competencia,.442)
        self.assertEqual(a.confianca,.5)
        self.assertAlmostEqual(b.confianca,.605)
        self.assertEqual([s.cnt[k] for k in ['N_req','N_fail','N_blocked','N_success']],[1,0,0,1])

    def test_bloqueio_nao_envia_e_nao_muda_confianca(self):
        s,a,b=self.sim()
        s.comunicar(a,s.tarefas[1],0,.6)
        self.assertEqual([s.cnt[k] for k in ['N_req','N_fail','N_blocked']],[0,0,1])
        self.assertEqual((a.confianca,b.confianca),(.5,.5))

    def test_pedido_enviado_sem_resposta_decrementa_respondente(self):
        s,a,b=self.sim();b.tarefa_atual=1;b.livre_em=10
        s.comunicar(a,s.tarefas[1],0,.2)
        self.assertEqual([s.cnt[k] for k in ['N_req','N_fail','N_blocked']],[1,1,0])
        self.assertEqual(a.confianca,.5);self.assertEqual(b.confianca,.49)

    def test_reset_competencia_por_subtarefa_sem_reset_confianca(self):
        s,a,b=self.sim(reset_competencia=True)
        inicial=s.competencias_iniciais[a.ident]
        s.preparar_subtarefa(a,1)
        a.competencia=.9;a.confianca=.7
        s.preparar_subtarefa(a,1)
        self.assertEqual(a.competencia,.9)
        s.preparar_subtarefa(a,2)
        self.assertEqual(a.competencia,inicial)
        self.assertEqual(a.confianca,.7)

    def test_laco_real_contabiliza_eventos_e_canais_diagonais(self):
        import copy
        from dataclasses import asdict
        import simulador as S
        import pandas as pd
        arq=sorted(pd.read_csv(S.RAIZ/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[0]
        g,disp,cpm=S.carregar_instancia(arq)
        p=S.carregar_parametros()
        for cen in ['centralizada','adaptativa']:
            opts=dict(lei_confianca='crowder',comunicacao_crowder=True,reset_competencia=True)
            a=SimulacaoMVP(g,disp,cpm,copy.deepcopy(p),cen,0,opcoes=OpcoesMVP(**opts))
            tau=S.v(p['cenarios'][cen]['tau_inicial'])
            b=SimulacaoMVP(g,disp,cpm,copy.deepcopy(p),cen,0,
                opcoes=OpcoesMVP(**opts,tau_portao=tau,tau_rede=tau))
            ra,rb=asdict(a.executar()),asdict(b.executar())
            self.assertEqual(ra,rb)
            self.assertEqual(a.cnt['N_req'],a.cnt['N_success']+a.cnt['N_fail'])
            self.assertEqual(a.cnt['N_req'],len([e for e in a.eventos if e['tipo']=='comunicacao']))
            self.assertFalse(ra['violacoes'])
            self.assertTrue(ra['concluiu'])
            for agente in a.agentes:
                self.assertEqual(agente.competencia,a.competencias_iniciais[agente.ident])

    def test_reset_no_periodo_final_do_horizonte(self):
        g,p=caso(n=1);g['duracao']=1
        s=SimulacaoMVP(g,[1],1,p,'centralizada',0,
            opcoes=OpcoesMVP(lei_confianca='crowder',reset_competencia=True,
                horizonte_automatico=False,rho_omissao=0.))
        a=s.agentes[0];base=a.competencia
        s.subtarefas_aprendizado[a.ident]=1;a.competencia=1.
        s.executar()
        self.assertTrue(s.tarefas[1].estado.startswith('concluida'))
        self.assertEqual(a.competencia,base)

    def test_override_portao_nao_altera_rede(self):
        g,p=caso(n=2)
        # Abrir o piso fuzzy para que a confiança da rede seja observável.
        p['fuzzy']['mu_minimo']['valor']=.2
        a=SimulacaoMVP(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP(lei_confianca='crowder'))
        b=SimulacaoMVP(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP(lei_confianca='crowder',tau_portao=.9))
        self.assertNotEqual(a.agentes[0].confianca,b.agentes[0].confianca)
        for pressao in [.1,.5,.9]:
            self.assertEqual(a.multiplicadores(a.agentes[0],pressao),b.multiplicadores(b.agentes[0],pressao))

    def test_canais_dinamicos_e_limites(self):
        s,a,b=self.sim(tau_portao=.5,tau_rede=.5)
        s.atualizar_confianca(b,True,.21)
        self.assertAlmostEqual(b.confianca,.605)
        self.assertEqual(s.confiancas_rede[b.ident],b.confianca)
        for _ in range(100):s.atualizar_confianca(b,True,.30)
        self.assertEqual(b.confianca,1.)
        for _ in range(101):s.atualizar_confianca(b,False,0.)
        self.assertEqual(b.confianca,0.)

if __name__=='__main__':unittest.main()
