"""C2: fechamento sob controle aproximado, sem ajustar momentos ou CV."""
import csv,hashlib,json,sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
from scipy.stats import beta,t
import yaml
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from heterogeneidade_erro import parametros_beta,NIVEIS,CV_ERRO
from ancoragem_stewart import ancora_stewart,MAPAS_PASSOS
OUT=ROOT/'outputs/diagnosticos/C2_fechamento_20260919'
BASES=[('historica_'+str(x),x,None) for x in [.05,.1,.15,.2,.25]]+[(m,None,m) for m in ['curto','longo']]
MET=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']
def preparar(base,het):
    nome,anc,mapa=base;p=S.carregar_parametros();op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
    op.update(heterogeneidade_erro=het,instrumentar_tarefas=False)
    if mapa:op.update(ancoragem_erro='stewart_linear',mapa_passos=mapa)
    else:p['risco']['F_ancora']['valor']=anc
    return p,op

def job(args):
    base,het,arquivo,seed,cen=args;p,op=preparar(base,het);g,d,c=S.carregar_instancia(arquivo)
    ids=dict(base=base[0],heterogeneidade=het,arquivo=arquivo,semente=seed,cenario=cen)
    try:s=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=OpcoesMVP(**op))
    except ValueError as e:
        if 'CV nao alterado' not in str(e):raise
        return dict(**ids,executada=False,concluiu=False,estatuto='REJEITADA_DOMINIO',motivo=str(e)),[]
    r=s.executar();n=r.contadores['p1_omissao']+r.contadores['p3_analitica']
    row=dict(**ids,executada=True,concluiu=r.concluiu,estatuto='COMPLETA' if r.concluiu else 'CENSURADA',motivo=r.contadores['motivo_termino'],violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=r.contadores['p1_omissao']/n if n else np.nan,TW=r.TW,TL=r.TL,TU=r.TU,TR=r.TR)
    row.update({k:getattr(r,k) for k in MET if k not in row})
    rates=[dict(base=base[0],semente=seed,agente=a,nivel=l,taxa=x,mu=s.F_base(l)) for a,v in getattr(s,'taxas_erro_agentes',{}).items() for l,x in v.items()]
    return row,rates

def ic(x):
    x=x.dropna();n=len(x);m=x.mean();h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n) if n>1 else np.nan
    return dict(media=m,ic95_inf=m-h,ic95_sup=m+h,N_instancias=n)

def analisar(d):
    d.groupby(['base','heterogeneidade','cenario']).agg(N=('executada','size'),executadas=('executada','sum'),completas=('concluiu','sum')).to_csv(OUT/'completude.csv')
    rows=[];effects=[]
    for (base,het),g in d.groupby(['base','heterogeneidade']):
        for m in MET:
            if not g.executada.all():
                rows.append(dict(base=base,heterogeneidade=het,metrica=m,estatuto='REJEITADA_DOMINIO',N_pares=0,media=np.nan,ic95_inf=np.nan,ic95_sup=np.nan,N_instancias=0));continue
            p=g.pivot(index=['arquivo','semente'],columns='cenario',values=m)
            ok=g.pivot(index=['arquivo','semente'],columns='cenario',values='concluiu').all(axis=1)
            delta=(p.adaptativa-p.centralizada)[ok]
            rows.append(dict(base=base,heterogeneidade=het,metrica=m,estatuto='COMPLETO' if ok.all() else 'CONDICIONAL_PARES_COMPLETOS',N_pares=len(delta),**ic(delta.groupby('arquivo').mean())))
    for (base,cen),g in d.groupby(['base','cenario']):
        for m in MET:
            if not g.executada.all():
                effects.append(dict(base=base,cenario=cen,metrica=m,estatuto='REJEITADA_DOMINIO',N_pares=0));continue
            p=g.pivot(index=['arquivo','semente'],columns='heterogeneidade',values=m)
            ok=g.pivot(index=['arquivo','semente'],columns='heterogeneidade',values='concluiu').all(axis=1)
            delta=(p.beta_cv113-p.nenhuma)[ok]
            effects.append(dict(base=base,cenario=cen,metrica=m,estatuto='COMPLETO' if ok.all() else 'CONDICIONAL_PARES_COMPLETOS',N_pares=len(delta),antes=p.nenhuma[ok].mean(),depois=p.beta_cv113[ok].mean(),**ic(delta.groupby('arquivo').mean())))
    pd.DataFrame(rows).to_csv(OUT/'cinco_indicadores_IC95.csv',index=False);pd.DataFrame(effects).to_csv(OUT/'efeito_beta_menos_nenhuma.csv',index=False)

