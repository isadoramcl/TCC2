import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/modelo'))
spec=importlib.util.spec_from_file_location('runner',ROOT/'src/modelo/20_experimento_mvp.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class ExperimentoTests(unittest.TestCase):
    def test_di_usa_quartis_globais(self):
        d=pd.DataFrame({'arquivo':['a']*4+['b']*4,'duracao_norm':[0,.1,.2,.3,.7,.8,.9,1], 'intensidade_norm':[0]*8,'criticidade_folga':[0]*8})
        r=m.recalcular_di(d,{'duracao':1,'recursos':0,'criticidade':0})
        self.assertEqual(list(r.nivel_dificuldade.astype(str)),['baixa']*2+['media']*2+['alta']*2+['muito alta']*2)
    def test_saida_existente_recusada(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileExistsError): m.preparar_saida(Path(d),{})
    def test_censura_preservada(self):
        d=pd.DataFrame([dict(configuracao='x',arquivo=a,semente=s,cenario=c,concluiu=not(c=='adaptativa' and s==0),metrica=3 if c=='adaptativa' else 1) for a in ['a','b'] for s in [0,1] for c in ['centralizada','adaptativa']])
        contrasts,summary=m.resumir(d)
        r=summary[summary.metrica=='metrica'].iloc[0]
        self.assertEqual(r.media_diferenca,2)
        self.assertEqual(r.n_pares_censurados,2)
        self.assertEqual(len(contrasts[contrasts.metrica=='metrica']),2)
if __name__=='__main__': unittest.main()
