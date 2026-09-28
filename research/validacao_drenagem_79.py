"""Etapas 2/3 do parecer 79; tabelas históricas permanecem congeladas."""
import sys,json,csv,itertools,shutil
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
import numpy as np,pandas as pd,yaml
from scipy.stats import t
import etapa1_drenagem_79 as E
ROOT=E.ROOT;BASE=E.OUT.parent;MET=E.MET
FACT=['tau_inicial','tau_min','p_reporte','p_deteccao']
def job(arg):
 tag,a,seed,cen,profile,stage=arg
 p=E.S.carregar_parametros(BASE/stage/'parametros_executados.yaml',BASE/stage/'parametros_derivados_executados.yaml')
 if profile is not None:
  for k,v in zip(FACT,profile):p['cenarios'][cen][k]['valor']=v
 op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];op['instrumentar_tarefas']=False
 g,d,c=E.S.carregar_instancia(a);r=E.SimulacaoMVP(g,d,c,p,cen,seed,opcoes=E.OpcoesMVP(**op)).executar()
 row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))};row.update(r.contadores);den=row['p1_omissao']+row['p3_analitica']
 row.update(conjunto=tag,arquivo=a,semente=seed,cenario=cen,violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=row['p1_omissao']/den,fracao_fuga=row['p1_fuga']/(den+row['p1_fuga']))
 if profile is not None:row.update(dict(zip(FACT,profile)))
 else:row.update({k:np.nan for k in FACT})
 return row

