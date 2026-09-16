"""Contratos do MVP: tempo, capacidade, conservação e censura."""
import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
import simulador as S
try:
    from simulador_mvp import SimulacaoMVP, OpcoesMVP
except ImportError:
    SimulacaoMVP = OpcoesMVP = None


def caso(n=1, falha=False, heuristico=False):
    p=S.carregar_parametros()
    p['agentes']['n_agentes']['valor']=n
    p['agentes']['competencia_inicial']['valor']={'media':.98,'desvio':0.}
    p['agentes']['tau_sat']['valor']=-100. if heuristico else 100.
    p['agentes']['s_transicao']['valor']=1.
    p['risco']['F_ancora']['valor']=1. if falha else 0.
    p['risco']['R_error']['valor']=0.
    p['retrabalho']['f_corrup']['valor']=0.
    p['retrabalho']['f_retrabalho']['valor']=.5
    p['cenarios']['centralizada']['p_reporte']['valor']=1.
    p['fuzzy']['mu_minimo']['valor']=1.
    p['execucao']['horizonte_maximo_fator']['valor']=1
    g=pd.DataFrame([dict(tarefa=1,duracao=8,R1=1,sucessores='',Di=.1,nivel_dificuldade='baixa')])
    return g,p


class TestMVP(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(SimulacaoMVP,'alternativa MVP ainda ausente')

    def run_case(self,p,g,**opts):
        s=SimulacaoMVP(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP(**opts))
        return s,s.executar()

    def test_omissao_reduz_tempo_imediato(self):
        g,p=caso(heuristico=True)
        _,antes=self.run_case(p,g,fator_omissao=1.,retrabalho_fila=False)
        _,depois=self.run_case(p,g,fator_omissao=.5,retrabalho_fila=False)
        self.assertEqual((antes.makespan,depois.makespan),(8,4))
        self.assertEqual((antes.TW,depois.TW),(8,4))

    def test_retrabalho_ocupa_agente_recurso_e_conserva(self):
        g,p=caso(n=2,falha=True)
        g=pd.concat([g,g.assign(tarefa=2)],ignore_index=True)
        s,r=self.run_case(p,g,fator_omissao=1.)
        self.assertTrue(r.concluiu)
        self.assertEqual(r.makespan,24)
        self.assertEqual(r.TR,8.)
        self.assertEqual(r.contadores['retrabalho_gerado'],r.TR)
        self.assertEqual(r.contadores['retrabalho_pendente'],0.)
        self.assertFalse(r.violacoes)
        self.assertTrue(all(max(u)<=1 for u in r.trajetorias['uso_recursos']))
        reparos=[e for e in s.eventos if e['tipo']=='inicio_retrabalho']
        self.assertEqual(len(reparos),2)
        self.assertTrue(all(e['t']>=8 for e in reparos))

    def test_automatico_estende_estado_ate_terminal(self):
        g,p=caso(falha=True)
        _,r=self.run_case(p,g,fator_omissao=1.,horizonte_automatico=True)
        self.assertEqual(r.makespan,12)
        self.assertTrue(r.concluiu)
        self.assertGreater(r.contadores['extensoes_horizonte'],0)
        _,c=self.run_case(p,g,fator_omissao=1.,horizonte_automatico=False)
        self.assertFalse(c.concluiu)
        self.assertEqual(c.contadores['retrabalho_pendente'],4.)

    def test_limite_seguranca_nao_declara_sucesso(self):
        g,p=caso(falha=True)
        _,r=self.run_case(p,g,fator_omissao=1.,limite_horizonte_fator=1)
        self.assertFalse(r.concluiu)
        self.assertEqual(r.contadores['motivo_termino'],'limite_seguranca')

    def test_confianca_constante_e_crowder_limitadas(self):
        g,p=caso()
        for lei in ['constante','crowder']:
            s=SimulacaoMVP(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP(lei_confianca=lei))
            a=s.agentes[0]; inicial=a.confianca
            s.atualizar_confianca(a,True,.15)
            self.assertEqual(a.confianca,inicial) if lei=='constante' else self.assertGreater(a.confianca,inicial)
            for _ in range(1000): s.atualizar_confianca(a,False)
            self.assertTrue(0<=a.confianca<=1)

    def test_recurso_inviavel_falha(self):
        g,p=caso(); g['R1']=2
        with self.assertRaises(ValueError): SimulacaoMVP(g,[1],8,p,'centralizada',0)

    def test_censura_conta_so_trabalho_realizado(self):
        g,p=caso(); g['duracao']=100
        _,r=self.run_case(p,g,fator_omissao=1.,limite_horizonte_fator=1)
        self.assertFalse(r.concluiu)
        self.assertEqual(r.TW,8.)

    def test_divida_zero_nao_impede_termino(self):
        g,p=caso(falha=True)
        p['retrabalho']['f_retrabalho']['valor']=0.
        p['cenarios']['centralizada']['p_reporte']['valor']=0.
        p['cenarios']['centralizada']['p_deteccao']['valor']=0.
        _,r=self.run_case(p,g,fator_omissao=1.,limite_horizonte_fator=2)
        self.assertTrue(r.concluiu)
        self.assertEqual(r.makespan,8)

    def test_opcao_desconhecida_falha(self):
        with self.assertRaises(ValueError): OpcoesMVP(lei_confianca='typo')

if __name__=='__main__': unittest.main()
