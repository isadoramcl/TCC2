"""79: guarda separada da identidade; custo medido em execução contrafactual."""
from pathlib import Path
import sys,unittest,copy
import pandas as pd,yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
class EstadoControlado(SimulacaoMVP):
    def decidir_porta(self,p_heu,sorteio):return self.heu
    def pressao(self,t):return 1.
    def multiplicadores(self,a,P):return 1.,1.
    def taxa_basal_agente(self,a,nivel):return 0.
def custo(heu,kh=None,dur=8):
    p=S.carregar_parametros();p['agentes']['n_agentes']['valor']=1
    p['agentes']['competencia_inicial']['valor']={'media':.98,'desvio':0.}
    p['risco']['R_error']['valor']=0.
    if kh is not None:p['agentes']['k_heuristico']['valor']=kh
    task=pd.DataFrame([dict(tarefa=1,duracao=dur,R1=1,sucessores='',Di=.2,nivel_dificuldade='baixa')])
    sim=EstadoControlado(task,[1],dur,p,'centralizada',0,opcoes=OpcoesMVP(fator_omissao=.75,rho_omissao=0.,retrabalho_fila=False))
    sim.heu=heu;r=sim.executar();b=[1.]+r.trajetorias['bateria_media'];dr=[x-y for x,y in zip(b,b[1:])]
    return dict(periodos=len(dr),total=1.-b[-1],drenagens=dr,violacoes=r.violacoes)
class DrenagemV3(unittest.TestCase):
    def test_custo_real_por_periodo_e_tarefa(self):
        # Restaurar kh=.10 faria este teste falhar; mede bateria no laço real.
        for dur in [4,8,12]:
            with self.subTest(dur=dur):
                h,a=custo(True,dur=dur),custo(False,dur=dur)
                self.assertLessEqual(max(h['drenagens']),max(a['drenagens'])+1e-14)
                self.assertLess(h['total'],a['total'])
                self.assertAlmostEqual(h['total']/a['total'],.75,places=12)
    def test_negativo_drenagem_acelerada_reprova_economia(self):
        h,a=custo(True,.10),custo(False,.10)
        self.assertGreater(max(h['drenagens']),max(a['drenagens']))
        self.assertGreater(h['total'],a['total'])
    def test_tarefa_unitaria_nao_promete_economia_estrita(self):
        h,a=custo(True,.04,1),custo(False,.04,1)
        self.assertEqual(h['periodos'],a['periodos']);self.assertEqual(h['total'],a['total'])
    def test_guarda_nova_independente_de_identidade(self):
        # violacoes é diagnóstico: 0.10 é inválido na v3, não campo de identidade.
        for kh,expected in [(.10,1),(.04,0)]:
            for cen in ['centralizada','adaptativa']:
                for cls in [S.Simulacao,SimulacaoMVP]:
                    with self.subTest(kh=kh,cenario=cen,classe=cls.__name__):
                        p=S.carregar_parametros();p['agentes']['k_heuristico']['valor']=kh
                        g,d,c=S.carregar_instancia('j6010_1.sm')
                        kw={}
                        if cls is SimulacaoMVP:
                            op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];op['instrumentar_tarefas']=False;kw['opcoes']=OpcoesMVP(**op)
                        r=cls(g,d,c,p,cen,0,**kw).executar()
                        self.assertEqual(len(r.violacoes),expected)
                        if expected:self.assertIn('não pode exceder',r.violacoes[0])
if __name__=='__main__':unittest.main()
