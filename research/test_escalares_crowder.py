"""Escalares devem atuar no evento; controle nominal independente vem do Git."""
import unittest
from test_crowder import Crowder
class Escalares(unittest.TestCase):
    def test_evento_responde_aos_dois_escalares(self):
        # C_p=.8 e C_r=.4: diferença na escala 0..5 é 2.
        for base,fator,ganho in [(7.5,1.5,.021),(15.,3.,.042),(22.5,6.,.06)]:
            with self.subTest(base=base,fator=fator):
                s,a,b=Crowder().sim()
                s.par['aprendizado']={'incremento_base':{'valor':base},'fator_transferencia':{'valor':fator}}
                s.comunicar(a,s.tarefas[1],0,.2)
                self.assertAlmostEqual(a.competencia,.4+ganho)
                self.assertAlmostEqual(s.eventos[-1]['dC'],ganho*5)
    def test_nominais_declarados_no_yaml(self):
        import simulador as S
        p=S.carregar_parametros()['aprendizado']
        self.assertEqual(S.v(p['incremento_base']),15)
        self.assertEqual(S.v(p['fator_transferencia']),3)
        self.assertEqual(p['incremento_base']['condicao'],'tcc1')

class IdentidadeAnterior(unittest.TestCase):
    def test_15_3_contra_dfc0d78_tres_caminhos(self):
        import copy,subprocess,types,sys
        from pathlib import Path
        from dataclasses import asdict
        import yaml
        import simulador as S
        import simulador_mvp as M
        from test_compatibilidade import bits
        root=Path(__file__).resolve().parents[1]
        def load(rel,name):
            m=types.ModuleType(name);m.__file__=str(root/rel);sys.modules[name]=m
            code=subprocess.check_output(['git','show','dfc0d78:'+rel],cwd=root,text=True)
            exec(compile(code,m.__file__,'exec'),m.__dict__);return m
        oldS=load('src/modelo/simulador.py','_antes_escalares_S')
        sys.modules['simulador']=oldS
        try:oldM=load('src/modelo/simulador_mvp.py','_antes_escalares_M')
        finally:sys.modules['simulador']=S
        nominal=yaml.safe_load((root/'config/mvp_v1.yaml').read_text())['opcoes']
        for arq in ['j6010_1.sm','j6021_1.sm']:
            g,d,c=S.carregar_instancia(arq)
            for cen in ['centralizada','adaptativa']:
                for seed in range(2):
                    for path in ['legado','mvp_nominal','mvp_comunicacao_legada']:
                        with self.subTest(arq=arq,cen=cen,seed=seed,path=path):
                            args=(g,d,c,S.carregar_parametros(),cen,seed)
                            if path=='legado':a=oldS.Simulacao(*copy.deepcopy(args));b=S.Simulacao(*copy.deepcopy(args))
                            else:
                                op=dict(nominal)
                                if path=='mvp_comunicacao_legada':op.update(comunicacao_crowder=False,lei_confianca='constante')
                                a=oldM.SimulacaoMVP(*copy.deepcopy(args),opcoes=oldM.OpcoesMVP(**op));b=M.SimulacaoMVP(*copy.deepcopy(args),opcoes=M.OpcoesMVP(**op))
                            self.assertEqual(bits(asdict(a.executar())),bits(asdict(b.executar())))
                            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
                            self.assertEqual(bits([vars(x) for x in a.agentes]),bits([vars(x) for x in b.agentes]))
                            self.assertEqual(bits({k:vars(v) for k,v in a.tarefas.items()}),bits({k:vars(v) for k,v in b.tarefas.items()}))
                            if path!='legado':
                                for attr in ['divida_pendente','eventos','registros_tarefas','reparos']:
                                    self.assertEqual(bits(getattr(a,attr)),bits(getattr(b,attr)))
