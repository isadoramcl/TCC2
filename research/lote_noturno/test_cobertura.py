import unittest,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from cobertura import estatistica
class Desenho(unittest.TestCase):
    def test_media_variancia_de_blocos(self):
        m,v=estatistica([[0.,2.],[2.,4.],[4.,6.],[6.,8.]])
        np.testing.assert_allclose(m,[3.,5.]);np.testing.assert_allclose(v,[5/3,5/3])
    def test_disjuncao_sementes(self):
        seeds=[10_000_000+b*28+off+j*2+i for b in range(500) for n,off in [(10,0),(4,20)] for j in range(n) for i in range(2)]
        self.assertEqual(len(seeds),14000);self.assertEqual(len(set(seeds)),14000)
if __name__=='__main__':unittest.main()
