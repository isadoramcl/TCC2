"""Snapshot antes/depois: todos os campos antigos, estados e RNG em float.hex."""
import argparse,json,sys
from dataclasses import asdict
from pathlib import Path
import pandas as pd
import yaml
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src/modelo'),str(ROOT/'research')]
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from test_compatibilidade import bits,projetar

def capturar():
    out={};nom=[]
    nomes=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::120]
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
    for nome in nomes:
        g,d,c=S.carregar_instancia(nome)
        for cen in ['centralizada','adaptativa']:
            for seed in range(4):
                for motor in ['legado','mvp']:
                    args=(g,d,c,S.carregar_parametros(),cen,seed)
                    s=S.Simulacao(*args) if motor=='legado' else SimulacaoMVP(*args,opcoes=OpcoesMVP(**op))
                    r=s.executar();res=asdict(r)
                    snap=dict(resultado=res,rng=s.rng.bit_generator.state,agentes=[vars(a) for a in s.agentes],tarefas={k:vars(t) for k,t in s.tarefas.items()},divida=s.divida_pendente)
                    if motor=='mvp':snap.update(eventos=s.eventos,registros=s.registros_tarefas)
                    out[f'{nome}/{cen}/{seed}/{motor}']=bits(snap)
                    if motor=='mvp':nom.append(dict(arquivo=nome,cenario=cen,semente=seed,TR=r.TR,E_plano=r.E_plano,retrabalho_sobre_esforco_total=r.TR/(r.E_plano+r.TR)))
    return json.loads(json.dumps(out)),nom
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('modo',choices=['antes','depois']);args=ap.parse_args()
    out=ROOT/'outputs/diagnosticos/noturno_D1';out.mkdir(exist_ok=True)
    atual,nom=capturar()
    if args.modo=='antes':
        p=out/'antes.json';assert not p.exists();p.write_text(json.dumps(atual,separators=(',',':'))+'\n')
    else:
        antigo=json.loads((out/'antes.json').read_text());assert projetar(atual,antigo)==antigo
        for x in atual.values():
            r=x['resultado'];esperado=float.fromhex(r['TR'])/(float.fromhex(r['E_plano'])+float.fromhex(r['TR']))
            assert r['retrabalho_sobre_esforco_total']==esperado.hex()
        (out/'controle.json').write_text(json.dumps(dict(exec=len(atual),identidade_campos_preexistentes=True,estados_rng_identicos=True,residuo_maximo=0),indent=2)+'\n')
        pd.DataFrame(nom).to_csv(out/'amostra_nominal.csv',index=False)
        print('Identidade exata:',len(atual))
