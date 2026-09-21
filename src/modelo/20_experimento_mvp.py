"""Experimentos declarados MVP; saídas exclusivas e manifesto pré-execução.
[DEC] Sem ranking. Diferença de cenário = adaptativa - centralizada.
IC t calculado sobre médias por instância, incluindo censura explicitamente.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.stats import t
import yaml
sys.path.insert(0,str(Path(__file__).resolve().parent))
import simulador as S
from simulador_mvp import SimulacaoMVP, OpcoesMVP
ROOT=Path(__file__).resolve().parents[2]

def recalcular_di(d,pesos):
    d=d.copy()
    d['Di']=sum(pesos[k]*d[c] for k,c in [('duracao','duracao_norm'),('recursos','intensidade_norm'),('criticidade','criticidade_folga')])
    cortes=d.Di.quantile([.25,.5,.75]).tolist()
    d['nivel_dificuldade']=pd.cut(d.Di,[-np.inf]+cortes+[np.inf],labels=['baixa','media','alta','muito alta'],right=True).astype(str)
    return d

def preparar_saida(path,manifesto):
    path.mkdir(parents=True,exist_ok=False)
    (path/'manifesto.json').write_text(json.dumps(manifesto,indent=2,ensure_ascii=False)+'\n')

def resumir(d):
    metricas=[c for c in d.select_dtypes(include=['number','bool']).columns if c!='semente']
    linhas=[]
    for nome,g in d.groupby('configuracao'):
        for met in metricas:
            p=g.pivot(index=['arquivo','semente'],columns='cenario',values=met).astype(float)
            ok=g.pivot(index=['arquivo','semente'],columns='cenario',values='concluiu')
            if p[['adaptativa','centralizada']].isna().any().any(): continue
            p['diferenca']=p.adaptativa-p.centralizada
            p['censurado']=~(ok.adaptativa & ok.centralizada)
            for arq,x in p.groupby(level=0):
                linhas.append(dict(configuracao=nome,arquivo=arq,metrica=met,centralizada=x.centralizada.mean(),adaptativa=x.adaptativa.mean(),diferenca=x.diferenca.mean(),n_pares=len(x),n_pares_censurados=int(x.censurado.sum())))
    ci=pd.DataFrame(linhas); resumo=[]
    for (nome,met),g in ci.groupby(['configuracao','metrica']):
        n=len(g); mean=g.diferenca.mean(); half=t.ppf(.975,n-1)*g.diferenca.std(ddof=1)/np.sqrt(n) if n>1 else np.nan
        resumo.append(dict(configuracao=nome,metrica=met,n_instancias=n,media_centralizada=g.centralizada.mean(),media_adaptativa=g.adaptativa.mean(),media_diferenca=mean,ic95_inferior=mean-half,ic95_superior=mean+half,n_positivo=int((g.diferenca>0).sum()),n_negativo=int((g.diferenca<0).sum()),n_zero=int((g.diferenca==0).sum()),n_pares_censurados=int(g.n_pares_censurados.sum())))
    return ci,pd.DataFrame(resumo)

def desenho(cfg,par,etapa):
    base=cfg['opcoes']; iguais={k:1/3 for k in ['duracao','recursos','criticidade']}
    pesos=par['dificuldade']['pesos_Di']; familias={'yaml_arredondado':pesos['valor'],**pesos['varredura_alternativa']}
    out=[]
    def add(nome,op,peso=iguais,mods=None,horizonte=1):
        out.append(dict(nome=nome,opcoes=op,pesos=peso,parametros=mods or {},horizonte=horizonte))
    if etapa=='alternativas':
        add('legado',None)
        neutro={**base,'fator_omissao':1.,'rho_omissao':0.,'retrabalho_fila':False,
                'horizonte_automatico':False,'lei_confianca':'constante',
                'comunicacao_crowder':False,'reset_competencia':False,
                'portao_assistencia':'limiar','regra_fuga':'constante'}
        add('controle_motor',neutro)
        tempo={**neutro,'fator_omissao':base['fator_omissao']}
        add('C4_tempo_apenas',tempo)
        qualidade={**tempo,'rho_omissao':float(S.v(par['risco']['rho_omissao']))}
        add('C4_completo',qualidade)
        fila={**qualidade,'retrabalho_fila':True}
        add('C4_C1',fila)
        comunicacao={**fila,'comunicacao_crowder':True}
        add('C4_C1_comunicacao',comunicacao)
        lei={**comunicacao,'lei_confianca':'crowder'}
        add('C4_C1_Crowder',lei)
        reset={**lei,'reset_competencia':True}
        add('C4_C1_Crowder_C6',reset)
        add('MVP_corrigido',{**reset,'horizonte_automatico':True})
        # [DEC 21/09] Degrau do nominal v2: portões suaves (projeto/74).
        add('MVP_v2_portoes_suaves',{**reset,'horizonte_automatico':True,'portao_assistencia':'logistico','regra_fuga':'logistica'})
        add('MVP_corrigido_Di_yaml',base,familias['yaml_arredondado'])
    else:
        r=cfg['robustez']; pontos=list(itertools.product(r['F_ancora'],r['f_retrabalho'],r['mu_minimo']))+[tuple(r['centro'])]
        for i,point in enumerate(pontos):
            mods=dict(zip(['F_ancora','f_retrabalho','mu_minimo'],point))
            for nome,p in familias.items(): add(f'p{i}_{nome}',base,p,mods)
        mods=dict(zip(['F_ancora','f_retrabalho','mu_minimo'],r['centro'])); p=familias['yaml_arredondado']
        for pol in r['politicas_porta2']:
            if pol!=base['politica_porta2']: add('centro_porta2_'+pol,{**base,'politica_porta2':pol},p,mods)
        for lei in r['leis_confianca']:
            if lei!=base['lei_confianca']: add('centro_tau_'+lei,{**base,'lei_confianca':lei},p,mods)
        for fator in r['fatores_omissao']:
            if fator!=base['fator_omissao']: add('centro_fator_'+str(fator),{**base,'fator_omissao':fator},p,mods)
        add('centro_horizonte_dobrado',base,p,mods,r['multiplicador_horizonte_verificacao'])
    if etapa=='robustez':
        out=[{**copy.deepcopy(c),'nome':c['nome']+(f'_rho{rho:.2f}' if rho!=.35 else ''),
              'opcoes':{**c['opcoes'],'rho_omissao':rho}}
             for rho in cfg['robustez']['rho_omissao'] for c in out]
    return out

_CACHE={}
def executar_job(job):
    conf,arq,seed,cen=job
    if not _CACHE:
        _CACHE.update(par=S.carregar_parametros(),tarefas=pd.read_csv(ROOT/'data/processed/psplib/tarefas_j60_com_di.csv'),inst=pd.read_csv(ROOT/'data/processed/psplib/instancias_j60.csv'))
    p=copy.deepcopy(_CACHE['par'])
    for key,val in conf['parametros'].items():
        grupo={'F_ancora':'risco','f_retrabalho':'retrabalho','mu_minimo':'fuzzy'}[key]
        p[grupo][key]['valor']=val
    p['execucao']['horizonte_maximo_fator']['valor']*=conf['horizonte']
    key=json.dumps(conf['pesos'],sort_keys=True)
    if key not in _CACHE:
        iguais=all(x==1/3 for x in conf['pesos'].values())
        _CACHE[key]=_CACHE['tarefas'].copy() if iguais else recalcular_di(_CACHE['tarefas'],conf['pesos'])
    g=_CACHE[key]; g=g[g.arquivo==arq].copy(); line=_CACHE['inst'].set_index('arquivo').loc[arq]
    args=(g,[int(x) for x in str(line.disponibilidades).split(';')],int(line.makespan_sem_recursos),p,cen)
    sim=S.Simulacao(*args,semente=seed) if conf['opcoes'] is None else SimulacaoMVP(*args,semente=seed,opcoes=OpcoesMVP(**conf['opcoes']))
    r=sim.executar(); data=asdict(r)
    row={k:v for k,v in data.items() if isinstance(v,(int,float,bool))}
    row.update({k:v for k,v in r.contadores.items() if isinstance(v,(int,float,bool,str))})
    row.update(configuracao=conf['nome'],arquivo=arq,semente=seed,cenario=cen,atraso_relativo=r.makespan/r.makespan_cpm,violacoes=json.dumps(r.violacoes,ensure_ascii=False),motivo_termino=r.contadores.get('motivo_termino','terminal_legado' if r.concluiu else 'limite_legado'),tarefas_pendentes=sum(not x.estado.startswith('concluida') for x in sim.tarefas.values()),dividas_pendentes=len(sim.divida_pendente))
    return row

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--etapa',choices=['alternativas','robustez'],required=True); ap.add_argument('--saida',type=Path,required=True); ap.add_argument('--workers',type=int,default=1); ap.add_argument('--somente-planejar',action='store_true'); args=ap.parse_args()
    if not 1<=args.workers<=4: ap.error('workers deve estar entre 1 e 4')
    cfg=yaml.safe_load((ROOT/'config/mvp.yaml').read_text()); par=S.carregar_parametros(); configs=desenho(cfg,par,args.etapa)
    todas=sorted(pd.read_csv(ROOT/'data/processed/psplib/tarefas_j60_com_di.csv').arquivo.unique()); n=cfg[args.etapa]['instancias']; inst=todas[::max(1,len(todas)//n)][:n]
    jobs=list(itertools.product(configs,inst,range(cfg[args.etapa]['sementes']),['centralizada','adaptativa']))
    inputs=['config/mvp.yaml','config/parametros.yaml','config/parametros_derivados.yaml','src/modelo/simulador.py','src/modelo/fuzzy.py','src/modelo/simulador_mvp.py','src/modelo/20_experimento_mvp.py','data/processed/psplib/tarefas_j60_com_di.csv','data/processed/psplib/instancias_j60.csv']
    manifest=dict(criado=datetime.now(timezone.utc).isoformat(),etapa=args.etapa,config=cfg,configuracoes=configs,instancias=inst,n_execucoes=len(jobs),sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in inputs},limitacoes=cfg['limitacoes'])
    preparar_saida(args.saida,manifest)
    if args.somente_planejar: return
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows=[]
        for row in pool.map(executar_job,jobs,chunksize=4):
            rows.append(row)
            if len(rows)%64==0: print(f'{len(rows)}/{len(jobs)}',flush=True)
    d=pd.DataFrame(rows); d.to_csv(args.saida/'bruto.csv',index=False)
    assert manifest['sha256']=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in inputs},'fonte mudou durante execução'
    ci,res=resumir(d); ci.to_csv(args.saida/'contrastes_por_instancia.csv',index=False); res.to_csv(args.saida/'resumo.csv',index=False)
    d.groupby(['configuracao','cenario']).agg(n=('concluiu','size'),concluidas=('concluiu','sum')).assign(censuradas=lambda x:x.n-x.concluidas).to_csv(args.saida/'censura.csv')
    if args.etapa=='alternativas':
        antes=res[res.configuracao=='legado'].drop(columns='configuracao')
        res.merge(antes,on='metrica',suffixes=('_DEPOIS','_ANTES')).to_csv(args.saida/'antes_depois.csv',index=False)
    else:
        a=d[d.configuracao=='p8_yaml_arredondado'].set_index(['arquivo','semente','cenario']); b=d[d.configuracao=='centro_horizonte_dobrado'].set_index(['arquivo','semente','cenario'])
        cols=[c for c in a.columns if c not in ['configuracao','extensoes_horizonte']]
        dif=[c for c in cols if not a[c].equals(b[c])]
        (args.saida/'verificacao_horizonte.json').write_text(json.dumps(dict(identico=not dif,colunas_divergentes=dif),indent=2))
        if dif: raise AssertionError(f'horizonte alterou resultados: {dif}')
    print(f'Concluído {len(d)} execuções; censura {(~d.concluiu).sum()}',flush=True)
if __name__=='__main__': main()
