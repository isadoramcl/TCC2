"""Identidade com implementação anterior à C2, incluindo estado e RNG."""
import subprocess,types,sys,unittest
from pathlib import Path
from dataclasses import asdict
import yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from test_compatibilidade import bits
class IdentidadeC2(unittest.TestCase):
    def test_nenhuma_contra_efd1248(self):
        name='_mvp_anterior_C2';mod=types.ModuleType(name);sys.modules[name]=mod
        code=subprocess.check_output(['git','show','efd1248:src/modelo/simulador_mvp.py'],cwd=ROOT,text=True)
        exec(compile(code,name,'exec'),mod.__dict__)
        op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
        for arq in ['j6010_1.sm','j6021_1.sm']:
            g,d,c=S.carregar_instancia(arq)
            for cen in ['centralizada','adaptativa']:
                for seed in range(2):
                    for modo in ['historica','stewart_linear']:
                        opts={**op,'ancoragem_erro':modo}
                        args=(g,d,c,S.carregar_parametros(),cen,seed)
                        a=mod.SimulacaoMVP(*args,opcoes=mod.OpcoesMVP(**opts))
                        b=SimulacaoMVP(*args,opcoes=OpcoesMVP(**opts,heterogeneidade_erro='nenhuma'))
                        self.assertEqual(bits(asdict(a.executar())),bits(asdict(b.executar())))
                        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
                        for attr in ['divida_pendente','eventos','registros_tarefas','reparos']:
                            self.assertEqual(bits(getattr(a,attr)),bits(getattr(b,attr)))
                        self.assertEqual(bits([vars(x) for x in a.agentes]),bits([vars(x) for x in b.agentes]))
                        self.assertEqual(bits({k:vars(v) for k,v in a.tarefas.items()}),bits({k:vars(v) for k,v in b.tarefas.items()}))
