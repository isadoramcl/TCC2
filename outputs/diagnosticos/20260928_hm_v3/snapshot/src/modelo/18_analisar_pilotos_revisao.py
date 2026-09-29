"""Analisa os pilotos preservados; inferência condicional às instâncias fixas."""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

sp=importlib.util.spec_from_file_location('pilotos',Path(__file__).with_name('17_pilotos_revisao.py'))
pilotos=importlib.util.module_from_spec(sp); sp.loader.exec_module(pilotos)
hm=pilotos.hm


def intervalo_pareado(x):
    x=np.asarray(x); m=float(x.mean()); se=float(stats.sem(x))
    half=float(stats.t.ppf(.975,len(x)-1)*se)
    return dict(media=m,IC95_min=m-half,IC95_max=m+half,n_sementes=len(x))


def main():
    p=argparse.ArgumentParser(); p.add_argument('--entrada',type=Path,required=True)
    p.add_argument('--saida',type=Path,required=True); args=p.parse_args()
    inp,out=args.entrada,args.saida; out.mkdir(parents=True,exist_ok=False)
    product=pd.read_csv(inp/'produto/bruto.csv')
    contrasts=[]
    for o in hm.OBSERVAVEIS:
        a=product[product.grupo=='F=0.12'].groupby('semente')[o].mean()
        b=product[product.grupo=='F=0.24'].groupby('semente')[o].mean()
        contrasts.append(dict(observavel=o,**intervalo_pareado(b-a)))
    pd.DataFrame(contrasts).to_csv(out/'produto_contrastes.csv',index=False)
    truth=pilotos.estatisticas(product[product.grupo=='F=0.18'])
    original_z=pd.read_csv(hm.TAB/'modelo_04_observacoes_sinteticas.csv').iloc[0]
    truth_rows=[]
    for o in hm.OBSERVAVEIS:
        den=np.sqrt(truth['var_legado_'+o]+original_z['var_media_'+o])
        truth_rows.append(dict(observavel=o,media_verdade=truth['media_'+o],
                               observacao=original_z['media_'+o],I=abs(truth['media_'+o]-original_z['media_'+o])/den))
    pd.DataFrame(truth_rows).to_csv(out/'verdade_K64.csv',index=False)
    trust=pd.read_csv(inp/'confianca/bruto.csv'); trust=trust[~trust.grupo.str.startswith('controle=')]
    terms=[]
    for o in hm.OBSERVAVEIS+['TL','TU','TW','TR']:
        cells=trust.groupby(['grupo','semente'])[o].mean().unstack(0)
        a=cells['gate=0.25;rede=0.25']; b=cells['gate=0.8;rede=0.25']
        c=cells['gate=0.25;rede=0.8']; d=cells['gate=0.8;rede=0.8']
        for name,x in [('portao',b-a),('rede',c-a),('interacao',d-b-c+a),('total',d-a)]:
            terms.append(dict(observavel=o,termo=name,**intervalo_pareado(x)))
        assert np.allclose((b-a)+(c-a)+(d-b-c+a),d-a)
    pd.DataFrame(terms).to_csv(out/'confianca_decomposicao.csv',index=False)
    trust.groupby('grupo')[hm.OBSERVAVEIS+['TL','TU','TW','TR']].mean().to_csv(out/'confianca_celulas.csv')
    noise=pd.read_csv(inp/'ruido/bruto.csv'); zr=pd.read_csv(hm.TAB/'modelo_04_observacoes_sinteticas.csv').iloc[0]
    results=[]
    for group,g in noise.groupby('grupo'):
        for k in [4,32]:
            sub=g[g.semente<k]; summary=pilotos.estatisticas(sub)
            for method in ['legado','pareada']:
                vals=[]
                for o in hm.OBSERVAVEIS:
                    I=abs(summary['media_'+o]-zr['media_'+o])/np.sqrt(summary[f'var_{method}_{o}']+zr['var_media_'+o])
                    vals.append(I)
                    results.append(dict(ponto=group,K=k,metodo=method,observavel=o,media=summary['media_'+o],
                                        Vsim=summary[f'var_{method}_{o}'],I=I))
                results.append(dict(ponto=group,K=k,metodo=method,observavel='maximo',I=max(vals)))
    pd.DataFrame(results).to_csv(out/'ruido_comparacao.csv',index=False)
    coverage=pd.read_csv(inp/'cobertura/bruto.csv'); details=[]
    for b in range(20):
        sim=pilotos.estatisticas(coverage[coverage.grupo==f'sim={b}'])
        obs=pilotos.estatisticas(coverage[coverage.grupo==f'obs={b}'])
        for target in ['publicada','renovada']:
            for method in ['legado','pareada']:
                vals=[]
                for o in hm.OBSERVAVEIS:
                    mean=zr['media_'+o] if target=='publicada' else obs['media_'+o]
                    var=zr['var_media_'+o] if target=='publicada' else obs[f'var_{method}_{o}']
                    den=np.sqrt(sim[f'var_{method}_{o}']+var)
                    delta=abs(sim['media_'+o]-mean)
                    I=delta/den if den>0 else (0 if delta==0 else np.inf)
                    vals.append(I)
                    details.append(dict(bloco=b,observacao=target,metodo=method,observavel=o,I=I,exclui=I>hm.CORTE))
                details.append(dict(bloco=b,observacao=target,metodo=method,observavel='maximo',I=max(vals),exclui=max(vals)>hm.CORTE))
    det=pd.DataFrame(details); det.to_csv(out/'cobertura_blocos.csv',index=False)
    cov=[]
    for keys,g in det.groupby(['observacao','metodo','observavel']):
        x=int(g.exclui.sum()); n=len(g)
        ci=stats.binomtest(x,n).proportion_ci(confidence_level=.95,method='exact')
        cov.append(dict(observacao=keys[0],metodo=keys[1],observavel=keys[2],exclusoes=x,n=n,taxa=x/n,IC95_min=ci.low,IC95_max=ci.high))
    pd.DataFrame(cov).to_csv(out/'cobertura_resumo.csv',index=False)
    checks={folder:json.loads((inp/folder/'verificacoes.json').read_text()) for folder in ['produto','ruido','cobertura','confianca','vertices']}
    (out/'verificacoes_consolidadas.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(pd.DataFrame(contrasts).to_string(index=False))
    print(pd.DataFrame(terms).query("observavel in ['atraso_relativo','E_total','TU']").to_string(index=False))
    print(pd.DataFrame(cov).query("observavel=='maximo'").to_string(index=False))


if __name__=='__main__': main()
