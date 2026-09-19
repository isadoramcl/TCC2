import sys,unittest
from pathlib import Path
from dataclasses import asdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from test_mvp import caso
from test_compatibilidade import bits
class IntegracaoAncora(unittest.TestCase):
    def test_mapas_modificam_risco_basal_efetivo(self):
        for mapa,k in [('curto',4),('longo',8)]:
            g,p=caso();g['nivel_dificuldade']='muito alta';p['agentes']['tau_sat']['valor']=100.
            a=SimulacaoMVP(g,[1],8,p,'centralizada',2,opcoes=OpcoesMVP(ancoragem_erro='stewart_linear',mapa_passos=mapa))
            a.executar();x=[r for r in a.registros_tarefas if r['executada']][0]
            self.assertAlmostEqual(x['p0'],k*.0128,delta=1e-12)
    def test_historica_explicita_default(self):
        g,p=caso();a=SimulacaoMVP(g,[1],8,p,'centralizada',2)
        b=SimulacaoMVP(g,[1],8,p,'centralizada',2,opcoes=OpcoesMVP(ancoragem_erro='historica'))
        self.assertEqual(bits(asdict(a.executar())),bits(asdict(b.executar())))
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
    def test_opcoes_invalidas(self):
        with self.assertRaises(ValueError):OpcoesMVP(ancoragem_erro='x')
        with self.assertRaises(ValueError):OpcoesMVP(mapa_passos='x')
