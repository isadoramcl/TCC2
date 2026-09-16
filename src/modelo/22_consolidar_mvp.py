"""Consolidação auditável do MVP e repetição B9 no mesmo desenho nominal.

Todos os comparativos preservam a fonte antiga. Não seleciona políticas.
"""
from __future__ import annotations
import argparse
import copy
from concurrent.futures import ProcessPoolExecutor
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy import stats
import yaml
ROOT=Path(__file__).resolve().parents[2]
T=ROOT/'outputs/tables'
SPEC=importlib.util.spec_from_file_location('experimento_mvp',Path(__file__).with_name('20_experimento_mvp.py'))
E=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(E)


def job_b9(job): return E.executar_job(job)


def rodar_b9(base,workers):
    cfg=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())
    todas=sorted(pd.read_csv(ROOT/'data/processed/psplib/tarefas_j60_com_di.csv').arquivo.unique())
    inst=todas[::len(todas)//16][:16]
    configs=[dict(nome=pol,opcoes={**cfg['opcoes'],'politica_porta2':pol},pesos={k:1/3 for k in ['duracao','recursos','criticidade']},parametros={},horizonte=1) for pol in ['sem_assistencia','assistencia_universal','sem_filtro_competencia']]
    files=['config/mvp.yaml','config/parametros.yaml','config/parametros_derivados.yaml','src/modelo/simulador.py','src/modelo/simulador_mvp.py','src/modelo/fuzzy.py','src/modelo/20_experimento_mvp.py','src/modelo/22_consolidar_mvp.py','data/processed/psplib/tarefas_j60_com_di.csv','data/processed/psplib/instancias_j60.csv']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    out=base/'b9_mvp';E.preparar_saida(out,dict(instancias=inst,sementes=list(range(12)),configuracoes=configs,hashes=hashes))
    jobs=list(itertools.product(configs,inst,range(12),['centralizada','adaptativa']))
    rows=[]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for row in pool.map(job_b9,jobs,chunksize=4):
            rows.append(row)
            if len(rows)%128==0:print(f'B9 {len(rows)}/{len(jobs)}',flush=True)
    pd.DataFrame(rows).to_csv(out/'bruto.csv',index=False)
    assert hashes=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}


def resumo_estat(c,a,maior=False):
    dif=a-c; sd=dif.std(ddof=1)
    return dict(media_centralizada=c.mean(),media_adaptativa=a.mean(),variacao_percentual=100*dif.mean()/c.mean() if c.mean()!=0 else np.nan,
                d_instancia=dif.mean()/sd if sd>0 else np.nan,
                favoraveis_instancia=np.mean(dif>0) if maior else np.mean(dif<0),
                p_instancia=float(stats.wilcoxon(a,c).pvalue) if not np.allclose(dif,0) else np.nan)


