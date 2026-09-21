import sys,pandas as pd,numpy as np
from scipy.stats import t
from pathlib import Path
O=Path(__file__).resolve().parents[3]/'outputs/diagnosticos/20260921_portoes_suaves'
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
grupo=sys.argv[1] if len(sys.argv)>1 else 'nominal'
vars_=sys.argv[2].split(',') if len(sys.argv)>2 else ['controle','G','F1','F2','GF']
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
def ic(x):
    x=x.dropna(); n=len(x); m=x.mean(); h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n); return m,m-h,m+h
res=[];desc=[]
for v in vars_:
    f=O/f'bruto_{v}_{grupo}.csv'
    if not f.exists(): continue
    d=pd.read_csv(f)
    for col in ['fracao_fuga']:
        if col not in d: d[col]=0.0
    for m in MET:
        q=d.pivot(index=['arquivo','semente'],columns='cenario',values=m)
        mm,lo,hi=ic((q['adaptativa']-q['centralizada']).groupby('arquivo').mean())
        res.append(dict(variante=v,metrica=m,contraste=round(mm,4),ic_inf=round(lo,4),ic_sup=round(hi,4)))
    g=d.groupby('cenario').agg(concluiu=('concluiu','mean'),atraso=('atraso_relativo','mean'),
        falha=('taxa_falha_efetiva','mean'),omissao=('taxa_omissao','mean'),porta1=('fracao_porta1','mean'),
        fuga=('fracao_fuga','mean'),N_req=('N_req','mean'),N_blocked=('N_blocked','mean'),
        ajuda=('p2_ajuda','mean'),conf_final=('confianca_media_final','mean')).round(4)
    g.insert(0,'variante',v); desc.append(g)
print(pd.concat(desc).to_string()); print()
r=pd.DataFrame(res); print(r.pivot(index='metrica',columns='variante',values='contraste')[ [v for v in vars_ if v in r.variante.unique()] ].to_string())
print(); print(r.to_string(index=False))
