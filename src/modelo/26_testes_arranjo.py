"""T1/T2: alternativas declaradas; nenhum ajuste ou substituição do nominal."""
import argparse
import copy
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
import yaml
import simulador as S
from simulador_mvp import SimulacaoMVP, OpcoesMVP
ROOT=Path(__file__).resolve().parents[2]
METRICAS=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']


def malha(tm):
    return sorted({round(x,6) for x in list(np.linspace(0,1,11))+[.25,.8,tm]+[tm+s*d for s in [-1,1] for d in [.1,.05,.02,.01,.001,.000001]] if 0<=x<=1})


def degrau_puro(x,y,tm):
    """Constância exata nos lados; rejeita inclinação (não prova continuidade)."""
    abaixo=[v for a,v in zip(x,y) if a<=tm]
    acima=[v for a,v in zip(x,y) if a>tm]
    return len(abaixo)>1 and len(acima)>1 and len(set(abaixo))==len(set(acima))==1 and abaixo[0]!=acima[0]


def celulas_t2(par):
    base=par['cenarios']['centralizada']; alto=par['cenarios']['adaptativa']
    out=[]
    for nome,campos in [('referencia',[]),('confianca',['tau_inicial','tau_min']),('reporte',['p_reporte','p_deteccao']),('ambos',list(base))]:
        c=copy.deepcopy(base)
        for k in campos:c[k]=copy.deepcopy(alto[k])
        out.append(dict(etapa='T2',nome=nome,cenario=c))
    return out


def celulas_t1(par):
    out=[]
    for origem in ['centralizada','adaptativa']:
        tm=S.v(par['cenarios'][origem]['tau_min'])
        for rep in ['centralizada','adaptativa']:
            for tau in malha(tm):
                c=copy.deepcopy(par['cenarios']['centralizada'])
                for k in ['p_reporte','p_deteccao']:c[k]=copy.deepcopy(par['cenarios'][rep][k])
                c['tau_min']['valor']=tm;c['tau_inicial']['valor']=tau
                out.append(dict(etapa='T1',nome=f'tm{tm}_rep{rep}_tau{tau}',cenario=c))
    return out


@lru_cache(None)
def entrada(arquivo):
    return S.carregar_instancia(arquivo)


def job(args):
    conf,arquivo,seed=args
    par=S.carregar_parametros();par['cenarios']['teste']=copy.deepcopy(conf['cenario'])
    g,disp,cpm=entrada(arquivo)
    op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
    s=SimulacaoMVP(g,disp,cpm,par,'teste',seed,opcoes=OpcoesMVP(**op))
    r=s.executar();n=r.contadores['p1_omissao']+r.contadores['p3_analitica']
    executadas=[e for e in s.registros_tarefas if e['executada']]
    assert n==len(executadas)
    if r.concluiu:
        assert n==len(s.tarefas)
        assert sum(e['falhou'] for e in executadas)==r.n_com_erro+r.n_reportadas
    return dict(etapa=conf['etapa'],configuracao=conf['nome'],arquivo=arquivo,semente=seed,
        **{k:float(S.v(v)) for k,v in conf['cenario'].items()},
        atraso_relativo=r.makespan/r.makespan_cpm,taxa_omissao=r.taxa_omissao,
        divida_latente_sobre_plano=r.divida_latente_sobre_plano,retrabalho_sobre_esforco_total=r.retrabalho_sobre_esforco_total,taxa_falha_efetiva=r.taxa_falha_efetiva,
        fracao_porta1=r.contadores['p1_omissao']/max(1,n),
        n_com_erro=r.n_com_erro,n_reportadas=r.n_reportadas,n_tarefas=len(s.tarefas),
        makespan=r.makespan,makespan_cpm=r.makespan_cpm,TW=r.TW,TL=r.TL,TU=r.TU,TR=r.TR,
        **{k:r.contadores[k] for k in ['N_req','N_fail','N_blocked','N_success','p1_omissao','p3_analitica','p2_ajuda','hiato_encontrado','hiato_colega_capaz_sem_confianca']},
        mu_rede_medio=float(np.mean(r.trajetorias['mu_rede'])),
        concluiu=r.concluiu,violacoes=len(r.violacoes))


