"""Nominal v2 (config/mvp.yaml com portões suaves): nominal 16 instâncias e fora da amostra 48.
Uso: python nominal_v2.py nominal | fora1 | fora2 | fora3 | analise"""
import sys,json,hashlib,time
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np,pandas as pd,yaml
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260921_nominal_v2'; OUT.mkdir(parents=True,exist_ok=True)
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
def job(arg):
    a,seed,cen=arg; p=S.carregar_parametros(); op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']; op['instrumentar_tarefas']=False
    g,d,c=S.carregar_instancia(a); r=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)).executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))}; row.update(r.contadores)
    den=row['p1_omissao']+row['p3_analitica']; dec=den+row['p1_fuga']
    row.update(arquivo=a,semente=seed,cenario=cen,violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,
               fracao_porta1=row['p1_omissao']/den if den else np.nan,fracao_fuga=row['p1_fuga']/dec if dec else np.nan)
    return row
def rodar(inst,tag):
    jobs=[(a,s,c) for a in inst for s in range(12) for c in ['centralizada','adaptativa']]
    with ProcessPoolExecutor(2) as p: d=pd.DataFrame(list(p.map(job,jobs,chunksize=8)))
    d.to_csv(OUT/f'bruto_{tag}.csv',index=False); return d
def ic(x):
    x=x.dropna();n=len(x);m=x.mean();h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n);return dict(media=m,ic95_inf=m-h,ic95_sup=m+h,N_instancias=n)
def contraste(d,**extra):
    out=[]
    for m in MET:
        q=d.pivot(index=['arquivo','semente'],columns='cenario',values=m)
        out.append(dict(metrica=m,**extra,**ic((q.adaptativa-q.centralizada).groupby('arquivo').mean())))
    return out
if __name__=='__main__':
    modo=sys.argv[1]; t0=time.time()
    nom=sorted(pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv').arquivo.unique())
    amostra=pd.read_csv(ROOT/'outputs/diagnosticos/20260920_fora_da_amostra/amostra_estratificada.csv')
    fora=sorted(amostra.arquivo.unique())
    if modo=='nominal':
        d=rodar(nom,'nominal')
        ref=pd.read_csv(ROOT/'outputs/diagnosticos/20260921_portoes_suaves/varredura_s/nominal_s0.25.csv',float_precision='round_trip')
        k=['arquivo','semente','cenario']; A=ref.set_index(k); B=pd.read_csv(OUT/'bruto_nominal.csv',float_precision='round_trip').set_index(k).sort_index()
        campos=[c for c in A.columns if c in B.columns and pd.api.types.is_numeric_dtype(A[c])]
        div=[c for c in campos if [float(x).hex() for x in B[c]]!=[float(x).hex() for x in A.loc[B.index,c]]]
        json.dump(dict(referencia='varredura_s/nominal_s0.25.csv (opcoes ligadas por sobreposicao)',campos=len(campos),divergentes=div),open(OUT/'identidade_config_vs_opcoes.json','w'),indent=2)
        print('config v2 == opcoes GF1 s=0,25:',len(campos),'campos, divergentes',div)
    elif modo.startswith('fora'):
        i=int(modo[-1]); rodar(fora[(i-1)*16:i*16],modo)
    else:
        d=pd.read_csv(OUT/'bruto_nominal.csv',float_precision='round_trip'); f=pd.concat([pd.read_csv(OUT/f'bruto_fora{i}.csv',float_precision='round_trip') for i in (1,2,3)])
        f.to_csv(OUT/'bruto_fora_da_amostra.csv',index=False)
        for nome,x in [('nominal',d),('fora',f)]:
            assert x.violacoes.sum()==0; print(nome,len(x),'execucoes, concluiu',int(x.concluiu.sum()))
        rows=contraste(d,conjunto='nominal_16')+contraste(f,conjunto='fora_48')
        f=f.merge(amostra[['arquivo','NC','RF','RS']].drop_duplicates('arquivo'),on='arquivo')
        f['RS_tercil']=pd.qcut(f.RS.rank(method='first'),3,labels=['baixo','medio','alto'])
        estr=[]
        for fator in ['NC','RF','RS_tercil']:
            for nivel,g in f.groupby(fator,observed=True): estr+=contraste(g,fator=fator,nivel=str(nivel))
        r=pd.DataFrame(rows); r.to_csv(OUT/'contrastes_IC95.csv',index=False)
        e=pd.DataFrame(estr); e.to_csv(OUT/'estratos_IC95.csv',index=False)
        print(r.round(4).to_string(index=False))
        print('estratos:',len(e),'| negativos com IC<0:',int((e.ic95_sup<0).sum()),'| negativos:',int((e.media<0).sum()))
        g=pd.concat([d.assign(conj='nominal'),f.assign(conj='fora')]).groupby(['conj','cenario']).agg(confianca_final=('confianca_media_final','mean'),fuga=('fracao_fuga','mean'),N_req=('N_req','mean'))
        print(g.round(3).to_string())
        files=['config/mvp.yaml','config/parametros.yaml','src/modelo/simulador.py','src/modelo/simulador_mvp.py','research/validacao/nominal_v2.py']
        json.dump(dict(data='2026-09-21',executado_por='Claude (revisor), sem auditoria independente',N_nominal=len(d),N_fora=len(f),
            hashes={x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in files}),open(OUT/'manifesto.json','w'),indent=2)
    print(round(time.time()-t0),'s')
