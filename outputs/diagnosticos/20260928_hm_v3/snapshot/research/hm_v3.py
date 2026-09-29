"""HM e cobertura internos v3. Protocolo pré-registrado: parecer 81.

O runner 04 e cobertura.py são históricos; este runner não escreve nos caminhos
legados e não importa suas funções. Não altera os simuladores nem o nominal.
"""
import argparse, copy, csv, hashlib, json, platform, shutil, sys, time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import yaml
from scipy.stats import norm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP, OpcoesMVP
PARAMETROS=[('risco','F_ancora',.05,.25),('retrabalho','f_retrabalho',.30,.80),('agentes','tau_sat',.70,1.40),('agentes','k_analitico',.02,.08),('fuzzy','mu_minimo',.40,.70)]
NOMES=[s+'.'+k for s,k,_,_ in PARAMETROS]
LIMITES=np.array([(lo,hi) for _,_,lo,hi in PARAMETROS])
VERDADE=dict(zip(NOMES,[.180,.420,.850,.065,.620]))
OBS=['taxa_omissao','atraso_relativo','retrabalho_sobre_plano','E_total']
CACHE={}

def aplicar(base,x):
 p=copy.deepcopy(base)
 for s,k,_,_ in PARAMETROS:p[s][k]['valor']=float(x[s+'.'+k])
 p['agentes']['k_heuristico']['valor']=p['agentes']['k_analitico']['valor']
 verificar_derivacao(p)
 return p

def verificar_derivacao(p):
 a=float(S.v(p['agentes']['k_analitico']));h=float(S.v(p['agentes']['k_heuristico']))
 assert a.hex()==h.hex(),f'Derivação violada: {a.hex()} != {h.hex()}'

def lhs(n,limites,rng):
 X=np.empty((n,len(limites)))
 for j,(lo,hi) in enumerate(limites):
  cortes=(np.arange(n)+rng.random(n))/n
  X[:,j]=lo+(hi-lo)*rng.permutation(cortes)
 return X

def estatistica(exec_por_bloco):
 blocos=np.asarray(exec_por_bloco).mean(axis=1)
 return blocos.mean(axis=0),blocos.var(axis=0,ddof=1)/len(blocos)

def semente_cobertura(b,grupo,bloco,i):return 10000000+28*b+(0 if grupo=='obs' else 20)+2*bloco+i

def indice(z,vo,f,vs):
 delta=abs(np.asarray(z)-f);den=np.sqrt(np.asarray(vo)+vs)
 return np.divide(delta,den,out=np.where(delta==0,0.,np.inf),where=den>0)

def setup(out):
 if 'base' not in CACHE:
  snap=Path(out)/'snapshot';CACHE['base']=S.carregar_parametros(snap/'config/parametros.yaml',snap/'config/parametros_derivados.yaml')
  CACHE['op']=yaml.safe_load((snap/'config/mvp.yaml').read_text())['opcoes'];CACHE['op']['instrumentar_tarefas']=False
  CACHE['inst']=json.loads((Path(out)/'desenho.json').read_text())['instancias']
 return CACHE['base'],CACHE['op'],CACHE['inst']

def executar_grupo(out,x,seeds,label,point,replica=-1):
 base,op,inst=setup(out);par=aplicar(base,x);raw=[];blocks=[]
 for j,pair in enumerate(seeds):
  values=[]
  for i,arq in enumerate(inst):
   if arq not in CACHE:CACHE[arq]=S.carregar_instancia(arq)
   g,d,c=CACHE[arq];seed=int(pair[i]);verificar_derivacao(par)
   r=SimulacaoMVP(g,d,c,par,'adaptativa',seed,opcoes=OpcoesMVP(**op)).executar()
   vals=[r.taxa_omissao,r.makespan/r.makespan_cpm,r.retrabalho_sobre_plano,r.E_total]
   row=dict(grupo=label,ponto=point,replica=replica,bloco=j,arquivo=arq,semente=seed,cenario='adaptativa',**x,k_heuristico=float(S.v(par['agentes']['k_heuristico'])),k_analitico_hex=float(S.v(par['agentes']['k_analitico'])).hex(),k_heuristico_hex=float(S.v(par['agentes']['k_heuristico'])).hex(),violacoes=len(r.violacoes),mensagens_violacao=' | '.join(r.violacoes),concluiu=r.concluiu,**dict(zip(OBS,vals)))
   raw.append(row);values.append(vals)
  blocks.append(values)
 mean,var=estatistica(blocks)
 return mean,var,raw

def point_job(args):
 out,label,i,x,seeds=args;mean,var,raw=executar_grupo(out,x,seeds,label,i)
 row=dict(grupo=label,ponto=i,**x)
 for j,o in enumerate(OBS):row.update({f'media_{o}':float(mean[j]),f'var_media_{o}':float(var[j])})
 return row,raw

def coverage_job(args):
 out,b=args;results=[];raw=[]
 for group,n in [('obs',10),('sim',4)]:
  seeds=[[semente_cobertura(b,group,j,i) for i in range(2)] for j in range(n)]
  m,v,r=executar_grupo(out,VERDADE,seeds,'cobertura_'+group,-1,b);results.append((m,v));raw.extend(r)
 (z,vo),(f,vs)=results;I=indice(z,vo,f,vs);row=dict(replica=b,I_max=float(max(I)),excluido=bool(max(I)>3))
 for j,o in enumerate(OBS):row.update({f'z_{o}':float(z[j]),f'f_{o}':float(f[j]),f'V_obs_{o}':float(vo[j]),f'V_sim_{o}':float(vs[j]),f'I_{o}':float(I[j])})
 return row,raw

