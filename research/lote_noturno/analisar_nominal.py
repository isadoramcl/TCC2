"""E2/E3/C4: análises do nominal arquivado, sem alterar dinâmica."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'outputs/diagnosticos/noturno_nominal'
d=pd.read_csv(out/'bruto.csv');t=pd.read_csv(out/'trajetorias.csv');r=pd.read_csv(out/'tarefas.csv')
assert len(d)==384 and d.concluiu.all()
keys=['arquivo','semente','cenario'];rows=[]
for ids,g in t.groupby(keys):
    cross=g[g.confianca_media>=.95]
    rows.append(dict(zip(keys,ids),cruzou=not cross.empty,primeiro_periodo=None if cross.empty else int(cross.t.min()),media_temporal=g.confianca_media.mean(),final=g.iloc[-1].confianca_media))
c=pd.DataFrame(rows);c.to_csv(out/'E2_cruzamentos.csv',index=False)
summary=c.groupby('cenario').agg(N=('cruzou','size'),cruzaram=('cruzou','sum'),primeiro_mediana=('primeiro_periodo','median'),primeiro_min=('primeiro_periodo','min'),primeiro_max=('primeiro_periodo','max'),media_temporal_por_execucao=('media_temporal','mean'),media_final=('final','mean'))
summary.to_csv(out/'E2_resumo.csv');print('E2',summary.to_string())
rows=[]
for unidade,df in [('periodo',t),('tarefa_executada',r[r.executada])]:
 for cen,g in df.groupby('cenario'):
  for met in ['mu_cog','mu_rede']:
   x=g[met];rows.append(dict(unidade=unidade,cenario=cen,metrica=met,N=len(g),media_pool=x.mean(),media_por_execucao=g.groupby(['arquivo','semente'])[met].mean().mean(),min=x.min(),q05=x.quantile(.05),q50=x.median(),q95=x.quantile(.95),max=x.max()))
e=pd.DataFrame(rows);e.to_csv(out/'E3_distribuicoes.csv',index=False);print('E3',e.to_string(index=False))
# C4: contrafactual local esperado em estados que efetivamente executaram tarefa.
rows=[]
for cen,g in r[r.executada].groupby('cenario'):
 for tau in [.7,1.,1.4]:
  for s in [.01,.25,.6]:
   vals=[]
   for P in [.3,1.]:
    E=g.Di*P/np.maximum(g.B,.05)
    prob=1/(1+np.exp(-np.clip((E-tau)/s,-700,700)))
    vals.append(prob.mean())
   rows.append(dict(cenario=cen,tau_sat=tau,s_transicao=s,N_estados=len(g),P_inferior=.3,P_superior=1.,fracao_esperada_inferior=vals[0],fracao_esperada_superior=vals[1],razao=vals[1]/vals[0]))
f=pd.DataFrame(rows);f.to_csv(out/'C4_extremos_pressao.csv',index=False);print('C4',f.to_string(index=False))
