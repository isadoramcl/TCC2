import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).parent/'tb2'))
from diagnostico import pares_completos,ic
class ParesCompletos(unittest.TestCase):
    def test_exclui_par_se_um_braco_nao_concluiu(self):
        d=pd.DataFrame([dict(arquivo='x',semente=s,cenario=c,concluiu=ok,y=y) for s,c,ok,y in [(0,'centralizada',True,5),(0,'adaptativa',True,3),(1,'centralizada',False,99),(1,'adaptativa',True,4)]])
        delta,n,ex=pares_completos(d,'y')
        self.assertEqual(delta.tolist(),[-2]);self.assertEqual((n,ex),(2,1))
        self.assertTrue(pd.isna(ic(delta.groupby('arquivo').mean())['ic95_inferior']))
    def test_nao_pareia_sementes_diferentes(self):
        d=pd.DataFrame([dict(arquivo='x',semente=0,cenario='centralizada',concluiu=True,y=5),dict(arquivo='x',semente=1,cenario='adaptativa',concluiu=True,y=3)])
        delta,n,ex=pares_completos(d,'y')
        self.assertEqual(len(delta),0);self.assertEqual(ex,2)
