import importlib.util
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/modelo'))
spec=importlib.util.spec_from_file_location('runner_tl',ROOT/'src/modelo/25_teste_tempo_aprendizado.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RunnerTL(unittest.TestCase):
    def test_par_real_inclui_cenario_sem_comunicacoes(self):
        import pandas as pd
        arquivo=sorted(pd.read_csv(m.BASE/'bruto.csv').arquivo.unique())[0]
        for cen in ['centralizada','adaptativa']:
            rows=m.job((arquivo,0,cen))
            self.assertEqual(len(rows),2)
            self.assertEqual([r['lei'] for r in rows],['unitario','crowder_eq3'])
            if cen=='centralizada':self.assertEqual([r['TL'] for r in rows],[0.,0.])
            self.assertTrue(all(r['concluiu'] and r['violacoes']==0 for r in rows))
if __name__=='__main__':unittest.main()
