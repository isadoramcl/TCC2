"""Estresse: (A1) limiares baixos onde a fuga por limiar travava; (B2) as 36 chaves incompletas."""
import sys,time
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import pandas as pd,numpy as np,yaml
ROOT=Path(__file__).resolve().parents[3]; MAIN=ROOT; sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
sys.path.insert(0,str(Path(__file__).resolve().parent)); from teste_portoes import VAR
VAR=dict(VAR,A1ref=dict(regra_fuga='dependente_estado'))
CAP=int(sys.argv[3]) if len(sys.argv)>3 else 256
def job(a):
    var,arq,seed,cen,par,canal=a
    p=S.carregar_parametros()
    for (sec,k),val in par.items(): p[sec][k]['valor']=val
    op=yaml.safe_load((ROOT/'config/mvp_v1.yaml').read_text())['opcoes']; op['instrumentar_tarefas']=False; op.update(VAR[var]); op['limite_horizonte_fator']=CAP
    if canal: op['canal_erro_direto']=canal
    g,d,c=S.carregar_instancia(arq); r=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)).executar()
    n=r.contadores['p1_fuga']+r.contadores['p1_omissao']+r.contadores['p3_analitica']
    return dict(variante=var,arquivo=arq,semente=seed,cenario=cen,canal=canal,**{f'{k}':v for (s_,k),v in par.items()},
        concluiu=r.concluiu,violacoes=len(r.violacoes),atraso=r.makespan/r.makespan_cpm,fuga=r.contadores['p1_fuga']/n if n else np.nan,
        N_req=r.contadores['N_req'],conf=r.contadores['confianca_media_final'],falha=r.taxa_falha_efetiva)
if __name__=='__main__':
    modo=sys.argv[1]; vs=sys.argv[2].split(','); parte=sys.argv[4] if len(sys.argv)>4 else None
    if modo=='A1':
        jobs=[(v,a,s,c,{('gestor','limite_aversao_perda'):lim},None) for v in vs for lim in [.1,.2,.3,.4]
              for a in ['j6010_1.sm','j6021_1.sm','j6032_1.sm','j6043_1.sm'] for s in range(4) for c in ['centralizada','adaptativa']]
    else:
        b=pd.read_csv(MAIN/'outputs/diagnosticos/lote41_B2_censura_20260918/bruto.csv'); b=b[~b.concluiu]
        jobs=[(v,r.arquivo,int(r.semente),r.cenario,{('agentes','tau_sat'):float(r.tau_sat),('agentes','s_transicao'):float(r.s_transicao)},r.canal)
              for v in vs for r in b.itertuples()]
    if parte: i,n=map(int,parte.split('/')); jobs=jobs[i::n]
    t0=time.time()
    with ProcessPoolExecutor(2) as p: d=pd.DataFrame(list(p.map(job,jobs,chunksize=4)))
    suf=('_p'+parte.replace('/','de')) if parte else ''
    d.to_csv(ROOT/('outputs/diagnosticos/20260921_portoes_suaves/estresse_%s_%s_cap%d%s.csv'%(modo,'_'.join(vs),CAP,suf)),index=False)
    keys=['variante','cenario']+(['limite_aversao_perda'] if modo=='A1' else ['s_transicao','tau_sat'])
    print(round(time.time()-t0),'s'); print(d.groupby(keys).agg(completas=('concluiu','sum'),N=('concluiu','size'),fuga=('fuga','mean'),N_req=('N_req','mean'),conf=('conf','mean'),atraso=('atraso','mean')).round(3).to_string())