def consolidar(base):
    out=base/'consolidado';out.mkdir(exist_ok=False)
    alt=pd.read_csv(base/'alternativas/bruto.csv')
    robust=pd.read_csv(base/'robustez/bruto.csv')
    b9=pd.read_csv(base/'b9_mvp/bruto.csv')
    b9=pd.concat([alt[alt.configuracao=='C4_C1'].assign(configuracao='nominal'),b9],ignore_index=True)
    rows=[];antigo=pd.read_csv(T/'modelo_14_experimento_por_instancia.csv')
    for nome,g in alt.groupby('configuracao'):
        for r in antigo.itertuples():
            m=r.metrica;p=g.groupby(['arquivo','cenario'])[m].mean().unstack()
            res=resumo_estat(p.centralizada.values,p.adaptativa.values,m=='E_total')
            for k,value in res.items():
                rows.append(dict(configuracao=nome,metrica=m,numero=k,ANTES=getattr(r,k),DEPOIS=value,delta=value-getattr(r,k)))
    pd.DataFrame(rows).to_csv(out/'antes_depois_numeros_experimento.csv',index=False)
    # Reprodução do bruto legado, incluindo todas as métricas comuns, mesmas chaves.
    oldraw=pd.read_csv(T/'modelo_03_experimento_bruto.csv')
    novo=alt[alt.configuracao=='legado']
    keys=['arquivo','semente','cenario']; merged=novo.merge(oldraw,on=keys,suffixes=('_novo','_antigo'),validate='one_to_one')
    assert len(merged)==len(novo)==len(oldraw)==384
    comuns=[c for c in oldraw.select_dtypes(include='number').columns if c not in keys and c in novo.columns]
    maxdiff=max((merged[c+'_novo']-merged[c+'_antigo']).abs().max() for c in comuns)
    assert maxdiff<1e-8,('legado difere',maxdiff)
    # B9: números de mecanismo e termos isolados do fatorial expandido.
    b9rows=[];before=pd.read_csv(T/'modelo_07_ablacao_mecanismo.csv')
    for m in before.metrica.unique():
        nominal=b9[b9.configuracao=='nominal'].groupby(['arquivo','cenario'])[m].mean().unstack()
        nominal_delta=(nominal.adaptativa-nominal.centralizada).mean()
        for pol,g in b9.groupby('configuracao'):
            p=g.groupby(['arquivo','cenario'])[m].mean().unstack(); res=resumo_estat(p.centralizada.values,p.adaptativa.values,m=='E_total')
            diff=res['media_adaptativa']-res['media_centralizada']
            match=before[(before.metrica==m)&(before.configuracao==pol)]
            b9rows.append(dict(metrica=m,configuracao=pol,DEPOIS_centralizada=res['media_centralizada'],DEPOIS_adaptativa=res['media_adaptativa'],DEPOIS_contraste=diff,DEPOIS_pct_restante=100*diff/nominal_delta if nominal_delta else np.nan,
                               ANTES_contraste=match.dif_absoluta.iloc[0] if len(match) else np.nan,ANTES_pct_restante=match.efeito_restante_pct_do_nominal.iloc[0] if len(match) else np.nan))
    pd.DataFrame(b9rows).to_csv(out/'antes_depois_B9_mecanismos.csv',index=False)
    groups=[];params=[];integridade=[];somas=[]
    oldpar=pd.read_csv(T/'modelo_07_ablacao_parametros.csv')
    oldfat=pd.read_csv(T/'modelo_10_fatorial_decomposicao.csv')
    for modelo in ['legado','mvp']:
        d=pd.read_csv(base/f'canais_{modelo}/decomposicao.csv')
        for m,g in d.groupby('metrica'):
            for nome,mask in [('portao_sem_rede',g.termo.str.contains('G')&~g.termo.str.contains('N')),('rede_sem_portao',g.termo.str.contains('N')&~g.termo.str.contains('G')),('portao_e_rede',g.termo.str.contains('G')&g.termo.str.contains('N')),('outros',~g.termo.str.contains('[GN]'))]:
                groups.append(dict(modelo=modelo,metrica=m,grupo=nome,parcela=g.loc[mask,'parcela'].sum(),pct_contraste=g.loc[mask,'pct_contraste'].sum()))
            for braco,terms in {'so_tau_inicial':['G','N','GN'],'so_tau_min':['B'],'so_p_reporte':['C'],'so_p_deteccao':['D'],'so_portao':['G'],'so_rede':['N']}.items():
                match=oldpar[(oldpar.metrica==m)&(oldpar.braco==braco)]
                params.append(dict(modelo=modelo,metrica=m,braco=braco,ANTES_pct=match.fracao_do_efeito_total_pct.iloc[0] if len(match) else np.nan,DEPOIS_pct=g[g.termo.isin(terms)].pct_contraste.sum(),DEPOIS_parcela=g[g.termo.isin(terms)].parcela.sum()))
            for nome,mask in [('SOMA_principais',g.termo.str.len()==1),('SOMA_interacoes',g.termo.str.len()>1)]:
                match=oldfat[(oldfat.metrica==m)&(oldfat.termo==nome)]
                somas.append(dict(modelo=modelo,metrica=m,termo=nome,ANTES_2x4_pct=match.pct_do_contraste.iloc[0],DEPOIS_2x5_pct=g.loc[mask,'pct_contraste'].sum(),nota='bases diferentes: GN era absorvido em A; mudança de decomposição, não mudança automática de total'))
        raw=pd.read_csv(base/f'canais_{modelo}/bruto.csv',dtype={'celula':str});raw['celula']=raw.celula.str.zfill(5)
        if modelo=='legado':
            diagonal=raw[raw.celula.str[0]==raw.celula.str[1]].copy(); diagonal['celula']=diagonal.celula.str[0]+diagonal.celula.str[2:]
            antigo_cel=pd.read_csv(T/'modelo_10_fatorial_celulas.csv',dtype={'celula':str});antigo_cel['celula']=antigo_cel.celula.str.zfill(4)
            assert set(map(tuple,diagonal[['arquivo','semente','celula']].values))==set(map(tuple,antigo_cel[['arquivo','semente','celula']].values))
            assert len(diagonal)==3072
        raw['terminal_completo']=raw.concluiu & (raw.divida_pendente==0)&(raw.reparo_pendente<1e-8)
        raw.groupby('celula').agg(exec=('terminal_completo','size'),terminais=('terminal_completo','sum'),violacoes=('violacoes','sum')).to_csv(out/f'censura_canais_{modelo}.csv')
        integridade.append(dict(etapa='canais_'+modelo,exec=len(raw),incompletas=int((~raw.terminal_completo).sum()),violacoes=int(raw.violacoes.sum())))
    pd.DataFrame(groups).to_csv(out/'atribuicao_grupos_canais.csv',index=False)
    pd.DataFrame(params).to_csv(out/'antes_depois_B9_parametros.csv',index=False)
    pd.DataFrame(somas).to_csv(out/'antes_depois_somas_fatoriais.csv',index=False)
    for name,d in [('alternativas',alt),('robustez',robust),('B9_mvp',b9[b9.configuracao!='nominal'])]:
        complete=d.concluiu & (d.dividas_pendentes==0)&(d.get('retrabalho_pendente',pd.Series(0,index=d.index)).fillna(0)<1e-8)
        integridade.append(dict(etapa=name,exec=len(d),incompletas=int((~complete).sum()),violacoes=int((d.violacoes!='[]').sum())))
    pd.DataFrame(integridade).to_csv(out/'verificacoes.csv',index=False)
    assert all(r['violacoes']==0 for r in integridade)
    # Complementa a proveniência das tabelas e arquivos lidos na consolidação.
    sources=list((T).glob('modelo_0[37]*.csv'))+list((T).glob('modelo_1[04]*.csv'))+[ROOT/'data/processed/psplib/instancias_j60.csv']
    files=list(base.rglob('*.csv'))+sources
    pd.DataFrame([dict(arquivo=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(set(files))]).to_csv(out/'hashes_evidencias.csv',index=False)
    (out/'controles.json').write_text(json.dumps(dict(max_diferenca_legado=float(maxdiff),n_legado=384,n_diagonais=3072),indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--entrada',type=Path,required=True);ap.add_argument('--rodar-b9',action='store_true');ap.add_argument('--workers',type=int,default=4);a=ap.parse_args()
    if a.rodar_b9: rodar_b9(a.entrada,a.workers)
    else: consolidar(a.entrada)
if __name__=='__main__': main()