def ic(x):
    x=np.asarray(x);m=x.mean();h=t.ppf(.975,len(x)-1)*x.std(ddof=1)/np.sqrt(len(x)) if len(x)>1 else np.nan
    return dict(media=m,ic95_inferior=m-h,ic95_superior=m+h,n_instancias=len(x))


def analisar(d,out):
    t1=d[d.etapa=='T1'];t2=d[d.etapa=='T2'];curvas=[];contrastes=[];formas=[]
    for chave,g in t1.groupby(['tau_min','p_reporte','p_deteccao','tau_inicial']):
        for met in METRICAS+['N_req','mu_rede_medio']:
            curvas.append(dict(zip(['tau_min','p_reporte','p_deteccao','tau_inicial'],chave),metrica=met,**ic(g.groupby('arquivo')[met].mean())))
    curva=pd.DataFrame(curvas);curva.to_csv(out/'T1_curvas_IC95.csv',index=False)
    for chave,g in curva.groupby(['tau_min','p_reporte','p_deteccao','metrica']):
        g=g.sort_values('tau_inicial');tm=chave[0]
        lo=g[g.tau_inicial==round(tm-1e-6,6)].media.iloc[0]
        eq=g[g.tau_inicial==tm].media.iloc[0]
        hi=g[g.tau_inicial==round(tm+1e-6,6)].media.iloc[0]
        formas.append(dict(zip(['tau_min','p_reporte','p_deteccao','metrica'],chave),
            degrau_puro=degrau_puro(g.tau_inicial,g.media,tm),
            amplitude_abaixo=g[g.tau_inicial<=tm].media.max()-g[g.tau_inicial<=tm].media.min(),
            amplitude_acima=g[g.tau_inicial>tm].media.max()-g[g.tau_inicial>tm].media.min(),
            vizinho_inferior=lo,igualdade=eq,vizinho_superior=hi,salto_local=hi-eq))
    pd.DataFrame(formas).to_csv(out/'T1_forma.csv',index=False)
    pares=[]
    for met in METRICAS:
        p=t2.pivot(index=['arquivo','semente'],columns='configuracao',values=met)
        for c in ['confianca','reporte','ambos']:
            delta=p[c]-p.referencia
            por_inst=delta.groupby('arquivo').mean()
            contrastes.append(dict(celula=c,metrica=met,referencia=p.referencia.mean(),intervencao=p[c].mean(),**ic(por_inst)))
            for arq,v in por_inst.items():pares.append(dict(celula=c,metrica=met,arquivo=arq,diferenca=v))
        inter=p.ambos-p.confianca-p.reporte+p.referencia
        contrastes.append(dict(celula='interacao',metrica=met,referencia=np.nan,intervencao=np.nan,**ic(inter.groupby('arquivo').mean())))
    pd.DataFrame(contrastes).to_csv(out/'T2_contrastes_IC95.csv',index=False)
    pd.DataFrame(pares).to_csv(out/'T2_contrastes_instancia.csv',index=False)
    # Controle nominal contra os números publicados; somente conversão CSV tolerada.
    antigo=pd.read_csv(ROOT/'outputs/diagnosticos/teste_TL_20260917/bruto.csv')
    checks=[]
    for c,cen in [('referencia','centralizada'),('ambos','adaptativa')]:
        novo=t2[t2.configuracao==c].set_index(['arquivo','semente'])
        old=antigo[(antigo.lei=='unitario')&(antigo.cenario==cen)].set_index(['arquivo','semente']).loc[novo.index]
        campos=['makespan','makespan_cpm','TW','TL','TU','TR','n_com_erro','n_reportadas','taxa_omissao','divida_latente_sobre_plano']
        for met in campos:
            delta=float((novo[met]-old[met]).abs().max());assert delta<1e-12,(met,delta)
            checks.append(dict(celula=c,metrica=met,diferenca_maxima=delta))
    pd.DataFrame(checks).to_csv(out/'controle_nominal.csv',index=False)
    graficos(curva,out)


