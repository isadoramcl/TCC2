"""B1/T4: portão × rede, reporte comum, diagonais verificadas bit a bit."""
import argparse
import copy
from dataclasses import asdict
import hashlib
import json
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import yaml
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
METRICAS=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
AUX=['mu_cog_medio','mu_rede_medio','duracao_efetiva_media','N_req','N_fail','N_success','N_blocked']


def bits(x):
    if isinstance(x,float):return x.hex()
    if isinstance(x,dict):return {k:bits(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [bits(v) for v in x]
    return x


def configurar(portao,rede,reporte):
    p=S.carregar_parametros();c=copy.deepcopy(p['cenarios']['centralizada'])
    for k in ['tau_inicial','tau_min']:c[k]=copy.deepcopy(p['cenarios'][portao][k])
    for k in ['p_reporte','p_deteccao']:c[k]=copy.deepcopy(p['cenarios'][reporte][k])
    p['cenarios']['teste']=c
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
    op.update(tau_portao=float(S.v(p['cenarios'][portao]['tau_inicial'])),tau_rede=float(S.v(p['cenarios'][rede]['tau_inicial'])))
    return p,op


def job(args):
    portao,rede,reporte,arquivo,seed=args
    p,op=configurar(portao,rede,reporte);g,disp,cpm=S.carregar_instancia(arquivo)
    s=SimulacaoMVP(g,disp,cpm,p,'teste',seed,opcoes=OpcoesMVP(**op));r=s.executar()
    diagonal=portao==rede
    if diagonal:
        sem={**op,'tau_portao':None,'tau_rede':None}
        controle=SimulacaoMVP(g,disp,cpm,copy.deepcopy(p),'teste',seed,opcoes=OpcoesMVP(**sem));rc=controle.executar()
        for nome,x,y in [('resultado',asdict(r),asdict(rc)),('RNG',s.rng.bit_generator.state,controle.rng.bit_generator.state),('agentes',[vars(a) for a in s.agentes],[vars(a) for a in controle.agentes]),('tarefas',{k:vars(v) for k,v in s.tarefas.items()},{k:vars(v) for k,v in controle.tarefas.items()}),('eventos',s.eventos,controle.eventos),('registros',s.registros_tarefas,controle.registros_tarefas),('divida',s.divida_pendente,controle.divida_pendente)]:
            assert bits(x)==bits(y),(portao,rede,reporte,arquivo,seed,nome)
    ts=[x for x in s.registros_tarefas if x['executada']]
    return dict(portao=portao,rede=rede,reporte=reporte,celula=portao[0].upper()+rede[0].upper(),arquivo=arquivo,semente=seed,
        atraso_relativo=r.makespan/r.makespan_cpm,taxa_omissao=r.taxa_omissao,divida_latente_sobre_plano=r.divida_latente_sobre_plano,taxa_falha_efetiva=r.taxa_falha_efetiva,
        fracao_porta1=r.contadores['p1_omissao']/len(ts),
        mu_cog_medio=float(np.mean(r.trajetorias['mu_cog'])),mu_rede_medio=float(np.mean(r.trajetorias['mu_rede'])),
        duracao_efetiva_media=float(np.mean([x['duracao_efetiva'] for x in ts])),
        **{k:r.contadores[k] for k in ['N_req','N_fail','N_success','N_blocked']},
        TW=r.TW,TL=r.TL,TU=r.TU,TR=r.TR,makespan=r.makespan,makespan_cpm=r.makespan_cpm,
        concluiu=r.concluiu,violacoes=len(r.violacoes),diagonal_bit_a_bit=diagonal)


def ic(x):
    x=np.asarray(x);m=x.mean();h=t.ppf(.975,len(x)-1)*x.std(ddof=1)/np.sqrt(len(x)) if len(x)>1 else np.nan
    return dict(media=m,ic95_inferior=m-h,ic95_superior=m+h,n_instancias=len(x))


def analisar(d,out):
    rows=[];contr=[];pares=[]
    for (rep,cel),g in d.groupby(['reporte','celula']):
        for met in METRICAS+AUX:rows.append(dict(reporte=rep,celula=cel,metrica=met,**ic(g.groupby('arquivo')[met].mean())))
    for rep,g in d.groupby('reporte'):
        for met in METRICAS+AUX:
            p=g.pivot(index=['arquivo','semente'],columns='celula',values=met)
            ds={'portao':p.AC-p.CC,'rede':p.CA-p.CC,'interacao':p.AA-p.AC-p.CA+p.CC,'total':p.AA-p.CC,'portao_rede_A':p.AA-p.CA,'rede_portao_A':p.AA-p.AC}
            np.testing.assert_allclose(ds['portao']+ds['rede']+ds['interacao'],ds['total'],atol=1e-12,rtol=0)
            for nome,delta in ds.items():
                por_inst=delta.groupby('arquivo').mean()
                contr.append(dict(reporte=rep,metrica=met,contraste=nome,**ic(por_inst)))
                for arq,val in por_inst.items():pares.append(dict(reporte=rep,metrica=met,contraste=nome,arquivo=arq,delta=val))
    pd.DataFrame(rows).to_csv(out/'celulas_IC95.csv',index=False)
    pd.DataFrame(contr).to_csv(out/'decomposicao_IC95.csv',index=False)
    pd.DataFrame(pares).to_csv(out/'contrastes_instancia.csv',index=False)
    old=pd.read_csv(ROOT/'outputs/diagnosticos/arranjo_20260917/bruto.csv');old=old[old.etapa=='T2'];checks=[]
    for (rep,cel),conf in {('centralizada','CC'):'referencia',('centralizada','AA'):'confianca',('adaptativa','CC'):'reporte',('adaptativa','AA'):'ambos'}.items():
        novo=d[(d.reporte==rep)&(d.celula==cel)].set_index(['arquivo','semente'])
        ref=old[old.configuracao==conf].set_index(['arquivo','semente']).loc[novo.index]
        for met in METRICAS+['TW','TL','TU','TR','makespan','makespan_cpm']:
            diff=float((novo[met]-ref[met]).abs().max())
            checks.append(dict(reporte=rep,celula=cel,referencia_T2=conf,metrica=met,diferenca_maxima=diff))
    pd.DataFrame(checks).to_csv(out/'controle_diagonais_T2.csv',index=False)
    assert all(c['diferenca_maxima']<1e-12 for c in checks),checks


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--piloto',action='store_true');ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    args.saida.mkdir(parents=True,exist_ok=False)
    m=json.loads((ROOT/'outputs/diagnosticos/arranjo_20260917/manifesto.json').read_text());inst=m['T2_instancias'];seeds=m['T2_sementes']
    if args.piloto:inst=inst[:1];seeds=seeds[:1]
    jobs=[(a,b,c,i,s) for a in ['centralizada','adaptativa'] for b in ['centralizada','adaptativa'] for c in ['centralizada','adaptativa'] for i in inst for s in seeds]
    files=[Path(__file__),ROOT/'research/lote41/PROTOCOLO.md',ROOT/'src/modelo/simulador.py',ROOT/'src/modelo/simulador_mvp.py',ROOT/'src/modelo/fuzzy.py']+list((ROOT/'config').glob('*.yaml'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (args.saida/'manifesto.json').write_text(json.dumps(dict(instancias=inst,sementes=seeds,execucoes=len(jobs),hashes=hashes,IC='t sobre médias por instância; pontuais; sementes pareadas',RNG='mesma sequência inicial, eventos podem desalinharem-se',piloto=args.piloto),indent=2)+'\n')
    rows=[]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for i,r in enumerate(pool.map(job,jobs,chunksize=4)):
            rows.append(r)
            if (i+1)%128==0:print(f'{i+1}/{len(jobs)}',flush=True)
    d=pd.DataFrame(rows);d.to_csv(args.saida/'bruto.csv',index=False)
    assert d.concluiu.all() and not d.violacoes.any()
    analisar(d,args.saida)
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (args.saida/'verificacoes.json').write_text(json.dumps(dict(exec=len(d),diagonais_bit_a_bit=int(d.diagonal_bit_a_bit.sum()),controle_T2='passou',incompletas=0,violacoes=0),indent=2)+'\n')
    print('T4 concluído',len(d),flush=True)
if __name__=='__main__':main()
