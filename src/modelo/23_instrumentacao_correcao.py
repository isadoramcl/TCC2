"""Amostra declarada de decisões; descrição condicional, não teste causal."""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import pandas as pd
import yaml
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);args=ap.parse_args()
    args.saida.mkdir(parents=True,exist_ok=False)
    todas=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())
    inst=todas[::len(todas)//16][:4]
    op=yaml.safe_load((ROOT/'config/mvp_v1.yaml').read_text())['opcoes']
    fontes=['src/modelo/simulador_mvp.py','src/modelo/simulador.py','src/modelo/fuzzy.py',
            'src/modelo/23_instrumentacao_correcao.py','config/mvp_v1.yaml','config/parametros.yaml',
            'config/parametros_derivados.yaml','data/processed/psplib/tarefas_j60_com_di.csv',
            'data/processed/psplib/instancias_j60.csv']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in fontes}
    (args.saida/'manifesto.json').write_text(json.dumps(dict(instancias=inst,sementes=list(range(4)),
        opcoes=op,hashes=hashes,denominador='oportunidades de decisão sobre tarefa elegível com recurso'),indent=2)+'\n')
    rows=[];execs=[]
    for arquivo in inst:
        g,disp,cpm=S.carregar_instancia(arquivo)
        for seed in range(4):
            for cen in ['centralizada','adaptativa']:
                sim=SimulacaoMVP(g,disp,cpm,S.carregar_parametros(),cen,seed,opcoes=OpcoesMVP(**op))
                r=sim.executar()
                rows.extend(dict(arquivo=arquivo,semente=seed,cenario=cen,**e) for e in sim.registros_tarefas)
                execs.append(dict(arquivo=arquivo,semente=seed,cenario=cen,concluiu=r.concluiu,
                    retrabalho_sobre_esforco_total=r.retrabalho_sobre_esforco_total,taxa_falha_efetiva=r.taxa_falha_efetiva,violacoes=len(r.violacoes),**{k:r.contadores[k] for k in ['N_req','N_fail','N_blocked','N_success']}))
    d=pd.DataFrame(rows)
    d.to_csv(args.saida/'tarefas.csv.gz',index=False,compression={'method':'gzip','mtime':0})
    pd.DataFrame(execs).to_csv(args.saida/'execucoes.csv',index=False)
    for c in ['Di','P','B']:
        d[c+'_faixa']=pd.cut(d[c],[-float('inf'),.25,.50,.75,float('inf')],labels=['ate_025','025_050','050_075','acima_075'])
    d.groupby(['cenario','Di_faixa','P_faixa','B_faixa'],observed=True).agg(
        oportunidades=('selecionou_p1','size'),p1=('selecionou_p1','sum'),
        probabilidade_media=('p_heu','mean'),q_medio=('q','mean')).assign(
        frequencia_p1=lambda x:x.p1/x.oportunidades).to_csv(args.saida/'selecao_condicional.csv')
    selecao=[]
    for cen,g in d.groupby('cenario'):
        p1=g[g.selecionou_p1]
        selecao.append(dict(cenario=cen,n=len(g),n_P1=len(p1),q_medio=g.q.mean(),
            q_condicional_P1=p1.q.mean(),taxa_P1=len(p1)/len(g),
            nota='seleção por p_heu; não comparar médias de duração/erro por porta como efeito causal'))
    pd.DataFrame(selecao).to_csv(args.saida/'selecao_q.csv',index=False)
    assert hashes=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in fontes}
    print(f'{len(execs)} execuções, {len(d)} oportunidades registradas')
if __name__=='__main__':main()
