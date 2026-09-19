import sys,unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).parent/'lote41'))
from rotulagem import rotular
class Rotulos(unittest.TestCase):
    def test_censura_e_indefinicao_chegam_ao_valor(self):
        x=pd.DataFrame([dict(media=-112.29,censuradas=7,pares_indefinidos=0),dict(media=float('nan'),censuradas=11,pares_indefinidos=12),dict(media=-1.,censuradas=0,pares_indefinidos=0)])
        y=rotular(x)
        self.assertIn('CENSURADO',y.iloc[0].valor_rotulado)
        self.assertIn('INDEFINIDO',y.iloc[1].valor_rotulado)
        self.assertIn('CENSURADO',y.iloc[1].valor_rotulado)
        self.assertEqual(y.iloc[2].estatuto,'COMPLETO')
        self.assertTrue(pd.isna(y.iloc[1].media));self.assertEqual(y.iloc[0].media,-112.29)
    def test_nao_aceita_tabela_sem_contagem(self):
        with self.assertRaises(ValueError):rotular(pd.DataFrame([dict(media=1.)]))
