"""Propagação da precisão impressa; regra do parecer 39, sem ajuste ao alvo."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from distribuicoes import binomial, beta_binomial, p_dependente


def limites_binomial(n, lo, hi):
    vals = []
    for k in range(n + 1):
        # d(log PMF)/dp é decrescente; sinais iguais certificam monotonicidade.
        d_lo = k / lo - (n-k) / (1-lo)
        d_hi = k / hi - (n-k) / (1-hi)
        assert d_lo * d_hi > 0
        ends = [binomial(n, p)[k] for p in (lo, hi)]
        vals.append((min(ends), max(ends)))
    return np.array(vals)


def limites_beta(n, al, ah, bl, bh):
    vals = []
    for k in range(n + 1):
        common_lo = sum(1/(ah+bh+i) for i in range(n))
        common_hi = sum(1/(al+bl+i) for i in range(n))
        da = (sum(1/(ah+i) for i in range(k))-common_hi,
              sum(1/(al+i) for i in range(k))-common_lo)
        db = (sum(1/(bh+i) for i in range(n-k))-common_hi,
              sum(1/(bl+i) for i in range(n-k))-common_lo)
        assert da[0]*da[1] > 0 and db[0]*db[1] > 0
        ends = [beta_binomial(n, a, b)[k] for a in (al, ah) for b in (bl, bh)]
        vals.append((min(ends), max(ends)))
    return np.array(vals)


def limites_pdependente(n, pl, ph, fl, fh):
    lo = np.zeros(n+1); hi = np.zeros(n+1); lo[0] = hi[0] = 1.
    for etapa in range(n):
        nl = np.zeros(n+1); nh = np.zeros(n+1)
        for k in range(etapa+1):
            a, b = pl*fl*(k+1), ph*fh*(k+1)
            assert 0 <= a <= b <= 1
            nl[k] += lo[k]*(1-b); nh[k] += hi[k]*(1-a)
            nl[k+1] += lo[k]*a; nh[k+1] += hi[k]*b
        lo, hi = nl, nh
    return np.column_stack([lo, hi])


def intervalo_chi(bounds):
    grupos = np.vstack([bounds[:3], bounds[3:].sum(axis=0)])
    low = high = 0.
    for obs, (a, b) in zip([68.,18.,5.,3.], grupos):
        f = lambda e: (obs-e)**2/e
        low += 0. if a <= obs <= b else min(f(a),f(b))
        high += max(f(a),f(b))
    return low, high


def executar(saida):
    from validar_c3 import PUBLICADO, CHI, R
    saida.mkdir(parents=True, exist_ok=False)
    pmfs = {'binomial':binomial(25,.0163),
            'beta_binomial':beta_binomial(25,.7546,45.4563),
            'p_dependente':p_dependente(25,.0163,.845)}
    bounds = {'binomial':limites_binomial(25,.01625,.01635),
              'beta_binomial':limites_beta(25,.75455,.75465,45.45625,45.45635),
              'p_dependente':limites_pdependente(25,.01625,.01635,.8445,.8455)}
    rows=[]; chis=[]
    for nome, pmf in pmfs.items():
        freq=94*pmf; lim=94*bounds[nome]
        for k, pub in enumerate(PUBLICADO[nome]):
            a,b=lim[k]; contem=bool(a <= pub <= b)
            conhecido=nome=='beta_binomial' and k==8
            rows.append(dict(distribuicao=nome,erros=k,publicado=pub,
                             calculado=freq[k],inferior=a,superior=b,
                             contem=contem,compativel_arredondamento_saida=bool(a <= pub+.0005 and b >= max(0.,pub-.0005)),discrepancia_conhecida=conhecido,
                             status='DISCREPANCIA_CONHECIDA' if conhecido else ('PASSA' if contem else 'REPROVA')))
        a,b=intervalo_chi(lim)
        esperado=np.r_[freq[:3],freq[3:].sum()]
        calculado=float(sum((np.array([68,18,5,3])-esperado)**2/esperado))
        chis.append(dict(distribuicao=nome,publicado=CHI[nome],calculado=calculado,
                         inferior=a,superior=b,contem=bool(a <= CHI[nome] <= b),
                         compativel_arredondamento_saida=bool(a <= CHI[nome]+.0005 and b >= CHI[nome]-.0005)))
    d=pd.DataFrame(rows);c=pd.DataFrame(chis)
    d.to_csv(saida/'frequencias.csv',index=False);c.to_csv(saida/'chi2.csv',index=False)
    falhas=int((d.status=='REPROVA').sum());falhas_chi=int((~c.contem).sum())
    fontes=[Path(__file__),Path(__file__).with_name('validar_c3.py'),Path(__file__).with_name('distribuicoes.py'),Path(__file__).with_name('PROTOCOLO_C3_39.md'),R/'projeto/39_C3_NAO_ESTA_BLOQUEADO.md']
    ver=dict(status='APROVADO' if falhas+falhas_chi==0 else 'BLOQUEADO_REGRA_39',
             regra='Inclusão literal do publicado na propagação da precisão impressa; BB8 exceção autorizada',
             alpha=.7546,beta=45.4563,intervalos={'alpha':[.75455,.75465],'beta':[45.45625,45.45635],'p':[.01625,.01635],'phi':[.8445,.8455]},
             frequencias_reprovadas=falhas,chi2_reprovados=falhas_chi,
             limites='BB/binomial: extremos certificados por sinal das derivadas; p-dependente e chi2: envoltórias conservadoras',
             fontes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in fontes})
    (saida/'veredito.json').write_text(json.dumps(ver,indent=2,ensure_ascii=False)+'\n')
    print(d.to_string(index=False));print(c.to_string(index=False));print(ver['status'])
    return int(falhas+falhas_chi>0)
