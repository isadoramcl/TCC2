import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).parent/'tb2'))
from varredura_confianca import configurar,MALHA
import simulador as S
class ConfiguracaoConfianca(unittest.TestCase):
    def test_principal_so_muda_tau_inicial(self):
        row=dict(tau_sat=1.,s_transicao=.01,canal='ativo')
        p,op=configurar(row,.25,'principal');n,no=configurar(row,.8,'principal')
        p['cenarios']['centralizada']['tau_inicial']['valor']=.8
        self.assertEqual(p,n);self.assertEqual(op,no)
    def test_controles_separam_estados_iniciais(self):
        row=dict(tau_sat=1.,s_transicao=.01,canal='ativo')
        p,op=configurar(row,.8,'portao');q,oq=configurar(row,.8,'rede')
        self.assertEqual(p,q);self.assertEqual((op['tau_portao'],op['tau_rede']),(.8,.25));self.assertEqual((oq['tau_portao'],oq['tau_rede']),(.25,.8))
        self.assertEqual(S.v(p['cenarios']['centralizada']['tau_min']),.6)
        self.assertEqual(S.v(p['cenarios']['centralizada']['tau_inicial']),.25)
    def test_malha_cruza_limiar_estrito(self):
        self.assertIn(.6,MALHA);self.assertIn(.600001,MALHA);self.assertIn(.25,MALHA)

    def test_override_nominal_exato(self):
        from dataclasses import asdict
        from simulador_mvp import SimulacaoMVP,OpcoesMVP
        from test_compatibilidade import bits
        row=dict(tau_sat=1.,s_transicao=.25,canal='ativo')
        p,op=configurar(row,.25,'principal');g,d,c=S.carregar_instancia('j6010_1.sm')
        a=SimulacaoMVP(g,d,c,p,'centralizada',0,opcoes=OpcoesMVP(**op))
        b=SimulacaoMVP(g,d,c,p,'centralizada',0,opcoes=OpcoesMVP(**{**op,'tau_portao':.25,'tau_rede':.25}))
        self.assertEqual(bits(asdict(a.executar())),bits(asdict(b.executar())))
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