def save_json(path,v):
 with path.open('x') as f:json.dump(v,f,indent=2,ensure_ascii=False)

def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def collect(pool,fn,jobs,out,name):
 rows=[];N=viol=inc=0;start=time.monotonic()
 with (out/(name+'_execucoes.csv')).open('x') as f:
  writer=None
  for row,raw in pool.map(fn,jobs,chunksize=1):
   if writer is None:writer=csv.DictWriter(f,fieldnames=list(raw[0]));writer.writeheader()
   writer.writerows(raw);f.flush();rows.append(row);N+=len(raw);viol+=sum(r['violacoes'] for r in raw);inc+=sum(not r['concluiu'] for r in raw)
   if viol:raise RuntimeError(f'Violações em {name}: {viol}; saídas preservadas, interrompido')
   if len(rows)%25==0:print(name,len(rows),'/',len(jobs),'execucoes',N,'s',round(time.monotonic()-start,1),flush=True)
 frame=pd.DataFrame(rows);frame.to_csv(out/(name+'_estatisticas.csv'),index=False)
 save_json(out/(name+'_validade.json'),dict(N=N,violacoes=viol,incompletas=inc,segundos=time.monotonic()-start))
 return frame

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--workers',type=int,default=4);args=ap.parse_args();out=args.saida.resolve();out.mkdir(parents=True,exist_ok=False)
 start=time.monotonic()
 frozen={str(p.relative_to(ROOT)):hashfile(p) for p in (ROOT/'outputs').rglob('*') if p.is_file() and not p.is_relative_to(out)}
 save_json(out/'evidencias_anteriores_hashes.json',frozen)
 sources=[*sorted((ROOT/'src/modelo').glob('*.py')),ROOT/'research/hm_v3.py',ROOT/'research/test_hm_v3.py',ROOT/'projeto/81_HM_V3_PRE_REGISTRO_E_RESULTADOS.md',*(ROOT/'config'/n for n in ['parametros.yaml','parametros_derivados.yaml','mvp.yaml'])]
 hashes={str(p.relative_to(ROOT)):hashfile(p) for p in sources}
 for p in sources:
  dest=out/'snapshot'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 files=sorted(pd.read_csv(ROOT/'data/processed/psplib/tarefas_j60_com_di.csv',float_precision='round_trip').arquivo.unique());inst=files[::len(files)//2][:2]
 save_json(out/'desenho.json',dict(versao='v3',verdade=VERDADE,parametros=PARAMETROS,instancias=inst,B=500,V_mod=0,observaveis=OBS,N_previsto=20428,workers=args.workers,python=sys.version,numpy=np.__version__,plataforma=platform.platform(),hashes=hashes))
 with ProcessPoolExecutor(args.workers) as pool:
  z=collect(pool,point_job,[(str(out),'verdade',-1,VERDADE,[[s,s] for s in range(100,110)])],out,'verdade').iloc[0]
  vtrue=collect(pool,point_job,[(str(out),'controle_verdade',-1,VERDADE,[[s,s] for s in range(200,204)])],out,'controle_verdade').iloc[0]
  obs=z[[f'media_{o}' for o in OBS]].to_numpy(float);vo=z[[f'var_media_{o}' for o in OBS]].to_numpy(float)
  I=indice(obs,vo,vtrue[[f'media_{o}' for o in OBS]].to_numpy(float),vtrue[[f'var_media_{o}' for o in OBS]].to_numpy(float))
  save_json(out/'controle_verdade_I.json',dict(I=dict(zip(OBS,I.tolist())),I_max=float(max(I)),excluido=bool(max(I)>3)))
  limites=LIMITES.copy()
  for wave in (1,2):
   X=lhs(400,limites,np.random.default_rng(20260905));points=[dict(zip(NOMES,row)) for row in X]
   pd.DataFrame(points).to_csv(out/f'onda{wave}_propostas.csv',index=False)
   d=collect(pool,point_job,[(str(out),f'onda{wave}',i,x,[[s,s] for s in range(4)]) for i,x in enumerate(points)],out,f'onda{wave}')
   d['implausibilidade']=[max(indice(obs,vo,row[[f'media_{o}' for o in OBS]].to_numpy(float),row[[f'var_media_{o}' for o in OBS]].to_numpy(float))) for _,row in d.iterrows()]
   d.to_csv(out/f'onda{wave}_hm.csv',index=False);nroy=d[d.implausibilidade<=3]
   print('ONDA',wave,'NROY',len(nroy),'/',len(d),flush=True)
   if nroy.empty:break
   limites=np.array([(nroy[n].min(),nroy[n].max()) for n in NOMES])
  cov=collect(pool,coverage_job,[(str(out),b) for b in range(500)],out,'cobertura')
 k=int(cov.excluido.sum());n=len(cov);q=norm.ppf(.975);ph=k/n;den=1+q*q/n;center=(ph+q*q/(2*n))/den;half=q*np.sqrt(ph*(1-ph)/n+q*q/(4*n*n))/den
 for rel,h in hashes.items():assert hashfile(ROOT/rel)==h,rel
 for rel,h in frozen.items():assert hashfile(ROOT/rel)==h,rel
 save_json(out/'resumo_execucao.json',dict(B=n,exclusoes=k,taxa=ph,IC95_Wilson=[center-half,center+half],p95_Imax=float(cov.I_max.quantile(.95)),segundos_total=time.monotonic()-start,evidencias_antigas_inalteradas=len(frozen),codigo_config_pre_registro_inalterados=True))
 print('CONCLUIDO',json.loads((out/'resumo_execucao.json').read_text()),flush=True)
if __name__=='__main__':main()
