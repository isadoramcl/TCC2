"""Teste isolado dos portões suaves. Uso: python teste_portoes.py VARIANTE [instancias]
Variantes: controle | G | F1 | F2 | GF. Não toca o repositório principal."""
import sys,json,time
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np,pandas as pd,yaml
ROOT=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260921_portoes_suaves'; OUT.mkdir(exist_ok=True)
VAR={'controle':{},
     'G':dict(portao_assistencia='logistico'),
     'F1':dict(regra_fuga='logistica',efeito_fuga='drena'),
     'F2':dict(regra_fuga='logistica',efeito_fuga='alivio'),
     'GF':dict(portao_assistencia='logistico',regra_fuga='logistica',efeito_fuga='alivio'),
     'GF1':dict(portao_assistencia='logistico',regra_fuga='logistica',efeito_fuga='drena')}
SEM=list(range(12)); ARMS=['centralizada','adaptativa']

def job(arg):
    a,seed,cen,var,par_extra=arg
    p=S.carregar_parametros()
    for (sec,k),val in par_extra.items(): p[sec][k]={'valor':val}
    op=yaml.safe_load((ROOT/'config/mvp_v1.yaml').read_text())['opcoes']; op['instrumentar_tarefas']=False
    op.update(VAR[var])
    g,d,c=S.carregar_instancia(a); r=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)).executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))}; row.update(r.contadores)
    den=row['p1_omissao']+row['p3_analitica']
    dec=row['p1_omissao']+row['p3_analitica']+row.get('p1_fuga',0)
    row.update(arquivo=a,semente=seed,cenario=cen,variante=var,violacoes=len(r.violacoes),
               atraso_relativo=r.makespan/r.makespan_cpm,
               fracao_porta1=row['p1_omissao']/den if den else np.nan,
               fracao_fuga=row.get('p1_fuga',0)/dec if dec else np.nan)
    return row

def rodar(var,inst,par_extra={},tag=None):
    jobs=[(a,s,c,var,par_extra) for a in inst for s in SEM for c in ARMS]
    with ProcessPoolExecutor(max_workers=2) as pool: rows=list(pool.map(job,jobs,chunksize=8))
    d=pd.DataFrame(rows); d.to_csv(OUT/f'bruto_{tag or var}.csv',index=False); return d

if __name__=='__main__':
    var=sys.argv[1]; grupo=sys.argv[2] if len(sys.argv)>2 else 'nominal'
    arq=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv',float_precision='round_trip')
    inst=sorted(arq.arquivo.unique())
    if grupo.startswith('fora'):
        todas=sorted(pd.read_csv(ROOT/'outputs/diagnosticos/20260920_fora_da_amostra/amostra_estratificada.csv').arquivo.unique())
        i=int(grupo[-1]); inst=todas[(i-1)*16:i*16]
    t0=time.time(); d=rodar(var,inst,tag=f'{var}_{grupo}')
    print(var,len(d),'execucoes',round(time.time()-t0),'s | violacoes',int(d.violacoes.sum()),
          '| concluiu',int(d.concluiu.sum()),'/',len(d))
    if var=='controle':
        k=['arquivo','semente','cenario']; a=arq.set_index(k).sort_index(); b=d.set_index(k).sort_index()
        campos=[c for c in a.columns if c in b.columns and pd.api.types.is_numeric_dtype(a[c])]
        falhas=[c for c in campos if [float(x).hex() for x in b[c]]!=[float(x).hex() for x in a.loc[b.index,c]]]
        json.dump(dict(campos=len(campos),divergentes=falhas),open(OUT/'identidade_controle.json','w'),indent=2)
        print('IDENTIDADE', len(campos),'campos | divergentes:',falhas)
