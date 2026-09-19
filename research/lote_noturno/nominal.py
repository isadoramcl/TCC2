"""Nominal histórico congelado por execução antes de alterar alternativas."""
import csv,json,sys,hashlib
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
import pandas as pd
import yaml
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP

def job(args):
    arquivo,seed,cen=args;g,d,c=S.carregar_instancia(arquivo)
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
    s=SimulacaoMVP(g,d,c,S.carregar_parametros(),cen,seed,opcoes=OpcoesMVP(**op));r=s.executar()
    ids=dict(arquivo=arquivo,semente=seed,cenario=cen)
    row={**ids,**{k:v for k,v in asdict(r).items() if k not in ['trajetorias','contadores','violacoes']},**r.contadores}
    row['retrabalho_sobre_esforco_total']=r.TR/(r.E_plano+r.TR)
    traj=[{**ids,**{k:v[i] for k,v in r.trajetorias.items() if k!='uso_recursos'}} for i in range(len(r.trajetorias['t']))]
    regs=[{**ids,**x} for x in s.registros_tarefas]
    return row,traj,regs
if __name__=='__main__':
    out=ROOT/'outputs/diagnosticos/noturno_nominal';out.mkdir(exist_ok=False)
    nomes=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::30][:16]
    jobs=[(a,s,c) for a in nomes for s in range(12) for c in ['centralizada','adaptativa']]
    files=[ROOT/'src/modelo'/f for f in ['simulador.py','simulador_mvp.py','fuzzy.py']]+[ROOT/'config/mvp.yaml',ROOT/'config/parametros.yaml']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (out/'manifesto.json').write_text(json.dumps(dict(N=len(jobs),instancias=nomes,seeds=list(range(12)),hashes=hashes),indent=2)+'\n')
    with (out/'bruto.csv').open('w') as f,(out/'trajetorias.csv').open('w') as g,(out/'tarefas.csv').open('w') as h,ProcessPoolExecutor(max_workers=2) as pool:
        writers=None
        for n,(r,tr,regs) in enumerate(pool.map(job,jobs)):
            if writers is None:
                writers=[csv.DictWriter(file,fieldnames=list(row),lineterminator='\n') for file,row in [(f,r),(g,tr[0]),(h,regs[0])]]
                for w in writers:w.writeheader()
            writers[0].writerow(r);writers[1].writerows(tr);writers[2].writerows(regs)
            for file in [f,g,h]:file.flush()
            if (n+1)%48==0:print(n+1,flush=True)
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print('384 completas; hashes conferidos',flush=True)
