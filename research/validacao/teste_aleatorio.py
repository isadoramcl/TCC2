"""Teste aleatório do nominal v2 (critério em outputs/diagnosticos/20260922_teste_aleatorio/CRITERIO.md).
Uso: python teste_aleatorio.py sortear | rodar PARTE/N | analise"""
import sys,json,time
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np,pandas as pd,yaml
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260922_teste_aleatorio'
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
SEM=list(range(100,112))
def job(a):
    arq,seed,cen=a; p=S.carregar_parametros(); op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']; op['instrumentar_tarefas']=False
    g,d,c=S.carregar_instancia(arq); r=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)).executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))}; row.update(r.contadores)
    den=row['p1_omissao']+row['p3_analitica']
    row.update(arquivo=arq,semente=seed,cenario=cen,violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=row['p1_omissao']/den if den else np.nan)
    return row
if __name__=='__main__':
    m=sys.argv[1]
    if m=='sortear':
        semente=int(time.time_ns()%2**31)
        todas=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())
        usadas=set(pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv').arquivo)|set(pd.read_csv(ROOT/'outputs/diagnosticos/20260920_fora_da_amostra/amostra_estratificada.csv').arquivo)
        livres=[a for a in todas if a not in usadas]
        sel=sorted(np.random.default_rng(semente).choice(livres,24,replace=False).tolist())
        json.dump(dict(semente_sorteio=semente,N_livres=len(livres),instancias=sel,sementes_simulacao=SEM),open(OUT/'amostra.json','w'),indent=2)
        print('semente',semente,'| livres',len(livres),'|',sel)
    elif m=='rodar':
        i,n=map(int,sys.argv[2].split('/')); inst=json.load(open(OUT/'amostra.json'))['instancias']
        jobs=[(a,s,c) for a in inst for s in SEM for c in ['centralizada','adaptativa']][i::n]
        with ProcessPoolExecutor(2) as p: d=pd.DataFrame(list(p.map(job,jobs,chunksize=8)))
        d.to_csv(OUT/f'bruto_p{i}de{n}.csv',index=False); print(len(d),'exec, concluiu',int(d.concluiu.sum()),'violacoes',int(d.violacoes.sum()))
    else:
        d=pd.concat([pd.read_csv(f,float_precision='round_trip') for f in sorted(OUT.glob('bruto_p*.csv'))]); d.to_csv(OUT/'bruto.csv',index=False)
        rows=[]
        for mt in MET:
            q=d.pivot(index=['arquivo','semente'],columns='cenario',values=mt); x=(q.adaptativa-q.centralizada).groupby('arquivo').mean()
            n=len(x); mm=x.mean(); h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n); rows.append(dict(metrica=mt,media=mm,ic95_inf=mm-h,ic95_sup=mm+h,N=n))
        r=pd.DataFrame(rows); r.to_csv(OUT/'contrastes_IC95.csv',index=False)
        c1=bool(d.concluiu.all() and d.violacoes.sum()==0); c2=bool((r.media<0).all()); c3=bool((r.set_index('metrica').loc[MET[:3],'ic95_sup']<0).all())
        res=dict(N=len(d),concluiu=int(d.concluiu.sum()),violacoes=int(d.violacoes.sum()),criterio1=c1,criterio2=c2,criterio3=c3,passou=c1 and c2 and c3)
        json.dump(res,open(OUT/'resultado.json','w'),indent=2); print(r.round(4).to_string(index=False)); print(res)