def graficos(curva,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(5,2,figsize=(12,16),sharex=True)
    for col,tm in enumerate(sorted(curva.tau_min.unique())):
        for row,met in enumerate(METRICAS):
            ax=axes[row,col]
            for pr,g in curva[(curva.tau_min==tm)&(curva.metrica==met)].groupby('p_reporte'):
                g=g.sort_values('tau_inicial');ax.plot(g.tau_inicial,g.media,'.-',label=f'p_reporte={pr}')
                ax.fill_between(g.tau_inicial,g.ic95_inferior,g.ic95_superior,alpha=.12)
            ax.axvline(tm,color='black',ls=':');ax.set_title(f'{met} | tau_min={tm}');ax.legend(fontsize=8)
            ax.set_xlabel('tau inicial');ax.grid(alpha=.2)
    fig.suptitle('T1: alternativas declaradas; IC95 por instância, pontuais')
    fig.tight_layout();fig.savefig(out/'T1_curvas.png',dpi=140);plt.close(fig)


def local(out,arquivo):
    g,disp,cpm=entrada(arquivo);s=SimulacaoMVP(g,disp,cpm,S.carregar_parametros(),'centralizada',0)
    a=s.agentes[0];a.bateria=.5;rows=[]
    for tau in np.linspace(0,1,1001):
        a.confianca=float(tau);mc,mr=s.multiplicadores(a,.5)
        rows.append(dict(tau=tau,P=.5,B=.5,mu_cog=mc,mu_rede=mr))
    pd.DataFrame(rows).to_csv(out/'T1_canal_fuzzy_estado_fixo.csv',index=False)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--piloto',action='store_true');ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    if not 1<=args.workers<=4:ap.error('workers entre 1 e 4')
    args.saida.mkdir(parents=True,exist_ok=False)
    antigo=pd.read_csv(ROOT/'outputs/diagnosticos/teste_TL_20260917/bruto.csv');inst=sorted(antigo.arquivo.unique());par=S.carregar_parametros()
    c1=celulas_t1(par);c2=celulas_t2(par)
    i1=inst[::4];i2=inst;s1=range(4);s2=range(12)
    if args.piloto:i1=i2=inst[:1];s1=s2=range(1)
    jobs=[(c,a,s) for cs,ins,seeds in [(c1,i1,s1),(c2,i2,s2)] for c in cs for a in ins for s in seeds]
    files=[Path(__file__),Path(S.__file__),ROOT/'src/modelo/simulador_mvp.py',ROOT/'src/modelo/fuzzy.py',ROOT/'research/PLANO_T1_T2_T3.md']+list((ROOT/'config').glob('*.yaml'))+list((ROOT/'data/processed/psplib').glob('*.csv'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (args.saida/'manifesto.json').write_text(json.dumps(dict(configuracoes=c1+c2,T1_instancias=i1,T2_instancias=i2,T1_sementes=list(s1),T2_sementes=list(s2),n_exec=len(jobs),hashes=hashes,IC='t sobre médias por instância',RNG='sementes e sequência comum; eventos podem desalinharem-se após divergência',piloto=args.piloto),indent=2)+'\n')
    rows=[]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for i,row in enumerate(pool.map(job,jobs,chunksize=4)):
            rows.append(row)
            if (i+1)%128==0:print(f'{i+1}/{len(jobs)}',flush=True)
    d=pd.DataFrame(rows);d.to_csv(args.saida/'bruto.csv',index=False)
    assert d.concluiu.all() and not d.violacoes.any(), 'censura/violação: examinar bruto antes de interpretar'
    analisar(d,args.saida);local(args.saida,inst[0])
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (args.saida/'verificacoes.json').write_text(json.dumps(dict(exec=len(d),incompletas=int((~d.concluiu).sum()),violacoes=int(d.violacoes.sum()),controle_nominal='passou',contagem_falhas_instrumentadas='confere em todas as execuções completas'),indent=2)+'\n')
    print('Concluído',len(d),flush=True)

if __name__=='__main__':main()
