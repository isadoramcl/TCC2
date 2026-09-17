"""Contrastes incrementais e verificações da correção; não seleciona parâmetros."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--entrada',type=Path,required=True);a=ap.parse_args()
    base=a.entrada.resolve();out=base/'correcao';out.mkdir(exist_ok=False)
    d=pd.read_csv(base/'alternativas/bruto.csv')
    ordem=[c['nome'] for c in json.loads((base/'alternativas/manifesto.json').read_text())['configuracoes']]
    keys=['arquivo','semente','cenario']
    metricas=[c for c in d.select_dtypes(include=['number','bool']).columns if c!='semente']
    rows=[]
    for antes,depois in zip(ordem,ordem[1:]):
        x=d[d.configuracao==antes].set_index(keys);y=d[d.configuracao==depois].set_index(keys)
        assert x.index.equals(y.index)
        for met in metricas:
            for cen in ['centralizada','adaptativa']:
                xx=x.xs(cen,level='cenario')[met].astype(float)
                yy=y.xs(cen,level='cenario')[met].astype(float)
                if xx.isna().any() or yy.isna().any():continue
                delta=(yy-xx).groupby('arquivo').mean();n=len(delta)
                meia=t.ppf(.975,n-1)*delta.std(ddof=1)/np.sqrt(n)
                rows.append(dict(ANTES_config=antes,DEPOIS_config=depois,cenario=cen,metrica=met,
                    ANTES=xx.mean(),DEPOIS=yy.mean(),delta=delta.mean(),
                    ic95_delta_inf=delta.mean()-meia,ic95_delta_sup=delta.mean()+meia,n_instancias=n))
    pd.DataFrame(rows).to_csv(out/'antes_depois_incremental.csv',index=False)
    old=pd.read_csv(ROOT/'outputs/diagnosticos/mvp_20260915/alternativas/bruto.csv')
    old=old[old.configuracao=='C4_C1'];new=d[d.configuracao=='MVP_corrigido']
    rows=[]
    for met in metricas:
        if met not in old:continue
        for cen in ['centralizada','adaptativa']:
            x=old[old.cenario==cen][met];y=new[new.cenario==cen][met]
            if x.isna().any() or y.isna().any():continue
            rows.append(dict(metrica=met,cenario=cen,ANTES_efd81b7=x.mean(),
                DEPOIS_corrigido=y.mean(),delta=y.mean()-x.mean()))
    pd.DataFrame(rows).to_csv(out/'antes_depois_MVP_pre_correcao.csv',index=False)
    robust=pd.read_csv(base/'robustez/resumo.csv');rr=[]
    for met,g in robust.groupby('metrica'):
        rr.append(dict(metrica=met,configuracoes=len(g),contraste_min=g.media_diferenca.min(),
            contraste_max=g.media_diferenca.max(),negativas=int((g.media_diferenca<0).sum()),
            positivas=int((g.media_diferenca>0).sum()),zero=int((g.media_diferenca==0).sum()),
            IC_inteiro_negativo=int((g.ic95_superior<0).sum()),
            IC_inteiro_positivo=int((g.ic95_inferior>0).sum()),
            pares_censurados=int(g.n_pares_censurados.sum())))
    pd.DataFrame(rr).to_csv(out/'sinais_robustez.csv',index=False)
    bruto_robusto=pd.read_csv(base/'robustez/bruto.csv')
    horizontes={}
    for rho in [.20,.35,.50]:
        sufixo=f'_rho{rho:.2f}' if rho!=.35 else ''
        x=bruto_robusto[bruto_robusto.configuracao=='p8_yaml_arredondado'+sufixo].set_index(keys).sort_index()
        y=bruto_robusto[bruto_robusto.configuracao=='centro_horizonte_dobrado'+sufixo].set_index(keys).sort_index()
        assert len(x)==len(y)==32 and x.index.equals(y.index)
        cols=[c for c in x if c not in ['configuracao','extensoes_horizonte']]
        divergentes=[c for c in cols if not x[c].equals(y[c])]
        assert not divergentes,(rho,divergentes)
        horizontes[str(rho)]=dict(pares=len(x),identico=True)

    canais=pd.read_csv(base/'canais_mvp/bruto.csv',dtype={'celula':str})
    canais.celula=canais.celula.str.zfill(5)
    diag=canais[canais.celula.isin(['00000','11111'])].copy()
    diag['cenario']=diag.celula.map({'00000':'centralizada','11111':'adaptativa'})
    join=new.merge(diag,on=keys,suffixes=('_nominal','_diagonal'),validate='one_to_one')
    assert len(join)==len(new)==384
    comuns=[m for m in metricas if m+'_diagonal' in join]
    dif={m:float((join[m+'_nominal'].astype(float)-join[m+'_diagonal'].astype(float)).abs().max()) for m in comuns}
    assert max(dif.values())<1e-8,dif
    frozen=json.loads((ROOT/'research/CONGELAMENTO_PRE_CORRECAO.json').read_text())['sha256']
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in frozen.items())
    log=pd.read_csv(base/'instrumentacao/tarefas.csv.gz')
    taxas=[]
    for cen,g in log.groupby('cenario'):
        execs=g[g.executada]
        taxas.append(dict(cenario=cen,oportunidades=len(g),execucoes=len(execs),
            taxa_P1_por_oportunidade=g.selecionou_p1.mean(),
            taxa_P1_entre_execucoes=(execs.porta=='P1_omissao').mean(),
            q_medio_oportunidades=g.q.mean(),q_condicional_P1=g[g.selecionou_p1].q.mean(),
            q_medio_execucoes=execs.q.mean(),
            q_condicional_P1_executada=execs[execs.porta=='P1_omissao'].q.mean()))
    pd.DataFrame(taxas).to_csv(out/'denominadores_selecao.csv',index=False)
    numeric=new.select_dtypes(include=['number','bool']).columns
    new.groupby('cenario')[list(numeric)].mean().to_csv(out/'nominal_corrigido.csv')
    (out/'verificacoes.json').write_text(json.dumps(dict(diagonais=len(join),diferencas=dif,
        arquivos_historicos_intactos=len(frozen),horizontes=horizontes),indent=2)+'\n')
    arquivos=sorted(p for p in base.rglob('*') if p.is_file())
    (out/'hashes.json').write_text(json.dumps({(str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in arquivos},indent=2)+'\n')
if __name__=='__main__':main()
