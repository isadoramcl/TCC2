import importlib.util
import itertools
import math
from pathlib import Path
import unittest
import numpy as np
from scipy.stats import binom,betabinom

class StewartC3(unittest.TestCase):
    def modulo(self):
        p=Path(__file__).parent/'lote37/distribuicoes.py'
        self.assertTrue(p.exists(),'distribuições C3 ainda ausentes')
        spec=importlib.util.spec_from_file_location('c3',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        return m

    def test_binomial_e_beta_contra_implementacao_independente(self):
        m=self.modulo()
        for n in [1,7,25]:
            np.testing.assert_allclose(m.binomial(n,.0163),binom.pmf(range(n+1),n,.0163),rtol=1e-12,atol=1e-14)
            np.testing.assert_allclose(m.beta_binomial(n,.7546,45.4563),betabinom.pmf(range(n+1),n,.7546,45.4563),rtol=1e-11,atol=1e-13)

    def test_recorrencia_reduz_a_binomial_e_confere_enumeracao(self):
        m=self.modulo()
        np.testing.assert_allclose(m.recorrencia(25,lambda k:.0163),binom.pmf(range(26),25,.0163),atol=1e-14)
        n=5;taxa=lambda k:.845*.0163*(k+1);bruto=np.zeros(n+1)
        for seq in itertools.product([0,1],repeat=n):
            k=0;prob=1.
            for falhou in seq:
                p=taxa(k);prob*=p if falhou else 1-p;k+=falhou
            bruto[k]+=prob
        np.testing.assert_allclose(m.recorrencia(n,taxa),bruto,atol=1e-14)
        self.assertAlmostEqual(m.p_dependente(25,.0163,.845)[0],(1-.845*.0163)**25,places=14)

    def test_beta_inviavel_falha_sem_clip(self):
        m=self.modulo()
        with self.assertRaises(ValueError):m.beta_parametros(.5,1.13)

    def test_portao_detecta_discrepancia_publicada(self):
        m=self.modulo()
        self.assertTrue(m.terceira_casa(62.3296428416,62.330))
        self.assertFalse(m.terceira_casa(67.5192333308,67.475))
