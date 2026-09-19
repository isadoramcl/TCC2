"""B2: família declarada de canal direto × tau_sat × s_transicao."""
import argparse
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
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from t4 import ic,METRICAS


def fracao_p1(p1,p3):
    return p1/(p1+p3) if p1+p3 else float("nan")


def job(args):
    etapa,canal,tau,escala,cen,arquivo,seed=args
    p=S.carregar_parametros();p['agentes']['tau_sat']['valor']=tau;p['agentes']['s_transicao']['valor']=escala
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];op['canal_erro_direto']=canal;op['instrumentar_tarefas']=False
    g,disp,cpm=S.carregar_instancia(arquivo);s=SimulacaoMVP(g,disp,cpm,p,cen,seed,opcoes=OpcoesMVP(**op));r=s.executar()
    n=r.contadores['p1_omissao']+r.contadores['p3_analitica']
    return dict(etapa=etapa,canal=canal,tau_sat=tau,s_transicao=escala,cenario=cen,arquivo=arquivo,semente=seed,
        atraso_relativo=r.makespan/r.makespan_cpm,taxa_omissao=r.taxa_omissao,divida_latente_sobre_plano=r.divida_latente_sobre_plano,taxa_falha_efetiva=r.taxa_falha_efetiva,
        fracao_porta1=fracao_p1(r.contadores['p1_omissao'],r.contadores['p3_analitica']),n_executadas=n,N_req=r.contadores['N_req'],N_blocked=r.contadores['N_blocked'],motivo_termino=r.contadores['motivo_termino'],TW=r.TW,TL=r.TL,TU=r.TU,TR=r.TR,
        concluiu=r.concluiu,violacoes=len(r.violacoes))


def analisar(d,out):
    cs=[];ds=[]
    ch=['etapa','canal','tau_sat','s_transicao']
    d.groupby(ch+['cenario']).agg(exec=('concluiu','size'),completas=('concluiu','sum'),sem_tarefas=('n_executadas',lambda x:int((x==0).sum()))).to_csv(out/'completude.csv')
    for chave,g in d.groupby(ch):
        for met in METRICAS:
            for cen,x in g.groupby('cenario'):
                cs.append(dict(zip(ch,chave),cenario=cen,metrica=met,censuradas=int((~x.concluiu).sum()),fracao_indefinida=int(x[met].isna().sum()),**ic(x.groupby('arquivo')[met].mean())))
            p=g.pivot(index=['arquivo','semente'],columns='cenario',values=met)
            ds.append(dict(zip(ch,chave),metrica=met,censuradas=int((~g.concluiu).sum()),pares_indefinidos=int((p.adaptativa-p.centralizada).isna().sum()),**ic((p.adaptativa-p.centralizada).groupby('arquivo').mean())))
    pd.DataFrame(cs).to_csv(out/'celulas_IC95.csv',index=False);pd.DataFrame(ds).to_csv(out/'contraste_A_menos_C_IC95.csv',index=False)
    old=pd.read_csv(ROOT/'outputs/diagnosticos/arranjo_20260917/bruto.csv');old=old[old.etapa=='T2'];checks=[]
    for cen,conf in [('centralizada','referencia'),('adaptativa','ambos')]:
        n=d[(d.etapa=='nominal')&(d.canal=='ativo')&(d.cenario==cen)].set_index(['arquivo','semente'])
        ref=old[old.configuracao==conf].set_index(['arquivo','semente']).loc[n.index]
        for met in METRICAS+['TW','TL','TU','TR']:
            diff=float((n[met]-ref[met]).abs().max());checks.append(dict(cenario=cen,metrica=met,diferenca_maxima=diff))
    pd.DataFrame(checks).to_csv(out/'controle_nominal_ativo.csv',index=False)
    assert all(x['diferenca_maxima']<1e-12 for x in checks)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);args=ap.parse_args();args.saida.mkdir(parents=True,exist_ok=False)
    m=json.loads((ROOT/'outputs/diagnosticos/arranjo_20260917/manifesto.json').read_text());ins=m['T2_instancias'];seeds=m['T2_sementes'];p=S.carregar_parametros()
    taus=p['agentes']['tau_sat']['varredura'];ss=p['agentes']['s_transicao']['varredura'];jobs=[]
    for etapa,inst,sems,ts,es in [('nominal',ins,seeds,[S.v(p['agentes']['tau_sat'])],[S.v(p['agentes']['s_transicao'])]),('grade',ins[::4],seeds[:4],taus,ss)]:
        jobs.extend((etapa,c,t,s,cen,a,k) for c in ['ativo','desligado'] for t in ts for s in es for cen in ['centralizada','adaptativa'] for a in inst for k in sems)
    files=[Path(__file__),ROOT/'research/lote41/PROTOCOLO_B2.md',ROOT/'research/lote41/t4.py',ROOT/'src/modelo/simulador_mvp.py',ROOT/'src/modelo/simulador.py',ROOT/'src/modelo/fuzzy.py']+list((ROOT/'config').glob('*.yaml'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (args.saida/'manifesto.json').write_text(json.dumps(dict(exec=len(jobs),nominal_instancias=ins,seeds=seeds,grade_instancias=ins[::4],grade_seeds=seeds[:4],tau_sat=taus,s_transicao=ss,hashes=hashes),indent=2)+'\n')
    rows=[]
    import csv
    checkpoint=(args.saida/'bruto.csv').open('w')
    writer=None
    with ProcessPoolExecutor(max_workers=4) as pool:
        for i,row in enumerate(pool.map(job,jobs,chunksize=4)):
            rows.append(row)
            if writer is None:
                writer=csv.DictWriter(checkpoint,fieldnames=list(row));writer.writeheader()
            writer.writerow(row);checkpoint.flush()
            if (i+1)%128==0:print(f'{i+1}/{len(jobs)}',flush=True)
    checkpoint.close()
    d=pd.DataFrame(rows)
    assert not d.violacoes.any()
    analisar(d,args.saida)
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (args.saida/'verificacoes.json').write_text(json.dumps(dict(exec=len(d),incompletas=int((~d.concluiu).sum()),sem_tarefas=int((d.n_executadas==0).sum()),violacoes=0,controle_ativo='passou'),indent=2)+'\n')
    print('B2 concluído',len(d),flush=True)
if __name__=='__main__':main()
