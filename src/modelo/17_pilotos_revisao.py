"""Pilotos previamente definidos em research/PLANO_REVISAO.md. Modelo nominal intacto.

Cada etapa grava execuções individuais, configuração e hashes. Recusa sobrescrita.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import platform
import time
from pathlib import Path
import numpy as np
import pandas as pd
import yaml

spec=importlib.util.spec_from_file_location('hm',Path(__file__).with_name('04_gemeo_identico.py'))
hm=importlib.util.module_from_spec(spec); spec.loader.exec_module(hm)
S=hm.S


class RedeSeparada(S.Simulacao):
    """Intervenção experimental: confiança da rede separada do portão, sem RNG novo."""
    def __init__(self,*args,confianca_rede=None,**kwargs):
        self.confianca_rede=confianca_rede
        super().__init__(*args,**kwargs)

    def multiplicadores(self,agente,P):
        if self.confianca_rede is None:
            return super().multiplicadores(agente,P)
        # Usa a implementação nominal; restaura imediatamente o valor do portão.
        antes=agente.confianca
        try:
            agente.confianca=self.confianca_rede
            return super().multiplicadores(agente,P)
        finally:
            agente.confianca=antes


def estatisticas(d):
    """Estimando: média esperada do conjunto fixo, sementes pareadas entre instâncias."""
    result={}
    for o in hm.OBSERVAVEIS:
        paired=d.pivot(index='semente',columns='instancia',values=o)
        assert not paired.isna().any().any()
        result['media_'+o]=float(d[o].mean())
        result['var_legado_'+o]=float(d[o].var(ddof=1)/len(d))
        result['var_pareada_'+o]=float(paired.mean(axis=1).var(ddof=1)/len(paired))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('etapa',choices=['produto','ruido','cobertura','confianca','vertices'])
    parser.add_argument('--saida',type=Path,required=True)
    args=parser.parse_args(); out=args.saida; out.mkdir(parents=True,exist_ok=False)
    inputs=[Path(__file__),Path(__file__).with_name('04_gemeo_identico.py'),Path(S.__file__),
            Path(S.__file__).with_name('fuzzy.py')]
    inputs+=list((hm.RAIZ/'config').glob('*.yaml'))+list((hm.RAIZ/'data/processed/psplib').glob('*.csv'))
    inputs+=list(hm.TAB.glob('modelo_04_*.csv'))+[hm.RAIZ/'research/PLANO_REVISAO.md']
    hashes={str(p.relative_to(hm.RAIZ)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    manifest={'etapa':args.etapa,'python':platform.python_version(),'numpy':np.__version__,
              'pandas':pd.__version__,'pyyaml':yaml.__version__,'hashes':hashes,
              'criterio':'PLANO_REVISAO.md; piloto não valida identificabilidade nem generalização'}
    (out/'manifesto.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    par=S.carregar_parametros(); insts=hm.instancias(); cache={}; rows=[]; start=time.monotonic()

    def run(label,x,seeds,instances=insts,cen=hm.CENARIO,gate=None,network=None,nominal=False):
        p=hm.aplicar(par,x)
        if gate is not None: p['cenarios'][cen]['tau_inicial']['valor']=gate
        for arq in instances:
            if arq not in cache: cache[arq]=S.carregar_instancia(arq)
            g,disp,cpm=cache[arq]
            for seed in seeds:
                cls=S.Simulacao if nominal else RedeSeparada
                extra={} if nominal else {'confianca_rede':network}
                sim=cls(g,disp,cpm,p,cen,semente=int(seed),**extra)
                before=[a.confianca for a in sim.agentes]
                result=sim.executar()
                assert before==[a.confianca for a in sim.agentes]
                vals={o:float(result.makespan/result.makespan_cpm if o=='atraso_relativo' else getattr(result,o)) for o in hm.OBSERVAVEIS}
                rows.append(dict(grupo=label,instancia=arq,semente=int(seed),**x,**vals,
                                 TL=result.TL,TU=result.TU,TW=result.TW,TR=result.TR,
                                 concluiu=result.concluiu,divida_pendente=len(sim.divida_pendente),
                                 violacoes=len(result.violacoes),makespan=result.makespan,
                                 tau_portao=gate,tau_rede=network))
        print(label,'execuções acumuladas',len(rows),flush=True)

    if args.etapa=='produto':
        for F in [.12,.18,.24]:
            x=dict(hm.VERDADE); x['risco.F_ancora']=F; x['retrabalho.f_retrabalho']=.0756/F
            run(f'F={F}',x,range(32))
    elif args.etapa=='ruido':
        a=pd.read_csv(hm.TAB/'modelo_04_hm_onda1.csv').sort_values('ponto')
        for i in np.linspace(0,len(a)-1,8,dtype=int): run(f'ponto={i}',a.iloc[i][hm.NOMES].to_dict(),range(32))
    elif args.etapa=='cobertura':
        for b in range(20):
            run(f'sim={b}',hm.VERDADE,range(1000+14*b,1004+14*b))
            run(f'obs={b}',hm.VERDADE,range(1004+14*b,1014+14*b))
    elif args.etapa=='confianca':
        todas=sorted(pd.read_csv(hm.RAIZ/'data/processed/psplib/tarefas_j60_com_di.csv').arquivo.unique())
        selected=[todas[i] for i in np.linspace(0,len(todas)-1,4,dtype=int)]
        x={sec+'.'+key:S.v(par[sec][key]) for sec,key,_,_ in hm.PARAMETROS}
        for gate,network in itertools.product([.25,.80],repeat=2):
            run(f'gate={gate};rede={network}',x,range(12),selected,cen='centralizada',gate=gate,network=network)
        for value in [.25,.80]:
            run(f'controle={value}',x,range(2),selected,cen='centralizada',gate=value,nominal=True)
        # Controle de canais no mesmo estado, antes de qualquer realimentação.
        g,disp,cpm=cache[selected[0]]
        a=RedeSeparada(g,disp,cpm,par,'centralizada',semente=0,confianca_rede=.25)
        b=RedeSeparada(g,disp,cpm,par,'centralizada',semente=0,confianca_rede=.80)
        ma=a.multiplicadores(a.agentes[0],.5); mb=b.multiplicadores(b.agentes[0],.5)
        assert ma[0]==mb[0] and ma[1]!=mb[1], 'A intervenção deve agir só na rede'
        (out/'controle_canais.json').write_text(json.dumps({'cognitivo_baixa':ma[0],'cognitivo_alta':mb[0],
                                                          'rede_baixa':ma[1],'rede_alta':mb[1]},indent=2)+'\n')
    else:
        for i,point in enumerate(itertools.product(*[(lo,hi) for _,_,lo,hi in hm.PARAMETROS])):
            run(f'vertice={i}',dict(zip(hm.NOMES,point)),range(2))
    d=pd.DataFrame(rows); d.to_csv(out/'bruto.csv',index=False)
    summaries=[]
    for group,g in d.groupby('grupo',sort=False):
        summaries.append(dict(grupo=group,n=len(g),**estatisticas(g)))
    pd.DataFrame(summaries).to_csv(out/'resumo.csv',index=False)
    controls={}
    if args.etapa=='confianca':
        cols=hm.OBSERVAVEIS+['TL','TU','TW','TR','makespan','concluiu','divida_pendente','violacoes']
        for value in [.25,.80]:
            a=d[d.grupo==f'controle={value}'].sort_values(['instancia','semente'])
            b=d[(d.grupo==f'gate={value};rede={value}')&(d.semente<2)].sort_values(['instancia','semente'])
            controls[str(value)]=bool(np.array_equal(a[cols].to_numpy(),b[cols].to_numpy()))
        assert all(controls.values()),'Intervenção alterou a diagonal nominal'
    checks={'n_execucoes':len(d),'tarefas_incompletas':int((~d.concluiu).sum()),
            'execucoes_com_divida':int((d.divida_pendente>0).sum()),'violacoes':int(d.violacoes.sum()),
            'controles_nominais':controls,'segundos':time.monotonic()-start,
            'fontes_preservadas':all(hashlib.sha256((hm.RAIZ/p).read_bytes()).hexdigest()==h for p,h in hashes.items())}
    (out/'verificacoes.json').write_text(json.dumps(checks,indent=2)+'\n')
    assert checks['fontes_preservadas']
    print(json.dumps(checks,indent=2),flush=True)


if __name__=='__main__': main()
