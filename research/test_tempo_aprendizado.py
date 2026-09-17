"""TL é uma convenção de contagem; Eq3 não deve mudar o estado físico."""
import unittest
import test_crowder
from simulador_mvp import OpcoesMVP

class TempoAprendizado(unittest.TestCase):
    def setUp(self):
        self.assertIn('lei_tempo_aprendizado',OpcoesMVP.__dataclass_fields__)

    def test_sucesso_eq3_usa_delta_na_escala_original(self):
        s,a,b=test_crowder.Crowder().sim(lei_tempo_aprendizado='crowder_eq3')
        s.comunicar(a,s.tarefas[1],0,.2)
        self.assertAlmostEqual(s.TL,.105)
        self.assertAlmostEqual(a.competencia,.442)

    def test_insucesso_eq3_conta_005_mas_bloqueio_nao(self):
        s,a,b=test_crowder.Crowder().sim(lei_tempo_aprendizado='crowder_eq3')
        s.comunicar(a,s.tarefas[1],0,.6)
        self.assertEqual(s.TL,0.)
        b.tarefa_atual=1
        s.comunicar(a,s.tarefas[1],0,.2)
        self.assertEqual(s.TL,.05)
        self.assertEqual(s.cnt['N_fail'],1)

    def test_unitario_preserva_convencao_anterior(self):
        self.assertEqual(OpcoesMVP().lei_tempo_aprendizado,'unitario')
        s,a,b=test_crowder.Crowder().sim(lei_tempo_aprendizado='unitario')
        b.tarefa_atual=1;s.comunicar(a,s.tarefas[1],0,.2)
        self.assertEqual(s.TL,0.)
        b.tarefa_atual=None;s.comunicar(a,s.tarefas[1],1,.2)
        self.assertEqual(s.TL,1.)

    def test_lei_desconhecida_rejeitada(self):
        with self.assertRaises(ValueError):OpcoesMVP(lei_tempo_aprendizado='typo')

if __name__=='__main__':unittest.main()
