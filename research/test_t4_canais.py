import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('t4',ROOT/'research/lote41/t4.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SeparacaoCanais(unittest.TestCase):
    def test_overrides_nao_trocam_reporte(self):
        for rep in ['centralizada','adaptativa']:
            pcc,occ=m.configurar('centralizada','centralizada',rep)
            pac,oac=m.configurar('adaptativa','centralizada',rep)
            pca,oca=m.configurar('centralizada','adaptativa',rep)
            self.assertEqual(pcc,pca)
            self.assertEqual(occ['tau_rede'],oac['tau_rede'])
            self.assertEqual(occ['tau_portao'],oca['tau_portao'])
            self.assertNotEqual(occ['tau_rede'],oca['tau_rede'])
            for k in ['p_reporte','p_deteccao']:
                self.assertEqual(pcc['cenarios']['teste'][k],pac['cenarios']['teste'][k])
