"""P1/P2: reanálise observacional; não reexecuta nem modifica o simulador."""
import hashlib,json,sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'research/lote41'))
from rotulagem import publicar
src=ROOT/'outputs/diagnosticos/lote41_B2_censura_20260918';out=ROOT/'outputs/diagnosticos/B2_rotulagem_20260919'
# Preservar artefatos históricos e publicar versões explicitamente rotuladas.
for name in ['celulas_IC95','contraste_A_menos_C_IC95']:
    d=pd.read_csv(src/(name+'.csv'));x=publicar(d,out/(name+'.csv'))
    assert x.loc[x.censuradas>0,'valor_rotulado'].str.contains('CENSURADO').all()
    pd.testing.assert_frame_equal(d,x[d.columns])
raw=pd.read_csv(src/'bruto.csv');bad=raw[~raw.concluiu]
assert len(bad)==36 and bad.cenario.eq('centralizada').all() and bad.s_transicao.eq(.01).all() and bad.tau_sat.ge(1).all()
keys=['etapa','canal','tau_sat','cenario','arquivo','semente'];rows=[]
for s in [.25,.6]:
    lookup=raw[raw.s_transicao==s].set_index(keys)
    for row in bad.to_dict('records'):
        alt=lookup.loc[tuple(row[k] for k in keys)];assert alt.concluiu
        rows.append({**{k:row[k] for k in keys},'s_antes':.01,'s_depois':s,'concluiu_antes':False,'concluiu_depois':bool(alt.concluiu),'fracao_porta1_depois':alt.fracao_porta1,'N_req_depois':alt.N_req})
pd.DataFrame(rows).to_csv(out/'validacao_cruzada_rotas.csv',index=False)
raw.groupby(['etapa','canal','cenario','tau_sat','s_transicao']).agg(N=('concluiu','size'),completas=('concluiu','sum')).to_csv(out/'completude.csv')
f=src/'bruto.csv';(out/'verificacoes.json').write_text(json.dumps(dict(incompletas=36,contrapartes_suaves=72,contrapartes_completas=72,metricas_numericas_preservadas=True,rotulos_censura_verificados=True,fonte_sha256=hashlib.sha256(f.read_bytes()).hexdigest()),indent=2)+'\n')
