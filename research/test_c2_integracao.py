import sys,unittest,copy
from pathlib import Path
from dataclasses import asdict
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from test_mvp import caso
from test_compatibilidade import bits
class Heterogeneidade(unittest.TestCase):
    def setup(self,op):
        g,p=caso();p['risco']['F_ancora']['valor']=.1
        return SimulacaoMVP(g,[1],8,p,'centralizada',9,opcoes=op)
    def test_nenhuma_explicita_identica_default(self):
        a=self.setup(OpcoesMVP());b=self.setup(OpcoesMVP(heterogeneidade_erro='nenhuma'))
        self.assertEqual(bits(asdict(a.executar())),bits(asdict(b.executar())))
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
    def test_beta_fixa_por_agente_e_usada_em_p0(self):
        a=self.setup(OpcoesMVP(heterogeneidade_erro='beta_cv113',rho_omissao=0))
        inicial=copy.deepcopy(a.taxas_erro_agentes);rng=copy.deepcopy(a.rng.bit_generator.state)
        b=self.setup(OpcoesMVP());self.assertEqual(rng,b.rng.bit_generator.state)
        a.executar();self.assertEqual(inicial,a.taxas_erro_agentes)
        x=next(x for x in a.registros_tarefas if x['executada'])
        self.assertEqual(x['p0'],inicial[x['agente']]['baixa'])
        self.assertNotEqual(x['p0'],a.F_base('baixa'))
    def test_invalida_antes_de_rng(self):
        g,p=caso();p['risco']['F_ancora']['valor']=.15
        with patch('numpy.random.default_rng',side_effect=AssertionError('RNG prematuro')):
            with self.assertRaisesRegex(ValueError,'muito alta.*CV nao alterado'):
                SimulacaoMVP(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP(heterogeneidade_erro='beta_cv113'))
    def test_c1_admissivel_e_opcao_invalida(self):
        for mapa in ['curto','longo']:
            a=self.setup(OpcoesMVP(ancoragem_erro='stewart_linear',mapa_passos=mapa,heterogeneidade_erro='beta_cv113'))
            self.assertEqual(len(a.taxas_erro_agentes[0]),4)
        with self.assertRaises(ValueError):OpcoesMVP(heterogeneidade_erro='x')
