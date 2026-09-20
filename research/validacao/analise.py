import numpy as np, pandas as pd
from scipy.stats import t
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/diagnosticos/20260920_fora_da_amostra'
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
def ic(x):
    x=x.dropna(); n=len(x); m=x.mean()
    h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n) if n>1 else np.nan
    return dict(media=m,ic95_inf=m-h,ic95_sup=m+h,N_inst=n)
def contraste(d,extra=None):
    out=[]
    for m in MET:
        q=d.pivot(index=['arquivo','semente'],columns='cenario',values=m)
        dif=q['adaptativa']-q['centralizada']
        out.append(dict(metrica=m,**(extra or {}),**ic(dif.groupby('arquivo').mean())))
    return out
arq=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv',float_precision='round_trip')
# derivadas, mesma formula do runner (job): nao alteram dado, so reconstroem colunas
if 'atraso_relativo' not in arq: arq['atraso_relativo']=arq.makespan/arq.makespan_cpm
if 'fracao_porta1' not in arq:
    _d=arq.p1_omissao+arq.p3_analitica
    arq['fracao_porta1']=np.where(_d>0,arq.p1_omissao/_d,np.nan)
oos=pd.read_csv(OUT/'bruto_fora_da_amostra.csv',float_precision='round_trip')
meta=pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').drop_duplicates('arquivo')
a=pd.DataFrame(contraste(arq)); b=pd.DataFrame(contraste(oos))
c=a.merge(b,on='metrica',suffixes=('_dentro','_fora'))
c['mesmo_sinal']=np.sign(c.media_dentro)==np.sign(c.media_fora)
c['exclui_zero_fora']=(c.ic95_inf_fora>0)|(c.ic95_sup_fora<0)
c['sobrepoe']=~((c.ic95_sup_dentro<c.ic95_inf_fora)|(c.ic95_sup_fora<c.ic95_inf_dentro))
c.to_csv(OUT/'A2_dentro_vs_fora.csv',index=False)
print('=== A2 — DENTRO (16 inst) x FORA (48 inst) ===')
for r in c.itertuples():
    print(f'{r.metrica:27s} dentro {r.media_dentro:+8.4f} [{r.ic95_inf_dentro:+.4f};{r.ic95_sup_dentro:+.4f}]   '
          f'fora {r.media_fora:+8.4f} [{r.ic95_inf_fora:+.4f};{r.ic95_sup_fora:+.4f}]   '
          f'sinal={"IGUAL" if r.mesmo_sinal else "INVERTEU"}  exclui0={"sim" if r.exclui_zero_fora else "NAO"}  IC sobrepoe={"sim" if r.sobrepoe else "nao"}')
m=oos.merge(meta[['arquivo','NC','RF','RS','combinacao']],on='arquivo')
estr=[]
for f in ['NC','RF','RS']:
    for niv,g in m.groupby(f):
        estr.extend(contraste(g,extra=dict(fator=f,nivel=round(float(niv),4),n_inst=g.arquivo.nunique())))
e=pd.DataFrame(estr); e['exclui_zero']=(e.ic95_inf>0)|(e.ic95_sup<0); e.to_csv(OUT/'A3_estratificado.csv',index=False)
print('\n=== A3 — POR ESTRATO (so os que NAO excluem zero ou trocam de sinal) ===')
prob=e[(~e.exclui_zero)|(e.media>0)]
print(prob[['fator','nivel','n_inst','metrica','media','ic95_inf','ic95_sup','exclui_zero']].to_string(index=False) if len(prob) else 'NENHUM: todos os estratos mantem sinal negativo com IC95 excluindo zero.')
print('\n=== A3 — RF=0,25, o nivel nunca antes testado ===')
r25=e[(e.fator=='RF')&(np.isclose(e.nivel,0.25))]
print(r25[['metrica','n_inst','media','ic95_inf','ic95_sup','exclui_zero']].to_string(index=False))
cob=[]
for nome,inst in [('publicado_nominal',sorted(arq.arquivo.unique())),('fora_da_amostra',sorted(oos.arquivo.unique()))]:
    s=meta[meta.arquivo.isin(inst)]
    for f in ['NC','RF','RS']:
        falta=sorted(set(np.round(meta[f].dropna().unique(),4))-set(np.round(s[f].dropna().unique(),4)))
        cob.append(dict(conjunto=nome,fator=f,usados=len(s[f].dropna().unique()),totais=len(meta[f].dropna().unique()),faltando=falta))
    cob.append(dict(conjunto=nome,fator='combinacao',usados=s.combinacao.nunique(),totais=meta.combinacao.nunique(),faltando=[]))
pd.DataFrame(cob).to_csv(OUT/'A1_cobertura.csv',index=False)
print('\n=== A1 — COBERTURA ==='); print(pd.DataFrame(cob).to_string(index=False))
