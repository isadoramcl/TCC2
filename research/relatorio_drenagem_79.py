"""Consolidação separada das três etapas do parecer 79."""
from pathlib import Path
import json,csv,statistics,hashlib,sys,math
import pandas as pd
from scipy.stats import t
import etapa1_drenagem_79 as E
R=E.ROOT;B=E.OUT.parent
LABEL={'v2':'v2 histórica','etapa2':'v3: kh=0,04, fuga acoplada','etapa3':'v3 final: kh=0,04, kf=0,10'}
NAMES={'atraso_relativo':'Atraso relativo','taxa_omissao':'Omissão','divida_latente_sobre_plano':'Dívida latente','taxa_falha_efetiva':'Falha efetiva','fracao_porta1':'Fração P1'}
def rd(p):return pd.read_csv(p,float_precision='round_trip')
def tab(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)+'\n'
def fmt(r):return f'{r.media:.4f} [{r.ic95_inf:.4f}; {r.ic95_sup:.4f}]'
def main():
 for stage in ['etapa2','etapa3']:
  v=json.loads((B/stage/'verificacoes.json').read_text());assert v['N']==v['completas']==4704 and v['violacoes']==0
 assert 'Ran 107 tests' in (B/'etapa3/suite_final.log').read_text() and (B/'etapa3/suite_final.log').read_text().rstrip().endswith('OK')
 ctrl=json.loads((B/'etapa3/controle_v2/controle_reconciliado.json').read_text());assert ctrl['identidade_1a'] and ctrl['guarda_1b_historico'] and not ctrl['divergencias']
 table=rd(B/'etapa3/contrastes_lado_a_lado.csv')
 # Independent aggregation: stdlib csv/statistics, paired seeds then instances.
 residuals=[]
 for stage in ['etapa2','etapa3']:
  with (B/stage/'bruto_completo.csv').open() as f:raw=list(csv.DictReader(f))
  lookup={(r['conjunto'],r['arquivo'],r['semente'],r['cenario']):r for r in raw}
  for row in table[table.versao==stage].itertuples():
   items=[r for r in raw if r['conjunto']==row.conjunto and r['cenario']=='adaptativa'];byfile={}
   for r in items:
    key=(r['conjunto'],r['arquivo'],r['semente'],'centralizada');delta=float(r[row.metrica])-float(lookup[key][row.metrica]);byfile.setdefault(r['arquivo'],[]).append(delta)
   x=[statistics.fmean(v) for v in byfile.values()];m=statistics.fmean(x);h=float(t.ppf(.975,len(x)-1))*statistics.stdev(x)/math.sqrt(len(x))
   residuals += [abs(row.media-m),abs(row.ic95_inf-(m-h)),abs(row.ic95_sup-(m+h))]
 assert max(residuals)<1e-12
 # Effects separately attributable to each sequential intervention, with paired ICs.
 raw2=rd(B/'etapa2/bruto_completo.csv');raw3=rd(B/'etapa3/bruto_completo.csv');effects=[]
 baseline={'nominal':E.read(E.REF),'fora48':E.read('outputs/diagnosticos/20260921_nominal_v2/bruto_fora_da_amostra.csv'),'aleatorio24':E.read('outputs/diagnosticos/20260922_teste_aleatorio/bruto.csv')}
 for group in baseline:
  datasets={'v2':baseline[group],'etapa2':raw2[raw2.conjunto==group],'etapa3':raw3[raw3.conjunto==group]}
  for metric in E.MET:
   vectors={}
   for version,g in datasets.items():
    q=g.pivot(index=['arquivo','semente'],columns='cenario',values=metric);vectors[version]=(q.adaptativa-q.centralizada).groupby('arquivo').mean()
   for before,after in [('v2','etapa2'),('etapa2','etapa3'),('v2','etapa3')]:
    x=vectors[after]-vectors[before];m=x.mean();h=t.ppf(.975,len(x)-1)*x.std(ddof=1)/math.sqrt(len(x))
    effects.append(dict(conjunto=group,metrica=metric,antes=before,depois=after,delta=m,ic95_inf=m-h,ic95_sup=m+h,N=len(x)))
 pd.DataFrame(effects).to_csv(B/'etapa3/mudancas_pareadas.csv',index=False)
 gov2=rd(B/'etapa2/GOV_sinais.csv');gov3=rd(B/'etapa3/GOV_sinais.csv');gov=pd.concat([gov2,gov3[gov3.versao=='etapa3']]);gov.to_csv(B/'etapa3/governanca_tres_versoes.csv',index=False)
 g2=rd(B/'etapa2/GOV_contrastes.csv');g3=rd(B/'etapa3/GOV_contrastes.csv');delta=g2.merge(g3,on=['ai','ci','metrica'],suffixes=('_etapa2','_etapa3'));delta['mudou_sinal']=(delta.media_etapa2>0).astype(int)-(delta.media_etapa2<0).astype(int)!=(delta.media_etapa3>0).astype(int)-(delta.media_etapa3<0).astype(int);delta.to_csv(B/'etapa3/GOV_etapa2_etapa3.csv',index=False)
 text='''\n\n## Resultado final — v3 adotada; três etapas concluídas separadamente\n\n**Execução local em macOS ARM; sem Git de escrita.** A identidade segue o critério reconciliado e a exceção de plataforma autorizada, não a regra original retratada. A mudança foi adotada por coerência da formulação; nenhum parâmetro foi escolhido por melhorar resultado.\n\n### Controles e testes\n\n- **1a:** 384 execuções × 48 campos numéricos; zero diferenças não permitidas. As 260 diferenças de plataforma estão em 160 execuções e se limitam a competencia_* / confianca_media_final, até 2 ULP. Controle repetido após a etapa 3 com o mesmo resultado. Evidência Linux exata foi informada pela autora, sem nova execução x86 nesta sessão.\n- **1b:** guarda dispara exatamente uma vez nas 384 execuções históricas com kh=0,10; não dispara nas candidatas com kh=0,04. Teste unitário adicional cobre legado/MVP e ambos os arranjos.\n- **Custo real de bateria:** mesma tarefa/estado/pressão/eficiência, sem erro ou fuga. Durações analíticas 4/8/12 contra heurísticas 3/6/9: intensidade igual e custo total 25% menor. Exemplo de oito períodos: 0,064 → 0,048. Controle negativo kh=0,10 reprova a economia. Duração de um período dá custo igual por arredondamento, explicitamente testado; não alegar economia estrita universal.\n- **Etapa 1:** todas as dez médias e os vinte limites dos IC95 reproduziram as quatro casas publicadas pela autora. 768/768 concluídas, zero violações.\n- **Etapa 2:** 4.704/4.704 concluídas, zero violações; suíte 106 testes aprovada. Inclui as 768 já verificadas na etapa 1, sem duplicá-las como amostras novas.\n- **Etapa 3:** novo lote completo de 4.704/4.704 concluídas, zero violações; suíte final **107 testes aprovada**. Teste de fuga falhou antes e passou depois nos dois laços: kh=0,04 e E=0,2, custo do adiamento 0,008 → 0,020; variar kh mantendo k_fuga fixo não altera essa drenagem.\n\nA primeira suíte pós-mudança teve 60 falhas em seis métodos de teste: identidade C2, identidade 1fd22ff, escalares Crowder, dois controles de portões e runner TL. As três primeiras famílias diferiam só na guarda; agora verificam explicitamente as listas de violações antigas/novas e continuam comparando todos os demais campos/estados/RNG. Os controles de portões passaram a repor kh histórico para comparar saídas históricas. No auditor de TL, sum() do Python recente divergia do acúmulo sequencial +=; a verificação agora reproduz a ordem temporal, sem mudar a dinâmica ou TL. Logs da falha e da aprovação foram preservados.\n\n### Resultados lado a lado\n\nContraste adaptativa − centralizada; IC95 t sobre médias de sementes por instância. Etapa 2 muda apenas kh e a guarda; etapa 3 muda apenas a drenagem da fuga para k_fuga=0,10. Não atribuir a etapa 1 os números da etapa 3.\n\n'''
 rows=[]
 for group in ['nominal','fora48','aleatorio24']:
  for metric in E.MET:
   values=table[(table.conjunto==group)&(table.metrica==metric)].set_index('versao');rows.append([group,NAMES[metric],*[fmt(values.loc[v]) for v in ['v2','etapa2','etapa3']]])
 text+=tab(['Conjunto','Indicador','v2','v3 etapa 1/2','v3 final (etapa 3)'],rows)
 text+='\nOs deltas com IC95 pareado estão em `etapa3/mudancas_pareadas.csv`: v2→etapa2 isola a correção inicial, etapa2→etapa3 isola o desacoplamento da fuga. Não são IC de diferenças calculados por subtração dos limites marginais.\n\n### Governança: sinal e magnitude\n\n81 perfis, quatro instâncias × quatro sementes × dois rótulos = 2.592 execuções por versão. Perfis iguais sob rótulos distintos foram conferidos idênticos. 1.215 pares ordenados não idênticos; negativos favorecem adaptativa. Contagem não equivale a significância, e pares compartilham perfis.\n\n'
 rows=[]
 for metric in E.MET:
  vals=gov[gov.metrica==metric].set_index('versao');rows.append([NAMES[metric],*[f"{int(vals.loc[v,'negativos'])}/1215 ({100*vals.loc[v,'negativos']/1215:.2f}%)" for v in ['v2','etapa2','etapa3']]])
 text+=tab(['Indicador','v2: negativos','etapa 2: negativos','etapa 3: negativos'],rows)
 text+='\nEm cada etapa, `GOV_contrastes.csv` traz cada par com média/IC95; `GOV_sinais.csv` separa sinais de IC excluindo zero. `GOV_antes_depois.csv` lista mudanças frente à v2 e `etapa3/GOV_etapa2_etapa3.csv` lista mudanças específicas do desacoplamento. Não há alegação de sinal estável em toda a grade.\n\n### Decisão e limites\n\nA v3 final usa kh=ka=0,04 e k_fuga=0,10. v2 preservada por `config/mvp_v2.yaml` + `config/parametros_v2.yaml`; v1 conserva `config/mvp_v1.yaml` e usa os parâmetros históricos ao reproduzir a evidência. A restauração histórica aciona a guarda atual por desenho; não esconder essa violação nem confundi-la com diferença de dinâmica. Código/configurações executados nas etapas 1/2 estão em snapshots separados. O fallback de k_fuga para kh em configurações antigas preserva o acoplamento anterior.\n\nA derivação do custo pressupõe mesmo E, eficiência e ausência de saturação de bateria; o teste registra exatamente esse contrafactual. Nas trajetórias livres, duração discreta, realimentações e bateria no piso impedem extrapolar “25% em toda tarefa”. A varredura declarada de kh [0,02;0,04] permanece como sensibilidade, sem procura de valor ótimo.\n\nA evidência empírica favorece o adaptativo nos pontos nominais/validações apresentados, mas a vantagem não é universal na grade de governança. Falha efetiva continua exigindo essa ressalva. Nenhuma onda de History Matching, ajuste de V_mod ou calibração foi realizada.\n\n### Reprodutibilidade e arquivos\n\nScripts: `research/test_drenagem_v3.py`, `test_fuga_desacoplada.py`, `etapa1_drenagem_79.py`, `validacao_drenagem_79.py`, `relatorio_drenagem_79.py`. Todos os CSV arquivados foram lidos com round_trip. Nova execução completa em diretório livre:\n\n```bash\npython research/validacao_drenagem_79.py rodar etapa3 outputs/diagnosticos/NOVA_VALIDACAO_V3\npython research/validacao_drenagem_79.py analisar etapa3 outputs/diagnosticos/NOVA_VALIDACAO_V3\npython -m unittest discover -s research -p "test_*.py" -v\n```\n\nSaídas deste lote: `outputs/diagnosticos/20260928_drenagem_heuristica/`, separadas em controle_previo, etapa1, etapa2 e etapa3. Não foram renomeadas nem apagadas saídas anteriores. A geração recusa sobrescrever bruto_novo.csv existente.\n'''
 text+=f'\nConferência independente de agregação (csv/statistics) das 30 estimativas atuais das etapas 2/3: resíduo máximo de médias/IC95 **{max(residuals):.3g}**. Este limite é verificação numérica das contas, não tolerância aplicada à identidade do simulador.\n'
 final=table[table.versao=='etapa3'];text+='\n'+('Os 15 contrastes finais dos três conjuntos mantêm IC95 inteiramente negativo.\n' if (final.ic95_sup<0).all() else '**Há contrastes finais cujo IC inclui zero ou muda de sinal; ver tabela. A adoção teórica não é revertida por esse resultado.**\n')
 p=R/'projeto/79_CONTRADICAO_TCC1_DRENAGEM_HEURISTICA.md';old=p.read_text();assert '## Resultado final — v3 adotada' not in old;lines=old.split('\n',1);p.write_text(lines[0]+'\n\n**Estado atual: v3 adotada. Interrupções abaixo são histórico; critérios reconciliados e resultados finais ao fim.**\n'+lines[1]+text)
 # README: replace active numerical claims, leave unrelated data-layer findings intact.
 p=R/'README.md';s=p.read_text();start=s.index('# 3. Experimentos');end=s.index('\n```',start);s=s[:start]+'''# 3. Validação nominal v3 (diretório novo; não sobrescreve a evidência)
python research/validacao_drenagem_79.py rodar etapa3 outputs/diagnosticos/NOVA_VALIDACAO_V3
python research/validacao_drenagem_79.py analisar etapa3 outputs/diagnosticos/NOVA_VALIDACAO_V3'''+s[end:]
 start=s.index('O modelo nominal está em');end=s.index('\n\nPara rodar',start);s=s[:start]+'''O nominal é a **v3**: opções em `config/mvp.yaml`, parâmetros em
`config/parametros.yaml`. A execução heurística usa `k_heuristico=k_analitico=0,04`;
a fuga usa `k_fuga=0,10` separado. A v2 histórica está em `config/mvp_v2.yaml`
com `config/parametros_v2.yaml`; a v1 mantém `config/mvp_v1.yaml` com os parâmetros
históricos. A identidade exclui o diagnóstico de violações e declara a exceção
de até 2 ULP em competências/confiança no Mac ARM (parecer 79).'''+s[end:]
 start=s.index('### Camada de simulação');end=s.index('## Documentação detalhada',start)
 body='''### Camada de simulação — nominal v3 final

Contraste adaptativa − centralizada, pareado por instância/semente; IC95 sobre
instâncias. Valores negativos favorecem o arranjo adaptativo.

'''
 rows=[]
 for metric in E.MET:
  vals=final[final.metrica==metric].set_index('conjunto');rows.append([NAMES[metric],*[fmt(vals.loc[g]) for g in ['nominal','fora48','aleatorio24']]])
 body+=tab(['Indicador','Nominal 16','Fora da amostra 48','Aleatórias 24'],rows)
 body+='''
**O que mudou.** A v3 resolve a tensão entre o alívio descrito no TCC I §4.1 e
a drenagem acelerada de §4.4.3: o atalho passa a ter a mesma intensidade por
período da execução analítica; a economia vem de terminar antes. Em tarefa/estado
pareados, o teste mede 25% de redução total quando a duração cai 25%; o
arredondamento pode anular essa economia em tarefas de um período. Adiar continua
sendo outro mecanismo: `k_fuga=0,10`. Não há mais coeficiente acelerado na execução
heurística. As etapas foram executadas e reportadas separadamente.

Comparação v2 → v3 inicial → v3 final, com IC95 e efeitos pareados:
[parecer 79](projeto/79_CONTRADICAO_TCC1_DRENAGEM_HEURISTICA.md) e
`outputs/diagnosticos/20260928_drenagem_heuristica/`.

## Estado atual

- Duas validações completas sequenciais: **4.704 execuções cada**, todas
  concluídas e sem violações. Cada lote cobre nominal, fora48, aleatórias24 e
  governança; a etapa 2 reaproveita 768 execuções da etapa 1.
- **107 testes aprovados** após a separação de fuga, incluindo controles negativos,
  guarda histórica/nova e drenagem efetivamente medida nos dois laços.
- Controle histórico final: **384 execuções × 48 campos**, sem diferenças fora
  da exceção autorizada de plataforma. A guarda dispara uma vez com kh=0,10 e
  zero no nominal v3. Não afirmar identidade integral do diagnóstico de violações.
- Os resultados acima foram recalculados para v3; as verificações de estresse,
  inclinação dos portões, sensibilidade à pressão e History Matching dos pareceres
  anteriores continuam históricas v1/v2 e não são apresentadas como revalidadas na v3.

### Ressalva de governança

A grade de 81 perfis contém 1.215 pares com premissas ordenadas. Frequência de
contrastes negativos não é significância estatística nem garantia universal:

'''
 rows=[]
 for metric in E.MET:
  vals=gov[gov.metrica==metric].set_index('versao');rows.append([NAMES[metric],int(vals.loc['v2','negativos']),int(vals.loc['etapa2','negativos']),int(vals.loc['etapa3','negativos'])])
 body+=tab(['Indicador','v2 (de 1.215)','v3 etapa 1/2','v3 final'],rows)
 body+='''
A vantagem em falha efetiva **não é uma conclusão geral para todo o espaço de
governança**. Tabelas com sinal, magnitude e IC95 de cada par estão nos diretórios
etapa2/etapa3; regiões com inversão permanecem reportadas. Nenhum parâmetro foi
ajustado para melhorar essa contagem. Os valores de governança e a inclinação dos
portões seguem premissas, sem calibração externa.

### Histórico preservado

A v1 usa portões duros; a v2 introduziu portões suaves (pareceres 74/75).
A auditoria 76 tem correções registradas no 77. O fatorial 78 não sustentou causa
única para a perda de robustez da falha efetiva na v2; não atribuir toda a diferença
à assistência. A v3 altera drenagem e separa fuga conforme o parecer 79.
O nominal atual não substitui nem apaga os resultados dessas versões.

---

'''
 s=s[:start]+body+s[end:];p.write_text(s)
 p=R/'config/mvp.yaml';s=p.read_text().replace('# Nominal v2 (21/09/2026). v1 congelado em config/mvp_v1.yaml.','# Nominal v3 (28/09/2026): drenagem coerente e k_fuga separado, parecer 79.\n# v2: config/mvp_v2.yaml + config/parametros_v2.yaml; v1: config/mvp_v1.yaml.');p.write_text(s)
 with (R/'docs/registro_de_decisoes.md').open('a') as f:f.write('''\n\n## 28/09/2026 — Parecer 79: v3, drenagem heurística e fuga separada\n\n[DEC] kh=ka=0,04 no nominal; economia pelo tempo, não drenagem acelerada. Guarda rejeita kh>ka. Sensibilidade kh [0,02;0,04]. TCC I §4.1 prevalece sobre pseudocódigo §4.4.3 para essa escolha; caso de duração unitária sem economia estrita documentado.\n\nEtapas 1/2 com fuga acoplada: referências recebidas reproduzidas e 4.704 execuções completas/zero violações. Só depois: k_fuga=0,10 congelado separado, novo lote 4.704 completas/zero violações. Resultados e IC95 lado a lado no parecer 79. Suíte final 107 testes. Não houve escolha de valor por resultado, calibração ou nova onda HM.\n\nIdentidade corrigida pela autora: 48 campos, exclui violacoes; guarda testada separadamente. Mac ARM admite até 2 ULP só em competencia_* e confianca_media_final; autora confirmou Linux exato. Controles completos repetidos com código final; zero divergências fora da exceção. Risco de decisões em empates/limiares de competência declarado, não negado. v2 preservada em parametros_v2.yaml/mvp_v2.yaml; outputs anteriores mantidos.\n''')
 verification=dict(etapa2=json.loads((B/'etapa2/verificacoes.json').read_text()),etapa3=json.loads((B/'etapa3/verificacoes.json').read_text()),suite=107,controle_48_campos=True,residuo_agregacao=max(residuals),IC_negativos_finais=int((final.ic95_sup<0).sum()))
 (B/'verificacao_final.json').write_text(json.dumps(verification,indent=2));print(json.dumps(verification,indent=2))
if __name__=='__main__':main()
