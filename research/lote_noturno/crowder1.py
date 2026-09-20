"""Grade predeclarada dos escalares Crowder; nominal e censura preservados."""
import csv,json,hashlib,sys
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
from scipy.stats import t
import yaml
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/GOV2_CROWDER1_20260919'
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
def job(args):
 base,factor,arq,seed,cen=args;p=S.carregar_parametros()
 p['aprendizado']['incremento_base']['valor']=base;p['aprendizado']['fator_transferencia']['valor']=factor
 op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];op['instrumentar_tarefas']=False
 g,d,c=S.carregar_instancia(arq);s=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op));r=s.executar()
 row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))};row.update(r.contadores)
 dc=[e['dC'] for e in s.eventos if e['tipo']=='comunicacao' and e['sucesso']]
 den=r.contadores['p1_omissao']+r.contadores['p3_analitica']
 row.update(incremento_base=base,fator_transferencia=factor,arquivo=arq,semente=seed,cenario=cen,violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=r.contadores['p1_omissao']/den if den else np.nan,dC_soma=sum(dc),dC_N=len(dc),dC_teto_N=sum(x==.3 for x in dc))
 return row

def ci(x):
 x=x.dropna();n=len(x);m=x.mean();h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n) if n>1 else np.nan
 return dict(media=m,ic95_inf=m-h,ic95_sup=m+h,N_instancias=n)
def analyze(d):
 rows=[];absolute=[];changes=[];activity=[]
 keys=['arquivo','semente'];nom=d[(d.incremento_base==15)&(d.fator_transferencia==3)]
 for (b,f),g in d.groupby(['incremento_base','fator_transferencia']):
  ok=g.pivot(index=keys,columns='cenario',values='concluiu').all(axis=1)
  for m in MET:
   p=g.pivot(index=keys,columns='cenario',values=m);diff=p.adaptativa-p.centralizada
   for est,delta in [('observado',diff),('pares_completos',diff[ok])]:
    rows.append(dict(incremento_base=b,fator_transferencia=f,metrica=m,estimando=est,pares_previstos=len(diff),pares_retidos=len(delta),pares_indefinidos=int(delta.isna().sum()),estatuto='COMPLETO' if ok.all() else 'CENSURADO' if est=='observado' else 'CONDICIONAL_A_CONCLUSAO',**ci(delta.groupby('arquivo').mean())))
  for cen,h in g.groupby('cenario'):
   a=nom[nom.cenario==cen].set_index(keys);z=h.set_index(keys);paired=z.concluiu&a.concluiu
   for m in MET:
    absolute.append(dict(incremento_base=b,fator_transferencia=f,cenario=cen,metrica=m,estatuto='COMPLETO' if h.concluiu.all() else 'CENSURADO',incompletas=int((~h.concluiu).sum()),**ci(h.groupby('arquivo')[m].mean())))
    for est,delta in [('observado',z[m]-a[m]),('pares_completos',(z[m]-a[m])[paired])]:
     changes.append(dict(incremento_base=b,fator_transferencia=f,cenario=cen,metrica=m,estimando=est,antes=a[m].mean(),depois=z[m].mean(),estatuto='COMPLETO' if paired.all() else 'CENSURADO' if est=='observado' else 'CONDICIONAL_A_CONCLUSAO',**ci(delta.groupby('arquivo').mean())))
   activity.append(dict(incremento_base=b,fator_transferencia=f,cenario=cen,N=len(h),completas=int(h.concluiu.sum()),N_req_medio=h.N_req.mean(),N_success_medio=h.N_success.mean(),TL_medio=h.TL.mean(),dC_por_sucesso=h.dC_soma.sum()/h.dC_N.sum() if h.dC_N.sum() else np.nan,fracao_sucessos_teto=h.dC_teto_N.sum()/h.dC_N.sum() if h.dC_N.sum() else np.nan))
 for name,r in [('CROWDER1_cinco_IC95.csv',rows),('CROWDER1_por_braco_IC95.csv',absolute),('CROWDER1_antes_depois.csv',changes),('CROWDER1_atividade.csv',activity)]:pd.DataFrame(r).to_csv(OUT/name,index=False)
 old=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv',float_precision='round_trip').set_index(keys+['cenario']);new=nom.set_index(keys+['cenario']);checks=[]
 fields=[m for m in old.columns if m in new and pd.api.types.is_numeric_dtype(old[m])]
 for m in fields:
  a=new[m].sort_index();b=old.loc[new.index,m].sort_index()
  assert [float(v).hex() for v in a]==[float(v).hex() for v in b],m
  checks.append(dict(campo=m,residuo=0.))
 pd.DataFrame(checks).to_csv(OUT/'CROWDER1_identidade_384.csv',index=False)
 central=d[d.cenario=='centralizada'];assert central.N_req.eq(0).all() and central.TL.eq(0).all()
 for (b,f),g in central.groupby(['incremento_base','fator_transferencia']):
  for m in fields:
   a=g.set_index(keys)[m].sort_index();ref=nom[nom.cenario=='centralizada'].set_index(keys)[m].sort_index()
   assert [float(v).hex() for v in a]==[float(v).hex() for v in ref],(b,f,m)
 assert d.violacoes.sum()==0
 (OUT/'CROWDER1_verificacoes.json').write_text(json.dumps(dict(N=len(d),completas=int(d.concluiu.sum()),violacoes=int(d.violacoes.sum()),nominal_384_bits=True,campos_nominais=len(fields),centralizada_inerte_todas_combinacoes=True),indent=2)+'\n')
def run():
 cfg=yaml.safe_load((ROOT/'config/robustez_crowder.yaml').read_text());names=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::30][:16]
 jobs=[(b,f,a,s,c) for b in cfg['incremento_base'] for f in cfg['fator_transferencia'] for a in names for s in cfg['sementes'] for c in ['centralizada','adaptativa']]
 files=[Path(__file__),ROOT/'research/lote_noturno/PROTOCOLO_CROWDER1.md',*list((ROOT/'src/modelo').glob('*.py')),ROOT/'config/parametros.yaml',ROOT/'config/mvp.yaml',ROOT/'config/robustez_crowder.yaml']
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 (OUT/'CROWDER1_manifesto.json').write_text(json.dumps(dict(N=len(jobs),config=cfg,instancias=names,hashes=hashes),indent=2)+'\n')
 rows=[]
 with (OUT/'CROWDER1_bruto.csv').open('x') as file,ProcessPoolExecutor(max_workers=4) as pool:
  w=None
  for i,row in enumerate(pool.map(job,jobs,chunksize=1)):
   if w is None:w=csv.DictWriter(file,fieldnames=list(row));w.writeheader()
   w.writerow(row);file.flush();rows.append(row)
   if (i+1)%192==0:print(i+1,len(jobs),flush=True)
 assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 analyze(pd.DataFrame(rows))
if __name__=='__main__':run()
