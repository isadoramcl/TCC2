import sys
from pathlib import Path
import unittest
import math
sys.path.insert(0,str(Path(__file__).parent/'lote41'))
import b2
class CensuraB2(unittest.TestCase):
    def test_sem_tarefa_nao_virar_fracao_zero(self):
        self.assertTrue(hasattr(b2,'fracao_p1'))
        self.assertTrue(math.isnan(b2.fracao_p1(0,0)))
        self.assertEqual(b2.fracao_p1(3,7),.3)
