"""Experimento independente 78. Não importa runners nem análises anteriores."""
import sys, json, csv, hashlib, random, platform, subprocess, math, time
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import asdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import scipy
from scipy.stats import t
import yaml
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP, OpcoesMVP
OUT=ROOT/'outputs/diagnosticos/20260922_discriminante_falha'
REPORT=ROOT/'projeto/78_CAUSA_DA_FALHA_EFETIVA_NA_V2.md'
FACT=['tau_inicial','tau_min','p_reporte','p_deteccao']
REF1='outputs/diagnosticos/SAT_GOV_20260919/bruto.csv'
REF2='outputs/diagnosticos/20260921_nominal_v2/governanca/bruto.csv'
SOURCE='outputs/diagnosticos/20260922_auditoria_v2/governanca_falha_positiva.csv'
PROFILES='outputs/diagnosticos/SAT_GOV_20260919/GOV_perfis.csv'
CORNERS={'00':('limiar','constante'),'10':('logistico','constante'),'01':('limiar','logistica'),'11':('logistico','logistica')}
KEY=['celula','arquivo','semente','cenario']
def read(p): return pd.read_csv(ROOT/p,float_precision='round_trip')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    assert not REPORT.exists(), 'Não sobrescrever o pré-registro'
    prof=read(PROFILES).set_index('celula'); src=read(SOURCE).sort_values(['ai','ci']).reset_index(drop=True)
    raw=read(REF2); means=raw[raw.cenario=='adaptativa'].pivot(index=['arquivo','semente'],columns='celula',values='taxa_falha_efetiva')
    ordered=[]
    for ai,a in prof.iterrows():
        for ci,c in prof.iterrows():
            if ai!=ci and a.tau_inicial>=c.tau_inicial and a.tau_min<=c.tau_min and a.p_reporte>=c.p_reporte and a.p_deteccao>=c.p_deteccao: ordered.append((ai,ci))
    pos={(a,c) for a,c in ordered if (means[a]-means[c]).groupby('arquivo').mean().mean()>0}
    assert len(ordered)==1215 and len(pos)==643 and pos==set(zip(src.ai,src.ci))
    seed=20260922; selected=src.iloc[random.Random(seed).sample(range(len(src)),20)].copy()
    selected['referencia_nominal']=False
    nominal={}
    params=S.carregar_parametros()
    for label,cen in [('ai','adaptativa'),('ci','centralizada')]:
        vals=[float(S.v(params['cenarios'][cen][k])) for k in FACT]
        match=prof[np.isclose(prof[FACT].to_numpy(),vals,rtol=0,atol=1e-14).all(axis=1)]
        assert len(match)==1;nominal[label]=int(match.index[0])
    assert not ((selected.ai==nominal['ai'])&(selected.ci==nominal['ci'])).any()
    selected=pd.concat([selected,pd.DataFrame([{**nominal,'referencia_nominal':True}])],ignore_index=True)
    selected['par']=['amostra_%02d'%i for i in range(1,21)]+['nominal']
    for prefix,col in [('A','ai'),('C','ci')]:
        for f in FACT:selected[f'{prefix}_{f}']=[prof.loc[int(i),f] for i in selected[col]]
    selected.to_csv(OUT/'amostra.csv',index=False)
    instances=sorted(raw.arquivo.unique()); seeds=sorted(int(x) for x in raw.semente.unique())
    assert len(instances)==4 and seeds==[0,1,2,3]
    protected=['config/mvp.yaml','config/mvp_v1.yaml','config/parametros.yaml','config/parametros_derivados.yaml']+[str(p.relative_to(ROOT)) for p in (ROOT/'src/modelo').glob('*.py')]
    files=protected+[REF1,REF2,SOURCE,PROFILES,'data/processed/psplib/tarefas_j60_com_di.csv','data/processed/psplib/instancias_j60.csv','research/discriminante_falha.py']
    manifest=dict(preregistro_utc=datetime.now(timezone.utc).isoformat(),seed_amostra=seed,algoritmo='random.Random(seed).sample sobre ai,ci ordenados',instancias=instances,sementes=seeds,nominal=nominal,cantos=CORNERS,commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),python=sys.version,platform=platform.platform(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__,opcoes=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes'],hashes={f:sha(ROOT/f) for f in files},protected=protected)
    (OUT/'manifesto_pre_execucao.json').write_text(json.dumps(manifest,indent=2))
    pre='''# 78 — Causa da falha efetiva na v2: teste discriminante

## Pré-registro — escrito antes de qualquer execução deste experimento

Clone independente `~/TCC2_discriminante`; execução no Mac autorizada pela autora em substituição ao Windows. Nenhum ajuste de parâmetros, alteração dos dois YAML nominais ou operação de publicação Git.

**Desenho:** 20 pares sorteados sem reposição dos 643 com contraste positivo na v2 (universo recontado independentemente), mais o par nominal. Semente 20260922, `random.Random.sample` sobre pares ordenados por `ai,ci`; seleção integral em `amostra.csv`. Quatro instâncias e sementes 0–3 da grade original. Canto 00 = limiar/constante; 10 = logístico/constante; 01 = limiar/logística; 11 = logístico/logística. Todas as demais opções vêm de `config/mvp.yaml`; instrumentação de tarefas desativada como nas grades. Execuções repetidas de um mesmo perfil/braço são reutilizadas entre pares, sem tratá-las como replicações adicionais.

**Porta de validade:** reexecutar primeiro 00 e 11; comparar TODOS os campos arquivados por chave, usando `float.hex()` nos números e igualdade nos demais, com leitura `float_precision='round_trip'`. Qualquer divergência interrompe o teste antes de interpretar e antes dos cantos mistos. Sem tolerância numérica. Censura ou violações impedem conclusão mecanística irrestrita.

### Hipóteses e resultados que as confirmariam ou derrubariam

Seja Dgf = falha adaptativa − centralizada no canto gf; negativo favorece adaptativa. Chamaremos inversão v1→v2 apenas D00<0 e D11>0; pares já positivos em 00 não são novas inversões. Sinal pontual e IC serão apresentados separadamente. IC que contém zero implica incerteza; não prova ausência de efeito.

- **H1 (assistência melhora o centralizado):** sustenta-se por célula se abrir apenas assistência eleva D (D10−D00>0), reduz a falha centralizada e essa redução é maior que a adaptativa; N_req/N_success centralizados devem crescer. É suficiente para inversão se D00<0<D10. Derrubada como explicação dessa célula se D10 não aumenta D ou se o deslocamento vem só do adaptativo piorando, sem melhora centralizada. IC95 do efeito e mudanças por braço medem a força da evidência. Repetir efeito da assistência com fuga ligada (D11−D01).
- **H2 (fuga altera o denominador/seleção de tarefas):** requer que ligar fuga mude o denominador real da taxa e as tarefas executadas, e desloque D em direção positiva. O código lido antes da execução define o denominador como `len(tarefas)` da instância: se a contagem continuar fixa e todas as tarefas terminarem, H2 é derrubada **na forma proposta**, mesmo que a fuga tenha efeitos no numerador, no tempo ou na porta de execução. Registrar numerador, denominador, conjunto de IDs executados e concluídos nos quatro cantos. Não confundir adiamentos com novas tarefas.
- **H3 (só os dois juntos):** sustenta-se descritivamente quando D00<0, D10<=0, D01<=0 e D11>0. Cai como necessidade conjunta se algum canto isolado já inverte. Estimar interação J=D11−D10−D01+D00 com IC95: só IC inteiramente positivo sustenta sinergia positiva; cruzamento apenas no canto conjunto pode ser soma de efeitos, não interação demonstrada. Se IC incluir zero, interação permanece inconclusiva.

**Análise:** para cada par e canto, diferença pareada por (arquivo,semente); média das quatro sementes por instância; IC t de Student com 4 instâncias, 3 graus de liberdade. Mesma construção para efeitos fatoriais, interação e mudanças por braço. Não usar 16 sementes como N independente. IC95 individuais, sem correção de multiplicidade. Os 20 pares foram selecionados pelo desfecho na mesma grade: análise diagnóstica condicionada, não nova validação nem estimativa da prevalência de inversões. Não agregar pares como observações independentes.

**Leituras:** taxa de falha=(n_com_erro+n_reportadas)/n_tarefas; número executado = tarefas com início registrado, com confirmação por p1_omissao+p3_analitica. Fração P1 = omissões/(omissões+analíticas); fração de fuga = fugas/(fugas+omissões+analíticas), excluindo tentativas P2; publicar também fugas/(fugas+omissões). Pedidos N_req, sucessos N_success, insucessos N_fail, bloqueios prévios N_blocked. Bateria média = média temporal dos estados médios dos agentes registrados ao fim de cada período, com igual peso por execução/instância, não um pool que sobrepese execuções longas. Confiança final = média dos agentes ao término.

**Limite de atribuição:** assistência e fuga usam um mesmo fluxo auxiliar; mudar um canto muda o consumo subsequente desse fluxo, e decisões afetam o fluxo principal por realimentação. Sementes comuns garantem replicação, não alinhamento de sorteios por evento. O fatorial identifica o efeito da troca de opções na implementação, não isola mediação por cada evento.

**Ambiente:** NumPy/pandas alinhados ao requirements; SciPy 1.18.1 para IC, pois scipy==1.15.3 exige numpy<2.5 e o requirements fixa numpy==2.5.2. Não foi alterado o requirements. Versões exatas e hashes em manifesto_pre_execucao.json.

## Resultados

PENDENTES — pré-registro preservado em `protocolo_pre_execucao.md` e por hash.
'''
    REPORT.write_text(pre);(OUT/'protocolo_pre_execucao.md').write_text(pre)
    manifest['hash_protocolo']=sha(REPORT);(OUT/'manifesto_pre_execucao.json').write_text(json.dumps(manifest,indent=2))
    print('PREREGISTRADO',manifest['preregistro_utc'], 'pares',len(selected),flush=True)
def job(arg):
    corner,cell,cen,arquivo,seed=arg
    prof=read(PROFILES).set_index('celula').loc[cell]
    params=S.carregar_parametros()
    for f in FACT: params['cenarios'][cen][f]['valor']=float(prof[f])
    options=yaml.safe_load((ROOT/'config/mvp.yaml').read_text())['opcoes']
    options.update(portao_assistencia=CORNERS[corner][0],regra_fuga=CORNERS[corner][1],instrumentar_tarefas=False)
    g,d,c=S.carregar_instancia(arquivo)
    sim=SimulacaoMVP(g,d,c,params,cen,seed,opcoes=OpcoesMVP(**options));r=sim.executar()
    row={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))};row.update(r.contadores)
    den=row['p1_omissao']+row['p3_analitica'];p1=row['p1_omissao']+row['p1_fuga']
    row.update(canto=corner,celula=cell,cenario=cen,arquivo=arquivo,semente=seed,kind='GOV',violacoes=len(r.violacoes),atraso_relativo=r.makespan/r.makespan_cpm,fracao_porta1=row['p1_omissao']/den if den else np.nan,n_selecoes_p1=p1,fracao_fuga_p1=row['p1_fuga']/p1 if p1 else np.nan,fracao_fuga=row['p1_fuga']/(den+row['p1_fuga']) if den+row['p1_fuga'] else np.nan,bateria_media=float(np.mean(r.trajetorias['bateria_media'])),denominador_falha=len(sim.tarefas),numerador_falha=r.n_com_erro+r.n_reportadas,n_executadas=sum(x.inicio is not None for x in sim.tarefas.values()),n_concluidas=sum(x.estado.startswith('concluida') for x in sim.tarefas.values()),ids_executadas=';'.join(str(j) for j,x in sorted(sim.tarefas.items()) if x.inicio is not None),ids_concluidas=';'.join(str(j) for j,x in sorted(sim.tarefas.items()) if x.estado.startswith('concluida')))
    assert row['N_req']==row['N_success']+row['N_fail']
    assert row['n_executadas']==den
    assert float(row['taxa_falha_efetiva']).hex()==float(row['numerador_falha']/row['denominador_falha']).hex()
    return row

