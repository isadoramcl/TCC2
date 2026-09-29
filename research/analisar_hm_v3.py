"""Auditoria a partir de execuções brutas, sem importar o runner HM."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import norm,binomtest
ROOT=Path(__file__).resolve().parents[1]
OBS=['taxa_omissao','atraso_relativo','retrabalho_sobre_plano','E_total']
def read(p):return pd.read_csv(p,float_precision='round_trip')
def est(d):
 b=d.groupby('bloco',sort=True)[OBS].mean()
 return b.mean().to_numpy(),(b.var(ddof=1)/len(b)).to_numpy()
def indices(z,vo,f,vs):
 return np.array([abs(a-b)/np.sqrt(c+d) if c+d>0 else (0 if a==b else np.inf) for a,b,c,d in zip(z,f,vo,vs)])
def audit(out):
 des=json.loads((out/'desenho.json').read_text());summary=json.loads((out/'resumo_execucao.json').read_text());rows=[];maxerr=0.;total=0;viol=0;inc=0
 rawsets={p.name.removesuffix('_execucoes.csv'):read(p) for p in out.glob('*_execucoes.csv')}
 for tag,d in rawsets.items():
  total+=len(d);viol+=int(d.violacoes.sum());inc+=int((~d.concluiu).sum())
  assert (d.k_analitico_hex==d.k_heuristico_hex).all()
  assert [float(x).hex() for x in d['agentes.k_analitico']]==d.k_analitico_hex.tolist()
  assert [float(x).hex() for x in d.k_heuristico]==d.k_heuristico_hex.tolist()
  assert not d.duplicated(['grupo','ponto','replica','bloco','arquivo']).any()
  for _,block in d.groupby(['grupo','ponto','replica','bloco']):assert len(block)==2 and set(block.arquivo)==set(des['instancias'])
  if not tag.startswith('onda'):
   for col,val in des['verdade'].items():assert all(float(x).hex()==float(val).hex() for x in d[col])
  if tag.startswith('onda'):assert len(d)==3200 and d.ponto.nunique()==400
 assert total==20428 and viol==0
 assert set(rawsets['verdade'].semente)==set(range(100,110))
 assert set(rawsets['controle_verdade'].semente)==set(range(200,204))
 z,vo=est(rawsets['verdade']);f,vs=est(rawsets['controle_verdade']);itrue=indices(z,vo,f,vs)
 for tag in ['onda1','onda2']:
  points=[];arch=read(out/(tag+'_hm.csv')).set_index('ponto')
  proposals=read(out/(tag+'_propostas.csv'));assert len(proposals)==400
  assert set(rawsets[tag].semente)==set(range(4))
  if tag=='onda1': bounds=[(lo,hi) for _,_,lo,hi in des['parametros']]
  else:
   prev=read(out/'onda1_hm.csv');prev=prev[prev.implausibilidade<=3]
   bounds=[(prev[s+'.'+n].min(),prev[s+'.'+n].max()) for s,n,_,_ in des['parametros']]
  for (sec,par,_,_),(lo,hi) in zip(des['parametros'],bounds):
   col=sec+'.'+par;assert proposals[col].between(lo,hi).all()
   strata=np.floor(400*(proposals[col].to_numpy()-lo)/(hi-lo)).astype(int)
   assert len(set(strata))==400 and min(strata)==0 and max(strata)==399
  for k,d in rawsets[tag].groupby('ponto'):
   for sec,par,_,_ in des['parametros']:
    col=sec+'.'+par;assert all(float(v).hex()==float(proposals.iloc[int(k)][col]).hex() for v in d[col])
   assert (d.groupby('bloco').semente.nunique()==1).all()
   m,v=est(d);I=indices(z,vo,m,v);points.append(dict(ponto=int(k),I_max=float(max(I)),**{s+'.'+n:float(d.iloc[0][s+'.'+n]) for s,n,_,_ in des['parametros']}));maxerr=max(maxerr,abs(max(I)-arch.loc[k,'implausibilidade']))
  a=pd.DataFrame(points);nroy=a[a.I_max<=3];volume=1
  for s,n,lo,hi in des['parametros']:
   name=s+'.'+n;low=nroy[name].min();high=nroy[name].max();red=1-(high-low)/(hi-lo);volume*=(high-low)/(hi-lo)
   rows.append(dict(versao='v3',onda=tag,parametro=name,minimo=low,maximo=high,contracao=red,rotulo_descritivo='identificado' if red>=.5 else ('parcialmente identificado' if red>=.25 else 'não identificado'),verdade_na_projecao=bool(low<=des['verdade'][name]<=high)))
  summary[tag]=dict(N=len(a),NROY=len(nroy),fracao_propostas=len(nroy)/len(a),volume_caixa_relativo=float(volume))
 # Cobertura independente: nenhuma linha de I do runner é usada para classificar.
 cov=[];arch=read(out/'cobertura_estatisticas.csv').set_index('replica');d=rawsets['cobertura']
 assert len(d)==14000 and d.semente.nunique()==14000
 for b,g in d.groupby('replica'):
  obs=g[g.grupo=='cobertura_obs'];sim=g[g.grupo=='cobertura_sim'];assert len(obs)==20 and len(sim)==8
  z_,vo_=est(obs);f_,vs_=est(sim);I=indices(z_,vo_,f_,vs_)
  maxerr=max(maxerr,abs(max(I)-arch.loc[b,'I_max']))
  cov.append(dict(replica=int(b),I_max=float(max(I)),excluido=bool(max(I)>3),**dict(zip(OBS,I))))
 c=pd.DataFrame(cov);k=int(c.excluido.sum());n=len(c);q=norm.ppf(.975);p=k/n;den=1+q*q/n;mid=(p+q*q/(2*n))/den;delta=q*np.sqrt(p*(1-p)/n+q*q/(4*n*n))/den
 summary.update(N_total=total,violacoes=viol,incompletas=inc,igualdade_hex_em_todas_execucoes=True,max_residuo_recalculo=float(maxerr),I_verdade=dict(zip(OBS,itrue.tolist())),Imax_verdade=float(max(itrue)),cobertura_independente=dict(B=n,exclusoes=k,taxa=p,IC95_Wilson=[mid-delta,mid+delta],diferenca_pp_frente_5=100*(p-.05),p95_Imax=float(c.I_max.quantile(.95)),cinco_porcento_no_IC=bool(mid-delta<=.05<=mid+delta),teste_binomial_bilateral_p=float(binomtest(k,n,.05).pvalue)))
 assert maxerr<1e-10
 hist=read(ROOT/'outputs/tables/modelo_04_hm_onda2.csv');hn=hist[hist.implausibilidade<=3]
 for s,n,lo,hi in [('risco','F_ancora',.05,.25),('retrabalho','f_retrabalho',.3,.8),('agentes','tau_sat',.7,1.4),('agentes','k_heuristico',.06,.16),('fuzzy','mu_minimo',.4,.7)]:
  col=s+'.'+n;red=1-(hn[col].max()-hn[col].min())/(hi-lo)
  rows.append(dict(versao='legado_v1_v2',onda='onda2',parametro=col,minimo=hn[col].min(),maximo=hn[col].max(),contracao=red,rotulo_descritivo='identificado' if red>=.5 else ('parcialmente identificado' if red>=.25 else 'não identificado'),verdade_na_projecao=bool(hn[col].min()<=dict(zip(['risco.F_ancora','retrabalho.f_retrabalho','agentes.tau_sat','agentes.k_heuristico','fuzzy.mu_minimo'],[.18,.42,.85,.135,.62]))[col]<=hn[col].max())))
 save=out/'auditoria';save.mkdir(exist_ok=False);pd.DataFrame(rows).to_csv(save/'identificabilidade_lado_a_lado.csv',index=False);c.to_csv(save/'cobertura_recalculada.csv',index=False)
 c0=read(ROOT/'outputs/diagnosticos/noturno_D2_execucao/replicas.csv');k0=int((c0.I_max>3).sum());n0=len(c0);p0=k0/n0;den0=1+q*q/n0;mid0=(p0+q*q/(2*n0))/den0;half0=q*np.sqrt(p0*(1-p0)/n0+q*q/(4*n0*n0))/den0
 pd.DataFrame([dict(versao='legado_v1_v2',B=n0,exclusoes=k0,taxa=p0,Wilson_inf=mid0-half0,Wilson_sup=mid0+half0,p95_Imax=c0.I_max.quantile(.95)),dict(versao='v3',B=n,exclusoes=k,taxa=p,Wilson_inf=mid-delta,Wilson_sup=mid+delta,p95_Imax=c.I_max.quantile(.95))]).to_csv(save/'cobertura_lado_a_lado.csv',index=False)
 # Complemento principal: conferir pareamento a partir do bruto, não do gerador.
 paired=out/'cobertura_pareada';d=read(paired/'cobertura_execucoes.csv');ar=read(paired/'cobertura_estatisticas.csv').set_index('replica')
 assert len(d)==14000 and d.semente.nunique()==7000 and (d.violacoes==0).all()
 assert (d.k_analitico_hex==d.k_heuristico_hex).all()
 assert [float(x).hex() for x in d['agentes.k_analitico']]==d.k_analitico_hex.tolist()
 assert [float(x).hex() for x in d.k_heuristico]==d.k_heuristico_hex.tolist()
 blocks=d.groupby(['replica','grupo','bloco']);assert (blocks.semente.nunique()==1).all() and (blocks.size()==2).all()
 assert (d.groupby('semente').size()==2).all()
 for _,block in blocks:assert set(block.arquivo)==set(des['instancias'])
 for col,val in des['verdade'].items():assert all(float(x).hex()==float(val).hex() for x in d[col])
 vals=[];err=0.
 for b,g in d.groupby('replica'):
  aa=g[g.grupo=='cobertura_obs'];bb=g[g.grupo=='cobertura_sim'];assert len(aa)==20 and len(bb)==8
  zz,vv=est(aa);ff,ss=est(bb);ii=indices(zz,vv,ff,ss);imax=float(max(ii));err=max(err,abs(imax-ar.loc[b,'I_max']))
  vals.append(dict(replica=b,I_max=imax,excluido=imax>3,**dict(zip(OBS,ii))))
 cc=pd.DataFrame(vals);kk=int(cc.excluido.sum());nn=len(cc);pp=kk/nn;dd=1+q*q/nn;mm=(pp+q*q/(2*nn))/dd;hh=q*np.sqrt(pp*(1-pp)/nn+q*q/(4*nn*nn))/dd
 assert err<1e-10
 cc.to_csv(save/'cobertura_pareada_recalculada.csv',index=False)
 comparison=read(save/'cobertura_lado_a_lado.csv');comparison.loc[comparison.versao=='v3','versao']='v3_instancias_independentes'
 comparison=pd.concat([comparison,pd.DataFrame([dict(versao='v3_pareada_PRINCIPAL',B=nn,exclusoes=kk,taxa=pp,Wilson_inf=mm-hh,Wilson_sup=mm+hh,p95_Imax=cc.I_max.quantile(.95))])],ignore_index=True)
 # Este arquivo ainda não foi entregue/congelado; a versão final distinta preserva a primeira tabela.
 comparison.to_csv(save/'coberturas_tres_desenhos.csv',index=False)
 summary['cobertura_pareada_principal']=dict(B=nn,exclusoes=kk,taxa=pp,IC95_Wilson=[mm-hh,mm+hh],p95_Imax=float(cc.I_max.quantile(.95)),cinco_porcento_no_IC=bool(mm-hh<=.05<=mm+hh),diferenca_pp_frente_5=100*(pp-.05),p_binomial_bilateral=float(binomtest(kk,nn,.05).pvalue),N=len(d),violacoes=int(d.violacoes.sum()),incompletas=int((~d.concluiu).sum()),residuo=err)
 summary['N_total_complemento_incluido']=total+len(d)
 (save/'verificacao_independente.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n');print(json.dumps(summary,indent=2));print(pd.DataFrame(rows).to_string(index=False))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('saida',type=Path);audit(a.parse_args().saida)