def run(stage):
 out=BASE/stage
 if (out/'bruto_novo.csv').exists():raise FileExistsError(f'Evidencia congelada: {out}; escolha outro diretorio de saida')
 out.mkdir(parents=True,exist_ok=True)
 assert json.loads((E.OUT/'resultado_etapa1.json').read_text())['referencias_reproduzidas']
 nom=sorted(E.read(E.REF).arquivo.unique());fora=E.read('outputs/diagnosticos/20260920_fora_da_amostra/amostra_estratificada.csv').arquivo.drop_duplicates().tolist()
 random=json.loads((ROOT/'outputs/diagnosticos/20260922_teste_aleatorio/amostra.json').read_text())
 prof=E.read('outputs/diagnosticos/SAT_GOV_20260919/GOV_perfis.csv');ref=E.read('outputs/diagnosticos/20260921_nominal_v2/governanca/bruto.csv');instances=sorted(ref.arquivo.unique())
 groups=[('nominal',nom,list(range(12))),('fora48',fora,list(range(12))),('aleatorio24',random['instancias'],random['sementes_simulacao'])]
 if stage=='etapa2':groups=[('fora48',fora[16:],list(range(12))),('aleatorio24',random['instancias'],random['sementes_simulacao'])]
 jobs=[(tag,a,s,c,None) for tag,files,seeds in groups for a in files for s in seeds for c in ['centralizada','adaptativa']]
 jobs += [(f'GOV_{int(r.celula)}',a,s,c,[float(getattr(r,k)) for k in FACT]) for r in prof.itertuples() for a in instances for s in range(4) for c in ['centralizada','adaptativa']]
 jobs=[(*j,stage) for j in jobs]
 source=(E.OUT/'snapshot_executado/config/parametros.yaml') if stage=='etapa2' else ROOT/'config/parametros.yaml'
 shutil.copyfile(source,out/'parametros_executados.yaml')
 shutil.copyfile(ROOT/'config/parametros_derivados.yaml',out/'parametros_derivados_executados.yaml')
 (out/'desenho.json').write_text(json.dumps(dict(N_novas=len(jobs),opcoes=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'],parametros_agentes=E.S.carregar_parametros()['agentes'],nominal=nom,fora48=fora,aleatorio=random,governanca_instancias=instances),indent=2))
 with (out/'bruto_novo.csv').open('x') as f,ProcessPoolExecutor(4) as pool:
  w=None
  for i,row in enumerate(pool.map(job,jobs,chunksize=1),1):
   if w is None:w=csv.DictWriter(f,fieldnames=list(row));w.writeheader()
   w.writerow(row);f.flush()
   if i%128==0 or i==len(jobs):print(stage,i,'/',len(jobs),flush=True)

def contrast_profiles(d,profiles):
 groups={int(tag.split('_')[1]):g[g.cenario=='adaptativa'].set_index(['arquivo','semente']) for tag,g in d.groupby('conjunto')}
 rows=[]
 for a in profiles.itertuples():
  for c in profiles.itertuples():
   if a.celula==c.celula or not(a.tau_inicial>=c.tau_inicial and a.tau_min<=c.tau_min and a.p_reporte>=c.p_reporte and a.p_deteccao>=c.p_deteccao):continue
   for m in MET:
    x=(groups[a.celula][m]-groups[c.celula][m]).groupby('arquivo').mean();avg=x.mean();h=t.ppf(.975,3)*x.std(ddof=1)/2
    rows.append(dict(ai=a.celula,ci=c.celula,metrica=m,media=avg,ic95_inf=avg-h,ic95_sup=avg+h))
 return pd.DataFrame(rows)
def analyze(stage):
 out=BASE/stage;d=pd.read_csv(out/'bruto_novo.csv',float_precision='round_trip')
 if stage=='etapa2':
  first=pd.read_csv(E.OUT/'bruto_candidato.csv',float_precision='round_trip');first['conjunto']=first.conjunto.replace({'fora16':'fora48'});d=pd.concat([first,d],ignore_index=True)
 assert len(d)==4704 and d.concluiu.all() and (d.violacoes==0).all()
 d.to_csv(out/'bruto_completo.csv',index=False)
 rows=[]
 for tag in ['nominal','fora48','aleatorio24']:
  g=d[d.conjunto==tag];rows.extend(dict(conjunto=tag,versao=stage,**r) for r in E.contrasts(g))
 versions=[('v2',{'nominal':E.REF,'fora48':'outputs/diagnosticos/20260921_nominal_v2/bruto_fora_da_amostra.csv','aleatorio24':'outputs/diagnosticos/20260922_teste_aleatorio/bruto.csv'})]
 for ver,paths in versions:
  for tag,p in paths.items():rows.extend(dict(conjunto=tag,versao=ver,**r) for r in E.contrasts(E.read(p)))
 if stage=='etapa3':
  prev=pd.read_csv(E.OUT.parent/'etapa2/contrastes_lado_a_lado.csv',float_precision='round_trip');rows+=prev[prev.versao=='etapa2'].to_dict('records')
 pd.DataFrame(rows).to_csv(out/'contrastes_lado_a_lado.csv',index=False)
 gov=d[d.conjunto.str.startswith('GOV_')].copy();profiles=E.read('outputs/diagnosticos/SAT_GOV_20260919/GOV_perfis.csv')
 # Same profile must be identical in either label before forming inter-profile contrasts.
 numeric=gov.select_dtypes('number').columns
 for tag,g in gov.groupby('conjunto'):
  aa=g[g.cenario=='adaptativa'].set_index(['arquivo','semente']);cc=g[g.cenario=='centralizada'].set_index(['arquivo','semente'])
  for f in [x for x in numeric if x not in ['semente']]:
   assert [float(v).hex() for v in aa[f]]==[float(v).hex() for v in cc.loc[aa.index,f]],(tag,f)
 cur=contrast_profiles(gov,profiles);assert len(cur)==6075;cur.to_csv(out/'GOV_contrastes.csv',index=False)
 old=E.read('outputs/diagnosticos/20260921_nominal_v2/governanca/bruto.csv');old['conjunto']='GOV_'+old.celula.astype(str)
 hist=contrast_profiles(old,profiles);hist.to_csv(out/'GOV_v2_recalculado.csv',index=False)
 summary=[]
 for version,table in [('v2',hist),(stage,cur)]:
  for metric,g in table.groupby('metrica'):summary.append(dict(versao=version,metrica=metric,N=len(g),negativos=int((g.media<0).sum()),positivos=int((g.media>0).sum()),zero=int((g.media==0).sum()),IC_negativo=int((g.ic95_sup<0).sum()),IC_positivo=int((g.ic95_inf>0).sum())))
 pd.DataFrame(summary).to_csv(out/'GOV_sinais.csv',index=False)
 changes=hist.merge(cur,on=['ai','ci','metrica'],suffixes=('_v2','_'+stage));changes['mudou_sinal']=np.sign(changes.media_v2)!=np.sign(changes['media_'+stage]);changes.to_csv(out/'GOV_antes_depois.csv',index=False)
 (out/'verificacoes.json').write_text(json.dumps(dict(N=len(d),completas=int(d.concluiu.sum()),violacoes=int(d.violacoes.sum()),perfis_iguais=True,pares_ordenados=1215),indent=2))
 print(pd.DataFrame(rows).round(6).to_string(index=False));print(pd.DataFrame(summary).to_string(index=False))
if __name__=='__main__':
 if len(sys.argv)>3:BASE=Path(sys.argv[3]).resolve()
 {'rodar':run,'analisar':analyze}[sys.argv[1]](sys.argv[2])
