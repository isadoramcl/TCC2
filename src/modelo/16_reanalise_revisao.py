"""Reanálise determinística do parecer; sem novas simulações nem outputs legados alterados."""
import argparse
import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

spec = importlib.util.spec_from_file_location('hm', Path(__file__).with_name('04_gemeo_identico.py'))
hm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hm)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--saida', type=Path, required=True)
    out = p.parse_args().saida
    out.mkdir(parents=True, exist_ok=False)
    a = pd.read_csv(hm.TAB/'modelo_04_hm_onda1.csv')
    z = pd.read_csv(hm.TAB/'modelo_04_observacoes_sinteticas.csv').iloc[0]
    cols = ['media_'+o for o in hm.OBSERVAVEIS]
    a[hm.NOMES+cols].corr().loc[hm.NOMES,cols].to_csv(out/'correlacoes.csv')
    X = a[hm.NOMES].to_numpy()
    product = X[:,0]*X[:,1]
    fits = []
    for name, mat in [('cinco_parametros',X),('produto_e_tres_parametros',np.column_stack([product,X[:,2:]]))]:
        mat = np.column_stack([np.ones(len(a)), mat])
        for o in cols:
            y = a[o].to_numpy(); coef = np.linalg.lstsq(mat,y,rcond=None)[0]
            fits.append(dict(modelo=name,observavel=o,R2=1-np.sum((y-mat@coef)**2)/np.sum((y-y.mean())**2)))
    pd.DataFrame(fits).to_csv(out/'r2_descritivo.csv',index=False)
    rows=[]
    for fs,fo,name in [(1,1,'legado'),(1/8,1,'so_Vsim_div8'),(1,1/8,'so_Vobs_div8'),(1/8,1/8,'ambas_div8')]:
        I=np.column_stack([abs(a['media_'+o]-z['media_'+o])/np.sqrt(fs*a['var_media_'+o]+fo*z['var_media_'+o]) for o in hm.OBSERVAVEIS])
        if name=='legado':
            assert np.allclose(I.max(axis=1),a.implausibilidade)
            pd.DataFrame({'observavel':hm.OBSERVAVEIS,'maximo_em_pontos':np.bincount(I.argmax(axis=1),minlength=4),
                          'aceitos_isoladamente':(I<=hm.CORTE).sum(axis=0),'I_mediano':np.median(I,axis=0)}).to_csv(out/'componentes_I.csv',index=False)
        n=a[I.max(axis=1)<=hm.CORTE]
        for sec,key,lo,hi in hm.PARAMETROS:
            col=sec+'.'+key
            rows.append(dict(alternativa=name,nroy=len(n),parametro=col,reducao=1-(n[col].max()-n[col].min())/(hi-lo)))
    pd.DataFrame(rows).to_csv(out/'sensibilidade_denominador.csv',index=False)
    boxes=[]
    prior=np.array([(lo,hi) for _,_,lo,hi in hm.PARAMETROS]); sample=prior.copy()
    for wave in ['onda1','onda2']:
        d=pd.read_csv(hm.TAB/f'modelo_04_hm_{wave}.csv'); n=d[d.implausibilidade<=hm.CORTE]
        box=np.array([(n[c].min(),n[c].max()) for c in hm.NOMES])
        boxes.append(dict(onda=wave,nroy=len(n),pontos=len(d),fracao_condicional=len(n)/len(d),
                          volume_caixa_amostrada_sobre_prior=np.prod(np.diff(sample).ravel()/np.diff(prior).ravel()),
                          volume_caixa_nroy_sobre_prior=np.prod(np.diff(box).ravel()/np.diff(prior).ravel())))
        sample=box
    pd.DataFrame(boxes).to_csv(out/'caixas.csv',index=False)
    b=pd.read_csv(hm.TAB/'modelo_04_hm_onda2.csv')
    na=a[a.implausibilidade<=hm.CORTE]; nb=b[b.implausibilidade<=hm.CORTE]
    sa=set(na.ponto);sb=set(nb.ponto)
    pd.DataFrame([dict(jaccard_indices=len(sa&sb)/len(sa|sb),
                       vetores_fisicos_comuns=len(na.merge(nb,on=hm.NOMES)))
                  ]).to_csv(out/'jaccard.csv',index=False)
    pilot=pd.read_csv(hm.RAIZ/'outputs/diagnosticos/hm_20260915/piloto_bruto.csv')
    decomposition=[]
    for (design,point),d in pilot.groupby(['desenho','ponto']):
        for o in hm.OBSERVAVEIS:
            means=d.groupby('instancia')[o].mean();counts=d.groupby('instancia')[o].size()
            sst=((d[o]-d[o].mean())**2).sum()
            ssb=(counts*(means-d[o].mean())**2).sum()
            iid=d[o].var(ddof=1)/len(d); cluster=means.var(ddof=1)/len(means)
            decomposition.append(dict(desenho=design,ponto=point,observavel=o,
                                      fracao_entre=ssb/sst,razao_cluster_iid=cluster/iid))
    pd.DataFrame(decomposition).to_csv(out/'decomposicao_variancia_legada.csv',index=False)
    print(pd.DataFrame(rows).pivot(index='alternativa',columns='parametro',values='reducao').to_string())


if __name__=='__main__': main()
