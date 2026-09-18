"""Verificação dos limites; não transforma o controle publicado em aprovação."""
import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).parent/'lote37'))
from validar_c3_39 import limites_beta,limites_binomial,limites_pdependente,intervalo_chi
from distribuicoes import binomial,beta_binomial,p_dependente

class PrecisaoPublicada(unittest.TestCase):
    def test_beta_zero_extremos_exatos_e_alvo_fora(self):
        b=94*limites_beta(25,.75455,.75465,45.45625,45.45635)
        def zero(a,b):
            return 94*np.prod([(b+i)/(a+b+i) for i in range(25)])
        np.testing.assert_allclose(b[0],[zero(.75465,45.45625),zero(.75455,45.45635)],atol=1e-10,rtol=0)
        self.assertGreater(b[0,0],67.4755) # Mesmo incluindo arredondamento do alvo.

    def test_envoltorias_contem_pontos_interiores(self):
        casos=[(limites_beta(25,.75455,.75465,45.45625,45.45635),
                [beta_binomial(25,a,b) for a in np.linspace(.75455,.75465,7) for b in np.linspace(45.45625,45.45635,7)]),
               (limites_binomial(25,.01625,.01635),[binomial(25,p) for p in np.linspace(.01625,.01635,11)]),
               (limites_pdependente(25,.01625,.01635,.8445,.8455),
                [p_dependente(25,p,f) for p in np.linspace(.01625,.01635,7) for f in np.linspace(.8445,.8455,7)])]
        for lim,vals in casos:
            for x in vals:
                self.assertTrue(np.all(x >= lim[:,0]-1e-12))
                self.assertTrue(np.all(x <= lim[:,1]+1e-12))
                es=94*np.r_[x[:3],x[3:].sum()]
                chi=sum((np.array([68,18,5,3])-es)**2/es)
                a,b=intervalo_chi(94*lim)
                self.assertLessEqual(a-1e-10,chi);self.assertLessEqual(chi,b+1e-10)
