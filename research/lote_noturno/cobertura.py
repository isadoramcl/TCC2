"""D2: cobertura no vetor verdadeiro, sem ondas nem ajuste de V_mod."""
import argparse,csv,hashlib,json,sys,types
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
from scipy.stats import beta
ROOT=Path(__file__).resolve().parents[2]
OBS=['taxa_omissao','atraso_relativo','retrabalho_sobre_plano','E_total']
CACHE={}

def carregar(out):
    if 'S' in CACHE:return CACHE['S'],CACHE['par'],CACHE['inst']
    snap=Path(out)/'snapshot'
    # __file__ original mantém RAIZ e dados, mas os bytes executados são congelados.
    sys.path.insert(0,str(snap))
    fuzzy=types.ModuleType('fuzzy');fuzzy.__file__=str(ROOT/'src/modelo/fuzzy.py');sys.modules['fuzzy']=fuzzy
    exec(compile((snap/'fuzzy.py').read_text(),str(snap/'fuzzy.py'),'exec'),fuzzy.__dict__)
    mod=types.ModuleType('simulador_congelado_d2');mod.__file__=str(ROOT/'src/modelo/simulador.py');sys.modules[mod.__name__]=mod
    exec(compile((snap/'simulador.py').read_text(),str(snap/'simulador.py'),'exec'),mod.__dict__)
    conf=json.loads((snap/'desenho.json').read_text());CACHE.update(S=mod,par=conf['par'],inst=conf['instancias'])
    return mod,conf['par'],conf['instancias']

def estatistica(blocos):
    x=np.array(blocos);return x.mean(axis=0),x.var(axis=0,ddof=1)/len(x)

def job(args):
    b,out=args;S,par,inst=carregar(out);grupos=[];raw=[];incompletas=0
    for grupo,n,offset in [('obs',10,0),('sim',4,20)]:
        blocos=[]
        for bloco in range(n):
            vals=[]
            for i,arquivo in enumerate(inst):
                seed=10_000_000+b*28+offset+bloco*2+i
                if arquivo not in CACHE:CACHE[arquivo]=S.carregar_instancia(arquivo)
                g,disp,cpm=CACHE[arquivo];r=S.Simulacao(g,disp,cpm,par,'adaptativa',semente=seed).executar()
                v=[r.taxa_omissao,r.makespan/r.makespan_cpm,r.retrabalho_sobre_plano,r.E_total];vals.append(v);incompletas+=int(not r.concluiu)
                raw.append(dict(replica=b,grupo=grupo,bloco=bloco,arquivo=arquivo,semente=seed,concluiu=r.concluiu,**dict(zip(OBS,v))))
            blocos.append(np.mean(vals,axis=0))
        grupos.append(estatistica(blocos))
    (z,vo),(f,vs)=grupos;den=np.sqrt(vo+vs)
    I=np.divide(abs(z-f),den,out=np.where(abs(z-f)==0,0.,np.inf),where=den>0)
    res=dict(replica=b,I_max=float(max(I)),excluido=bool(max(I)>3),incompletas=incompletas)
    for j,o in enumerate(OBS):res.update({f'z_{o}':z[j],f'f_{o}':f[j],f'V_obs_{o}':vo[j],f'V_sim_{o}':vs[j],f'I_{o}':I[j]})
    return res,raw

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);args=ap.parse_args();out=args.saida.resolve();out.mkdir(parents=True,exist_ok=True);snap=out/'snapshot';snap.mkdir(exist_ok=False)
    import shutil
    for nome in ['simulador.py','fuzzy.py']:shutil.copyfile(ROOT/'src/modelo'/nome,snap/nome)
    sys.path.insert(0,str(ROOT/'src/modelo'));import simulador as S
    par=S.carregar_parametros()
    for sec,nome,val in [('risco','F_ancora',.18),('retrabalho','f_retrabalho',.42),('agentes','tau_sat',.85),('agentes','k_heuristico',.135),('fuzzy','mu_minimo',.62)]:par[sec][nome]['valor']=val
    todas=sorted(pd.read_csv(ROOT/'data/processed/psplib/tarefas_j60_com_di.csv').arquivo.unique());inst=todas[::len(todas)//2][:2]
    (snap/'desenho.json').write_text(json.dumps(dict(par=par,instancias=inst,B=500,V_mod=0,n_blocos_obs=10,n_blocos_sim=4),indent=2)+'\n')
    sources=[Path(__file__),Path(__file__).with_name('PROTOCOLO_D2_D3.md'),*snap.glob('*')]
    (out/'manifesto.json').write_text(json.dumps(dict(B=500,hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}),indent=2)+'\n')
    rows=[]
    with (out/'replicas.csv').open('w') as f,(out/'execucoes.csv').open('w') as g,ProcessPoolExecutor(max_workers=2) as pool:
        w=v=None
        for n,(r,raw) in enumerate(pool.map(job,[(b,str(out)) for b in range(500)],chunksize=1)):
            if w is None:w=csv.DictWriter(f,fieldnames=list(r),lineterminator='\n');w.writeheader();v=csv.DictWriter(g,fieldnames=list(raw[0]),lineterminator='\n');v.writeheader()
            w.writerow(r);v.writerows(raw);f.flush();g.flush();rows.append(r)
            if (n+1)%25==0:print(f'{n+1}/500',flush=True)
    d=pd.DataFrame(rows);k=int(d.excluido.sum());B=len(d);lo=0. if k==0 else beta.ppf(.025,k,B-k+1);hi=1. if k==B else beta.ppf(.975,k+1,B-k)
    ver=dict(B=B,falsas_exclusoes=k,taxa=k/B,ic95_binomial=[lo,hi],p95_Imax=float(d.I_max.quantile(.95)),incompletas=int(d.incompletas.sum()),V_mod=0,usar_HM=False,status='DIAGNOSTICO_SOB_REVISAO' if k/B>.3 or d.incompletas.sum() else 'VERIFICACAO_INTERNA_CONCLUIDA')
    (out/'veredito.json').write_text(json.dumps(ver,indent=2)+'\n');print(json.dumps(ver),flush=True)
if __name__=='__main__':main()
