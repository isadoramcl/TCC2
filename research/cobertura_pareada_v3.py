"""Cobertura do desenho HM pareado; pré-registro 81A, sem escolher taxa."""
import argparse,json,time,shutil
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy.stats import norm
import hm_v3 as H

def seeds(b,group):
 start=20000000+14*b+(0 if group=='obs' else 10)
 return [[s,s] for s in range(start,start+(10 if group=='obs' else 4))]

def job(args):
 base,out,b=args
 # Dados efetivamente lidos vêm da cópia congelada deste complemento.
 H.S.RAIZ=Path(out)/'snapshot'
 results=[];raw=[]
 for group in ['obs','sim']:
  m,v,r=H.executar_grupo(base,H.VERDADE,seeds(b,group),'cobertura_'+group,-1,b);results.append((m,v));raw.extend(r)
 (z,vo),(f,vs)=results;I=H.indice(z,vo,f,vs);row=dict(replica=b,I_max=float(max(I)),excluido=bool(max(I)>3))
 for j,o in enumerate(H.OBS):row.update({f'z_{o}':float(z[j]),f'f_{o}':float(f[j]),f'V_obs_{o}':float(vo[j]),f'V_sim_{o}':float(vs[j]),f'I_{o}':float(I[j])})
 return row,raw

def main():
 ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);a=ap.parse_args();base=a.base.resolve();out=base/'cobertura_pareada';out.mkdir(exist_ok=False);start=time.monotonic()
 assert (base/'resumo_execucao.json').exists(),'Concluir e preservar lote inicial antes do complemento'
 prior=json.loads((base/'desenho.json').read_text())
 for rel,sha in prior['hashes'].items():assert H.hashfile(H.ROOT/rel)==sha,rel
 files=[H.ROOT/rel for rel in prior['hashes']]+[Path(__file__),H.ROOT/'projeto/81A_COBERTURA_PAREADA_PRE_REGISTRO.md',H.ROOT/'research/test_cobertura_pareada_v3.py',H.ROOT/'data/processed/psplib/tarefas_j60_com_di.csv',H.ROOT/'data/processed/psplib/instancias_j60.csv']
 hashes={str(p.relative_to(H.ROOT)):H.hashfile(p) for p in files}
 hist=json.loads((H.ROOT/'outputs/diagnosticos/20260922_discriminante_falha/manifesto_pre_execucao.json').read_text())['hashes']
 for rel in ['data/processed/psplib/tarefas_j60_com_di.csv','data/processed/psplib/instancias_j60.csv']:assert hashes[rel]==hist[rel]
 for p in files:
  dst=out/'snapshot'/p.relative_to(H.ROOT);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
 H.save_json(out/'manifesto.json',dict(hashes=hashes,desenho='pareamento interinstâncias idêntico ao HM',B=500,semente_base=20000000,dados_iguais_manifesto78=True))
 with ProcessPoolExecutor(4) as pool:cov=H.collect(pool,job,[(str(base),str(out),b) for b in range(500)],out,'cobertura')
 n=len(cov);k=int(cov.excluido.sum());q=norm.ppf(.975);p=k/n;den=1+q*q/n;mid=(p+q*q/(2*n))/den;half=q*np.sqrt(p*(1-p)/n+q*q/(4*n*n))/den
 for rel,sha in hashes.items():assert H.hashfile(H.ROOT/rel)==sha,rel
 H.save_json(out/'resumo_execucao.json',dict(B=n,exclusoes=k,taxa=p,IC95_Wilson=[mid-half,mid+half],p95_Imax=float(cov.I_max.quantile(.95)),segundos_total=time.monotonic()-start,hashes_finais_iguais=True))
 print(json.loads((out/'resumo_execucao.json').read_text()),flush=True)
if __name__=='__main__':main()
