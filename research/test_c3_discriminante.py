import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).parent/'lote41'))
from c3 import controles,metricas,auditar_fonte
class ControleDiscriminante(unittest.TestCase):
    def test_cinco_erros_sao_discriminados(self):
        cs=controles();ref=metricas(cs.pop('candidata'))
        self.assertFalse(ref['monotona'])
        self.assertEqual(len(cs),5)
        for nome,x in cs.items():
            with self.subTest(nome=nome):
                self.assertGreater(metricas(x)['maior_desvio_pct'],1.)
                self.assertGreaterEqual(metricas(x)['maior_desvio_pct']/ref['maior_desvio_pct'],10.)
    def test_candidata_confere_com_implementacao_original(self):
        import importlib.util
        import numpy as np
        spec=importlib.util.spec_from_file_location('distribuicoes_c3',Path(__file__).parent/'lote37/distribuicoes.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        np.testing.assert_allclose(controles()['candidata'],94*m.beta_binomial(25,.7546,45.4563)[:5],atol=1e-10,rtol=0)

    def test_A16(self):
        d,inv=auditar_fonte()
        self.assertEqual(len(d),5329)
        self.assertTrue(d.construtos_compativeis.all())
        self.assertFalse(d.E0_compativel.any())
        self.assertGreater(inv['alpha_inverso'],.75465)
        self.assertLess(inv['beta_inverso'],45.45625)
