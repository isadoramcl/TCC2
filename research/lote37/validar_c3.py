"""Portão científico: sai com código 1 se a Tabela 2 não for reproduzida."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from distribuicoes import binomial,beta_binomial,beta_parametros,p_dependente,terceira_casa
R=Path(__file__).resolve().parents[2]
PUBLICADO={
 'binomial':[62.330,25.820,5.134,.652,.059,.004,.000,.000,.000],
 'beta_binomial':[67.475,18.334,5.639,1.765,.549,.167,.050,.014,.000],
 'p_dependente':[66.416,19.719,5.690,1.593,.432,.113,.029,.007,.002]}
CHI={'binomial':10.174,'beta_binomial':.162,'p_dependente':.583}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True)
    ap.add_argument('--regra',choices=['parecer39','historica'],default='parecer39')
    args=ap.parse_args()
    if args.regra=='parecer39':
        from validar_c3_39 import executar
        return executar(args.saida)
    o=args.saida;o.mkdir(parents=True,exist_ok=False)
    a,b=beta_parametros(.0163,1.13)
    dist={'binomial':binomial(25,.0163),'beta_binomial':beta_binomial(25,a,b),'p_dependente':p_dependente(25,.0163,.845)}
    linhas=[];chis=[];obs=np.array([68.,18.,5.,3.])
    for nome,pmf in dist.items():
        assert abs(pmf.sum()-1)<1e-12 and min(pmf)>=0
        e=94*pmf
        for k,pub in enumerate(PUBLICADO[nome]):
            linhas.append(dict(distribuicao=nome,erros=k,publicado=pub,calculado=e[k],delta=e[k]-pub,passou=terceira_casa(e[k],pub)))
        esperado=np.r_[e[:3],e[3:].sum()];chi=float(sum((obs-esperado)**2/esperado))
        chis.append(dict(distribuicao=nome,publicado=CHI[nome],calculado=chi,delta=chi-CHI[nome],passou=terceira_casa(chi,CHI[nome]),grupos='0;1;2;>=3'))
    d=pd.DataFrame(linhas);c=pd.DataFrame(chis);d.to_csv(o/'frequencias.csv',index=False);c.to_csv(o/'chi2.csv',index=False)
    # Fontes alternativas de parâmetros são impressas no artigo, não ajustadas à tabela.
    x=.4083;s2=.6057;n=25
    am=-x*(s2-x*(n-x))/(n*s2-x*(n-x));bm=am*(n-x)/x
    variantes=[]
    for origem,aa,bb in [('mu_CV_literais',a,b),('alpha_beta_impressos',.7546,45.4563),('momentos_impressos_eq6',am,bm)]:
        prob=94*beta_binomial(25,aa,bb)
        for k in range(9):variantes.append(dict(origem=origem,alpha=aa,beta=bb,erros=k,esperado=PUBLICADO['beta_binomial'][k],calculado=prob[k]))
    pd.DataFrame(variantes).to_csv(o/'diagnostico_beta.csv',index=False)
    adicionais=[]
    for origem,p in [('p_literal',.0163),('fracao_tabela1',38/2327),('media_erros_sobre_n',.4083/25)]:
        adicionais.append(dict(origem=origem,p=p,binomial_zero=94*binomial(25,p)[0],p_dependente_zero=94*p_dependente(25,p,.845)[0]))
    pd.DataFrame(adicionais).to_csv(o/'diagnostico_precisao_p.csv',index=False)
    pdf=Path('/Users/isadoracarvalho/Downloads/Modelling human error rates for human reliability analysis of a structural design task.pdf')
    fontes=[Path(__file__),Path(__file__).with_name('distribuicoes.py'),Path(__file__).with_name('PROTOCOLO_C3.md'),R/'projeto/37_ORDEM_DE_SERVICO_COM_TESTES.md']
    aprovado=bool(d.passou.all() and c.passou.all())
    manifest=dict(status='APROVADO' if aprovado else 'BLOQUEADO_CONTROLE_PUBLICADO',n=25,respondentes=94,p=.0163,CV=1.13,phi=.845,alpha_calculado=a,beta_calculado=b,
        frequencias_falhas=int((~d.passou).sum()),chi2_falhas=int((~c.passou).sum()),
        criterio='mesma terceira casa decimal; parâmetros e alvo não ajustados',
        pdf=str(pdf),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),paginas=[174,175],
        fontes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in fontes})
    (o/'veredito.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print(d.to_string(index=False));print(c.to_string(index=False));print(manifest['status'])
    return 0 if aprovado else 1

if __name__=='__main__':raise SystemExit(main())
