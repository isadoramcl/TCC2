import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
import simulador_mvp as M
class Qualidade(unittest.TestCase):
    def test_excesso_no_complemento_e_dependente_do_estado(self):
        self.assertTrue(hasattr(M,'risco_porta'),'risco adicional ainda ausente')
        self.assertAlmostEqual(M.risco_porta(.2,.9,True,.35),.424)
        self.assertEqual(M.risco_porta(.2,.9,False,.35),.2)
        self.assertEqual(M.risco_porta(.2,.5,True,.35),.2)
        self.assertGreater(M.risco_porta(.2,.9,True,.35),M.risco_porta(.2,.6,True,.35))
    def test_rho_zero_preserva_bits_e_extremos(self):
        self.assertTrue(hasattr(M,'risco_porta'),'risco adicional ainda ausente')
        for p0 in [0.,.1,.19999999999997,.5,1.]:
            self.assertEqual(M.risco_porta(p0,.99,True,0.).hex(),p0.hex())
            for rho in [0.,.2,.35,.5,1.]:
                self.assertTrue(p0<=M.risco_porta(p0,.9,True,rho)<=1)
if __name__=='__main__':unittest.main()
