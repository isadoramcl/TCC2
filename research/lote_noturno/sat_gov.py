"""Diagnóstico SAT e robustez GOV: nenhuma alteração da dinâmica."""
import sys,json,hashlib,itertools,csv
from pathlib import Path
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
from scipy.stats import t
import yaml
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/SAT_GOV_20260919'
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
FACT=['tau_inicial','tau_min','p_reporte','p_deteccao']
def sat1():
 d=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv');r=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/tarefas.csv')
 assert len(d)==384 and d.concluiu.all()
 assert len(r[['arquivo','semente','cenario']].drop_duplicates())==384
 rows=[];hist=[]
 for pop,g in [('todas_decisoes',r),('selecionou_p1',r[r.selecionou_p1])]:
  for cen,h in [('ambos',g),*list(g.groupby('cenario'))]:
   x=h.p_heu;rows.append(dict(populacao=pop,cenario=cen,N=len(h),menor_001=(x<.01).mean(),maior_099=(x>.99).mean(),meio_01_09=x.between(.1,.9).mean()))
   counts,bins=np.histogram(x,bins=np.linspace(0,1,101))
   hist.extend(dict(populacao=pop,cenario=cen,inferior=bins[i],superior=bins[i+1],N=int(n),fracao=n/len(x)) for i,n in enumerate(counts))
 pd.DataFrame(rows).to_csv(OUT/'SAT1_resumo.csv',index=False);pd.DataFrame(hist).to_csv(OUT/'SAT1_histograma.csv',index=False)
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(2,2,figsize=(10,6),sharex=True)
 for i,(pop,g) in enumerate([('Todas as decisões',r),('Seleções P1',r[r.selecionou_p1])]):
  for j,(cen,h) in enumerate(g.groupby('cenario')):
   axes[i,j].hist(h.p_heu,bins=np.linspace(0,1,51),weights=np.ones(len(h))/len(h));axes[i,j].set_title(pop+' — '+cen);axes[i,j].set_ylabel('Fração');axes[i,j].set_xlabel('p_heu')
 fig.tight_layout();fig.savefig(OUT/'SAT1_histograma.png',dpi=150);plt.close(fig)
 qrows=[]
 for pop,g in [('todas_decisoes',r),('selecionou_p1',r[r.selecionou_p1])]:
  for cen,h in [('ambos',g),*list(g.groupby('cenario'))]:
   q=h.q;qrows.append(dict(populacao=pop,cenario=cen,N=len(h),q_zero=(q==0).mean(),q_menor_001=(q<.01).mean(),q_maior_099=(q>.99).mean(),q_meio_01_09=q.between(.1,.9).mean()))
 pd.DataFrame(qrows).to_csv(OUT/'SAT1_q_suplementar.csv',index=False)
 print(pd.DataFrame(rows).to_string(index=False),flush=True)
 return bool(rows[0]['meio_01_09']<.1)

def job(arg):
 kind,cell,vals,a,seed,cen=arg;p=S.carregar_parametros();op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];op['instrumentar_tarefas']=False
 if kind=='GOV':
  for k,v in zip(FACT,vals):p['cenarios'][cen][k]['valor']=v
 else:
  p['agentes']['s_transicao']['valor']=vals[0];op['regra_fuga']='dependente_estado'
 g,d,c=S.carregar_instancia(a);sim=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op));r=sim.executar()
 row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))};row.update(r.contadores)
 n=row['p1_fuga']+row['p1_omissao'];den=row['p1_omissao']+row['p3_analitica']
 row.update(kind=kind,celula=cell,arquivo=a,semente=seed,cenario=cen,violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=row['p1_omissao']/den if den else np.nan,n_selecoes_p1=n,fracao_fuga_p1=row['p1_fuga']/n if n else np.nan)
 return row

def ci(x):
 x=x.dropna();n=len(x);m=x.mean();h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n) if n>1 else np.nan
 return dict(media=m,ic95_inf=m-h,ic95_sup=m+h,N_instancias=n,sinal='positivo' if m>0 else 'negativo' if m<0 else 'zero',evidencia='positivo' if m-h>0 else 'negativo' if m+h<0 else 'inclui_zero')

