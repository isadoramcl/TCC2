"""Controle publicado C2 antes de autorizar Beta no simulador. Sem ajuste."""
import json,sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S

def parametros_beta(mu,cv=1.13):
    teto=1/(1+cv**2)
    if not np.isfinite(mu) or not 0<mu<teto:
        raise ValueError(f'Beta CV={cv}: media={mu} fora do dominio estrito (0,{teto}); CV nao alterado')
    sigma=cv*mu;t=mu*(1-mu)/sigma**2-1
    return mu*t,(1-mu)*t

if __name__=='__main__':
    out=ROOT/'outputs/diagnosticos/C2_20260919';out.mkdir(exist_ok=False)
    mu=.0163;cv=1.13;a,b=parametros_beta(mu,cv)
    # Terceira casa: mesmo arredondamento em três casas e erro <=0,0005.
    controles=[]
    for nome,calc,pub in [('alpha',a,.7546),('beta',b,45.4563)]:
        controles.append(dict(parametro=nome,calculado=calc,publicado=pub,diferenca=calc-pub,erro_relativo_pct=100*(calc/pub-1),passa_terceira_casa=bool(round(calc,3)==round(pub,3) and abs(calc-pub)<=.0005)))
    pd.DataFrame(controles).to_csv(out/'controle_publicado.csv',index=False)
    ap,bp=.7546,45.4563;mp=ap/(ap+bp);vp=ap*bp/((ap+bp)**2*(ap+bp+1));cvp=np.sqrt(vp)/mp
    rows=[];rr=S.v(S.carregar_parametros()['risco']['razoes_de_risco'])
    for ancora in [.05,.1,.15,.2,.25]:
        for nivel,r in rr.items():
            m=ancora*r
            try:aa,bb=parametros_beta(m);valid=True;msg=''
            except ValueError as e:aa=bb=None;valid=False;msg=str(e)
            rows.append(dict(F_ancora=ancora,nivel=nivel,F_base=m,beta_valida=valid,alpha=aa,beta=bb,motivo=msg))
    pd.DataFrame(rows).to_csv(out/'dominio_celulas.csv',index=False)
    ok=all(c['passa_terceira_casa'] for c in controles)
    ver=dict(mu_literal=mu,CV_literal=cv,alpha_calculado=a,beta_calculado=b,media_implicita_impressos=mp,CV_implicito_impressos=cvp,teto_media_beta=1/(1+cv**2),controle_publicado_passou=ok,estado='PASSOU' if ok else 'REPROVADO_POR_INCOMPATIBILIDADE_NUMERICA',modelo_alterado=False,sorteios_agentes_executados=False)
    (out/'veredicto.json').write_text(json.dumps(ver,indent=2)+'\n');print(json.dumps(ver),flush=True)
    if not ok:raise SystemExit(1)
