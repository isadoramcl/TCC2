"""Testa em memória a inversão solicitada; não altera módulos/configurações."""
from pathlib import Path
import sys,types,csv,json,hashlib,time
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import pandas as pd,numpy as np,yaml
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src/modelo'))
OUT=ROOT/'outputs/diagnosticos/20260928_drenagem_heuristica/controle_previo'
import simulador as Original
from simulador_mvp import SimulacaoMVP as Old,OpcoesMVP as OldOptions

def initialize():
 global New,NewOptions
 source=(ROOT/'src/modelo/simulador.py').read_text()
 assert source.count('if k_he <= k_an:')==1
 source=source.replace('if k_he <= k_an:','if k_he > k_an:').replace('k_heuristico deve exceder k_analitico (TCC I)','k_heuristico não pode exceder k_analitico (TCC I §4.1)')
 m=types.ModuleType('controle79_legacy');m.__file__=str(ROOT/'src/modelo/simulador.py');sys.modules[m.__name__]=m;exec(compile(source,m.__file__,'exec'),m.__dict__)
 source=(ROOT/'src/modelo/simulador_mvp.py').read_text()
 assert source.count('if kh<=ka:')==1
 source=source.replace('if kh<=ka:','if kh>ka:').replace('k_heuristico deve exceder k_analitico (TCC I)','k_heuristico não pode exceder k_analitico (TCC I §4.1)').replace('from simulador import Simulacao, v','from controle79_legacy import Simulacao, v')
 m=types.ModuleType('controle79_mvp');m.__file__=str(ROOT/'src/modelo/simulador_mvp.py');sys.modules[m.__name__]=m;exec(compile(source,m.__file__,'exec'),m.__dict__);New=m.SimulacaoMVP;NewOptions=m.OpcoesMVP

def job(key):
 a,s,c=key;result=[]
 for tag,cls,optclass in [('anterior',Old,OldOptions),('checagem_invertida',New,NewOptions)]:
  p=Original.carregar_parametros();p['agentes']['k_heuristico']['valor']=.10
  options=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'];options['instrumentar_tarefas']=False
  g,d,cp=Original.carregar_instancia(a);r=cls(g,d,cp,p,c,s,opcoes=optclass(**options)).executar()
  row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))};row.update(r.contadores);den=row['p1_omissao']+row['p3_analitica'];n=den+row['p1_fuga']
  row.update(variante=tag,arquivo=a,semente=s,cenario=c,violacoes=len(r.violacoes),mensagens_violacoes=';'.join(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=row['p1_omissao']/den,fracao_fuga=row['p1_fuga']/n)
  result.append(row)
 return result

def main():
 protected=list((ROOT/'src/modelo').glob('*.py'))+list((ROOT/'config').glob('*.yaml'))
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
 ref=pd.read_csv(ROOT/'outputs/diagnosticos/20260921_nominal_v2/bruto_nominal.csv',float_precision='round_trip');cols=list(ref.select_dtypes('number').columns);assert len(ref)==384 and len(cols)==49
 keys=['arquivo','semente','cenario'];indexed=ref.set_index(keys);jobs=[(r.arquivo,int(r.semente),r.cenario) for r in ref.itertuples()]
 (OUT/'manifesto.json').write_text(json.dumps(dict(criterio='49 campos numericos por float.hex, sem excecoes novas',N=384,campos=cols,hashes=hashes,python=sys.version,numpy=np.__version__,nota='Inversao em memoria, inclusive legado; arquivos de producao preservados'),indent=2))
 allrows=[];diffs=[];beforeafter=[]
 with ProcessPoolExecutor(4,initializer=initialize) as pool:
  for i,result in enumerate(pool.map(job,jobs,chunksize=1),1):
   for row in result:
    old=indexed.loc[tuple(row[k] for k in keys)]
    for f in cols:
     a=float(row[f]);b=float(row['semente'] if f=='semente' else old[f])
     if a.hex()!=b.hex():diffs.append(dict(**{k:row[k] for k in keys},variante=row['variante'],campo=f,referencia=b,obtido=a,hex_ref=b.hex(),hex_obtido=a.hex(),delta=a-b))
   for f in cols:
    a,b=float(result[0][f]),float(result[1][f])
    if a.hex()!=b.hex():beforeafter.append(dict(**{k:result[0][k] for k in keys},campo=f,anterior=a,novo=b,delta=b-a))
   allrows.extend(result)
   if i%64==0:print(i,'/384',flush=True)
 pd.DataFrame(allrows).to_csv(OUT/'bruto.csv',index=False);pd.DataFrame(diffs).to_csv(OUT/'divergencias_referencia.csv',index=False);pd.DataFrame(beforeafter).to_csv(OUT/'divergencias_antes_depois.csv',index=False)
 assert all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in hashes.items())
 counts=pd.DataFrame(diffs).groupby(['variante','campo']).size()
 summary=dict(N_controles=384,campos=49,N_exec=768,completas=sum(r['concluiu'] for r in allrows),divergencias_referencia=[dict(variante=a,campo=b,N=int(n)) for (a,b),n in counts.items()],inversao_so_muda_campos=sorted(set(r['campo'] for r in beforeafter)),N_alteradas_pela_inversao=len(beforeafter),arquivos_protegidos_inalterados=True,criterio_identidade_satisfeito=False)
 (OUT/'resumo.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
