"""Teste discriminante C3 e diagnóstico A-16; parâmetros nunca ajustados."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import betabinom, binom
ROOT=Path(__file__).resolve().parents[2]
PUBLICADO=np.array([67.475,18.334,5.639,1.765,.549])


def controles():
    mu=.0163;cv=1.13;sigma=cv*mu
    s_errado=mu*(1-mu)/sigma**2
    sigma_n5=cv*mu**2
    s_n5=mu*(1-mu)/sigma_n5**2-1
    k=np.arange(5)
    return {
        'candidata':94*betabinom.pmf(k,25,.7546,45.4563),
        'N1_sem_menos_um':94*betabinom.pmf(k,25,mu*s_errado,(1-mu)*s_errado),
        'N2_n24':94*betabinom.pmf(k,24,.7546,45.4563),
        'N3_binomial':94*binom.pmf(k,25,mu),
        'N4_troca_alpha_beta':94*betabinom.pmf(k,25,45.4563,.7546),
        'N5_sigma_CV_mu_quadrado':94*betabinom.pmf(k,25,mu*s_n5,(1-mu)*s_n5)}


def metricas(valores):
    razoes=valores/PUBLICADO
    d=np.diff(razoes)
    return dict(maior_desvio_pct=float(100*np.max(np.abs(razoes-1))),
                amplitude_pct=float(100*np.ptp(razoes)),
                razao_min=float(min(razoes)),razao_max=float(max(razoes)),
                monotona=bool(np.all(d>=0) or np.all(d<=0)))


def auditar_fonte():
    rows=[]
    for a in np.linspace(.75455,.75465,73):
        for b in np.linspace(45.45625,45.45635,73):
            mu=a/(a+b);cv=np.sqrt(b/(a*(a+b+1)))
            e0=94*np.prod([(b+i)/(a+b+i) for i in range(25)])
            rows.append(dict(alpha=a,beta=b,mu=mu,CV=cv,E0=e0,
                construtos_compativeis=f'{mu:.4f}'=='0.0163' and f'{cv:.2f}'=='1.13',
                E0_compativel=f'{e0:.3f}'=='67.475'))
    def e0(a,b):return 94*np.prod([(b+i)/(a+b+i) for i in range(25)])
    a=brentq(lambda a:e0(a,45.4563)-67.475,.75,.76,xtol=1e-14)
    b=brentq(lambda b:e0(.7546,b)-67.475,45.,46.,xtol=1e-12)
    return pd.DataFrame(rows),dict(alpha_inverso=a,beta_inverso=b,
        desvio_E0_pct=100*abs(e0(.7546,45.4563)/67.475-1),
        finalidade='inversos diagnósticos; não usados na implementação operacional')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);args=ap.parse_args()
    args.saida.mkdir(parents=True,exist_ok=False)
    cs=controles();base=metricas(cs['candidata'])['maior_desvio_pct'];rows=[];res=[]
    for nome,val in cs.items():
        m=metricas(val);neg=nome!='candidata'
        m.update(implementacao=nome,separacao_vezes=m['maior_desvio_pct']/base,
                 acima_1pct=m['maior_desvio_pct']>1,
                 separa_10x=m['maior_desvio_pct']>=10*base)
        rows.append(m)
        for k,x in enumerate(val):res.append(dict(implementacao=nome,k=k,publicado=PUBLICADO[k],calculado=x,razao=x/PUBLICADO[k],residuo_pct=100*(x/PUBLICADO[k]-1)))
    d=pd.DataFrame(rows);pd.DataFrame(res).to_csv(args.saida/'residuos.csv',index=False);d.to_csv(args.saida/'bateria.csv',index=False)
    busca,inversos=auditar_fonte();busca.to_csv(args.saida/'busca_A16_5329.csv',index=False)
    neg=d[d.implementacao!='candidata'];c1=bool((neg.acima_1pct & neg.separa_10x).all() and len(neg)>=4)
    c2=not metricas(cs['candidata'])['monotona'];c4=bool(len(busca)==5329 and busca.construtos_compativeis.all() and not busca.E0_compativel.any())
    sources=[Path(__file__),Path(__file__).with_name('PROTOCOLO.md')]
    ver=dict(C1=c1,C2=c2,C3=True,C4=c4,validada=c1 and c2 and c4,
             veredito='implementação validada; fonte internamente inconsistente na quarta casa significativa' if c1 and c2 and c4 else 'controle discriminante falhou',
             alpha_operacional=.7546,beta_operacional=45.4563,
             pontos=len(busca),construtos_compativeis=int(busca.construtos_compativeis.sum()),frequencias_compativeis=int(busca.E0_compativel.sum()),
             E0_min=float(busca.E0.min()),E0_max=float(busca.E0.max()),**inversos,
             fontes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
    (args.saida/'veredito.json').write_text(json.dumps(ver,indent=2,ensure_ascii=False)+'\n')
    print(d.to_string(index=False));print(json.dumps(ver,indent=2,ensure_ascii=False))
    return int(not ver['validada'])

if __name__=='__main__':raise SystemExit(main())
