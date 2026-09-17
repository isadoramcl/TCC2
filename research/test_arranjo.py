import importlib.util
import sys
import unittest
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S

class Arranjo(unittest.TestCase):
    def modulo(self):
        p=ROOT/'src/modelo/26_testes_arranjo.py'
        self.assertTrue(p.exists(),'runner T1/T2 ainda ausente')
        spec=importlib.util.spec_from_file_location('arranjo',p)
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        return m

    def test_celulas_isolam_blocos(self):
        m=self.modulo();p=S.carregar_parametros();cs={c['nome']:c for c in m.celulas_t2(p)}
        ref=cs['referencia']['cenario'];a=cs['confianca']['cenario'];b=cs['reporte']['cenario']
        self.assertEqual({k for k in ref if ref[k]!=a[k]},{'tau_inicial','tau_min'})
        self.assertEqual({k for k in ref if ref[k]!=b[k]},{'p_reporte','p_deteccao'})
        self.assertEqual(cs['ambos']['cenario'],p['cenarios']['adaptativa'])

    def test_malha_inclui_igualdade_e_vizinhos_estritos(self):
        m=self.modulo()
        for tm in [.25,.6]:
            x=m.malha(tm)
            self.assertIn(tm,x);self.assertIn(round(tm-1e-6,6),x);self.assertIn(round(tm+1e-6,6),x)
            self.assertEqual((min(x),max(x)),(0.,1.))

    def test_detector_rejeita_inclinacao_e_aceita_degrau(self):
        m=self.modulo()
        x=[.1,.2,.25,.3,.4]
        self.assertTrue(m.degrau_puro(x,[0,0,0,1,1],.25))
        self.assertFalse(m.degrau_puro(x,x,.25))
        self.assertFalse(m.degrau_puro(x,[0,0,.1,1,1],.25))