def run():
 confirmed=sat1();cfg=yaml.safe_load((ROOT/'config/robustez_sat_gov.yaml').read_text())
 names=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::120]
 profiles=list(itertools.product(*[cfg['gov'][k] for k in FACT]));pd.DataFrame([dict(celula=i,**dict(zip(FACT,v))) for i,v in enumerate(profiles)]).to_csv(OUT/'GOV_perfis.csv',index=False)
 jobs=[('GOV',i,v,a,s,c) for i,v in enumerate(profiles) for a in names for s in cfg['sementes'] for c in ['centralizada','adaptativa']]
 if confirmed:jobs=[('SAT2',i,[v],a,s,c) for i,v in enumerate(cfg['s_transicao']) for a in names for s in cfg['sementes'] for c in ['centralizada','adaptativa']]+jobs
 files=list((ROOT/'src/modelo').glob('*.py'))+[ROOT/'config/parametros.yaml',ROOT/'config/mvp.yaml',Path(__file__),ROOT/'config/robustez_sat_gov.yaml']
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 (OUT/'manifesto.json').write_text(json.dumps(dict(config=cfg,N=len(jobs),instancias=names,SAT1_confirma=confirmed,hashes=hashes),indent=2))
 rows=[]
 with (OUT/'bruto.csv').open('x') as f,ProcessPoolExecutor(max_workers=4) as pool:
  w=None
  for i,row in enumerate(pool.map(job,jobs,chunksize=1)):
   if w is None:w=csv.DictWriter(f,fieldnames=list(row));w.writeheader()
   w.writerow(row);f.flush();rows.append(row)
   if (i+1)%64==0:print(i+1,len(jobs),flush=True)
 assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 d=pd.DataFrame(rows);assert d.violacoes.sum()==0
 analyze(d,cfg)

def analyze(d,cfg):
 sat=d[d.kind=='SAT2'];rows=[];inds=[]
 for (cell,cen),g in sat.groupby(['celula','cenario']):
  x=g.fracao_fuga_p1;rows.append(dict(s_transicao=cfg['s_transicao'][cell],cenario=cen,N=len(g),incompletas=int((~g.concluiu).sum()),fracao_fuga_p1_pool=g.p1_fuga.sum()/g.n_selecoes_p1.sum(),media=x.mean(),dp=x.std(),min=x.min(),q25=x.quantile(.25),mediana=x.median(),q75=x.quantile(.75),max=x.max()))
 pd.DataFrame(rows).to_csv(OUT/'SAT2_fuga.csv',index=False)
 # Absolute readouts for every profile and arm; CIs over instance means.
 for (kind,cell,cen),g in d.groupby(['kind','celula','cenario']):
  for m in MET:inds.append(dict(kind=kind,celula=cell,cenario=cen,metrica=m,incompletas=int((~g.concluiu).sum()),estatuto='COMPLETO' if g.concluiu.all() else 'CENSURADO: observado ate teto',**ci(g.groupby('arquivo')[m].mean())))
 pd.DataFrame(inds).to_csv(OUT/'indicadores_por_braco_IC95.csv',index=False)
 gov=d[d.kind=='GOV'];contr=[]
 groups={(int(cell),cen):g.set_index(['arquivo','semente']) for (cell,cen),g in gov.groupby(['celula','cenario'])}
 for a in sorted(gov.celula.unique()):
  for c in sorted(gov.celula.unique()):
   ga=groups[(a,'adaptativa')];gc=groups[(c,'centralizada')];ok=ga.concluiu&gc.concluiu
   for m in MET:
    diff=ga[m]-gc[m]
    for est,x in [('observado',diff),('pares_completos',diff[ok])]:
     contr.append(dict(perfil_adaptativa=a,perfil_centralizada=c,metrica=m,estimando=est,pares_previstos=len(diff),pares_retidos=len(x),pares_indefinidos=int(x.isna().sum()),estatuto='COMPLETO' if ok.all() else 'CENSURADO' if est=='observado' else 'CONDICIONAL_A_CONCLUSAO',**ci(x.groupby('arquivo').mean())))
 pd.DataFrame(contr).to_csv(OUT/'GOV_contrastes_IC95.csv',index=False)
 # Exact control: same profiles in both labels and historic nominal subset.
 equal=[]
 for a in sorted(gov.celula.unique()):
  aa=groups[(a,'adaptativa')];cc=groups[(a,'centralizada')]
  for m in MET+['TW','TL','TU','TR','makespan']:equal.append(float((aa[m]-cc[m]).abs().max()))
 assert max(equal)==0
 profiles=pd.read_csv(OUT/'GOV_perfis.csv');old=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv',float_precision='round_trip').set_index(['arquivo','semente','cenario']);checks=[]
 for cen,vals in [('centralizada',[.25,.6,.15,.03]),('adaptativa',[.8,.25,.75,.12])]:
  cell=int(profiles[np.isclose(profiles[FACT],vals).all(axis=1)].celula.iloc[0]);g=groups[(cell,cen)]
  for m in ['TW','TL','TU','TR','makespan','p1_fuga','p1_omissao','N_req']:
   o=old.xs(cen,level='cenario').loc[g.index,m];delta=float((g[m]-o).abs().max());assert delta==0;checks.append(dict(cenario=cen,metrica=m,residuo=delta))
 pd.DataFrame(checks).to_csv(OUT/'identidade_nominal.csv',index=False)
 (OUT/'verificacoes.json').write_text(json.dumps(dict(N=len(d),completas=int(d.concluiu.sum()),violacoes=int(d.violacoes.sum()),perfis_iguais_residuo=max(equal),identidade_nominal=True),indent=2))
if __name__=='__main__':run()