def run(phase):
    manifest=json.loads((OUT/'manifesto_pre_execucao.json').read_text())
    for f,h in manifest['hashes'].items(): assert sha(ROOT/f)==h, f+' mudou'
    assert sha(OUT/'protocolo_pre_execucao.md')==manifest['hash_protocolo']
    selection=pd.read_csv(OUT/'amostra.csv'); combos=sorted(set([(int(x),'adaptativa') for x in selection.ai]+[(int(x),'centralizada') for x in selection.ci]))
    corners=['00','11'] if phase=='controles' else ['10','01']
    if phase!='controles':assert json.loads((OUT/'identidade.json').read_text())['aprovado']
    refs={}
    if phase=='controles':
        for corner,path in [('00',REF1),('11',REF2)]:
            d=read(path)
            if 'kind' in d:d=d[d.kind=='GOV']
            assert not d.duplicated(KEY).any();refs[corner]=d.set_index(KEY)
    jobs=[(co,ce,cen,a,s) for co in corners for ce,cen in combos for a in manifest['instancias'] for s in manifest['sementes']]
    checks={co:dict(exec=0,comparacoes=0,campos=[]) for co in corners};start=time.time()
    with (OUT/f'bruto_{phase}.csv').open('x') as file, ProcessPoolExecutor(max_workers=4) as pool:
        writer=None
        for n,row in enumerate(pool.map(job,jobs,chunksize=1),1):
            if writer is None:writer=csv.DictWriter(file,fieldnames=list(row));writer.writeheader()
            writer.writerow(row);file.flush()
            if phase=='controles':
                corner=row['canto'];ref=refs[corner].loc[tuple(row[k] for k in KEY)];diff=[]
                for f,old in ref.items():
                    if f not in row:diff.append(dict(campo=f,motivo='campo ausente'));continue
                    new=row[f]
                    if isinstance(old,(int,float,np.number)) and not isinstance(old,(bool,np.bool_)):
                        a,b=float(old),float(new);ok=a.hex()==b.hex() or math.isnan(a) and math.isnan(b)
                        if not ok:diff.append(dict(campo=f,referencia=a,obtido=b,hex_referencia=a.hex(),hex_obtido=b.hex(),delta=b-a))
                    elif not (old==new or pd.isna(old) and pd.isna(new)):diff.append(dict(campo=f,referencia=str(old),obtido=str(new)))
                checks[corner]['exec']+=1;checks[corner]['comparacoes']+=len(ref);checks[corner]['campos']=list(ref.index)
                if diff:
                    failure=dict(aprovado=False,canto=corner,chave={k:row[k] for k in KEY},divergencias=diff,contagens=checks)
                    (OUT/'identidade.json').write_text(json.dumps(failure,indent=2))
                    with REPORT.open('a') as f:f.write('\n\n**INTERROMPIDO: controle de identidade DIVERGENTE.** Não interpretar hipóteses. Detalhes em identidade.json.\n'+json.dumps(failure,ensure_ascii=False,indent=2)+'\n')
                    print('CONTROLE FALHOU',json.dumps(failure),flush=True);pool.shutdown(wait=False,cancel_futures=True);raise SystemExit(2)
            if n%32==0 or n==len(jobs):print(phase,n,'/',len(jobs),'segundos',round(time.time()-start),flush=True)
    for f in manifest['protected']: assert sha(ROOT/f)==manifest['hashes'][f]
    if phase=='controles':(OUT/'identidade.json').write_text(json.dumps(dict(aprovado=True,contagens=checks),indent=2))
    print('FASE CONCLUIDA',phase,flush=True)

if __name__=='__main__':
    if sys.argv[1]=='preparar':prepare()
    else:run(sys.argv[1])
