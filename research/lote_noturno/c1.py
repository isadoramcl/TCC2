"""C1: alternativas declaradas, sem substituição do nominal nem otimização."""
import csv,hashlib,json,sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
import yaml
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from ancoragem_stewart import ancora_stewart,MAPAS_PASSOS
METRICAS=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1','retrabalho_sobre_esforco_total']
def job(args):
    mapa,a,seed,cen=args
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];op.update(instrumentar_tarefas=False)
    if mapa!='historica':op.update(ancoragem_erro='stewart_linear',mapa_passos=mapa)
    g,d,c=S.carregar_instancia(a);s=SimulacaoMVP(g,d,c,S.carregar_parametros(),cen,seed,opcoes=OpcoesMVP(**op));r=s.executar();n=r.contadores['p1_omissao']+r.contadores['p3_analitica']
    row=dict(mapa=mapa,arquivo=a,semente=seed,cenario=cen,concluiu=r.concluiu,violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=r.contadores['p1_omissao']/n if n else np.nan,TW=r.TW,TL=r.TL,TU=r.TU,TR=r.TR)
    row.update({k:getattr(r,k) for k in METRICAS if k not in row})
    return row
if __name__=='__main__':
    out=ROOT/'outputs/diagnosticos/C1_20260919'
    controls=[dict(k=k,publicado=p,calculado=ancora_stewart(k),residuo=ancora_stewart(k)-p) for k,p in [(1,.0128),(2,.0256),(3,.0384),(4,.0512),(5,.0640),(8,.1024)]]
    assert max(abs(x['residuo']) for x in controls)<1e-12
    pd.DataFrame(controls).to_csv(out/'seis_pontos.csv',index=False)
    pd.DataFrame([dict(F_ancora=x,k_implicito=x/.0128,rotulo='faixa publicada; transporte declarado' if x/.0128<=8 else 'CENARIO DE SENSIBILIDADE: extrapolacao') for x in [.05,.1,.15,.2,.25]]).to_csv(out/'mapa_reverso.csv',index=False)
    par=S.carregar_parametros();rows=[]
    for mapa,m in MAPAS_PASSOS.items():
        for nivel,k in m.items():rows.append(dict(mapa=mapa,nivel=nivel,k_sintetico=k,F_base_antes=S.v(par['risco']['F_ancora'])*S.v(par['risco']['razoes_de_risco'])[nivel.replace(' ','_')],F_base_depois=ancora_stewart(k)))
    pd.DataFrame(rows).to_csv(out/'mapas_sinteticos.csv',index=False)
    names=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::120]
    jobs=[(m,a,s,c) for m in ['historica','curto','longo'] for a in names for s in range(4) for c in ['centralizada','adaptativa']]
    files=[Path(__file__),ROOT/'src/modelo/simulador_mvp.py',ROOT/'src/modelo/simulador.py',ROOT/'src/modelo/ancoragem_stewart.py',ROOT/'research/lote_noturno/PLANO_ALTERNATIVAS.md',*list((ROOT/'config').glob('*.yaml'))];hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (out/'manifesto.json').write_text(json.dumps(dict(N=len(jobs),instancias=names,seeds=list(range(4)),hashes=hashes),indent=2)+'\n')
    rows=[]
    with (out/'bruto.csv').open('w') as f,ProcessPoolExecutor(max_workers=4) as pool:
        w=None
        for i,r in enumerate(pool.map(job,jobs)):
            if w is None:w=csv.DictWriter(f,fieldnames=list(r),lineterminator='\n');w.writeheader()
            w.writerow(r);f.flush();rows.append(r)
            if (i+1)%16==0:print(f'{i+1}/{len(jobs)}',flush=True)
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    d=pd.DataFrame(rows);assert not d.violacoes.any();contr=[];antes=[]
    for m,g in d.groupby('mapa'):
        for met in METRICAS:
            p=g.pivot(index=['arquivo','semente'],columns='cenario',values=met)
            ok=g.pivot(index=['arquivo','semente'],columns='cenario',values='concluiu').all(axis=1);p=p[ok]
            diff=(p.adaptativa-p.centralizada).groupby(level=0).mean();n=len(diff);half=t.ppf(.975,n-1)*diff.std(ddof=1)/np.sqrt(n) if n>1 else np.nan
            contr.append(dict(mapa=m,metrica=met,N_pares=len(p),N_instancias=n,diferenca=diff.mean(),ic95_inf=diff.mean()-half,ic95_sup=diff.mean()+half))
            for cen in ['centralizada','adaptativa']:
                base=d[(d.mapa=='historica')&(d.cenario==cen)].set_index(['arquivo','semente']);novo=g[g.cenario==cen].set_index(['arquivo','semente']);mask=base.concluiu&novo.concluiu
                antes.append(dict(mapa=m,cenario=cen,metrica=met,N_pares=int(mask.sum()),antes=base.loc[mask,met].mean(),depois=novo.loc[mask,met].mean()))
    pd.DataFrame(contr).to_csv(out/'contrastes.csv',index=False);pd.DataFrame(antes).to_csv(out/'antes_depois.csv',index=False)
    (out/'verificacoes.json').write_text(json.dumps(dict(N=len(d),completas=int(d.concluiu.sum()),violacoes=int(d.violacoes.sum()),seis_pontos=True),indent=2)+'\n')
