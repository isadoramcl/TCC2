import unittest,importlib.util
from pathlib import Path
class CoberturaPareadaTest(unittest.TestCase):
 def test_pareamento_e_disjuncao(self):
  p=Path(__file__).with_name('cobertura_pareada_v3.py');self.assertTrue(p.exists(),'Complemento pareado ainda não implementado')
  spec=importlib.util.spec_from_file_location('covpaired',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  seen=set()
  for b in range(500):
   for group,n in [('obs',10),('sim',4)]:
    seeds=m.seeds(b,group)
    self.assertEqual(len(seeds),n)
    for pair in seeds:
     self.assertEqual(pair[0],pair[1]);self.assertNotIn(pair[0],seen);seen.add(pair[0])
  self.assertEqual(len(seen),7000)
if __name__=='__main__':unittest.main()
