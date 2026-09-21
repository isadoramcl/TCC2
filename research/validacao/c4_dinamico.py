"""C4 dinâmico: trajetórias completas com P fixada em 0,30 e em 1,00, malha tau_sat x s_transicao.
Modelo nominal sem alteração (opções default); só a função de pressão é substituída por uma constante.
Uso: python c4_dinamico.py PARTE/N [v1|v2]  (v1 = evidência de 21/09 em 20260921_c4_dinamico; v2 = nominal atual)"""
import sys,time
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import pandas as pd,numpy as np,yaml
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'src/modelo'))
VERSAO=sys.argv[2] if len(sys.argv)>2 else 'v2'
CONFIG={'v1':'config/mvp_v1.yaml','v2':'config/mvp.yaml'}[VERSAO]
SAIDA=ROOT/{'v1':'outputs/diagnosticos/20260921_c4_dinamico','v2':'outputs/diagnosticos/20260921_nominal_v2/c4_dinamico'}[VERSAO]; SAIDA.mkdir(parents=True,exist_ok=True)
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
class PressaoFixa(SimulacaoMVP):
    P_FIXA=None
    def pressao(self,t): return self.P_FIXA
def job(a):
    arq,seed,cen,P,ts,s=a
    p=S.carregar_parametros(); p['agentes']['tau_sat']['valor']=ts; p['agentes']['s_transicao']['valor']=s
    op=yaml.safe_load((ROOT/CONFIG).read_text())['opcoes']; op.update(instrumentar_tarefas=False,limite_horizonte_fator=16)
    g,d,c=S.carregar_instancia(arq); sim=PressaoFixa(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)); sim.P_FIXA=P; r=sim.executar()
    n=r.contadores['p1_omissao']+r.contadores['p3_analitica']
    return dict(arquivo=arq,semente=seed,cenario=cen,P=P,tau_sat=ts,s_transicao=s,concluiu=r.concluiu,
                p1=r.contadores['p1_omissao'],executadas=n,fracao_porta1=r.contadores['p1_omissao']/n if n else np.nan)
if __name__=='__main__':
    i,n=map(int,sys.argv[1].split('/'))
    inst=sorted(pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv').arquivo.unique())
    jobs=[(a,s,c,P,ts,sv) for ts in [.7,1.,1.4] for sv in [.01,.25,.6] for P in [.3,1.] for c in ['centralizada','adaptativa'] for a in inst for s in range(4)]
    jobs=jobs[i::n]; t0=time.time()
    with ProcessPoolExecutor(2) as p: d=pd.DataFrame(list(p.map(job,jobs,chunksize=8)))
    d.to_csv(SAIDA/f"c4_dinamico_p{i}de{n}.csv",index=False); print(len(d),'execucoes',round(time.time()-t0),'s')
