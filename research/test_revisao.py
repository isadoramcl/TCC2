"""Controles de regressão do relatório e do estimador experimental."""
import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


class TestRevisao(unittest.TestCase):
    def test_relatorio_nao_declara_convergencia_ou_produto_suficiente(self):
        hm=load('relatorio','src/modelo/04_gemeo_identico.py')
        with tempfile.TemporaryDirectory() as tmp:
            tab=Path(tmp)/'tables'; tab.mkdir(); hm.TAB=tab; hm.LOGS=Path(tmp)/'logs'
            for name in ['modelo_04_hm_onda1.csv','modelo_04_hm_onda2.csv','modelo_04_observacoes_sinteticas.csv']:
                shutil.copy2(ROOT/'outputs/tables'/name,tab/name)
            before=sys.argv
            try:
                sys.argv=['04_gemeo_identico.py','relatorio']
                output=io.StringIO()
                with contextlib.redirect_stdout(output): hm.main()
            finally: sys.argv=before
            text=output.getvalue()
            self.assertNotIn('as ondas CONVERGIRAM',text)
            self.assertNotIn('Os observaveis agregados so veem',text)
            self.assertIn('nao demonstra identificabilidade estrutural',text)
            # Mesma tabela numérica: a alteração é de interpretação.
            pd.testing.assert_frame_equal(pd.read_csv(tab/'modelo_04_identificabilidade.csv'),
                                          pd.read_csv(ROOT/'outputs/tables/modelo_04_identificabilidade.csv'))

    def test_estimando_fixo_nao_trata_offset_entre_instancias_como_ruido(self):
        m=load('pilotos_test','src/modelo/17_pilotos_revisao.py')
        rows=[]
        for seed in range(4):
            for instance,value in [('a',0.),('b',10.)]:
                rows.append(dict(semente=seed,instancia=instance,**{o:value for o in m.hm.OBSERVAVEIS}))
        s=m.estatisticas(pd.DataFrame(rows))
        self.assertEqual(s['var_pareada_taxa_omissao'],0.)
        self.assertGreater(s['var_legado_taxa_omissao'],0.)

    def test_estimador_pareado_preserva_covariancia_da_semente(self):
        m=load('pilotos_cov','src/modelo/17_pilotos_revisao.py')
        rows=[]
        for seed in range(2):
            for instance,offset in [('a',0.),('b',10.)]:
                rows.append(dict(semente=seed,instancia=instance,**{o:offset+2*seed for o in m.hm.OBSERVAVEIS}))
        s=m.estatisticas(pd.DataFrame(rows))
        self.assertAlmostEqual(s['var_pareada_taxa_omissao'],1.)


if __name__=='__main__': unittest.main()
