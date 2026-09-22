"""Conferência independente com csv/statistics e redação do relatório 78."""
import csv,json,math,statistics,hashlib
from pathlib import Path
import pandas as pd
import fatorial_78 as F
from discriminante_falha import OUT as BASE, REPORT, ROOT
OUT=F.OUT

def independent_verify():
 # Invert the closed-form Student-t CDF for df=3 independently of scipy.
 lo,hi=0.,10.
 for _ in range(100):
  x=(lo+hi)/2;u=x/math.sqrt(3);cdf=.5+(math.atan(u)+u/(1+u*u))/math.pi
  if cdf<.975:lo=x
  else:hi=x
 critical=(lo+hi)/2
 with (OUT/'bruto_completo.csv').open() as f:raw=list(csv.DictReader(f))
 with (BASE/'amostra.csv').open() as f:sel={r['par']:r for r in csv.DictReader(f)}
 lookup={(r['canto'],int(r['celula']),r['cenario'],r['arquivo'],int(r['semente'])):r for r in raw};assert len(lookup)==1920
 files=sorted({r['arquivo'] for r in raw});seeds=sorted({int(r['semente']) for r in raw})
 def value(pair,corner,arm,metric,file,seed):
  cell=int(sel[pair]['ai' if arm=='adaptativa' else 'ci'])
  return float(lookup[corner,cell,arm,file,seed][metric])
 def vector(pair,corner,arm,metric):
  return [statistics.fmean(value(pair,corner,arm,metric,f,s) for s in seeds) for f in files]
 def contrast(pair,corner):
  return [statistics.fmean(value(pair,corner,'adaptativa','taxa_falha_efetiva',f,s)-value(pair,corner,'centralizada','taxa_falha_efetiva',f,s) for s in seeds) for f in files]
 def check(row,x):
  m=statistics.fmean(x);h=critical*statistics.stdev(x)/2
  return max(abs(float(row[k])-v) for k,v in [('media',m),('ic95_inf',m-h),('ic95_sup',m+h)])
 residuals=[];n=0
 for name in ['leituras_por_braco_IC95','contrastes_IC95','efeitos_IC95']:
  with (OUT/(name+'.csv')).open() as f:
   for r in csv.DictReader(f):
    pair=r['par']
    if name=='leituras_por_braco_IC95':vec=vector(pair,r['canto'],r['cenario'],r['metrica'])
    elif name=='contrastes_IC95':vec=contrast(pair,r['canto'])
    else:
     values={c:(contrast(pair,c) if r['cenario']=='contraste_A_menos_C' else vector(pair,c,r['cenario'],'taxa_falha_efetiva')) for c in ['00','10','01','11']}
     terms={'assistencia_fuga_desligada':[('10',1),('00',-1)],'assistencia_fuga_ligada':[('11',1),('01',-1)],'fuga_assistencia_limiar':[('01',1),('00',-1)],'fuga_assistencia_logistica':[('11',1),('10',-1)],'total_v2_menos_v1':[('11',1),('00',-1)],'interacao':[('11',1),('10',-1),('01',-1),('00',1)]}[r['efeito']]
     vec=[sum(values[c][i]*sign for c,sign in terms) for i in range(4)]
    residuals.append(check(r,vec));n+=1
 assert max(residuals)<1e-12
 F.integrity()
 result=dict(tabelas_IC_conferidas=3,linhas_IC_conferidas=n,max_residuo_media_limites=max(residuals),metodo='csv.DictReader + statistics.fmean/stdev; t_3 por bissecao da CDF analitica; segunda implementacao, sem agregacoes pandas',criterio_tabelas=1e-12,nota='Tolerancia apenas entre formulas equivalentes de agregacao; nao modifica a identidade dos controles',protegidos_inalterados=True)
 (OUT/'verificacao_independente_analise.json').write_text(json.dumps(result,indent=2))
 return result

