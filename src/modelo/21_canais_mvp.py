"""Fatorial 2^5: portão G, rede N, limiar B, reporte C, detecção D.

Nunca escolher melhor configuração. Instância é a unidade de resumo; sementes
são réplicas internas pareadas. Legado e MVP publicados separadamente.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import yaml
from scipy import stats
sys.path.insert(0,str(Path(__file__).resolve().parent))
import simulador as S
from simulador_mvp import SimulacaoMVP, OpcoesMVP
ROOT=Path(__file__).resolve().parents[2]
FATORES='GNBCD'
CELULAS=[''.join(map(str,c)) for c in itertools.product([0,1],repeat=5)]
METRICAS=['taxa_falha_efetiva','atraso_relativo','E_total','TW','TL','TU','TR','taxa_omissao','retrabalho_sobre_plano','divida_latente_sobre_plano','S_UR_maximo','n_com_erro']

class RedeSeparada(S.Simulacao):
    def __init__(self,*args,tau_rede,**kwargs):
        self.tau_rede=tau_rede
        super().__init__(*args,**kwargs)
    def multiplicadores(self,a,P):
        anterior=a.confianca
        try:
            a.confianca=self.tau_rede
            return super().multiplicadores(a,P)
        finally: a.confianca=anterior


def matriz():
    cols=['intercepto']+[''.join(x) for k in range(1,6) for x in itertools.combinations(FATORES,k)]
    M=[]
    for c in CELULAS:
        bits=dict(zip(FATORES,map(int,c)))
        M.append([1. if t=='intercepto' else np.prod([bits[l] for l in t]) for t in cols])
    return np.array(M),cols


def rodar_job(job):
    modelo,arq,celula,n_sementes=job
    par=S.carregar_parametros(); central=par['cenarios']['centralizada']; adap=par['cenarios']['adaptativa']
    novo=copy.deepcopy(central)
    for bit,chave in zip(celula[2:],['tau_min','p_reporte','p_deteccao']):
        if bit=='1': novo[chave]=copy.deepcopy(adap[chave])
    g=S.v((adap if celula[0]=='1' else central)['tau_inicial'])
    n=S.v((adap if celula[1]=='1' else central)['tau_inicial'])
    novo['tau_inicial']['valor']=g; par['cenarios']['celula']=novo
    tarefas,disp,cpm=S.carregar_instancia(arq)
    rows=[]
    for sem in range(n_sementes):
        if modelo=='legado': sim=RedeSeparada(tarefas,disp,cpm,par,'celula',sem,tau_rede=n)
        else:
            op=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
            op.update(tau_portao=g,tau_rede=n)
            sim=SimulacaoMVP(tarefas,disp,cpm,par,'celula',sem,opcoes=OpcoesMVP(**op))
        r=sim.executar()
        rows.append(dict(modelo=modelo,arquivo=arq,celula=celula,semente=sem,
                         atraso_relativo=r.makespan/r.makespan_cpm,
                         **{m:getattr(r,m) for m in METRICAS if m!='atraso_relativo'},
                         concluiu=r.concluiu,divida_pendente=len(sim.divida_pendente),
                         reparo_pendente=r.contadores.get('retrabalho_pendente',0.),
                         violacoes=len(r.violacoes),p2_ajuda=r.contadores['p2_ajuda']))
    return rows


def analisar(d,out):
    M,cols=matriz(); inv=np.linalg.inv(M); saida=[]; diagonais=[]
    for modelo,g in d.groupby('modelo'):
        for m in METRICAS:
            tab=g.groupby(['celula','arquivo'])[m].mean().unstack('arquivo').reindex(CELULAS)
            B=inv@tab.values; contraste=tab.loc['11111'].values-tab.loc['00000'].values
            assert np.max(np.abs(B[1:].sum(0)-contraste))<1e-7
            for j,termo in enumerate(cols[1:],1):
                x=B[j]; n=len(x); se=np.std(x,ddof=1)/np.sqrt(n); ci=stats.t.ppf(.975,n-1)*se
                pct=100*x.mean()/contraste.mean() if abs(contraste.mean())>1e-12 else np.nan
                saida.append(dict(modelo=modelo,metrica=m,termo=termo,parcela=x.mean(),ic95_inf=x.mean()-ci,ic95_sup=x.mean()+ci,pct_contraste=pct,n_instancias=n))
            # Restrição G=N reproduz o fatorial de quatro fatores: A agrega G,N,GN.
            for k in range(1,5):
                for tt in itertools.combinations('ABCD',k):
                    termo=''.join(tt)
                    if 'A' in termo:
                        resto=termo.replace('A',''); nomes=['G'+resto,'N'+resto,'GN'+resto]
                    else: nomes=[termo]
                    efeito=sum(B[cols.index(nome)] for nome in nomes)
                    diagonais.append(dict(modelo=modelo,metrica=m,termo=termo,parcela=efeito.mean(),pct_contraste=100*efeito.mean()/contraste.mean() if abs(contraste.mean())>1e-12 else np.nan))
    df=pd.DataFrame(saida); df.to_csv(out/'decomposicao.csv',index=False)
    diag=pd.DataFrame(diagonais); diag.to_csv(out/'diagonais.csv',index=False)
    antigo=pd.read_csv(ROOT/'outputs/tables/modelo_10_fatorial_decomposicao.csv')
    antigo=antigo[~antigo.termo.str.startswith('SOMA')][['metrica','termo','parcela_media','pct_do_contraste']]
    comp=diag.merge(antigo,on=['metrica','termo'],validate='many_to_one')
    comp=comp.rename(columns={'parcela_media':'ANTES_parcela_publicada','pct_do_contraste':'ANTES_pct_publicado','parcela':'DEPOIS_parcela','pct_contraste':'DEPOIS_pct'})
    comp['delta_parcela']=comp.DEPOIS_parcela-comp.ANTES_parcela_publicada
    comp['delta_pct']=comp.DEPOIS_pct-comp.ANTES_pct_publicado
    comp.to_csv(out/'antes_depois_fatorial.csv',index=False)
    # Checagem nominal com dados anteriores é válida somente no legado.
    old=pd.read_csv(ROOT/'outputs/tables/modelo_10_fatorial_celulas.csv',dtype={'celula':str})
    legacy=d[(d.modelo=='legado') & (d.celula.str[0]==d.celula.str[1])].copy()
    checks={}
    if len(legacy):
        legacy['celula']=legacy.celula.str[0]+legacy.celula.str[2:]
        old['celula']=old.celula.str.zfill(4)
        join=legacy.merge(old,on=['arquivo','semente','celula'],suffixes=('_novo','_antigo'),validate='one_to_one')
        checks['n_diagonais_comparadas']=len(join)
        checks['max_diferenca_diagonais']=max(float((join[m+'_novo']-join[m+'_antigo']).abs().max()) for m in METRICAS if m in old.columns)
        checks['metricas_sem_baseline_historico']=[m for m in METRICAS if m not in old.columns]
        if checks['max_diferenca_diagonais']>1e-8: raise AssertionError(checks)
    checks.update(exec=len(d),incompletas=int((~d.concluiu).sum()),violacoes=int(d.violacoes.sum()),max_divida=int(d.divida_pendente.max()),max_reparo=float(d.reparo_pendente.max()))
    (out/'verificacoes.json').write_text(json.dumps(checks,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--modelo',choices=['legado','mvp'],required=True);ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--workers',type=int,default=4)
    args=ap.parse_args(); args.saida.mkdir(parents=True,exist_ok=False)
    todas=sorted(pd.read_csv(ROOT/'data/processed/psplib/tarefas_j60_com_di.csv').arquivo.unique())
    inst=todas[::max(1,len(todas)//16)][:16]
    arquivos=['src/modelo/simulador.py','src/modelo/simulador_mvp.py','src/modelo/fuzzy.py','src/modelo/21_canais_mvp.py','config/parametros.yaml','config/mvp.yaml','config/parametros_derivados.yaml','data/processed/psplib/tarefas_j60_com_di.csv']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in arquivos}
    (args.saida/'manifesto.json').write_text(json.dumps(dict(modelo=args.modelo,instancias=inst,sementes=list(range(12)),celulas=CELULAS,hashes=hashes,opcoes=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']),indent=2)+'\n')
    jobs=[(args.modelo,a,c,12) for c in CELULAS for a in inst]
    rows=[]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for i,r in enumerate(pool.map(rodar_job,jobs)):
            rows.extend(r)
            if (i+1)%32==0: print(f'{args.modelo}: {i+1}/{len(jobs)} blocos',flush=True)
    d=pd.DataFrame(rows);d.to_csv(args.saida/'bruto.csv',index=False)
    assert hashes=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in arquivos},'fonte mudou durante execução'
    analisar(d,args.saida)
if __name__=='__main__':main()
