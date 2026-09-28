"""Etapa 3: adiar usa k_fuga; executar atalho continua usando k_heuristico."""
import unittest
import pandas as pd
from test_drenagem_v3 import EstadoControlado,S,OpcoesMVP
class FugaForcada(EstadoControlado):
    def deve_fugir(self,*args):return True

def custo_fuga(cls,kh,kf):
    p=S.carregar_parametros();p['agentes']['n_agentes']['valor']=1
    p['agentes']['k_heuristico']['valor']=kh;p['agentes']['k_fuga']={'valor':kf}
    p['agentes']['r_recuperacao']['valor']=0.;p['agentes']['tau_sat']['valor']=-100.
    p['gestor']['P_min']['valor']=p['gestor']['P_max']['valor']=1.
    p['gestor']['omega']['valor']=1.;p['gestor']['limite_aversao_perda']['valor']=0.
    p['execucao']['horizonte_maximo_fator']['valor']=1
    task=pd.DataFrame([dict(tarefa=1,duracao=8,R1=1,sucessores='',Di=.2,nivel_dificuldade='baixa')])
    kw={} if cls is S.Simulacao else {'opcoes':OpcoesMVP(horizonte_automatico=False)}
    sim=cls(task,[1],1,p,'centralizada',0,**kw);sim.heu=True;r=sim.executar()
    assert r.contadores['p1_fuga']==1
    return 1.-sim.agentes[0].bateria
class FugaDesacoplada(unittest.TestCase):
    def test_k_fuga_controla_drenagem_nos_dois_lacos(self):
        for cls in [S.Simulacao,FugaForcada]:
            with self.subTest(classe=cls.__name__):
                self.assertAlmostEqual(custo_fuga(cls,.04,.10),.02,places=14)
                self.assertEqual(custo_fuga(cls,.02,.10),custo_fuga(cls,.04,.10))
                self.assertAlmostEqual(custo_fuga(cls,.04,.04),.008,places=14)
if __name__=='__main__':unittest.main()