def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)+'\n'
def interval(r):return f"{100*r.media:+.3f} [{100*r.ic95_inf:+.3f}; {100*r.ic95_sup:+.3f}]"
def main():
 verification=independent_verify()
 k=pd.read_csv(OUT/'classificacao_hipoteses.csv',float_precision='round_trip');a=k[~k.nominal]
 c=pd.read_csv(OUT/'contrastes_IC95.csv',float_precision='round_trip',dtype={'canto':str})
 b=pd.read_csv(OUT/'leituras_por_braco_IC95.csv',float_precision='round_trip',dtype={'canto':str})
 e=pd.read_csv(OUT/'efeitos_IC95.csv',float_precision='round_trip')
 wide=b.pivot(index=['par','ai','ci','nominal','canto','cenario'],columns='metrica',values='media').reset_index();wide.to_csv(OUT/'leituras_por_braco_medias.csv',index=False)
 text='''

## Resultado final — fatorial concluído sob o critério atualizado

**Resumo:** os controles passaram com a única exceção de plataforma autorizada; **1.920/1.920 execuções completas**, zero violações. Foram reaproveitados os 960 controles integralmente reexecutados e rodadas 960 execuções novas nos cantos mistos. Nenhum parâmetro foi ajustado e nenhuma configuração nominal foi alterada.

### 1. Vereditos H1–H3

| Hipótese | Veredito | Evidência discriminante |
|---|---|---|
| H1: assistência melhora o centralizado e desloca o contraste | **Sustentação parcial, não explicação única** | Assistência isolada reduz a falha centralizada em 15/20 pares; o padrão completo pré-registrado (melhora centralizada maior que a adaptativa, mais pedidos e sucessos) ocorre em 9/20, dos quais 7 são novas inversões. Assistência isolada eleva o contraste em 12/20 e o reduz em 8/20. |
| H2: fuga altera o denominador / conjunto executado | **Derrubada na forma proposta** | Todas as 1.920 execuções executam e concluem as mesmas 60 tarefas; denominador=60 em todos os cantos. Os conjuntos de IDs coincidem nas 480 chaves perfil/arranjo/instância/semente. A fuga pode alterar o numerador, mas não por mudar esse denominador ou excluir tarefas. |
| H3: só os dois juntos produzem a inversão | **Padrão presente em parte das células; sinergia não demonstrada** | Em 6 das 14 novas inversões da amostra, apenas o canto conjunto fica positivo. Nas outras 8, ao menos uma mudança isolada já inverte. Todos os 20 IC95 da interação incluem zero; também inclui zero o do par nominal. |

**Precisão:** estes são padrões de médias pareadas, não 20 provas independentes. Na assistência isolada, apenas um IC95 do deslocamento do contraste é inteiramente positivo (par 34/51: +2,917 p.p. [0,156; 5,677]); há também um inteiramente negativo (68/66: −1,875 p.p. [−3,453; −0,297]). Os demais incluem zero. A assistência é um fator causal manipulado no fatorial, mas os contadores associados não demonstram sozinhos toda a cadeia de mediação.

### 2. Onde o sinal inverte

Dos 20 pares sorteados por serem positivos na v2, **6 já eram positivos na v1**; portanto, apenas **14 são novas inversões**. Entre essas 14:

- 3 invertem com assistência isolada;
- 6 invertem com fuga isolada;
- 1 pertence aos dois grupos acima;
- 6 só ficam positivos com as duas mudanças juntas.

Em **19/20** pares o contraste aumenta de 00 para 11; no par 68/66 ele diminui e continua positivo. Na passagem completa v1→v2, o braço centralizado melhora em **20/20** pares. O adaptativo piora em **12/20**; nos outros oito também melhora. Isso impede atribuir toda a mudança apenas a melhora centralizada ou apenas a piora adaptativa. A decomposição por par abaixo mostra ambas.

Nos 14 pares que realmente invertem, oito já invertem em algum canto isolado: logo H3 não é necessária em geral. Nos seis restantes, cruzar zero apenas em 11 não prova sinergia; efeitos aditivos podem produzir o mesmo padrão. Não foi ajustado o desenho para estreitar os intervalos.

### 3. Contrastes completos com IC95

Valores em **pontos percentuais** de falha efetiva, adaptativa − centralizada. IC95 t sobre quatro médias de instância, com quatro sementes pareadas em cada uma. 00=limiar/constante; 10=logístico/constante; 01=limiar/logística; 11=logístico/logística. Sinais pontuais não equivalem a IC excluindo zero.

'''
 rows=[]
 for r in k.itertuples():
  rr=c[c.par==r.par].set_index('canto')
  pattern='já positivo em 00' if r.ja_positivo_v1 else ('só conjunto' if r.somente_juntos else 'assistência e fuga isoladas' if r.assistencia_so_inverte and r.fuga_so_inverte else 'assistência isolada' if r.assistencia_so_inverte else 'fuga isolada' if r.fuga_so_inverte else 'sem nova inversão')
  rows.append([r.par,f'{r.ai}/{r.ci}',*[interval(rr.loc[co]) for co in ['00','10','01','11']],pattern])
 text+=table(['Par','Perfis A/C','D00 [IC95]','D10 [IC95]','D01 [IC95]','D11 [IC95]','Padrão pontual'],rows)
 text+='''
Apenas dois dos 20 contrastes selecionados têm IC95 de 11 inteiramente positivo: 61/55 e 34/51. **Não chamar os demais de inversões estatisticamente estabelecidas:** são inversões do sinal da estimativa, com incerteza. A seleção foi feita usando os mesmos dados/sementes, e os perfis são compartilhados entre pares; os resultados não estimam a prevalência de mecanismos na população dos 643 pares nem em novas instâncias.

### 4. Qual braço muda — passagem 00→11

Mudanças em pontos percentuais. Negativo significa que a taxa de falha do braço caiu. IC95 completos das mudanças de cada braço e dos efeitos isolados estão em `efeitos_IC95.csv`; a tabela abaixo é a decomposição pontual, não um teste de significância adicional.

'''
 text+=table(['Par (A/C)','Δ centralizada','Δ adaptativa','Δ contraste A−C'],[[f'{r.par} ({r.ai}/{r.ci})',f'{100*r.total_delta_C:+.3f}',f'{100*r.total_delta_A:+.3f}',f'{100*(r.D11-r.D00):+.3f}'] for r in k.itertuples()])
 text+='''
### 5. Referência nominal: quatro instâncias × quatro sementes

**Esta é a referência nominal dentro da grade de governança, não o experimento nominal completo de 16 instâncias × 12 sementes.** Não se deve substituir a conclusão daquele experimento por este pequeno subconjunto. Aqui D11=+0,104 p.p., IC95 [−5,531; +5,740], compatível com os dois sinais; a identidade com o bruto v2 foi confirmada.

- Centralizada: falha **30,729% → 27,604%** (−3,125 p.p.).
- Adaptativa: falha **25,938% → 27,708%** (+1,771 p.p.).
- Contraste: **−4,792 → +0,104 p.p.**, mudança +4,896 p.p., IC95 [+0,867; +8,924]. Um IC da mudança excluindo zero não faz o IC do contraste final excluir zero.
- Assistência isolada: centralizada −1,979 p.p., adaptativa +0,417 p.p.; desloca D em +2,396 p.p., IC95 [−2,015; +6,806].
- Fuga isolada: centralizada −0,833 p.p., adaptativa +1,354 p.p.; desloca D em +2,188 p.p., IC95 [−3,970; +8,345].
- Interação: **+0,313 p.p.**, IC95 [−7,078; +7,703]. Os dois efeitos isolados explicam aritmeticamente +4,583 dos +4,896 p.p. da mudança; o resto é a interação estimada, muito imprecisa. Não há demonstração de sinergia.

Leituras médias por execução para o par nominal:

'''
 n=wide[wide.nominal].sort_values(['canto','cenario'])
 text+=table(['Canto','Braço','Falha (%)','N_req','N_success','N_fail','N_blocked'],[[r.canto,r.cenario,f'{100*r.taxa_falha_efetiva:.3f}',*[f'{getattr(r,f):.3f}' for f in ['N_req','N_success','N_fail','N_blocked']]] for r in n.itertuples()])
 text+='\n'
 text+=table(['Canto','Braço','Fração P1','Fração fuga','Executadas','Bateria média','Confiança final'],[[r.canto,r.cenario,f'{r.fracao_porta1:.4f}',f'{r.fracao_fuga:.4f}',int(r.n_executadas),f'{r.bateria_media:.4f}',f'{r.confianca_media_final:.4f}'] for r in n.itertuples()])
 text+='''
**Todas as células, não apenas a referência:** `leituras_por_braco_medias.csv` contém as 168 combinações par×canto×braço, com todos os indicadores pedidos. `leituras_por_braco_IC95.csv` contém as mesmas leituras com IC95 para cada indicador. Incluem N_req, N_success, N_fail, N_blocked, p2_bloqueio, as duas definições explícitas de fração de fuga, tarefas executadas/concluídas, numerador/denominador, bateria média e confiança final. Definições e fronteiras estão no pré-registro.

### 6. O que a monografia pode afirmar

> No diagnóstico fatorial dos 20 pares amostrados que favoreciam o centralizado na v2, seis já o favoreciam na v1 e 14 apresentaram nova inversão do sinal estimado. A suavização da assistência contribui em parte das células, mas não explica sozinha todos os casos. A fuga também modifica o contraste mesmo com assistência por limiar, sem alterar o denominador ou o conjunto final de tarefas: todas as execuções completam as mesmas 60 tarefas. Em seis novas inversões o cruzamento ocorre somente com as duas mudanças juntas, porém os intervalos da interação incluem zero. O diagnóstico não sustenta uma causa única nem sinergia demonstrada, e seus sinais pontuais devem ser lidos com a incerteza de quatro instâncias e a seleção de células pelo resultado.

Retirar qualquer afirmação categórica de que a perda de robustez decorre **apenas** de abrir assistência no centralizado. Também não sustentar H2 como diluição do denominador, nem equiparar cruzamento conjunto a interação estatisticamente comprovada. Não se avaliou mediação por tarefa nem se alinhou RNG por evento; não atribuir o efeito remanescente da fuga a uma cadeia cognitiva específica sem outro teste.

### 7. Arquivos, comandos e verificação

Todos os arquivos novos ficam em `outputs/diagnosticos/20260922_discriminante_falha/fatorial_completo/`. As saídas antigas, o protocolo inicial e a primeira lista de diferenças permanecem intactos.

```bash
.venv/bin/python research/fatorial_78.py controle
.venv/bin/python research/fatorial_78.py executar
.venv/bin/python research/fatorial_78.py analisar
.venv/bin/python research/relatar_fatorial_78.py
```

- `controle_criterio_atualizado.json`: revalidação campo a campo e todas as exceções.
- `criterio_pre_cantos_mistos.md` e `manifesto_retomada.json`: emenda registrada antes da execução.
- `bruto_mistos.csv` / `bruto_completo.csv`: 960 novos resultados / 1.920 resultados dos quatro cantos.
- `contrastes_IC95.csv` e `diferencas_por_instancia.csv`: 84 contrastes e suas quatro médias pareadas.
- `efeitos_IC95.csv`: assistência, fuga, interação e mudanças por braço, 336 estimativas com IC95.
- `classificacao_hipoteses.csv`: classificação transparente das 21 células, sem eleger variante.
- `leituras_por_braco_medias.csv` / `leituras_por_braco_IC95.csv`: decomposição de todas as células, 168 linhas largas / 2.520 estimativas com IC95.
- `verificacoes.json`: integralidade, ausência de violações e igualdade dos conjuntos de tarefas.
- `verificacao_independente_analise.json`: segunda implementação das contas com `csv` e `statistics`, sem as agregações pandas da análise principal.

'''
 text+=f"A segunda implementação conferiu **{verification['linhas_IC_conferidas']} linhas de estimativas/IC95**; maior diferença entre médias ou limites = **{verification['max_residuo_media_limites']:.3g}**, inferior a 1e-12 (checagem das tabelas, não tolerância dos controles de identidade). Os hashes de todos os arquivos protegidos permanecem iguais. Sem alterações do modelo, dos YAML nominais, das referências e sem `git add`, `commit` ou `push`.\n"
 old=REPORT.read_text();assert '## Resultado final — fatorial concluído' not in old
 banner='\n**Estado atual: fatorial concluído sob a exceção de 1 ULP autorizada. Os blocos de parada abaixo são históricos; ver “Resultado final” ao fim.**\n'
 lines=old.split('\n',1);REPORT.write_text(lines[0]+'\n'+banner+lines[1]+text)
 paths=[REPORT,ROOT/'research/fatorial_78.py',Path(__file__)]+[p for p in OUT.iterdir() if p.is_file()]
 (OUT/'hashes_entrega.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2))
 print(json.dumps(verification),flush=True)
if __name__=='__main__':main()
