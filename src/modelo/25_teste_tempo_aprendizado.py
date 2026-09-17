"""Experimento pareado de TL: duas convenções, sem seleção de uma vencedora."""
import argparse,copy,hashlib,json,platform
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
import yaml
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'outputs/diagnosticos/correcao_estrutural_20260916/alternativas'

def bits(x):
    if isinstance(x,float):return x.hex()
    if isinstance(x,dict):return {k:bits(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [bits(v) for v in x]
    return x

def job(chave):
    arquivo,seed,cen=chave
    g,disp,cpm=S.carregar_instancia(arquivo)
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
    sims=[];res=[];rows=[]
    for lei in ['unitario','crowder_eq3']:
        s=SimulacaoMVP(g,disp,cpm,S.carregar_parametros(),cen,seed,
            opcoes=OpcoesMVP(**{**op,'lei_tempo_aprendizado':lei}))
        r=s.executar();d=asdict(r);sims.append(s);res.append(d)
        rows.append(dict(arquivo=arquivo,semente=seed,cenario=cen,lei=lei,
            **{k:v for k,v in d.items() if isinstance(v,(int,float,bool))},
            N_req=s.cnt['N_req'],N_success=s.cnt['N_success'],N_fail=s.cnt['N_fail'],
            N_blocked=s.cnt['N_blocked'],violacoes=len(r.violacoes)))
    assert bits({k:v for k,v in res[0].items() if k not in ['TL','E_total','retrabalho_sobre_esforco_realizado']})==bits({k:v for k,v in res[1].items() if k not in ['TL','E_total','retrabalho_sobre_esforco_realizado']}),chave
    a,b=sims
    assert a.rng.bit_generator.state==b.rng.bit_generator.state,chave
    for attr in ['eventos','registros_tarefas','divida_pendente','reparos']:
        assert bits(getattr(a,attr))==bits(getattr(b,attr)),(chave,attr)
    for attr in ['agentes','tarefas']:
        x=getattr(a,attr);y=getattr(b,attr)
        if isinstance(x,dict):x=list(x.values());y=list(y.values())
        assert bits([vars(k) for k in x])==bits([vars(k) for k in y]),(chave,attr)
    tl=sum((.5*e['dC'] if e['sucesso'] else .05 for e in b.eventos if e['tipo']=='comunicacao'),0.)
    assert tl.hex()==b.TL.hex()
    return rows

def intervalo(x):
    n=len(x);m=x.mean();h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n)
    return dict(media=float(m),ic95_inf=float(m-h),ic95_sup=float(m+h),n_instancias=n)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True)
    ap.add_argument('--workers',type=int,default=4);a=ap.parse_args()
    if not 1<=a.workers<=4:ap.error('workers entre 1 e 4')
    out=a.saida;out.mkdir(parents=True,exist_ok=False)
    antigo=pd.read_csv(BASE/'bruto.csv');nom=antigo[antigo.configuracao=='MVP_corrigido']
    keys=['arquivo','semente','cenario'];jobs=list(nom[keys].itertuples(index=False,name=None))
    arquivos=[ROOT/'src/modelo'/f for f in ['simulador.py','simulador_mvp.py','fuzzy.py','25_teste_tempo_aprendizado.py']]+[ROOT/'config'/f for f in ['mvp.yaml','parametros.yaml','parametros_derivados.yaml']]+[BASE/'bruto.csv',BASE/'manifesto.json',ROOT/'data/processed/psplib/tarefas_j60_com_di.csv',ROOT/'data/processed/psplib/instancias_j60.csv']
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    hashes={str(p.relative_to(ROOT)):sha(p) for p in arquivos}
    (out/'manifesto.json').write_text(json.dumps(dict(baseline='1fd22ff',leis=['unitario','crowder_eq3'],
        n_execucoes=2*len(jobs),chaves=jobs,opcoes=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'],hashes=hashes,
        unidade_IC='instancia; sementes pareadas internas',python=platform.python_version()),indent=2)+'\n')
    rows=[]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for i,r in enumerate(pool.map(job,jobs,chunksize=4)):
            rows.extend(r)
            if (i+1)%64==0:print(f'{2*(i+1)}/{2*len(jobs)}',flush=True)
    d=pd.DataFrame(rows);d.to_csv(out/'bruto.csv',index=False)
    assert d.concluiu.all() and not d.violacoes.any()
    unit=d[d.lei=='unitario'].set_index(keys).sort_index();old=nom.set_index(keys).sort_index()
    assert unit.index.equals(old.index)
    comuns=[c for c in unit.select_dtypes(include=['number','bool']) if c in old and c!='violacoes']
    maxdif={c:float((unit[c].astype(float)-old[c].astype(float)).abs().max()) for c in comuns}
    assert max(maxdif.values())<1e-12,maxdif
    # Médias de razões individuais, não razão das médias dos componentes.
    means=d.groupby(['lei','arquivo','cenario'])[['E_total','TW','TL','TU','TR']].mean()
    rr=[];contrastes={}
    for lei in ['unitario','crowder_eq3']:
        p=means.loc[lei]['E_total'].unstack('cenario')
        delta=p.adaptativa-p.centralizada;contrastes[lei]=delta
        rr.append(dict(lei=lei,centralizada=p.centralizada.mean(),adaptativa=p.adaptativa.mean(),**intervalo(delta)))
    pd.DataFrame(rr).to_csv(out/'E_total_IC95.csv',index=False)
    mudanca=intervalo(contrastes['crowder_eq3']-contrastes['unitario'])
    pd.DataFrame([mudanca]).to_csv(out/'mudanca_contraste_IC95.csv',index=False)
    means.to_csv(out/'componentes_por_instancia.csv')
    d.groupby(['lei','cenario'])[['TW','TL','TU','TR','E_total']].mean().to_csv(out/'componentes_nominais.csv')
    ordem=[c['nome'] for c in json.loads((BASE/'manifesto.json').read_text())['configuracoes']]
    comp=antigo.groupby(['configuracao','cenario'])[['TW','TL','TU','TR','E_total']].mean().reset_index()
    comp['degrau']=comp.configuracao.map({c:i for i,c in enumerate(ordem)})
    comp.sort_values(['degrau','cenario']).to_csv(out/'componentes_escada.csv',index=False)
    assert hashes=={str(p.relative_to(ROOT)):sha(p) for p in arquivos}
    (out/'verificacoes.json').write_text(json.dumps(dict(exec=len(d),pares_estado_identico=len(jobs),
        incompletas=int((~d.concluiu).sum()),violacoes=int(d.violacoes.sum()),
        diferencas_nominal_unitario=maxdif,inverte_sinal=bool(contrastes['unitario'].mean()*contrastes['crowder_eq3'].mean()<0)),indent=2)+'\n')
    print(pd.DataFrame(rr).to_string(index=False),flush=True)
if __name__=='__main__':main()
