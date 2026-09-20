import sys,json,time
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np, pandas as pd, yaml
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260920_fora_da_amostra'
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
SEM=list(range(12)); ARMS=['centralizada','adaptativa']
def job(arg):
    a,seed,cen=arg
    p=S.carregar_parametros(); op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
    op['instrumentar_tarefas']=False
    g,d,c=S.carregar_instancia(a); sim=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)); r=sim.executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))}; row.update(r.contadores)
    den=row['p1_omissao']+row['p3_analitica']
    row.update(arquivo=a,semente=seed,cenario=cen,violacoes=len(r.violacoes),
               atraso_relativo=r.makespan/r.makespan_cpm,
               fracao_porta1=row['p1_omissao']/den if den else np.nan)
    return row
import sys as _s
LOTE=int(_s.argv[1])
_all=sorted(pd.read_csv(OUT/'amostra_estratificada.csv').arquivo.unique())
sel=_all[LOTE*12:(LOTE+1)*12]
jobs=[(a,s,c) for a in sel for s in SEM for c in ARMS]
t0=time.time(); rows=[]
with ProcessPoolExecutor(max_workers=4) as pool:
    for r in pool.map(job,jobs,chunksize=16): rows.append(r)
oos=pd.DataFrame(rows); oos.to_csv(OUT/f'bruto_lote{LOTE}.csv',index=False)
print(f'{len(oos)} execucoes em {time.time()-t0:.0f}s | violacoes={oos.violacoes.sum()} | concluiu={oos.concluiu.all()}',flush=True)