def controles():
    # Inputs literais inalterados. Impresso é compatível com seu arredondamento.
    a,b=parametros_beta(.0163);m,v=beta.stats(a,b,moments='mv')
    assert abs(m-.0163)<1e-14 and abs(np.sqrt(v)/m-1.13)<1e-13
    mp,vp=beta.stats(.7546,45.4563,moments='mv');cp=np.sqrt(vp)/mp
    assert .01625<=mp<.01635 and 1.125<=cp<1.135
    pd.DataFrame([dict(parametro=n,calculado=x,impresso=y,residuo=x-y) for n,x,y in [('alpha',a,.7546),('beta',b,45.4563)]]).to_csv(OUT/'controle_aproximado.csv',index=False)
    dom=[];means={.0163}
    rr=S.v(S.carregar_parametros()['risco']['razoes_de_risco'])
    for nome,anc,mapa in BASES:
        for nivel in NIVEIS:
            mu=ancora_stewart(MAPAS_PASSOS[mapa][nivel]) if mapa else anc*rr[nivel.replace(' ','_')]
            try:aa,bb=parametros_beta(mu);valid=True;motivo='';means.add(mu)
            except ValueError as e:aa=bb=None;valid=False;motivo=str(e)
            dom.append(dict(base=nome,nivel=nivel,mu=mu,admissivel=valid,alpha=aa,beta=bb,motivo=motivo))
    pd.DataFrame(dom).to_csv(OUT/'dominio.csv',index=False)
    samples=[]
    for i,mu in enumerate(sorted(means)):
        seed=20260919+i;x=np.random.default_rng(seed).beta(*parametros_beta(mu),size=200000)
        cv=x.std(ddof=1)/x.mean();errm=abs(x.mean()/mu-1);errcv=abs(cv/1.13-1)
        samples.append(dict(mu=mu,seed=seed,N=len(x),media=x.mean(),CV=cv,erro_rel_media=errm,erro_rel_CV=errcv,passou=bool(errm<.03 and errcv<.03)))
    pd.DataFrame(samples).to_csv(OUT/'momentos_200mil.csv',index=False)
    assert all(x['passou'] for x in samples),'controle de momentos falhou; nao iniciar grade'
    return dict(alpha=a,beta=b,mu_impresso=mp,CV_impresso=cp,controle_momentos=True,controle_aproximado=True)

if __name__=='__main__':
    if (OUT/'bruto.csv').exists():raise FileExistsError('preservar rodada anterior; nao sobrescrever')
    ver=controles()
    names=sorted(pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::120]
    jobs=[(b,h,a,s,c) for b in BASES for h in ['nenhuma','beta_cv113'] for a in names for s in range(4) for c in ['centralizada','adaptativa']]
    files=[Path(__file__),Path(__file__).with_name('PROTOCOLO_C2_FECHAMENTO.md'),*[ROOT/'src/modelo'/s for s in ['simulador.py','simulador_mvp.py','fuzzy.py','ancoragem_stewart.py','heterogeneidade_erro.py']],*list((ROOT/'config').glob('*.yaml')),*list((ROOT/'data/processed/psplib').glob('*j60*.csv'))]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (OUT/'manifesto.json').write_text(json.dumps(dict(N_planejadas=len(jobs),bases=BASES,instancias=names,seeds=list(range(4)),hashes=hashes),indent=2)+'\n')
    cols=['base','heterogeneidade','arquivo','semente','cenario','executada','concluiu','estatuto','motivo','violacoes',*MET,'TW','TL','TU','TR'];rows=[];rates=[]
    with (OUT/'bruto.csv').open('w') as f,ProcessPoolExecutor(max_workers=4) as pool:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader()
        for i,(r,rs) in enumerate(pool.map(job,jobs)):
            w.writerow(r);f.flush();rows.append(r);rates.extend(rs)
            if (i+1)%32==0:print(f'{i+1}/{len(jobs)}',flush=True)
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    d=pd.DataFrame(rows);assert d.violacoes.fillna(0).eq(0).all();analisar(d)
    rt=pd.DataFrame(rates);keys=['base','semente','agente','nivel'];assert rt.groupby(keys).taxa.nunique().eq(1).all()
    rt=rt.drop_duplicates(keys);rt.to_csv(OUT/'taxas_agentes_unicas.csv',index=False)
    rt.groupby(['base','nivel']).agg(N=('taxa','size'),mu=('mu','first'),media=('taxa','mean'),desvio=('taxa','std')).assign(CV=lambda z:z.desvio/z.media).to_csv(OUT/'momentos_agentes_simulados.csv')
    ver.update(N_planejadas=len(d),N_executadas=int(d.executada.sum()),N_rejeitadas=int((~d.executada).sum()),N_completas=int(d.concluiu.sum()),violacoes=0)
    (OUT/'verificacoes.json').write_text(json.dumps(ver,indent=2)+'\n');print(json.dumps(ver),flush=True)
