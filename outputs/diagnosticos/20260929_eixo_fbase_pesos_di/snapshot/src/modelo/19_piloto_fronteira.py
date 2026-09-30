"""Continuação dirigida ao limite do NROY; ver research/PLANO_FRONTEIRA.md."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd

sp=importlib.util.spec_from_file_location('pilotos',Path(__file__).with_name('17_pilotos_revisao.py'))
m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
hm=m.hm


def main():
    p=argparse.ArgumentParser();p.add_argument('--saida',type=Path,required=True)
    out=p.parse_args().saida;out.mkdir(parents=True,exist_ok=False)
    wave=pd.read_csv(hm.TAB/'modelo_04_hm_onda1.csv').sort_values('ponto')
    nroy=wave[wave.implausibilidade<=hm.CORTE]
    inside=nroy.iloc[np.linspace(0,len(nroy)-1,4,dtype=int)].ponto.astype(int).tolist()
    outside=wave[wave.implausibilidade>hm.CORTE].sort_values(['implausibilidade','ponto']).head(4).ponto.astype(int).tolist()
    selected=inside+outside
    inputs=[Path(__file__),Path(m.__file__),Path(hm.__file__),Path(hm.S.__file__),
            Path(hm.S.__file__).with_name('fuzzy.py'),hm.RAIZ/'research/PLANO_FRONTEIRA.md']
    inputs+=list((hm.RAIZ/'config').glob('*.yaml'))+list((hm.RAIZ/'data/processed/psplib').glob('*.csv'))
    inputs+=list(hm.TAB.glob('modelo_04_*.csv'))
    hashes={str(f.relative_to(hm.RAIZ)):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs}
    (out/'manifesto.json').write_text(json.dumps({'aceitos':inside,'rejeitados':outside,'sementes':list(range(32)),
        'instancias':hm.instancias(),'hashes':hashes},indent=2)+'\n')
    par=hm.S.carregar_parametros(); cache={f:hm.S.carregar_instancia(f) for f in hm.instancias()}
    raw=[]; summary=[];z=pd.read_csv(hm.TAB/'modelo_04_observacoes_sinteticas.csv').iloc[0]
    for point in selected:
        original=wave[wave.ponto==point].iloc[0]; x=original[hm.NOMES].to_dict(); params=hm.aplicar(par,x)
        rows=[]
        for arq,(g,disp,cpm) in cache.items():
            for seed in range(32):
                sim=hm.S.Simulacao(g,disp,cpm,params,hm.CENARIO,semente=seed); r=sim.executar()
                row=dict(retrabalho_sobre_esforco_total=r.retrabalho_sobre_esforco_total,taxa_falha_efetiva=r.taxa_falha_efetiva,ponto=point,instancia=arq,semente=seed,**x,concluiu=r.concluiu,
                         divida_pendente=len(sim.divida_pendente),violacoes=len(r.violacoes),
                         **{o:float(r.makespan/r.makespan_cpm if o=='atraso_relativo' else getattr(r,o)) for o in hm.OBSERVAVEIS})
                raw.append(row);rows.append(row)
        frame=pd.DataFrame(rows); small=m.estatisticas(frame[frame.semente<4]);large=m.estatisticas(frame)
        assert all(abs(small['media_'+o]-original['media_'+o])<1e-10 for o in hm.OBSERVAVEIS)
        for name,s,scale in [('K8_real',small,1),('K64_aproximado',small,1/8),('K64_real',large,1)]:
            for var in ['legado','pareada']:
                vals=[abs(s['media_'+o]-z['media_'+o])/np.sqrt(scale*s[f'var_{var}_{o}']+z['var_media_'+o]) for o in hm.OBSERVAVEIS]
                summary.append(dict(ponto=point,alternativa=name,variancia=var,I=max(vals),aceito=max(vals)<=hm.CORTE))
        print('ponto',point,'concluído',flush=True)
    d=pd.DataFrame(raw);d.to_csv(out/'bruto.csv',index=False);pd.DataFrame(summary).to_csv(out/'comparacao.csv',index=False)
    checks={'execucoes':len(d),'tarefas_incompletas':int((~d.concluiu).sum()),'divida_pendente':int((d.divida_pendente>0).sum()),
            'violacoes':int(d.violacoes.sum()),'hashes_preservados':all(hashlib.sha256((hm.RAIZ/f).read_bytes()).hexdigest()==h for f,h in hashes.items())}
    (out/'verificacoes.json').write_text(json.dumps(checks,indent=2)+'\n');assert checks['hashes_preservados']


if __name__=='__main__':main()
