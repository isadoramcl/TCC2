import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
from ancoragem_stewart import ancora_stewart
class Ancora(unittest.TestCase):
    def test_seis_pontos_publicados(self):
        for k,p in [(1,.0128),(2,.0256),(3,.0384),(4,.0512),(5,.0640),(8,.1024)]:
            self.assertAlmostEqual(ancora_stewart(k),p,delta=1e-12)
    def test_dominio_nao_extrapola_silencioso(self):
        for k in [-1,0,9,float('nan')]:
            with self.assertRaises(ValueError):ancora_stewart(k)
if __name__=='__main__':unittest.main()
