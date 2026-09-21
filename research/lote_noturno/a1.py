"""A1: malha pré-declarada, exportação incremental e denominadores explícitos."""
import csv,hashlib,json,sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from dataclasses import asdict
import numpy as np
import pandas as pd
import yaml
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
class Instrumentada(SimulacaoMVP):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw);self.hist_q=np.zeros(10,dtype=int)
    def deve_fugir(self,p_heu,omega,limite):
        q=max(0.,2*p_heu-1.);self.hist_q[min(9,int(q*10))]+=1
        return super().deve_fugir(p_heu,omega,limite)

def job(args):
    regra,lim,arquivo,seed,cen=args
    p=S.carregar_parametros();p['gestor']['limite_aversao_perda']['valor']=lim
    op=yaml.safe_load((ROOT/'config/mvp_v1.yaml').read_text())['opcoes'];op.update(regra_fuga=regra,instrumentar_tarefas=False)
    g,d,c=S.carregar_instancia(arquivo);s=Instrumentada(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op));r=s.executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(float,int,bool))};row.update(r.contadores)
    n=r.contadores['p1_fuga']+r.contadores['p1_omissao'];dec=n+r.contadores['p3_analitica']+r.contadores['hiato_encontrado']
    row.update(regra=regra,limite=lim,arquivo=arquivo,semente=seed,cenario=cen,violacoes=len(r.violacoes),n_selecoes_p1=n,n_decisoes=dec,fracao_fuga_p1=r.contadores['p1_fuga']/n if n else np.nan,fracao_fuga_decisoes=r.contadores['p1_fuga']/dec if dec else np.nan,atraso_relativo=r.makespan/r.makespan_cpm)
    row.update({f'q_bin{i}':int(n) for i,n in enumerate(s.hist_q)})
    assert sum(s.hist_q)==n
    return row

def analisar(d,out):
    rows=[]
    for key,g in d.groupby(['regra','limite','cenario']):
        rows.append(dict(zip(['regra','limite','cenario'],key),N=len(g),completas=int(g.concluiu.sum()),incompletas=int((~g.concluiu).sum()),p1_fuga_medio=g.p1_fuga.mean(),p1_omissao_medio=g.p1_omissao.mean(),fracao_fuga_p1_pool=g.p1_fuga.sum()/g.n_selecoes_p1.sum(),fracao_fuga_p1_media=g.fracao_fuga_p1.mean(),N_req_medio=g.N_req.mean(),tarefas_executadas_media=(g.p1_omissao+g.p3_analitica).mean()))
    pd.DataFrame(rows).to_csv(out/'resumo.csv',index=False)
    old=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/bruto.csv').set_index(['arquivo','semente','cenario'])
    baseline=d[(d.regra=='constante')&(d.limite==.6)].set_index(['arquivo','semente','cenario']);checks=[]
    for field in ['makespan','TW','TL','TU','TR','p1_fuga','p1_omissao','N_req']:
        delta=float((baseline[field]-old.loc[baseline.index,field]).abs().max());assert delta<1e-12;checks.append(dict(campo=field,residuo=delta))
    pd.DataFrame(checks).to_csv(out/'baseline.csv',index=False)
    # Mesmos estados/sorteios nominais em cada limiar, sem confundir com dinâmica.
    reg=pd.read_csv(ROOT/'outputs/diagnosticos/noturno_nominal/tarefas.csv');reg=reg[reg.selecionou_p1]
    rows=[]
    for cen,g in reg.groupby('cenario'):
        for lim in np.arange(61)/100:
            rows.append(dict(cenario=cen,limite=lim,N_estados=len(g),fracao_fuga_constante=float(.5>lim),fracao_fuga_estado=float((.5*g.q>lim).mean())))
    pd.DataFrame(rows).to_csv(out/'sensibilidade_local.csv',index=False)
    (out/'verificacoes.json').write_text(json.dumps(dict(N=len(d),violacoes=int(d.violacoes.sum()),baseline_passou=True,completas=int(d.concluiu.sum()),fuga_positiva=bool(d[d.regra=='dependente_estado'].p1_fuga.gt(0).any())),indent=2)+'\n')

if __name__=='__main__':
    out=ROOT/'outputs/diagnosticos/A1_20260919'
    cfg=yaml.safe_load((ROOT/'config/robustez_a1.yaml').read_text());names=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::120]
    jobs=[(r,l,a,s,c) for r in cfg['regras_fuga'] for l in cfg['limite_aversao_perda'] for a in names for s in cfg['sementes'] for c in ['centralizada','adaptativa']]
    files=[Path(__file__),Path(__file__).with_name('PROTOCOLO_A1.md'),ROOT/'src/modelo/simulador.py',ROOT/'src/modelo/simulador_mvp.py',ROOT/'src/modelo/fuzzy.py',*list((ROOT/'config').glob('*.yaml'))]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (out/'manifesto.json').write_text(json.dumps(dict(N=len(jobs),config=cfg,instancias=names,hashes=hashes),indent=2)+'\n')
    rows=[]
    with (out/'bruto.csv').open('w') as f,ProcessPoolExecutor(max_workers=4) as pool:
        w=None
        for i,row in enumerate(pool.map(job,jobs,chunksize=1)):
            if w is None:w=csv.DictWriter(f,fieldnames=list(row),lineterminator='\n');w.writeheader()
            w.writerow(row);f.flush();rows.append(row)
            if (i+1)%16==0:print(f'{i+1}/{len(jobs)}',flush=True)
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    d=pd.DataFrame(rows);assert not d.violacoes.any();analisar(d,out)
