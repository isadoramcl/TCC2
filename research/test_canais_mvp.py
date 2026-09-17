import importlib.util
from pathlib import Path
import unittest
import numpy as np
P=Path(__file__).resolve().parents[1]/'src/modelo/21_canais_mvp.py'
class TestCanais(unittest.TestCase):
    def test_decomposicao_recupera_interacao_conhecida(self):
        self.assertTrue(P.exists(),'instrumento fatorial ainda ausente')
        spec=importlib.util.spec_from_file_location('canais',P); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        M,cols=m.matriz()
        alvo=np.array([2+3*int(c[0])-4*int(c[1])+5*int(c[0])*int(c[1]) for c in m.CELULAS])
        b=np.linalg.solve(M,alvo)
        self.assertAlmostEqual(b[cols.index('G')],3)
        self.assertAlmostEqual(b[cols.index('N')],-4)
        self.assertAlmostEqual(b[cols.index('GN')],5)
        self.assertAlmostEqual(b[1:].sum(),4)
if __name__=='__main__': unittest.main()
