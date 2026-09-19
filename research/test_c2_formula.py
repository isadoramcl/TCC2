import sys,unittest
from pathlib import Path
from scipy.stats import beta
sys.path.insert(0,str(Path(__file__).parent/'lote_noturno'))
from c2_precontrole import parametros_beta
class FormulaBeta(unittest.TestCase):
    def test_momentos_por_biblioteca_independente(self):
        for mu in [.0163,.05,.1,.2985]:
            a,b=parametros_beta(mu);m,var=beta.stats(a,b,moments='mv')
            self.assertAlmostEqual(m,mu,places=14)
            self.assertAlmostEqual(float(var)**.5/m,1.13,places=13)
    def test_dominio_explicito(self):
        for mu in [0.,-.1,1/(1+1.13**2),.44775,float('nan')]:
            with self.assertRaisesRegex(ValueError,'CV nao alterado'):parametros_beta(mu)
    def test_momentos_impressos_arredondam_como_fonte(self):
        m,var=beta.stats(.7546,45.4563,moments='mv')
        self.assertEqual(round(float(m),4),.0163)
        self.assertEqual(round(float(var)**.5/m,2),1.13)
