import copy
import unittest
from test_mvp import caso
from simulador_mvp import SimulacaoMVP, OpcoesMVP

class TaxaFalha(unittest.TestCase):
    def test_falha_total_independe_de_reporte_na_tarefa_controlada(self):
        for falha in (False, True):
            for reporte in (0., 1.):
                g,p=caso(falha=falha)
                p['cenarios']['centralizada']['p_reporte']['valor']=reporte
                p['cenarios']['centralizada']['p_deteccao']['valor']=1.
                s=SimulacaoMVP(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP())
                r=s.executar()
                self.assertTrue(r.concluiu)
                self.assertTrue(hasattr(r,'taxa_falha_efetiva'),'Resultado deve expor taxa efetiva')
                self.assertEqual(r.taxa_falha_efetiva,float(falha))
                self.assertEqual(r.taxa_omissao,float(falha)*(1-reporte))
