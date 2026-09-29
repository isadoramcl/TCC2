"""Controles do desenho v3; uma atribuição esquecida de k_he deve falhar."""
import unittest, importlib.util, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
class HMv3Test(unittest.TestCase):
 def module(self):
  path=ROOT/'research/hm_v3.py'
  self.assertTrue(path.exists(), 'Runner v3 com derivação ainda não implementado')
  spec=importlib.util.spec_from_file_location('hm_v3_tested',path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
 def test_derivacao_em_todas_propostas_e_extremos(self):
  m=self.module();base=m.S.carregar_parametros();before=base['agentes']['k_heuristico']['valor']
  points=m.lhs(400,m.LIMITES,np.random.default_rng(20260905))
  points=np.vstack([points,m.LIMITES[:,0],m.LIMITES[:,1],list(m.VERDADE.values())])
  for values in points:
   p=m.aplicar(base,dict(zip(m.NOMES,values)));self.assertEqual(float(p['agentes']['k_heuristico']['valor']).hex(),float(p['agentes']['k_analitico']['valor']).hex());self.assertEqual(p['agentes']['k_fuga']['valor'],.10)
  self.assertEqual(base['agentes']['k_heuristico']['valor'],before)
 def test_controle_negativo_derivacao(self):
  m=self.module();p=m.aplicar(m.S.carregar_parametros(),m.VERDADE);p['agentes']['k_heuristico']['valor']=np.nextafter(.065,1.)
  with self.assertRaises(AssertionError):m.verificar_derivacao(p)
 def test_variancia_unidade_bloco(self):
  m=self.module();v=np.array([[[1,1,1,1],[3,3,3,3]],[[3,3,3,3],[5,5,5,5]]]);a,b=m.estatistica(v)
  np.testing.assert_array_equal(a,[3]*4);np.testing.assert_array_equal(b,[1]*4)
 def test_sementes_cobertura_disjuntas(self):
  m=self.module();seeds=[m.semente_cobertura(b,g,j,i) for b in range(500) for g,n in [('obs',10),('sim',4)] for j in range(n) for i in range(2)]
  self.assertEqual(len(seeds),14000);self.assertEqual(len(set(seeds)),14000)
if __name__=='__main__':unittest.main()
