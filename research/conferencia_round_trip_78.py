"""Rechecagem integral dos 960 controles do desenho 78; sem parada precoce."""
import csv,json,math,time
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
import discriminante_falha as D
OUT=D.OUT/'rechecagem_round_trip'
def main():
 OUT.mkdir(exist_ok=True)
 m=json.loads((D.OUT/'manifesto_pre_execucao.json').read_text())
 for f,h in m['hashes'].items():assert D.sha(D.ROOT/f)==h,f
 selected=pd.read_csv(D.OUT/'amostra.csv',float_precision='round_trip')
 combos=sorted(set([(int(x),'adaptativa') for x in selected.ai]+[(int(x),'centralizada') for x in selected.ci]))
 refs={};literals={};literal_target=[]
 for co,path in [('00',D.REF1),('11',D.REF2)]:
  with (D.ROOT/path).open(newline='') as f:
   literals[co]={}
   for line,row in enumerate(csv.DictReader(f),2):
    if 'kind' in row and row['kind']!='GOV':continue
    key=(int(row['celula']),row['arquivo'],int(row['semente']),row['cenario'])
    literals[co][key]=(line,row)
    if co=='00' and key==(2,'j6010_1.sm',3,'adaptativa'):
     value=row['competencia_minima_inicial'];literal_target.append(dict(arquivo=path,linha=line,chave=key,campo='competencia_minima_inicial',texto_exato=value,float_nativo_hex=float(value).hex()))
  df=pd.read_csv(D.ROOT/path,float_precision='round_trip')
  if 'kind' in df:df=df[df.kind=='GOV']
  assert not df.duplicated(D.KEY).any();refs[co]=df.set_index(D.KEY)
 (OUT/'valor_literal.json').write_text(json.dumps(literal_target,indent=2))
 jobs=[(co,ce,cen,a,s) for co in ['00','11'] for ce,cen in combos for a in m['instancias'] for s in m['sementes']]
 diffs=[];stats={co:dict(exec=0,comparacoes=0,campos=[]) for co in refs};start=time.time()
 with (OUT/'bruto.csv').open('x') as f,ProcessPoolExecutor(4) as pool:
  writer=None
  for n,row in enumerate(pool.map(D.job,jobs,chunksize=1),1):
   if writer is None:writer=csv.DictWriter(f,fieldnames=list(row));writer.writeheader()
   writer.writerow(row);f.flush()
   co=row['canto'];key=tuple(row[k] for k in D.KEY);old=refs[co].loc[key];line,text=literals[co][key]
   for field,val in old.items():
    common=dict(canto=co,**dict(zip(D.KEY,key)),campo=field,linha_referencia=line,texto_exato=text[field])
    if field not in row:diffs.append(dict(**common,tipo='ausente'));continue
    new=row[field]
    if isinstance(val,(int,float,np.number)) and not isinstance(val,(bool,np.bool_)):
     a,b=float(val),float(new)
     # Native float() on the raw token independently checks the CSV parser.
     raw=float(text[field]);assert a.hex()==raw.hex() or math.isnan(a) and math.isnan(raw),(co,key,field,'parser round_trip diverge do literal')
     if a.hex()!=b.hex() and not(math.isnan(a) and math.isnan(b)):
      diffs.append(dict(**common,tipo='numero',referencia=a,obtido=b,hex_referencia=a.hex(),hex_obtido=b.hex(),delta=b-a))
    elif not(val==new or pd.isna(val) and pd.isna(new)):
     diffs.append(dict(**common,tipo='texto',referencia=str(val),obtido=str(new)))
   stats[co]['exec']+=1;stats[co]['comparacoes']+=len(old);stats[co]['campos']=list(old.index)
   if n%32==0 or n==len(jobs):print(n,'/',len(jobs),'diferencas',len(diffs),'segundos',round(time.time()-start),flush=True)
 columns=['canto',*D.KEY,'campo','linha_referencia','texto_exato','tipo','referencia','obtido','hex_referencia','hex_obtido','delta']
 dd=pd.DataFrame(diffs,columns=columns);dd.to_csv(OUT/'divergencias_todas.csv',index=False)
 summary={}
 for co,st in stats.items():
  x=dd[dd.canto==co];summary[co]={**st,'execucoes_divergentes':len(x[D.KEY].drop_duplicates()),'divergencias':len(x),'por_campo':x.groupby('campo').size().to_dict()}
 dynamic=['makespan','TW','TL','TU','TR','taxa_falha_efetiva','p1_omissao','N_req']
 dynamic_diffs=dd[dd.campo.isin(dynamic)]
 result=dict(aprovado=not len(dd),escopo='Todos os controles dos 21 pares pre-registrados: 30 perfis/bracos unicos x 4 instancias x 4 sementes x 2 cantos; nao a grade inteira de 81 perfis',N_exec=len(jobs),resumo=summary,campos_dinamicos=dynamic,N_divergencias_dinamicas=len(dynamic_diffs),somente_competencia_minima_inicial=bool(len(dd) and set(dd.campo)=={'competencia_minima_inicial'}),parser_round_trip_igual_float_literal=True,protegidos_inalterados={f:D.sha(D.ROOT/f)==m['hashes'][f] for f in m['protected']})
 assert all(result['protegidos_inalterados'].values())
 (OUT/'resumo.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
