import copy
from dataclasses import asdict
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from test_compatibilidade import bits
from test_mvp import caso
class CanalErroDireto(unittest.TestCase):
    def test_opcao_existe_com_default_ativo(self):
        self.assertEqual(getattr(OpcoesMVP(),'canal_erro_direto',None),'ativo')
    def test_desligado_equivale_a_R_zero(self):
        self.assertIn('canal_erro_direto',OpcoesMVP.__dataclass_fields__)
        g,par=caso(falha=True)
        par0=copy.deepcopy(par);par0['risco']['R_error']['valor']=0.
        for seed in range(5):
            a=SimulacaoMVP(g,[1],1,copy.deepcopy(par),'centralizada',seed,opcoes=OpcoesMVP(canal_erro_direto='desligado'))
            b=SimulacaoMVP(g,[1],1,copy.deepcopy(par0),'centralizada',seed,opcoes=OpcoesMVP(canal_erro_direto='ativo'))
            self.assertEqual(bits(asdict(a.executar())),bits(asdict(b.executar())))
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
            self.assertEqual(bits(a.registros_tarefas),bits(b.registros_tarefas))
    def test_instrumentacao_desligada_preserva_resultado_e_rng(self):
        g,par=caso(falha=True)
        for canal in ['ativo','desligado']:
            a=SimulacaoMVP(g,[1],1,copy.deepcopy(par),'centralizada',1,opcoes=OpcoesMVP(canal_erro_direto=canal))
            b=SimulacaoMVP(g,[1],1,copy.deepcopy(par),'centralizada',1,opcoes=OpcoesMVP(canal_erro_direto=canal,instrumentar_tarefas=False))
            self.assertEqual(bits(asdict(a.executar())),bits(asdict(b.executar())))
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)

    def test_valor_invalido_rejeitado(self):
        self.assertIn('canal_erro_direto',OpcoesMVP.__dataclass_fields__)
        with self.assertRaises(ValueError):OpcoesMVP(canal_erro_direto='outro')
