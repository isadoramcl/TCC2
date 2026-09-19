"""T-B2.3: família declarada, sem ajuste de valores ou política do modelo."""
import argparse
import csv
from dataclasses import asdict
import hashlib
import json
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import yaml
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/modelo'))
sys.path.insert(0,str(ROOT/'research/lote41'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from t4 import bits
FONTE=ROOT/'outputs/diagnosticos/lote41_B2_censura_20260918/bruto.csv'
MALHA=[.25,.59,.60,.600001,.61,.65,.80,1.]


def configurar(row,tau,modo):
    p=S.carregar_parametros();p['agentes']['tau_sat']['valor']=row['tau_sat'];p['agentes']['s_transicao']['valor']=row['s_transicao']
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];assert op['limite_horizonte_fator']==256
    op.update(canal_erro_direto=row['canal'],instrumentar_tarefas=False)
    assert S.v(p['cenarios']['centralizada']['tau_inicial'])==.25
    assert S.v(p['cenarios']['centralizada']['tau_min'])==.6
    if modo=='principal':p['cenarios']['centralizada']['tau_inicial']['valor']=tau
    elif modo=='portao':op.update(tau_portao=tau,tau_rede=.25)
    elif modo=='rede':op.update(tau_portao=.25,tau_rede=tau)
    else:raise ValueError(modo)
    return p,op


def simular(row,tau,modo):
    p,op=configurar(row,tau,modo);g,disp,cpm=S.carregar_instancia(row['arquivo'])
    s=SimulacaoMVP(g,disp,cpm,p,'centralizada',int(row['semente']),opcoes=OpcoesMVP(**op));r=s.executar()
    return s,r


def job(args):
    row,tau,modo=args;s,r=simular(row,tau,modo)
    n=r.contadores['p1_omissao']+r.contadores['p3_analitica'];h=r.contadores['hiato_encontrado'];bloq=r.contadores['hiato_colega_capaz_sem_confianca']
    return dict(modo=modo,tau_varrida=tau,cenario='centralizada',canal=row['canal'],tau_sat=row['tau_sat'],s_transicao=row['s_transicao'],arquivo=row['arquivo'],semente=row['semente'],
        concluiu=r.concluiu,violacoes=len(r.violacoes),n_executadas=n,makespan=r.makespan,makespan_cpm=r.makespan_cpm,
        atraso_relativo=r.makespan/r.makespan_cpm,TW=r.TW,TL=r.TL,TU=r.TU,TR=r.TR,taxa_omissao=r.taxa_omissao,taxa_falha_efetiva=r.taxa_falha_efetiva,divida_latente_sobre_plano=r.divida_latente_sobre_plano,
        N_req=r.contadores['N_req'],N_fail=r.contadores['N_fail'],N_success=r.contadores['N_success'],N_blocked=r.contadores['N_blocked'],hiato_encontrado=h,hiato_colega_capaz_sem_confianca=bloq,
        fracao_hiato_sem_confianca=bloq/h if h else float('nan'),confianca_media_final=r.contadores['confianca_media_final'],motivo_termino=r.contadores['motivo_termino'])


def analisar(d,out,base):
    rows=[]
    for (modo,tau),g in d.groupby(['modo','tau_varrida']):
        rows.append(dict(modo=modo,tau_varrida=tau,N=len(g),completas=int(g.concluiu.sum()),incompletas=int((~g.concluiu).sum()),sem_tarefas=int((g.n_executadas==0).sum()),
            hiato_sem_confianca_media=g.hiato_colega_capaz_sem_confianca.mean(),hiato_encontrado_media=g.hiato_encontrado.mean(),fracao_hiato_sem_confianca=g.hiato_colega_capaz_sem_confianca.sum()/g.hiato_encontrado.sum(),
            N_req_medio=g.N_req.mean(),N_fail_medio=g.N_fail.mean(),N_success_medio=g.N_success.mean(),TL_medio=g.TL.mean(),confianca_final_media=g.confianca_media_final.mean()))
    resumo=pd.DataFrame(rows);resumo.to_csv(out/'resumo.csv',index=False)
    d.groupby(['modo','tau_varrida','canal','tau_sat','s_transicao']).agg(N=('concluiu','size'),completas=('concluiu','sum'),hiato_sem_confianca_medio=('hiato_colega_capaz_sem_confianca','mean'),N_req_medio=('N_req','mean')).to_csv(out/'estratos.csv')
    keys=['canal','tau_sat','s_transicao','arquivo','semente'];novo=d[(d.modo=='principal')&(d.tau_varrida==.25)].set_index(keys);old=base.set_index(keys).loc[novo.index];checks=[]
    for met in ['n_executadas','N_req','N_blocked','TW','TL','TU','TR','atraso_relativo','taxa_omissao','taxa_falha_efetiva','divida_latente_sobre_plano']:
        delta=float((novo[met]-old[met]).abs().max());checks.append(dict(metrica=met,diferenca_maxima=delta));assert delta<1e-12,(met,delta)
    pd.DataFrame(checks).to_csv(out/'controle_baseline.csv',index=False)
    principais=resumo[resumo.modo=='principal'].sort_values('tau_varrida')
    zeros=principais[principais.incompletas==0]
    primeiro=None if zeros.empty else float(zeros.tau_varrida.min())
    todos_superiores=False if primeiro is None else bool(principais[principais.tau_varrida>=primeiro].incompletas.eq(0).all())
    return dict(exec=len(d),violacoes=int(d.violacoes.sum()),primeiro_tau_testado_sem_incompletas=primeiro,sem_incompletas_em_todos_superiores_testados=todos_superiores,controle_baseline='passou')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);args=ap.parse_args();out=args.saida;out.mkdir(parents=True,exist_ok=False)
    b=pd.read_csv(FONTE);base=b[~b.concluiu];assert len(base)==36 and base.cenario.eq('centralizada').all()
    base.to_csv(out/'selecionadas_36.csv',index=False)
    configs=[('principal',t) for t in MALHA]+[('portao',t) for t in [.600001,.8,1.]]+[('rede',t) for t in [.8,1.]]
    files=[Path(__file__),Path(__file__).with_name('PROTOCOLO_TB23.md'),FONTE,ROOT/'src/modelo/simulador.py',ROOT/'src/modelo/simulador_mvp.py',ROOT/'src/modelo/fuzzy.py']+list((ROOT/'config').glob('*.yaml'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (out/'manifesto.json').write_text(json.dumps(dict(N_casos=36,N_exec=468,configuracoes=configs,limite_horizonte_fator=256,hashes=hashes),indent=2)+'\n')
    rows=[];jobs=[(r,t,m) for m,t in configs for r in base.to_dict('records')]
    with (out/'bruto.csv').open('w') as f,ProcessPoolExecutor(max_workers=4) as pool:
        writer=None
        for i,row in enumerate(pool.map(job,jobs,chunksize=1)):
            if writer is None:writer=csv.DictWriter(f,fieldnames=list(row),lineterminator='\n');writer.writeheader()
            writer.writerow(row);f.flush();rows.append(row)
            if (i+1)%12==0:print(f'{i+1}/468 {row["modo"]} tau={row["tau_varrida"]}',flush=True)
    d=pd.DataFrame(rows);assert not d.violacoes.any()
    ver=analisar(d,out,base)
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (out/'verificacoes.json').write_text(json.dumps(ver,indent=2)+'\n');print(json.dumps(ver),flush=True)
if __name__=='__main__':main()
