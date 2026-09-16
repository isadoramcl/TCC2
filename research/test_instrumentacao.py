import unittest
from dataclasses import asdict
from test_mvp import caso
from simulador_mvp import SimulacaoMVP, OpcoesMVP

class Instrumentacao(unittest.TestCase):
    def test_registro_completo_sem_mudar_resultado_ou_rng(self):
        g,p=caso(heuristico=True,falha=True)
        sims=[SimulacaoMVP(g,[1],8,p,'centralizada',0,
             opcoes=OpcoesMVP(instrumentar_tarefas=ativo)) for ativo in [True,False]]
        a,b=sims
        self.assertEqual(asdict(a.executar()),asdict(b.executar()))
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(b.registros_tarefas,[])
        self.assertEqual(len(a.registros_tarefas),1)
        r=a.registros_tarefas[0]
        campos={'E','E_menos_tau_sat','p_heu','q','Di','P','B','mu_cog','porta',
                'p0','p_fail','excesso','duracao_nominal','duracao_efetiva',
                'sorteio_porta','sorteio_falha','falhou','executada'}
        self.assertTrue(campos<=r.keys())
        self.assertEqual(r['porta'],'P1_omissao')
        self.assertEqual((r['duracao_nominal'],r['duracao_efetiva']),(8,6))
        self.assertEqual(r['excesso'],r['p_fail']-r['p0'])
        self.assertTrue(r['executada']);self.assertTrue(r['falhou'])

if __name__=='__main__':unittest.main()
