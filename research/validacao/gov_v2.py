"""Robustez de governança (81 perfis, mesmo desenho do SAT_GOV_20260919) sob o nominal v2.
Uso: python gov_v2.py PARTE/N | analise"""
import sys,itertools,time,json
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np,pandas as pd,yaml
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260921_nominal_v2/governanca'; OUT.mkdir(parents=True,exist_ok=True)
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
FACT=['tau_inicial','tau_min','p_reporte','p_deteccao']
cfg=yaml.safe_load((ROOT/'config/robustez_sat_gov.yaml').read_text())
names=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::120]
profiles=list(itertools.product(*[cfg['gov'][k] for k in FACT]))
def job(arg):
    cell,vals,a,seed,cen=arg; p=S.carregar_parametros(); op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']; op['instrumentar_tarefas']=False
    for k,v in zip(FACT,vals): p['cenarios'][cen][k]['valor']=v
    g,d,c=S.carregar_instancia(a); r=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)).executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))}; row.update(r.contadores)
    den=row['p1_omissao']+row['p3_analitica']
    row.update(celula=cell,arquivo=a,semente=seed,cenario=cen,violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=row['p1_omissao']/den if den else np.nan)
    return row
def ic(x):
    x=x.dropna();n=len(x);m=x.mean();h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n);return m,m-h,m+h
if __name__=='__main__':
    if sys.argv[1]!='analise':
        i,n=map(int,sys.argv[1].split('/')); t0=time.time()
        jobs=[(c,v,a,s,cen) for c,v in enumerate(profiles) for a in names for s in cfg['sementes'] for cen in ['centralizada','adaptativa']][i::n]
        with ProcessPoolExecutor(2) as p: d=pd.DataFrame(list(p.map(job,jobs,chunksize=16)))
        d.to_csv(OUT/f'bruto_p{i}de{n}.csv',index=False); print(len(d),'exec',round(time.time()-t0),'s, concluiu',int(d.concluiu.sum()),'violacoes',int(d.violacoes.sum()))
    else:
        d=pd.concat([pd.read_csv(f,float_precision='round_trip') for f in sorted(OUT.glob('bruto_p*.csv'))]); d.to_csv(OUT/'bruto.csv',index=False)
        print(len(d),'execucoes; concluiu',int(d.concluiu.sum()),'; violacoes',int(d.violacoes.sum()))
        G={(c,cen):g.set_index(['arquivo','semente']).sort_index() for (c,cen),g in d.groupby(['celula','cenario'])}
        rows=[]
        for a in range(len(profiles)):
            for c in range(len(profiles)):
                ga,gc=G[(a,'adaptativa')],G[(c,'centralizada')]
                for m in MET:
                    mm,lo,hi=ic((ga[m]-gc[m]).groupby('arquivo').mean())
                    rows.append(dict(perfil_adaptativa=a,perfil_centralizada=c,metrica=m,media=mm,ic95_inf=lo,ic95_sup=hi))
        r=pd.DataFrame(rows); r.to_csv(OUT/'contrastes_IC95.csv',index=False)
        v1=pd.read_csv(ROOT/'outputs/diagnosticos/SAT_GOV_20260919/GOV_contrastes_IC95.csv'); v1=v1[v1.estimando=='observado']
        def resumo(x,nome):
            return pd.DataFrame(dict(versao=nome,pares=x.groupby('metrica').size(),sinal_negativo=x.groupby('metrica').media.apply(lambda s:(s<0).sum()),
                inversoes_positivo_com_IC=x.groupby('metrica').ic95_inf.apply(lambda s:(s>0).sum())))
        out=pd.concat([resumo(v1,'v1'),resumo(r,'v2')]).reset_index(); out.to_csv(OUT/'resumo_v1_v2.csv',index=False)
        print(out.to_string(index=False))
        nom=r[(r.perfil_adaptativa==[i for i,p in enumerate(profiles) if np.allclose(p,[.8,.25,.75,.12])][0])&(r.perfil_centralizada==[i for i,p in enumerate(profiles) if np.allclose(p,[.25,.6,.15,.03])][0])]
        print('perfil nominal nesta grade (4 instancias x 4 sementes):'); print(nom[['metrica','media','ic95_inf','ic95_sup']].round(4).to_string(index=False))
