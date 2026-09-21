"""Varredura de s_portoes (critério em projeto/75). Uso: python varredura_s.py S [nominal|b2]"""
import sys,time
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import pandas as pd,numpy as np,yaml
ROOT=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260921_portoes_suaves/varredura_s'; OUT.mkdir(parents=True,exist_ok=True)
GF1=dict(portao_assistencia='logistico',regra_fuga='logistica',efeito_fuga='drena')
def job(a):
    arq,seed,cen,sp,par,canal,cap=a
    p=S.carregar_parametros()
    for (sec,k),v in par.items(): p[sec][k]['valor']=v
    op=yaml.safe_load((ROOT/'config/mvp_v1.yaml').read_text())['opcoes']; op.update(GF1,instrumentar_tarefas=False,s_portoes=sp,limite_horizonte_fator=cap)
    if canal: op['canal_erro_direto']=canal
    g,d,c=S.carregar_instancia(arq); r=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)).executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))}; row.update(r.contadores)
    den=row['p1_omissao']+row['p3_analitica']; dec=den+row['p1_fuga']
    row.update(arquivo=arq,semente=seed,cenario=cen,s_portoes=sp,violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,
               fracao_porta1=row['p1_omissao']/den if den else np.nan,fracao_fuga=row['p1_fuga']/dec if dec else np.nan)
    return row
if __name__=='__main__':
    sp=float(sys.argv[1]); modo=sys.argv[2]
    if modo=='nominal':
        inst=sorted(pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv').arquivo.unique())
        jobs=[(a,s,c,sp,{},None,256) for a in inst for s in range(12) for c in ['centralizada','adaptativa']]
    else:
        b=pd.read_csv(ROOT/'outputs/diagnosticos/lote41_B2_censura_20260918/bruto.csv'); b=b[~b.concluiu]
        jobs=[(r.arquivo,int(r.semente),r.cenario,sp,{('agentes','tau_sat'):float(r.tau_sat),('agentes','s_transicao'):float(r.s_transicao)},r.canal,16) for r in b.itertuples()]
    t0=time.time()
    with ProcessPoolExecutor(2) as p: d=pd.DataFrame(list(p.map(job,jobs,chunksize=8)))
    d.to_csv(OUT/f'{modo}_s{sp}.csv',index=False)
    print(modo,sp,len(d),'exec',round(time.time()-t0),'s | concluiu',int(d.concluiu.sum()),'| violacoes',int(d.violacoes.sum()))
