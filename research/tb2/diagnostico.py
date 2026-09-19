"""Horizonte dobrado nas incompletas e contrastes condicionais pareados."""
import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import yaml
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/modelo'))
sys.path.insert(0,str(ROOT/'research/lote41'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from t4 import ic,METRICAS
from b2 import fracao_p1
FONTE=ROOT/'outputs/diagnosticos/lote41_B2_censura_20260918/bruto.csv'
CH=['etapa','canal','tau_sat','s_transicao','cenario','arquivo','semente']


def pares_completos(g,met):
    p=g.pivot(index=['arquivo','semente'],columns='cenario',values=met)
    ok=g.pivot(index=['arquivo','semente'],columns='cenario',values='concluiu')
    mask=ok.centralizada.eq(True)&ok.adaptativa.eq(True)
    delta=p.loc[mask,'adaptativa']-p.loc[mask,'centralizada']
    assert delta.notna().all()
    return delta,int(len(p)),int((~mask).sum())


def tabular(d,out,sufixo):
    grade=d[d.etapa=='grade']; assert len(grade)==576
    partes=[]
    for var in ['cenario','canal','tau_sat','s_transicao']:
        for val,g in grade.groupby(var):partes.append(dict(parametro=var,valor=str(val),N_grade=576,N_grupo=len(g),incompletas=int((~g.concluiu).sum()),fracao_incompleta=float((~g.concluiu).mean())))
    pd.DataFrame(partes).to_csv(out/f'marginais_{sufixo}.csv',index=False)
    grade.groupby(['cenario','canal','tau_sat','s_transicao']).agg(N=('concluiu','size'),completas=('concluiu','sum')).reset_index().assign(N_grade=576).to_csv(out/f'cruzamento_{sufixo}.csv',index=False)
    cs=[];ret=[];arm=[]
    for chave,g in d.groupby(['etapa','canal','tau_sat','s_transicao']):
        base=dict(zip(['etapa','canal','tau_sat','s_transicao'],chave))
        for met in METRICAS:
            delta,N,excl=pares_completos(g,met)
            por=delta.groupby('arquivo').mean()
            cs.append(dict(**base,metrica=met,N_pares_previstos=N,N_pares_retidos=len(delta),N_pares_excluidos=excl,**ic(por)))
            for (arq,sem),val in delta.items():ret.append(dict(**base,metrica=met,arquivo=arq,semente=sem,diferenca=val))
            for cen,h in g.groupby('cenario'):
                completo=h[h.concluiu]
                arm.append(dict(**base,metrica=met,cenario=cen,N_total=len(h),N_completas=len(completo),media_marginal_completas=float(completo[met].mean())))
    pd.DataFrame(cs).to_csv(out/f'contrastes_pares_completos_{sufixo}.csv',index=False)
    pd.DataFrame(ret).to_csv(out/f'pares_retidos_{sufixo}.csv',index=False)
    pd.DataFrame(arm).to_csv(out/f'medias_marginais_completas_{sufixo}.csv',index=False)


def job(row):
    p=S.carregar_parametros();p['agentes']['tau_sat']['valor']=row['tau_sat'];p['agentes']['s_transicao']['valor']=row['s_transicao']
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];assert op['limite_horizonte_fator']==256
    op.update(limite_horizonte_fator=512,canal_erro_direto=row['canal'],instrumentar_tarefas=False)
    g,disp,cpm=S.carregar_instancia(row['arquivo']);s=SimulacaoMVP(g,disp,cpm,p,row['cenario'],int(row['semente']),opcoes=OpcoesMVP(**op));r=s.executar()
    n=r.contadores['p1_omissao']+r.contadores['p3_analitica']
    pronto=s.elegiveis(r.makespan,[0]*len(disp)) if all(a.tarefa_atual is None for a in s.agentes) else []
    return {**{k:row[k] for k in CH},'atraso_relativo':r.makespan/r.makespan_cpm,'taxa_omissao':r.taxa_omissao,'divida_latente_sobre_plano':r.divida_latente_sobre_plano,'taxa_falha_efetiva':r.taxa_falha_efetiva,'fracao_porta1':fracao_p1(r.contadores['p1_omissao'],r.contadores['p3_analitica']),
        'n_executadas':n,'N_req':r.contadores['N_req'],'N_blocked':r.contadores['N_blocked'],'motivo_termino':r.contadores['motivo_termino'],'TW':r.TW,'TL':r.TL,'TU':r.TU,'TR':r.TR,'concluiu':r.concluiu,'violacoes':len(r.violacoes),
        'CPM':r.makespan_cpm,'makespan':r.makespan,'cap_fator':512,'n_executadas_antes':row['n_executadas'],'concluiu_antes':row['concluiu'],
        'agentes_ocupados_final':sum(a.tarefa_atual is not None for a in s.agentes),'prontas_final':json.dumps(pronto),'competencia_max_final':max(a.competencia for a in s.agentes)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);args=ap.parse_args();out=args.saida;out.mkdir(parents=True,exist_ok=False)
    d=pd.read_csv(FONTE);assert len(d)==1344 and len(d[d.etapa=='nominal'])==768
    faltam=d[~d.concluiu];assert len(faltam)==36 and not faltam.duplicated(CH).any() and faltam.etapa.eq('grade').all()
    faltam.to_csv(out/'selecionadas_36.csv',index=False);tabular(d,out,'h256')
    files=[Path(__file__),Path(__file__).with_name('PROTOCOLO.md'),FONTE,ROOT/'src/modelo/simulador_mvp.py',ROOT/'src/modelo/simulador.py',ROOT/'src/modelo/fuzzy.py']+list((ROOT/'config').glob('*.yaml'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (out/'manifesto.json').write_text(json.dumps(dict(N_grade=576,N_nominal=768,N_reexecutar=36,horizonte_antes=256,horizonte_depois=512,hashes=hashes),indent=2)+'\n')
    rows=[]
    with (out/'horizonte_dobrado_36.csv').open('w') as f, ProcessPoolExecutor(max_workers=4) as pool:
        writer=None
        for i,row in enumerate(pool.map(job,faltam.to_dict('records'),chunksize=1)):
            if writer is None:writer=csv.DictWriter(f,fieldnames=list(row),lineterminator='\n');writer.writeheader()
            writer.writerow(row);f.flush();rows.append(row);print(f'{i+1}/36; completou={row["concluiu"]}; tarefas={row["n_executadas"]}',flush=True)
    novo=pd.DataFrame(rows);assert not novo.violacoes.any()
    atualizado=d.set_index(CH).copy();n=novo.set_index(CH)
    assert set(n.index)==set(faltam.set_index(CH).index)
    for col in d.columns.difference(CH):atualizado.loc[n.index,col]=n[col]
    pd.testing.assert_frame_equal(atualizado.loc[d[d.concluiu].set_index(CH).index],d[d.concluiu].set_index(CH))
    atualizado=atualizado.reset_index();atualizado.to_csv(out/'grade_e_nominal_substituicao_36.csv',index=False);tabular(atualizado,out,'h512_seletivo')
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (out/'verificacoes.json').write_text(json.dumps(dict(reexecutadas=36,completaram=int(novo.concluiu.sum()),incompletas=int((~novo.concluiu).sum()),violacoes=0,linhas_completas_anteriores='inalteradas',nenhum_parametro_alem_horizonte_alterado=True),indent=2)+'\n')
if __name__=='__main__':main()
