"""Contrafactual executa o simulador real; observação do risco não o substitui."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
import simulador as S
import simulador_mvp as M

class Sorteios:
    def __init__(self):self.i=iter([.4,.25,.9])
    def random(self):return next(self.i)

class Forcada(M.SimulacaoMVP):
    def decidir_porta(self,p_heu,sorteio):return self.forcar_p1

def par_contrafactual(fator,rho):
    g=pd.DataFrame([dict(tarefa=1,duracao=8,R1=1,sucessores='',Di=.8,nivel_dificuldade='baixa')])
    p=S.carregar_parametros(); p['agentes']['n_agentes']['valor']=1
    p['agentes']['competencia_inicial']['valor']={'media':.98,'desvio':0.}
    p['agentes']['tau_sat']['valor']=.3
    p['gestor']['P_min']['valor']=p['gestor']['P_max']['valor']=.9
    p['fuzzy']['mu_minimo']['valor']=1.
    p['risco']['F_ancora']['valor']=.1; p['risco']['R_error']['valor']=0.
    p['cenarios']['centralizada']['p_reporte']['valor']=1.
    res=[];real=M.risco_porta
    for heu in [True,False]:
        s=Forcada(g,[1],8,copy.deepcopy(p),'centralizada',0,opcoes=M.OpcoesMVP(fator_omissao=fator,rho_omissao=rho,retrabalho_fila=False))
        s.forcar_p1=heu;s.rng=Sorteios();registro=[]
        def observar(*args):
            prob=real(*args);registro.append((args,prob));return prob
        with patch.object(M,'risco_porta',side_effect=observar):r=s.executar()
        args,prob=registro[0]
        res.append(dict(porta=s.tarefas[1].porta,duracao=s.tarefas[1].fim-s.tarefas[1].inicio,p0=args[0],p_heu=args[1],p_falha=prob,reportadas=r.n_reportadas))
    return res

def detecta_troca(par):
    a,b=par
    return a['duracao']<b['duracao'] and a['p_falha']>b['p_falha']

class Causal(unittest.TestCase):
    def test_efeito_causal_no_mesmo_estado_e_sorteio(self):
        self.assertTrue(hasattr(M.SimulacaoMVP,'decidir_porta'),'intervenção da porta ainda ausente')
        a,b=par_contrafactual(.75,.35)
        self.assertEqual((a['porta'],b['porta']),('P1_omissao','P3_analitica'))
        self.assertEqual(a['p0'],b['p0']);self.assertEqual(a['p_heu'],b['p_heu'])
        self.assertLessEqual(a['duracao'],b['duracao']);self.assertGreaterEqual(a['p_falha'],b['p_falha'])
        self.assertTrue(detecta_troca([a,b]))
        self.assertEqual((a['reportadas'],b['reportadas']),(1,0))
    def test_controle_negativo_falha_em_detectar_efeito(self):
        self.assertTrue(hasattr(M.SimulacaoMVP,'decidir_porta'),'intervenção da porta ainda ausente')
        a,b=par_contrafactual(1.,0.)
        self.assertEqual(a['duracao'],b['duracao']);self.assertEqual(a['p_falha'],b['p_falha'])
        self.assertFalse(detecta_troca([a,b]),'verificador declarou mecanismo no controle neutro')
        self.assertEqual((a['reportadas'],b['reportadas']),(0,0))
if __name__=='__main__': unittest.main()
