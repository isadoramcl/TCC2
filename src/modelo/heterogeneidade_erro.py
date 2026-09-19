"""C2: parâmetros Beta com CV fixo; não ajusta o CV ao domínio."""
import math
NIVEIS=('baixa','media','alta','muito alta')
CV_ERRO=1.13

def parametros_beta(mu):
    teto=1/(1+CV_ERRO**2)
    if not math.isfinite(mu) or not 0<mu<teto:
        raise ValueError(f'Beta CV={CV_ERRO}: media={mu} fora de (0,{teto}); CV nao alterado')
    sigma=CV_ERRO*mu
    t=mu*(1-mu)/sigma**2-1
    return mu*t,(1-mu)*t
