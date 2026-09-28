"""79 etapa 1: controles 1a/1b, referências externas e tabelas v2/v3."""
from pathlib import Path
import sys,json,struct,csv,time,hashlib
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np,pandas as pd,yaml
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260928_drenagem_heuristica/etapa1'
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
REF='outputs/diagnosticos/20260921_nominal_v2/bruto_nominal.csv'
def read(p):return pd.read_csv(ROOT/p,float_precision='round_trip')
def job(arg):
 tag,a,seed,cen,kh=arg;p=S.carregar_parametros(OUT/'snapshot_executado/config/parametros.yaml',OUT/'snapshot_executado/config/parametros_derivados.yaml');p['agentes']['k_heuristico']['valor']=kh
 op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];op['instrumentar_tarefas']=False
 g,d,c=S.carregar_instancia(a);r=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op)).executar()
 row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))};row.update(r.contadores);den=row['p1_omissao']+row['p3_analitica']
 row.update(conjunto=tag,arquivo=a,semente=seed,cenario=cen,kh=kh,violacoes=len(r.violacoes),mensagens_violacoes=';'.join(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=row['p1_omissao']/den,fracao_fuga=row['p1_fuga']/(den+row['p1_fuga']))
 return row

def execute(jobs,path):
 with path.open('x') as file,ProcessPoolExecutor(4) as pool:
  w=None
  for i,row in enumerate(pool.map(job,jobs,chunksize=1),1):
   if w is None:w=csv.DictWriter(file,fieldnames=list(row));w.writeheader()
   w.writerow(row);file.flush()
   if i%64==0:print(i,'/',len(jobs),flush=True)
 return pd.read_csv(path,float_precision='round_trip')
def control(output=None):
 output=output or OUT;output.mkdir(exist_ok=True)
 ref=read(REF);jobs=[('controle',r.arquivo,int(r.semente),r.cenario,.10) for r in ref.itertuples()]
 d=execute(jobs,output/'bruto_controle_reconciliado.csv');keys=['arquivo','semente','cenario'];A=ref.set_index(keys,drop=False);cols=[c for c in ref.select_dtypes('number').columns if c!='violacoes'];assert len(cols)==48
 exceptions=[];failures=[]
 for row in d.to_dict('records'):
  old=A.loc[tuple(row[k] for k in keys)]
  for field in cols:
   a,b=float(old[field]),float(row[field])
   if a.hex()==b.hex():continue
   ulp=abs(struct.unpack('>Q',struct.pack('>d',a))[0]-struct.unpack('>Q',struct.pack('>d',b))[0])
   info=dict(**{k:row[k] for k in keys},campo=field,hex_ref=a.hex(),hex_obtido=b.hex(),distancia_ulp=ulp)
   if (field.startswith('competencia_') or field=='confianca_media_final') and ulp<=2:exceptions.append(info)
   else:failures.append(info)
 guard=bool((d.violacoes==1).all() and d.mensagens_violacoes.str.contains('não pode exceder').all())
 result=dict(identidade_1a=not failures,guarda_1b_historico=guard,N=len(d),campos=48,excecoes=exceptions,divergencias=failures,completas=int(d.concluiu.sum()))
 (output/'controle_reconciliado.json').write_text(json.dumps(result,indent=2));assert not failures and guard and d.concluiu.all(),result
 print('CONTROLES APROVADOS',len(exceptions),'excecoes autorizadas',flush=True)
def contrasts(d):
 rows=[]
 for m in MET:
  q=d.pivot(index=['arquivo','semente'],columns='cenario',values=m);v=(q.adaptativa-q.centralizada).groupby('arquivo').mean();avg=v.mean();h=t.ppf(.975,len(v)-1)*v.std(ddof=1)/np.sqrt(len(v))
  rows.append(dict(metrica=m,media=avg,ic95_inf=avg-h,ic95_sup=avg+h,N_instancias=len(v)))
 return rows

def candidate():
 assert json.loads((OUT/'controle_reconciliado.json').read_text())['identidade_1a']
 nom=sorted(read(REF).arquivo.unique());outside=read('outputs/diagnosticos/20260920_fora_da_amostra/amostra_estratificada.csv').arquivo.drop_duplicates().tolist()[:16]
 assert len(nom)==len(outside)==16
 jobs=[(tag,a,s,c,.04) for tag,files in [('nominal',nom),('fora16',outside)] for a in files for s in range(12) for c in ['centralizada','adaptativa']]
 (OUT/'desenho_etapa1.json').write_text(json.dumps(dict(nominal=nom,fora16=outside,ordem_fora='primeiras 16 linhas distintas do arquivo, sem novo sorteio',sementes=list(range(12)),kh=.04),indent=2))
 d=execute(jobs,OUT/'bruto_candidato.csv');assert d.concluiu.all() and (d.violacoes==0).all(),'Guarda 1b/conclusao falhou'
 expected={'nominal':[[-.8682,-.9866,-.7497],[-.1759,-.1940,-.1577],[-.0552,-.0615,-.0489],[-.0217,-.0342,-.0092],[-.0523,-.0669,-.0376]],'fora16':[[-.9975,-1.1377,-.8573],[-.1785,-.1929,-.1641],[-.0600,-.0686,-.0515],[-.0227,-.0371,-.0082],[-.0476,-.0634,-.0318]]}
 rows=[];mismatches=[]
 for tag,g in d.groupby('conjunto'):
  for i,row in enumerate(contrasts(g)):
   rows.append(dict(conjunto=tag,versao='v3_etapa1',**row))
   for field,exp in zip(['media','ic95_inf','ic95_sup'],expected[tag][i]):
    if format(row[field],'.4f')!=format(exp,'.4f'):mismatches.append(dict(conjunto=tag,metrica=row['metrica'],campo=field,referencia=exp,obtido=row[field],delta=row[field]-exp))
 pd.DataFrame(rows).to_csv(OUT/'contrastes_candidato.csv',index=False)
 result=dict(N=len(d),completas=int(d.concluiu.sum()),violacoes=int(d.violacoes.sum()),guarda_1b_candidato=True,referencias_reproduzidas=not mismatches,divergencias=mismatches)
 (OUT/'resultado_etapa1.json').write_text(json.dumps(result,indent=2));print(pd.DataFrame(rows).to_string(index=False));print(json.dumps(result,indent=2))
 if mismatches:raise SystemExit(2)
 before=read(REF);oldfora=read('outputs/diagnosticos/20260921_nominal_v2/bruto_fora_da_amostra.csv');oldfora=oldfora[oldfora.arquivo.isin(outside)]
 for tag,g in [('nominal',before),('fora16',oldfora)]:
  rows.extend(dict(conjunto=tag,versao='v2',**r) for r in contrasts(g))
 pd.DataFrame(rows).to_csv(OUT/'v2_v3_lado_a_lado.csv',index=False)
if __name__=='__main__':{'controle':control,'controle_final':lambda:control(OUT.parent/'etapa3'/'controle_v2'),'candidato':candidate}[sys.argv[1]]()
