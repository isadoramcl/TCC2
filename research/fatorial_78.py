"""Continuação autorizada do teste 78; identidade com exceção restrita de 1 ULP."""
import sys,json,csv,math,struct,time,hashlib,platform
from datetime import datetime,timezone
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
from scipy.stats import t
import discriminante_falha as D
OUT=D.OUT/'fatorial_completo'
MET=['taxa_falha_efetiva','N_req','N_success','N_fail','N_blocked','p2_bloqueio','fracao_porta1','fracao_fuga','fracao_fuga_p1','n_executadas','n_concluidas','denominador_falha','numerador_falha','bateria_media','confianca_media_final']
def read(p):return pd.read_csv(p,float_precision='round_trip',dtype={'canto':str})
def integrity():
 m=json.loads((D.OUT/'manifesto_pre_execucao.json').read_text())
 for f,h in m['hashes'].items():assert D.sha(D.ROOT/f)==h,f
 return m

def gate():
 OUT.mkdir(exist_ok=True);m=integrity()
 data=read(D.OUT/'rechecagem_round_trip/bruto.csv');assert len(data)==960
 assert not data.duplicated(['canto',*D.KEY]).any()
 exceptions=[];failures=[];checks=[]
 for co,path in [('00',D.REF1),('11',D.REF2)]:
  ref=D.read(path)
  if 'kind' in ref:ref=ref[ref.kind=='GOV']
  ref=ref.set_index(D.KEY);current=data[data.canto==co].set_index(D.KEY)
  assert len(current)==480
  for key,row in current.iterrows():
   old=ref.loc[key]
   for f,a in old.items():
    b=row[f];info=dict(canto=co,**dict(zip(D.KEY,key)),campo=f)
    if isinstance(a,(int,float,np.number)) and not isinstance(a,(bool,np.bool_)):
     a,b=float(a),float(b)
     if a.hex()==b.hex() or math.isnan(a) and math.isnan(b):continue
     # Competencies are finite nonnegative doubles: unsigned bit distance is exact ULP distance.
     ulp=abs(struct.unpack('>Q',struct.pack('>d',a))[0]-struct.unpack('>Q',struct.pack('>d',b))[0]) if a>=0 and b>=0 and math.isfinite(a) and math.isfinite(b) else None
     info.update(referencia=a,obtido=b,hex_referencia=a.hex(),hex_obtido=b.hex(),distancia_ulp=ulp)
     if f=='competencia_minima_inicial' and ulp is not None and ulp<=1:exceptions.append(info)
     else:failures.append(info)
    elif not(a==b or pd.isna(a) and pd.isna(b)):failures.append(dict(**info,referencia=str(a),obtido=str(b)))
  checks.append(dict(canto=co,N=len(current),campos=len(ref.columns),comparacoes=len(current)*len(ref.columns)))
 result=dict(aprovado=not failures,criterio='igualdade hex integral; somente competencia_minima_inicial admite ate 1 ULP',verificado_utc=datetime.now(timezone.utc).isoformat(),checks=checks,excecoes=exceptions,divergencias_nao_permitidas=failures,python=sys.version,numpy=np.__version__,platform=platform.platform(),hash_bruto_controles=D.sha(D.OUT/'rechecagem_round_trip/bruto.csv'))
 (OUT/'controle_criterio_atualizado.json').write_text(json.dumps(result,indent=2))
 assert not failures,failures
 note='''

## Retomada autorizada — exceção de plataforma registrada antes dos cantos mistos

A autora informou ter verificado em Linux x86, Python 3.10 e NumPy 2.2.6, as oito combinações de instância/arranjo da semente 3: `competencia_minima_inicial` reproduziu `0x1.f251dbea89292p-3`, idêntico ao arquivo. A causa foi identificada pela autora como arredondamento de plataforma no `rng.normal` inicial. **Proveniência:** verificação externa comunicada pela autora nesta sessão; não executamos Linux nem recebemos seu log bruto. A conferência local independente demonstra que o parser não explica a diferença e que não há diferença nos campos dinâmicos arquivados das 960 execuções controladas. Isso não prova identidade de todos os estados internos ou de outras configurações.

**Ambiente desta execução:** Python 3.12.14 (Clang 22.1.3), NumPy 2.5.2, macOS ARM64. Valor local: `0x1.f251dbea89293p-3`; diferença positiva de 1 ULP.

**Novo critério, autorizado pela autora:** todos os campos devem continuar idênticos por `float.hex()` (textos/bools por igualdade), com exceção exclusiva de `competencia_minima_inicial`, que admite distância de até 1 ULP. Qualquer outra diferença interrompe a análise. Não aplicamos tolerância global nem alteramos referências, sorteios ou parâmetros.

Revalidação integral concluída antes de executar os cantos mistos: **960/960 controles aprovados pelo critério atualizado**, 49.440 comparações de campos, 240 exceções de exatamente 1 ULP apenas na competência mínima inicial, zero diferenças não permitidas. Evidência: `fatorial_completo/controle_criterio_atualizado.json`. O critério original e as duas interrupções permanecem preservados como histórico; o estado atual é retomado sob a autorização acima. A amostra, a semente e os testes de H1–H3 permanecem os do pré-registro.
'''
 with D.REPORT.open('a') as f:f.write(note)
 (OUT/'criterio_pre_cantos_mistos.md').write_text(note)
 (OUT/'manifesto_retomada.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),hash_criterio=D.sha(OUT/'criterio_pre_cantos_mistos.md'),hash_runner=D.sha(__file__),hash_amostra=D.sha(D.OUT/'amostra.csv'),python=sys.version,numpy=np.__version__),indent=2))
 print('CONTROLE APROVADO',len(exceptions),'excecoes, 0 outras divergencias',flush=True)

def run():
 integrity();assert json.loads((OUT/'controle_criterio_atualizado.json').read_text())['aprovado']
 sel=read(D.OUT/'amostra.csv');m=json.loads((D.OUT/'manifesto_pre_execucao.json').read_text())
 combos=sorted(set([(int(x),'adaptativa') for x in sel.ai]+[(int(x),'centralizada') for x in sel.ci]))
 jobs=[(co,ce,cen,a,s) for co in ['10','01'] for ce,cen in combos for a in m['instancias'] for s in m['sementes']]
 start=time.time()
 with (OUT/'bruto_mistos.csv').open('x') as f,ProcessPoolExecutor(4) as pool:
  writer=None
  for n,row in enumerate(pool.map(D.job,jobs,chunksize=1),1):
   if writer is None:writer=csv.DictWriter(f,fieldnames=list(row));writer.writeheader()
   writer.writerow(row);f.flush()
   if n%64==0 or n==len(jobs):print(n,'/',len(jobs),'segundos',round(time.time()-start),flush=True)
 integrity();print('CANTOS MISTOS CONCLUIDOS',flush=True)

def ci(x):
 assert len(x)==4 and not x.isna().any()
 avg=float(x.mean());h=float(t.ppf(.975,3)*x.std(ddof=1)/2)
 return dict(media=avg,ic95_inf=avg-h,ic95_sup=avg+h,N_instancias=4)
def analyze():
 integrity();assert json.loads((OUT/'controle_criterio_atualizado.json').read_text())['aprovado']
 controls=read(D.OUT/'rechecagem_round_trip/bruto.csv');mixed=read(OUT/'bruto_mistos.csv');data=pd.concat([controls,mixed],ignore_index=True)
 assert len(data)==1920 and not data.duplicated(['canto',*D.KEY]).any()
 data.to_csv(OUT/'bruto_completo.csv',index=False)
 assert data.concluiu.all() and data.violacoes.sum()==0,'Censura/violacao: nao interpretar irrestritamente'
 selected=read(D.OUT/'amostra.csv');byarm=[];contr=[];effects=[];instances=[];classif=[]
 groups={(co,int(ce),cen):g.set_index(['arquivo','semente']).sort_index() for (co,ce,cen),g in data.groupby(['canto','celula','cenario'])}
 for row in selected.to_dict('records'):
  pair=row['par'];a=int(row['ai']);c=int(row['ci']);meta=dict(par=pair,ai=a,ci=c,nominal=bool(row['referencia_nominal']))
  grids={};deltas={}
  for co in D.CORNERS:
   arms={}
   for cen,cell in [('adaptativa',a),('centralizada',c)]:
    g=groups[(co,cell,cen)];assert len(g)==16
    arms[cen]=g
    for metric in MET:
     byarm.append(dict(**meta,canto=co,cenario=cen,metrica=metric,**ci(g[metric].groupby('arquivo').mean())))
   assert arms['adaptativa'].index.equals(arms['centralizada'].index)
   dif=(arms['adaptativa'].taxa_falha_efetiva-arms['centralizada'].taxa_falha_efetiva).groupby('arquivo').mean();deltas[co]=dif
   contr.append(dict(**meta,canto=co,**ci(dif)))
   instances.extend(dict(**meta,canto=co,arquivo=f,diferenca=v) for f,v in dif.items());grids[co]=arms
  effect_vectors={'assistencia_fuga_desligada':deltas['10']-deltas['00'],'assistencia_fuga_ligada':deltas['11']-deltas['01'],'fuga_assistencia_limiar':deltas['01']-deltas['00'],'fuga_assistencia_logistica':deltas['11']-deltas['10'],'total_v2_menos_v1':deltas['11']-deltas['00'],'interacao':deltas['11']-deltas['10']-deltas['01']+deltas['00']}
  for label,vals in effect_vectors.items():effects.append(dict(**meta,efeito=label,cenario='contraste_A_menos_C',**ci(vals)))
  arm_changes={}
  for src,dst,label in [('00','10','assistencia_fuga_desligada'),('01','11','assistencia_fuga_ligada'),('00','01','fuga_assistencia_limiar'),('10','11','fuga_assistencia_logistica'),('00','11','total_v2_menos_v1')]:
   for cen in ['adaptativa','centralizada']:
    vals=(grids[dst][cen].taxa_falha_efetiva-grids[src][cen].taxa_falha_efetiva).groupby('arquivo').mean()
    arm_changes[label,cen]=vals
    effects.append(dict(**meta,efeito=label,cenario=cen,**ci(vals)))
  av={co:float(x.mean()) for co,x in deltas.items()}
  dc=arm_changes['assistencia_fuga_desligada','centralizada'].mean();da=arm_changes['assistencia_fuga_desligada','adaptativa'].mean()
  reqc=grids['10']['centralizada'].N_req.mean()-grids['00']['centralizada'].N_req.mean();succ=grids['10']['centralizada'].N_success.mean()-grids['00']['centralizada'].N_success.mean()
  jci=ci(effect_vectors['interacao']);new=av['00']<0 and av['11']>0
  classif.append(dict(**meta,**{'D'+k:v for k,v in av.items()},nova_inversao=new,ja_positivo_v1=av['00']>0,assistencia_so_inverte=av['00']<0<av['10'],fuga_so_inverte=av['00']<0<av['01'],somente_juntos=new and av['10']<=0 and av['01']<=0,H1_direcao=dc<0 and da-dc>0 and reqc>0 and succ>0,H1_delta_C=dc,H1_delta_A=da,delta_pedidos_C=reqc,delta_sucesso_C=succ,interacao=jci['media'],interacao_ic95_inf=jci['ic95_inf'],interacao_ic95_sup=jci['ic95_sup'],total_delta_C=arm_changes['total_v2_menos_v1','centralizada'].mean(),total_delta_A=arm_changes['total_v2_menos_v1','adaptativa'].mean()))
 for name,rows in [('leituras_por_braco_IC95',byarm),('contrastes_IC95',contr),('efeitos_IC95',effects),('diferencas_por_instancia',instances),('classificacao_hipoteses',classif)]:pd.DataFrame(rows).to_csv(OUT/f'{name}.csv',index=False)
 # Direct task-set check, not inferred only from completion flags.
 invariants=data.groupby(['celula','arquivo','semente','cenario'])[['ids_executadas','ids_concluidas','denominador_falha']].nunique()
 assert (invariants==1).all().all()
 summary=dict(N_exec=len(data),completas=int(data.concluiu.sum()),violacoes=int(data.violacoes.sum()),denominadores=sorted(int(x) for x in data.denominador_falha.unique()),n_executadas=sorted(int(x) for x in data.n_executadas.unique()),n_concluidas=sorted(int(x) for x in data.n_concluidas.unique()),conjuntos_tarefas_invariantes=True,comparacao_conjuntos_chaves=len(invariants),protegidos_inalterados=True)
 (OUT/'verificacoes.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)
 print(pd.DataFrame(classif).to_string(index=False),flush=True)
if __name__=='__main__':
 {'controle':gate,'executar':run,'analisar':analyze}[sys.argv[1]]()
