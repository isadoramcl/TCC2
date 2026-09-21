"""Bloco A — validacao fora da amostra. Nao altera nominal, dinamica nem RNG."""
import sys,json,hashlib,csv,time
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np, pandas as pd, yaml
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260920_fora_da_amostra'; OUT.mkdir(parents=True,exist_ok=True)
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
SEM=list(range(12)); ARMS=['centralizada','adaptativa']; SEED_AMOSTRA=20260920

def job(arg):
    a,seed,cen=arg
    p=S.carregar_parametros(); op=yaml.safe_load((ROOT/'config/mvp_v1.yaml').read_text())['opcoes']
    op['instrumentar_tarefas']=False
    g,d,c=S.carregar_instancia(a); sim=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)); r=sim.executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))}; row.update(r.contadores)
    den=row['p1_omissao']+row['p3_analitica']
    row.update(arquivo=a,semente=seed,cenario=cen,violacoes=len(r.violacoes),
               atraso_relativo=r.makespan/r.makespan_cpm,
               fracao_porta1=row['p1_omissao']/den if den else np.nan)
    return row

def rodar(nomes,tag):
    jobs=[(a,s,c) for a in nomes for s in SEM for c in ARMS]
    rows=[]; t0=time.time()
    with ProcessPoolExecutor(max_workers=4) as pool:
        for i,r in enumerate(pool.map(job,jobs,chunksize=8)):
            rows.append(r)
            if (i+1)%384==0: print(f'{tag} {i+1}/{len(jobs)} {time.time()-t0:.0f}s',flush=True)
    d=pd.DataFrame(rows); d.to_csv(OUT/f'bruto_{tag}.csv',index=False); return d

def ic(x):
    x=x.dropna(); n=len(x); m=x.mean()
    h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n) if n>1 else np.nan
    return dict(media=m,ic95_inf=m-h,ic95_sup=m+h,N_instancias=n)

def contraste(d,extra=None):
    p=d.pivot(index=['arquivo','semente'],columns='cenario',values=None)
    out=[]
    for m in MET:
        q=d.pivot(index=['arquivo','semente'],columns='cenario',values=m)
        dif=q['adaptativa']-q['centralizada']
        out.append(dict(metrica=m,**(extra or {}),**ic(dif.groupby('arquivo').mean())))
    return out

# ---------- 1. CONTROLE: reproduzir o nominal arquivado ----------
arq=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv',float_precision='round_trip')
nom_inst=sorted(arq.arquivo.unique())
print('CONTROLE: reproduzindo',len(nom_inst),'instancias do nominal',flush=True)
ctl=rodar(nom_inst,'controle_nominal')
k=['arquivo','semente','cenario']
a=arq.set_index(k).sort_index(); b=ctl.set_index(k).sort_index()
campos=[c for c in a.columns if c in b.columns and pd.api.types.is_numeric_dtype(a[c])]
falhas=[]
for c in campos:
    x=[float(v).hex() for v in b[c]]; y=[float(v).hex() for v in a.loc[b.index,c]]
    if x!=y: falhas.append(c)
json.dump(dict(campos_conferidos=len(campos),campos_divergentes=falhas,
               identidade_exata=not falhas),open(OUT/'controle_identidade.json','w'),indent=2)
print('CONTROLE identidade exata:',not falhas,'| divergentes:',falhas,flush=True)
assert not falhas, f'O runner nao reproduz o nominal: {falhas}'

# ---------- 2. AMOSTRA ESTRATIFICADA FORA DA AMOSTRA ----------
meta=pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').drop_duplicates('arquivo')
livres=meta[~meta.arquivo.isin(nom_inst)]
rng=np.random.default_rng(SEED_AMOSTRA)
sel=[]
for comb,g in livres.groupby('combinacao'):
    sel.append(g.arquivo.iloc[rng.integers(len(g))])
sel=sorted(sel)
pd.DataFrame(dict(arquivo=sel)).merge(meta,on='arquivo').to_csv(OUT/'amostra_estratificada.csv',index=False)
print('AMOSTRA: ',len(sel),'instancias, uma por combinacao, semente',SEED_AMOSTRA,flush=True)
oos=rodar(sel,'fora_da_amostra')
assert oos.violacoes.sum()==0, 'violacoes na amostra fora'

# ---------- 3. CONTRASTES ----------
dentro=contraste(arq); fora=contraste(oos)
cmp=pd.DataFrame(dentro).merge(pd.DataFrame(fora),on='metrica',suffixes=('_dentro','_fora'))
cmp['sobrepoe']=~((cmp.ic95_sup_dentro<cmp.ic95_inf_fora)|(cmp.ic95_sup_fora<cmp.ic95_inf_dentro))
cmp['mesmo_sinal']=np.sign(cmp.media_dentro)==np.sign(cmp.media_fora)
cmp.to_csv(OUT/'A2_dentro_vs_fora.csv',index=False)

# ---------- 4. ESTRATIFICACAO ----------
m=oos.merge(meta[['arquivo','NC','RF','RS','combinacao']],on='arquivo')
estr=[]
for fator in ['NC','RF','RS']:
    for nivel,g in m.groupby(fator):
        estr.extend(contraste(g,extra=dict(fator=fator,nivel=nivel,n_inst=g.arquivo.nunique())))
pd.DataFrame(estr).to_csv(OUT/'A3_estratificado.csv',index=False)

# ---------- 5. COBERTURA ----------
cob=[]
for nome,inst in [('publicado_nominal',nom_inst),('fora_da_amostra',sel)]:
    s=meta[meta.arquivo.isin(inst)]
    for f in ['NC','RF','RS']:
        cob.append(dict(conjunto=nome,fator=f,niveis_usados=len(s[f].dropna().unique()),
                        niveis_totais=len(meta[f].dropna().unique()),
                        faltando=sorted(set(meta[f].dropna().unique())-set(s[f].dropna().unique()))))
    cob.append(dict(conjunto=nome,fator='combinacao',niveis_usados=s.combinacao.nunique(),
                    niveis_totais=meta.combinacao.nunique(),faltando=[]))
pd.DataFrame(cob).to_csv(OUT/'A1_cobertura.csv',index=False)
print('\n=== A2: DENTRO x FORA ===',flush=True)
print(cmp[['metrica','media_dentro','ic95_inf_dentro','ic95_sup_dentro','media_fora','ic95_inf_fora','ic95_sup_fora','mesmo_sinal','sobrepoe']].to_string(index=False),flush=True)
print('\nCONCLUIU',flush=True)
