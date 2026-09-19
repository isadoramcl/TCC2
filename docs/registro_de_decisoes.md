# Registro de decisões metodológicas, achados e problemas

> **MVP — atualização de 16/09/2026:** a alternativa está em
> [`simulador_mvp.py`](../src/modelo/simulador_mvp.py), preservando o legado.
> C4 reduz a duração da omissão; C1 põe reparos na fila com agente e recurso;
> C3 oferece duas leis candidatas, sem eleger uma. Robustez entra no MVP;
> calibração e fragilidades vêm depois, juntas. Nenhuma nova onda de HM.
> As premissas e a sequência de controles estão em
> [PLANO_MVP](../research/PLANO_MVP.md); números anteriores abaixo são históricos.

> **Resposta à revisão científica:** a [reanálise e os pilotos](../projeto/10_RESPOSTA_REVISAO_2026-09-15.md)
> refutaram a suficiência do produto F_ancora × f_retrabalho para todas as saídas.
> A interpretação histórica abaixo foi superada; a crista empírica permanece,
> mas não prova identificabilidade estrutural. Confiança afeta portão e rede.
> Consulte a resposta para o alcance dos resultados e a prioridade atual.

> **Nota de atualização — 15/09/2026:** este arquivo contém registros anteriores
> à auditoria atual. Consulte o [estado auditado e as divergências](../projeto/08_AUDITORIA_AUTONOMA_2026-09-15.md)
> antes de reutilizar conclusões. A análise preliminar oficial é o DOCX local
> `docs/entrega1_metodologia_resultados_iniciais.docx`, por indicação da autora.
> Em particular, convergência das ondas e identificabilidade estrutural ainda
> não estão demonstradas; o simulador contabiliza TR sem ocupar agentes, embora
> a especificação histórica descreva retorno do retrabalho à fila.

Documento vivo. Cada entrada indica a **origem**: `[LITERATURA]` para o que vem
de fonte publicada, `[DECISÃO]` para escolha metodológica deste trabalho,
`[ACHADO]` para resultado empírico obtido pelo pipeline, `[ABERTO]` para questão
ainda não resolvida.

Última atualização: 03/09/2026.

---

## 0. Resumo para leitura rápida

O que foi construído: um pipeline de seis scripts que audita, valida, consolida,
modela e calibra a base NASA MDP, com verificação automática em cada etapa e
execução reproduzida de forma idêntica em dois ambientes computacionais.

O achado principal é **negativo e importante**: a complexidade ciclomática não
tem efeito sobre a ocorrência de defeito que seja independente do tamanho do
módulo. Isso não inviabiliza o uso das faixas de complexidade como escala
ordinal de risco — a ordenação é forte e robusta —, mas proíbe afirmar efeito
causal independente, e tem consequência direta sobre a ponderação do índice de
dificuldade técnica no PSPLIB J60.

**Decisão pendente de revisão sua:** ver seção 8.

---

## 1. Procedimento de limpeza D'' — o que a fonte efetivamente diz

`[LITERATURA]` SHEPPERD, M.; SONG, Q.; SUN, Z.; MAIR, C. Data Quality: Some
Comments on the NASA Software Defect Datasets. *IEEE Transactions on Software
Engineering*, v. 39, n. 9, p. 1208-1215, 2013.
Manuscrito aceito: <https://bura.brunel.ac.uk/bitstream/2438/7926/2/TSE_NASADataQualNote_V26.pdf>

### 1.1 Ordem de aplicação das regras (pseudocódigo, verbatim do artigo)

1. Remover os atributos `MODULE_ID` e `ERROR_DENSITY`; converter `ERROR_COUNT`
   em rótulo binário
2. Remover casos com valores implausíveis
3. Remover casos com valores conflitantes entre atributos
4. Remover casos idênticos — *somente em D''*
5. Remover casos inconsistentes (iguais exceto no rótulo) — *somente em D''*
6. Remover casos com valores ausentes
7. Remover atributos constantes e atributos idênticos

`[LITERATURA]` Citação sobre a ordem: *"Note that, the pre-processing order of
these two situations cannot be swapped, otherwise some inconsistent cases may
not be removed."*

`[LITERATURA]` No passo 4 o pseudocódigo remove apenas a ocorrência posterior
(`DS.Value[k]`), preservando a primeira. No passo 5 remove **ambas** as linhas
do par (`DS.Value[i]` e `DS.Value[k]`).

### 1.2 Tabela I do artigo (versões brutas, verbatim)

| Conjunto | Casos MDP | Casos Promise | Atributos MDP | Atributos Promise |
|---|---|---|---|---|
| CM1 | 505 | 498 | 43 | 22 |
| JM1 | 10.878 | 10.885 | 24 | 22 |
| KC1 | 2.107 | 2.109 | 27 | 22 |
| KC2 | n.a. | 522 | n.a. | 22 |
| KC3 | 458 | 458 | 43 | 40 |
| KC4 | 125 | n.a. | 43 | n.a. |
| MC1 | 9.466 | 9.466 | 42 | 39 |
| MC2 | 161 | 161 | 43 | 40 |
| MW1 | 403 | 403 | 43 | 38 |
| PC1 | 1.107 | 1.109 | 43 | 22 |
| PC2 | 5.589 | 5.589 | 43 | 37 |
| PC3 | 1.563 | 1.563 | 43 | 38 |
| PC4 | 1.458 | 1.458 | 43 | 38 |
| PC5 | 17.186 | 17.186 | 42 | 39 |

`[LITERATURA]` Nota de rodapé nº 1 do artigo: *"KC2 was not present on the MDP
website and KC4 is not present in the Promise Data Repository."*
→ **Resolve** duas questões que estavam em aberto: por que o KC2 não tem
contraparte limpa, e por que o KC4 não tem versão PROMISE.

`[LITERATURA]` Em 2018 os autores migraram as versões limpas para o Figshare e
declararam recomendar D''.
Coleção: <https://figshare.com/collections/NASA_MDP_Software_Defects_Data_Sets/4054940>

---

## 2. Decisão sobre a base de entrada

`[ACHADO]` O passo 1 do algoritmo opera sobre atributos (`MODULE_ID`,
`ERROR_DENSITY`, `ERROR_COUNT`) **ausentes** dos arquivos do repositório PROMISE
disponíveis, que têm 22 colunas com nomes curtos e rótulo `defects`. Aplicar as
regras a esses arquivos seria **adaptação, não replicação**.

`[DECISÃO]` Usar a versão **D'' publicada** como base de análise, documentando a
proveniência, em vez de reproduzir a limpeza a partir dos brutos. Isso preserva
comparabilidade com a literatura e concentra o esforço na pergunta própria do
TCC — a relação entre complexidade e risco — e não na reimplementação de uma
limpeza alheia.

`[DECISÃO]` Essa decisão só é defensável se os arquivos D'' forem verificados.
Ver seção 4.

---

## 3. Achados da auditoria dos arquivos brutos (`01_auditar_raw.py`)

`[ACHADO]` 23 arquivos auditados, 49.942 observações lidas, 8.779 duplicatas
exatas, 25 células ausentes. Resultados idênticos em duas execuções
independentes (ambiente do assistente e computador da autora).

### 3.1 Correspondência entre pares ARFF e CSV do PROMISE

| conjunto | ARFF | CSV | veredito |
|---|---|---|---|
| cm1 | 498 | 498 | idênticos (texto) |
| kc1 | 2.109 | 2.109 | idênticos (texto) |
| pc1 | 1.109 | 1.109 | idênticos (texto) |
| kc2 | 522 | 522 | equivalentes — mesmos valores, grafia numérica diferente (`59` vs `59.0`) |
| **jm1** | **10.885** | **13.204** | **divergentes** |

`[ACHADO]` O valor do ARFF (10.885) **coincide exatamente** com a Tabela I do
artigo para a versão Promise. O valor do CSV (13.204) não corresponde a nenhuma
versão catalogada. Os dois arquivos compartilham quase o mesmo conjunto de
observações distintas (8.912 no ARFF, 8.908 no CSV; 5 exclusivas do ARFF, 1 do
CSV), diferindo na **multiplicidade** das repetições.

`[DECISÃO]` O `jm1.csv` é descartado. O arquivo ARFF é o legítimo.

`[DECISÃO]` A comparação entre arquivos é feita em dois níveis, textual e
numérico. Sem o nível numérico, a diferença de grafia do KC2 (`59` vs `59.0`)
produziria 374 divergências inexistentes.

---

## 4. Validação dos arquivos D'' (`03_validar_dpp.py`)

`[ACHADO]` Dispondo também da versão D', foi possível aplicar a ela os passos 4
e 5 do algoritmo — os únicos que separam D' de D'' — e comparar com o D''
distribuído.

| interpretação | contagem reproduzida | conteúdo reproduzido |
|---|---|---|
| (A) remover ambos — leitura literal do pseudocódigo | 4/12 | 4/12 |
| (B) preservar um representante por vetor de atributos | **12/12** | 5/12 |

`[ACHADO]` O **multiconjunto de vetores de atributos** é reproduzido em
**12/12** conjuntos. Ou seja: os módulos preservados no D'' publicado são
exatamente os que o algoritmo seleciona.

`[ACHADO]` O resíduo — **46 registros em 17.377, ou 0,26%** — restringe-se a
*qual rótulo* foi preservado nos grupos que tinham rótulos conflitantes. Nem
"preservar o primeiro" nem "preservar o último" explicam a escolha.

`[ACHADO]` Conclusão: os arquivos distribuídos são consistentes com o
procedimento publicado quanto aos módulos selecionados, **mas não seguem
literalmente o pseudocódigo** quanto ao tratamento do rótulo em casos
inconsistentes. Este é, ele próprio, um exemplo do problema de documentação de
pré-processamento que os autores denunciam — e é material para um parágrafo da
monografia.

---

## 5. Consolidação da base (`02_consolidar_dpp.py`)

`[DECISÃO]` KC4 excluído: contém apenas cabeçalho, sem observações (49 bytes).
Registrado em log, não silenciosamente.

`[DECISÃO]` Usar a **interseção** das métricas comuns às 12 bases, e não a
união com preenchimento de ausentes. Justificativa: a ausência de métricas é
sistematicamente correlacionada com o projeto (JM1 e KC1 têm conjunto reduzido),
e o projeto é exatamente a variável cujo efeito se quer controlar; preencher
ausências introduziria confundimento.
Verificação: **todas** as métricas candidatas do trabalho sobrevivem à
interseção, de modo que a decisão não custa nenhuma variável de interesse.

`[DECISÃO]` Rastreabilidade: cada linha carrega `project`, `source_file` e
`source_row`, permitindo reconduzir qualquer observação ao arquivo e à linha de
origem.

`[ACHADO]` Base final: **17.377 observações, 12 projetos, 20 métricas, zero
valores ausentes**, todas as verificações automáticas aprovadas.

`[ACHADO]` Taxa de defeito por projeto varia de **2,15% (PC2) a 35,20% (MC2)** —
variação de 16 vezes. Isso justifica, sozinho, incluir o efeito de projeto em
todos os modelos.

---

## 6. Modelos estatísticos (`04_modelos_logisticos.py`)

`[DECISÃO]` O projeto entra como efeito fixo (categórico), não aleatório: são 12
projetos conhecidos e fixos, não uma amostra de uma população de projetos, e o
interesse é controlar seu efeito, não estimar sua distribuição.

`[DECISÃO]` Métricas usadas em escala original **e** em log(1+x). Métricas de
software são fortemente assimétricas à direita; um coeficiente linear na escala
original é dominado pelos poucos módulos extremos.

`[DECISÃO]` `HALSTEAD_ERROR_EST` **excluída** da seleção por circularidade: é
definida como estimativa do número de erros derivada do volume do programa
(B = V/3000). Usá-la para explicar defeito é prever defeito a partir de uma
previsão de defeito. `[ACHADO]` Sua correlação de Spearman com
`HALSTEAD_EFFORT` é **0,979**, confirmando que não carrega informação estrutural
independente.

### 6.1 Modelos aninhados

| comparação | LR | gl | p |
|---|---|---|---|
| nulo → projeto | 1.014,4 | 11 | 1,5 × 10⁻²¹⁰ |
| projeto → + complexidade | 639,8 | 1 | 3,6 × 10⁻¹⁴¹ |
| + complexidade → + tamanho | 431,2 | 1 | 9,0 × 10⁻⁹⁶ |
| + tamanho → modelo completo | 43,3 | 3 | 2,1 × 10⁻⁹ |

### 6.2 ACHADO PRINCIPAL — complexidade não sobrevive ao controle por tamanho

`[ACHADO]`

| teste | LR | p | RC ajustada | IC 95% |
|---|---|---|---|---|
| tamanho acrescenta sobre complexidade | 431,2 | 9,0 × 10⁻⁹⁶ | 2,090 | [1,947; 2,243] |
| **complexidade acrescenta sobre tamanho** | **1,92** | **0,166** | **0,944** | **[0,870; 1,024]** |

Isoladamente a complexidade ciclomática tem RC = 1,90. Controlando o tamanho, o
efeito **desaparece** — o intervalo de confiança contém 1.

`[ACHADO]` Testadas todas as métricas sob controle de `log(LOC_TOTAL)`, nenhuma
apresenta efeito **positivo** independente. As que permanecem distinguíveis do
nulo o fazem com sinal **negativo** (RC < 1), padrão característico de
colinearidade e não de mecanismo causal.

`[ACHADO]` Multicolinearidade: `HALSTEAD_EFFORT` VIF = 23,1 e
`HALSTEAD_DIFFICULTY` VIF = 15,2 (problema sério, convenção VIF > 10);
`CYCLOMATIC_COMPLEXITY` 6,6 e `LOC_TOTAL` 6,0 (atenção, VIF > 5).

`[DECISÃO]` **Interpretação adotada:** a complexidade ciclomática opera nestes
dados como **marcador ordinal** de risco, correlacionado ao tamanho, e **não**
como fator de risco independente dele. Para o propósito do trabalho —
transferência ordinal — um marcador estável é suficiente. A afirmação de efeito
independente é explicitamente abandonada. Esta era exatamente a bifurcação
prevista no Guia Metodológico ("se não, estudar índice multivariado"), e a
resolução escolhida é preservar a ciclomática como eixo ordinal declarando sua
natureza de marcador.

---

## 7. Faixas e F_base (`05_faixas_complexidade.py`)

`[LITERATURA]` NASA Software Engineering Handbook, **SWE-220** (Requisito
3.7.5), verbatim: *"the project manager shall ensure all identified
safety-critical software components have a cyclomatic complexity value of 15 or
lower. Any exceedance shall be reviewed and waived with rationale by the project
manager or technical approval authority."*
Faixas interpretativas da fonte: 1-10, 10-15, 15-20, 20-40, >40.
<https://swehb.nasa.gov/spaces/SWEHBVD/pages/105709643/SWE-220+-+Cyclomatic+Complexity+for+Safety-Critical+Software>

`[LITERATURA]` NASA/TM-20205011566 (NESC): a escolha de 15 é deliberada; a
evidência acadêmica é *"mixed"*; outras organizações adotam 10-20. Achado F-1 do
relatório: *"the number of SLOC does not indicate the complexity of the code"*.

`[DECISÃO]` Adaptação a quatro faixas não sobrepostas, alinhadas ao limiar
normativo de 15: **v(G) ≤ 10 / 11-15 / 16-20 / > 20**. É adaptação metodológica
deste trabalho, **não** a classificação oficial da NASA, e deve ser descrita
como tal.

`[DECISÃO]` Os cortes exploratórios do TCC1 (1-3 / 4-7 / 8-15 / >15) ficam
abandonados por não terem fundamentação externa.

### 7.1 F_base resultante

| nível | n | freq. bruta | IC 95% | prob. ajustada por projeto |
|---|---|---|---|---|
| baixa (≤10) | 14.986 | 0,1470 | [0,1414; 0,1528] | 0,1488 |
| média (11-15) | 1.079 | 0,2845 | [0,2584; 0,3122] | 0,2729 |
| alta (16-20) | 503 | 0,3479 | [0,3076; 0,3906] | 0,3310 |
| muito alta (>20) | 809 | 0,4388 | [0,4050; 0,4732] | 0,3942 |

Teste de tendência de Cochran-Armitage: **z = 25,59; p ≈ 1,8 × 10⁻¹⁴⁴**.
Monotonicidade preservada na frequência bruta e na probabilidade ajustada.

`[ACHADO]` **Sensibilidade aos cortes:** monotonicidade preservada em **5/5**
esquemas alternativos testados (referência, mais permissivo, mais restritivo,
cortes do TCC1, quartis da base).

`[ACHADO]` **Leave-one-project-out:** monotonicidade preservada em **12/12**
reamostragens. Amplitude do F_base entre reamostragens: 0,045 (baixa) a 0,087
(muito alta).

`[DECISÃO]` O script calcula o F_base sobre **dois eixos** — complexidade
ciclomática e tamanho (`LOC_TOTAL`, cortado por quartis) — para que a escolha do
eixo seja decisão explícita e informada, e não consequência silenciosa do código.
Sobre o eixo de tamanho o F_base é 0,063 / 0,121 / 0,180 / 0,340, com tendência
ainda mais forte (z = 34,3).

---

## 8. Decisões de implementação e infraestrutura

- `[DECISÃO]` Projeto mantido **fora** de pasta sincronizada por iCloud.
  Motivo verificado empiricamente durante o trabalho: arquivos do J60 e o
  `j60_sm_merged.json` estavam como *placeholders* de nuvem e falhavam na
  leitura com erro de E/S. Sincronização entre computadores via GitHub.
- `[DECISÃO]` Dados brutos versionados no repositório (4,4 MB), para que
  qualquer replicação parta exatamente dos mesmos arquivos de entrada.
- `[DECISÃO]` `.gitattributes` com `*.arff -text` e `*.csv -text`. Sem isso o
  Git converteria finais de linha ao entregar os arquivos no Windows, alterando
  fisicamente dados declarados imutáveis e quebrando a verificação por hash
  entre máquinas. Verificado: os arquivos do PROMISE estão em CRLF e os do D'/D''
  em LF; a conversão automática afetaria apenas um dos conjuntos, silenciosamente.
- `[DECISÃO]` O script de auditoria usa exclusivamente a biblioteca padrão do
  Python. Leitores de alto nível convertem tipos, tratam ausentes e descartam
  linhas malformadas silenciosamente, destruindo a evidência que a auditoria
  precisa coletar. A partir do script 02 o pandas é usado normalmente.
- `[DECISÃO]` Cada script encerra com verificações automáticas contra
  invariantes conhecidas e sai com código de erro se alguma falhar, para que uma
  etapa defeituosa não alimente a seguinte.

---

## 9. Questões em aberto e decisões pendentes de revisão

- `[ABERTO]` **Proveniência de segunda mão.** Os arquivos do PROMISE vieram de
  um espelho público no GitHub (`NASA-promise-dataset-repository`) que declara
  origem no repositório da Universidade de Ottawa. Os arquivos D' e D'' têm data
  de 2011, anterior ao artigo de 2013 e à migração para o Figshare em 2018.
  **Ação recomendada antes da redação final:** baixar da coleção oficial no
  Figshare e comparar os resumos SHA-256 com os já registrados pelo script 01.
- `[ABERTO]` **Eixo do F_base.** A decisão registrada na seção 6.2 preserva a
  complexidade ciclomática como eixo, na condição de marcador ordinal. A
  alternativa — usar magnitude (tamanho) como eixo — tem suporte empírico maior
  e, no domínio de destino, análogo direto (duração e intensidade de recursos da
  tarefa no J60). **Vale discutir com o Prof. André**, pois muda o enquadramento
  do capítulo de calibração.
- `[ABERTO]` **Ponderação do índice `Di` no J60.** Consequência da seção 6.2: o
  componente de magnitude tem respaldo empírico; o componente estrutural
  (criticidade na rede) não tem respaldo independente. Recomendação registrada:
  ponderar conservadoramente o componente estrutural e submetê-lo a análise de
  sensibilidade específica.
- `[RESOLVIDA]` **PSPLIB J60 auditado.** Ver seção 11.

---

## 10. Estado do pipeline

| script | função | situação |
|---|---|---|
| `01_auditar_raw.py` | auditoria dos brutos, hashes, pares ARFF/CSV | concluído, verificações OK |
| `02_consolidar_dpp.py` | base única com rastreabilidade | concluído, verificações OK |
| `03_validar_dpp.py` | validação D' → D'' | concluído, 12/12 |
| `04_modelos_logisticos.py` | modelos aninhados, OR, IC, LRT, VIF | concluído, verificações OK |
| `05_faixas_complexidade.py` | faixas, F_base, tendência, sensibilidade, LOO | concluído, verificações OK |
| `06_figuras.py` | figuras 300 dpi para o documento | concluído |
| `src/psplib/01_auditar_j60.py` | auditoria do J60, reconstrução de NC/RF/RS | concluído, verificações OK |
| `src/psplib/02_indice_dificuldade.py` | CPM, índice `Di` e níveis ordinais | concluído, verificações OK |
| `src/psplib/03_transferencia_ordinal.py` | razões de risco NASA → J60 | concluído, verificações OK |
| `src/psplib/04_figuras.py` | figuras do bloco PSPLIB | concluído |

Entrega ao orientador: `docs/entrega1_metodologia_resultados_iniciais.docx`.


---

## 11. Auditoria do PSPLIB J60 (`src/psplib/01_auditar_j60.py`)

`[LITERATURA]` KOLISCH, R.; SPRECHER, A.; DREXL, A. Characterization and
Generation of a General Class of Resource-Constrained Project Scheduling
Problems. *Management Science*, v. 41, n. 10, p. 1693-1703, 1995.
Resumo confirma os três parâmetros: restrições de topologia de rede, fator de
recursos (densidade da matriz de coeficientes) e força de recursos
(disponibilidade).

### 11.1 Definições implementadas

- **NC** = |A| / |V| — arcos de precedência por nó (atividades, incluindo as
  fictícias de origem e destino).
- **RF** = (1/n) · Σⱼ [ (1/K) · Σₖ 1{ r_jk > 0 } ] — fração média de tipos de
  recurso requisitados por atividade real.
- **RS_k** = (a_k − r_k^min) / (r_k^max − r_k^min), onde a_k é a disponibilidade,
  r_k^min = maxⱼ r_jk (mínimo para viabilidade) e r_k^max é o pico de demanda no
  cronograma de inícios mais cedo (CPM sem restrição de recursos).

`[DECISÃO]` O cálculo de RS exige o cronograma de inícios mais cedo, obtido por
passagem para frente sobre o grafo em **ordem topológica explícita** (algoritmo
de Kahn), e não pela numeração dos arquivos. A numeração do PSPLIB é de fato
topológica, mas isso não está documentado como garantia — depender dela seria
apoiar o resultado em convenção não declarada.

### 11.2 Integridade estrutural

`[ACHADO]` 480 arquivos, todos com: 62 nós (60 atividades reais mais duas
fictícias), 4 recursos renováveis, 0 não renováveis. **480/480 grafos
acíclicos.** Nomenclatura `j60<combinação>_<instância>.sm` consistente, com 48
combinações de exatamente 10 instâncias.

### 11.3 Reconstrução do delineamento experimental

`[ACHADO]` NC e RF são **exatamente constantes** dentro de cada combinação. O RS
**não é**: seus valores se agrupam em torno de quatro patamares sem coincidir
com eles.

`[ACHADO]` A causa é estrutural, não defeito de leitura: a disponibilidade a_k
precisa ser inteira, de modo que o gerador não realiza exatamente o RS
pretendido e arredonda. A maior amplitude de RS realizado dentro de uma mesma
combinação é 0,12.

`[DECISÃO]` Os níveis nominais foram **reconstruídos a partir dos dados**, por
agrupamento nos maiores saltos dos valores ordenados, e não assumidos de
qualquer tabela. Resultado:

| parâmetro | níveis reconstruídos | nominais do delineamento |
|---|---|---|
| NC | 1,5000 / 1,8065 / 2,1129 | 1,5 / 1,8 / 2,1 |
| RF | 0,2500 / 0,5042 / 0,7542 / 1,0000 | 0,25 / 0,50 / 0,75 / 1,00 |
| RS | 0,1975 / 0,5106 / 0,7038 / 1,0000 | 0,20 / 0,50 / 0,70 / 1,00 |

`[ACHADO]` **Delineamento fatorial 3 × 4 × 4 = 48 células, uma combinação por
célula, 10 instâncias por combinação — completo e balanceado.** Como os níveis
foram derivados dos arquivos e não supostos, este resultado valida
simultaneamente a leitura dos arquivos e as três fórmulas implementadas.

`[DECISÃO]` **Nível nominal e valor realizado são variáveis distintas e devem
ser tratadas como tais.** O nível nominal é um fator do delineamento
experimental; o RS realizado é uma medida contínua. Usar o valor realizado como
se fosse tratamento converteria ruído de arredondamento em variação
experimental. Nos modelos, o nível nominal entra como fator; o valor realizado,
se necessário, como covariável.

### 11.4 Descritivas das tarefas

`[ACHADO]` 29.760 registros de tarefa (480 × 62), dos quais 28.800 com duração
positiva (480 × 60). Duração mínima 1, mediana 6, máxima 10. Número de
sucessores: mínimo 0, mediana 2, máximo 3.

### 11.5 Saídas

- `data/processed/psplib/instancias_j60.csv` — 480 linhas, uma por instância
- `data/processed/psplib/tarefas_j60.csv` — 29.760 linhas, uma por tarefa
- `outputs/tables/psplib_01_grade_parametros.csv` — 48 linhas, a grade

### 11.6 Próximo passo no J60

`[ABERTO]` Construção do proxy de dificuldade técnica `Di` sobre a base de
tarefas, combinando duração normalizada, intensidade de recursos e criticidade
na rede. A ponderação deve levar em conta o achado da seção 6.2: o componente de
magnitude tem respaldo empírico na base NASA; o componente estrutural não tem
respaldo independente e deve ser ponderado conservadoramente, com análise de
sensibilidade específica.


---

## 12. Índice de dificuldade técnica `Di` (`src/psplib/02_indice_dificuldade.py`)

### 12.1 Correção de proveniência de uma referência

`[ACHADO]` O Guia Metodológico atribuía a construção do `Di` a DE REYCK, B.;
HERROELEN, W. *On the use of the complexity index as a measure of complexity in
activity networks.* EJOR, v. 91, n. 2, p. 347-366, 1996.

**A atribuição está incorreta.** O índice de complexidade ali avaliado deriva de
BEIN, W.; KAMBUROWSKI, J.; STALLMANN, M. *Optimal reduction of two-terminal
directed acyclic graphs.* SIAM Journal on Computing, v. 21, n. 6, p. 1112-1129,
1992, e mede a distância da **rede inteira** à série-paralelidade. É propriedade
do grafo, não da atividade. O gerador RanGen (DEMEULEMEESTER et al., *Journal of
Scheduling*, 2003) o emprega como parâmetro de topologia de instância.

`[DECISÃO]` A referência permanece no trabalho, **realocada**: sustenta a
caracterização da rede por instância (o NC do script 01), não o índice por
tarefa. O `Di` é declarado como construção deste trabalho, com cada componente
apoiado em fonte própria.

### 12.2 Componentes e suas origens

| componente | definição | origem |
|---|---|---|
| duração normalizada | min-max da duração, **dentro da instância** | medida direta do arquivo |
| intensidade de recursos | (1/K)·Σₖ (r_jk / a_k) | análogo por atividade do *resource factor* de Kolisch, Sprecher & Drexl (1995); versão por atividade é adaptação deste trabalho |
| criticidade | 1 − folga_norm, com folga = LS − ES do CPM | medida canônica de criticidade por atividade |

`[DECISÃO]` A normalização é **intra-instância**: o modelo compara tarefas dentro
de um mesmo projeto, não entre projetos diferentes.

`[DECISÃO]` A intensidade de recursos é ponderada pela disponibilidade a_k.
Consumir 4 unidades de um recurso com 5 disponíveis é muito mais restritivo do
que consumir 4 de um recurso com 40.

### 12.3 ACHADO — contagem de sucessores não mede criticidade

`[ACHADO]` O Guia previa **contagem de sucessores** como medida de criticidade.
Comparada à folga total na mesma base:

- **Correlação de Spearman entre as duas: 0,1164** — praticamente nenhuma.
- 5.742 tarefas (19,94%) estão sobre o caminho crítico (folga zero).
- **3.488 tarefas têm folga acima da mediana e 3 ou mais sucessores** — muitos
  sucessores e nenhuma urgência.

`[DECISÃO]` A criticidade do `Di` passa a ser medida por **folga total**. A
contagem de sucessores permanece calculada e gravada na base, como variável
alternativa disponível para análise de sensibilidade, mas não compõe o índice.

### 12.4 ACHADO — os três componentes são quase ortogonais

`[ACHADO]` Correlações de Spearman entre os componentes:

| | duração | intensidade | criticidade |
|---|---|---|---|
| duração | 1,000 | −0,004 | 0,193 |
| intensidade | −0,004 | 1,000 | 0,003 |
| criticidade | 0,193 | 0,003 | 1,000 |

Cada componente carrega informação distinta: o composto não é uma única grandeza
sob três nomes. Contraste com a base NASA, onde complexidade e tamanho tinham
correlação de 0,75 e o composto colapsava em um só eixo.

### 12.5 Pesos e sensibilidade

`[DECISÃO]` Pesos de partida iguais (1/3 cada), conforme o Guia, que os trata
como suposição inicial sujeita a sensibilidade.

`[ACHADO]` Correlação de ordenação (Spearman) entre esquemas de peso:

| esquema | w_dur | w_rec | w_crit | ρ vs. referência |
|---|---|---|---|---|
| iguais (referência) | 0,33 | 0,33 | 0,33 | 1,0000 |
| criticidade reduzida (achado NASA) | 0,40 | 0,40 | 0,20 | 0,9695 |
| duração dominante | 0,60 | 0,20 | 0,20 | 0,9036 |
| criticidade dominante | 0,20 | 0,20 | 0,60 | 0,8944 |
| só magnitude | 0,50 | 0,50 | 0,00 | 0,8488 |
| recursos dominante | 0,20 | 0,60 | 0,20 | 0,8470 |

A menor correlação entre qualquer par é 0,847: a ordenação das tarefas é
razoavelmente robusta à ponderação, mas **não indiferente** a ela. O esquema
"criticidade reduzida", sugerido pelo achado da seção 6.2, mantém ρ = 0,97 com a
referência — a mudança de ponderação sugerida pela NASA alteraria pouco a
ordenação.

### 12.6 Níveis ordinais

`[DECISÃO]` Cortes nos **quartis** da distribuição de `Di`. Justificativa: não
existe, para tarefas de projeto, limiar normativo externo equivalente ao SWE-220
do domínio de software. Quartis produzem quatro níveis de tamanho comparável,
requisito para a transferência ordinal. É decisão declarada deste trabalho, não
limiar da literatura.

`[ACHADO]` Cortes em Di = 0,4137 / 0,5424 / 0,6662. Comportamento dos níveis:

| nível | n | duração média | folga média |
|---|---|---|---|
| baixa | 7.200 | 2,87 | 26,07 |
| média | 7.200 | 4,62 | 16,45 |
| alta | 7.200 | 6,38 | 11,22 |
| muito alta | 7.200 | 8,22 | 5,42 |

Duração cresce e folga cai monotonicamente ao longo dos níveis — comportamento
coerente com a interpretação do índice.

### 12.7 Verificações

`[ACHADO]` 28.800 tarefas reais (480 × 60); componentes e `Di` dentro de [0,1];
tarefas fictícias de início e fim com folga zero em todas as instâncias;
makespan da passagem para trás coincidente com o do script 01 em 480/480.

### 12.8 Próximo passo

`[RESOLVIDA]` **Transferência ordinal NASA → J60.** Ver seção 13.


---

## 13. Transferência ordinal de risco NASA → J60 (`src/psplib/03_transferencia_ordinal.py`)

### 13.1 A decisão e a evidência que a determina

`[DECISÃO]` A transferência é feita por **razão de risco relativo**, não por
correspondência direta de rótulos.

`[ACHADO]` A razão é numérica e verificável. Os quatro níveis não têm o mesmo
tamanho relativo nos dois domínios:

| nível | NASA (módulos) | J60 (tarefas) |
|---|---|---|
| baixa | 86,24% | 25,00% |
| média | 6,21% | 25,00% |
| alta | 2,89% | 25,00% |
| muito alta | 4,66% | 25,00% |

Atribuir a cada nível do J60 o `F_base` absoluto do nível homônimo da NASA
produziria risco médio de **0,3046** nas tarefas, contra taxa observada de
**0,1749** na NASA — **inflação de 1,74×** gerada exclusivamente pela diferença
de tamanho dos estratos. Seria artefato de construção apresentado como resultado.

`[DECISÃO]` O que os dados NASA sustentam não é o **nível** absoluto de risco de
um módulo de software — que não tem razão para valer em tarefas de engenharia —
e sim a **forma** do gradiente. A razão é adimensional e independe da taxa basal
do domínio:

    F(nível) = F_ancora × RR(nível)

### 13.2 Razões de risco estimadas

`[ACHADO]` Estimativas na base NASA, com intervalos por **bootstrap por projeto**
(4.000 réplicas, semente fixa 20260905):

| nível | F_base NASA | RR | IC 95% |
|---|---|---|---|
| baixa (referência) | 0,1470 | 1,000 | — |
| media | 0,2845 | 1,935 | [1,758; 2,599] |
| alta | 0,3479 | 2,367 | [1,720; 3,229] |
| muito alta | 0,4388 | 2,985 | [1,878; 4,156] |

`[DECISÃO]` A reamostragem é feita **por projeto**, não por observação. As
observações dentro de um mesmo projeto não são independentes — compartilham
equipe, processo, domínio e critério de registro de defeito. Reamostrar módulos
individuais trataria 17.377 observações como 17.377 evidências independentes e
produziria intervalos artificialmente estreitos. É o mesmo raciocínio da
validação leave-one-project-out.

`[ACHADO]` Os intervalos são largos, sobretudo no nível mais alto ([1,88; 4,16]).
Isso é informação, não defeito: com 12 projetos, a incerteza sobre o gradiente é
substancial, e a monografia deve reportá-la em vez de apresentar o valor pontual
como preciso.

### 13.3 A âncora

`[ABERTO]` `F_ancora` é a taxa basal de retrabalho do domínio de engenharia, no
nível de dificuldade mais baixo. **Não é estimada neste trabalho até aqui**: é
parâmetro do modelo, a ser fixado por dado do domínio (ObrasGov.br, CoST, World
Bank Projects, já identificados como fontes) ou tratado como incerteza na
simulação. A varredura está em `outputs/tables/psplib_03_ancora_sensibilidade.csv`.

`[ACHADO]` Nenhuma âncora entre 0,05 e 0,25 produz risco acima de 1 em qualquer
nível.

### 13.4 O que a base de tarefas recebe

`[DECISÃO]` `tarefas_j60_com_risco.csv` grava o **multiplicador** de risco e seu
intervalo, não uma probabilidade absoluta. A probabilidade só existe depois que o
modelo fixa `F_ancora`; gravá-la aqui embutiria um valor arbitrário na base como
se fosse dado.

### 13.5 Limitação a declarar na monografia

`[LIMITACAO]` A construção assume que o **gradiente ordinal** de risco por
dificuldade é transferível entre domínios, ainda que o nível não seja. É
suposição, não resultado. É mais fraca do que supor equivalência métrica direta —
que os dados não sustentam — mas não é vazia e deve ser declarada explicitamente.


---

## 14. Entrega 1 — estado final

`[DECISÃO]` A entrega foi segurada até que o arco NASA → J60 estivesse fechado.
Justificativa: até a seção 11, o documento mostrava duas bases auditadas
separadamente; ele não mostrava as duas **ligadas**, que é a contribuição do
trabalho. Com as seções 12 e 13 concluídas, a entrega passa de "auditei duas
bases" para "liguei uma à outra, com incerteza quantificada".

`[DECISÃO]` A Figura 1 do documento (arquitetura) foi redesenhada. A versão
anterior exibia apenas o ramo NASA; mantê-la descreveria um sistema que não é
mais o sistema construído. A nova figura mostra os dois ramos e o ponto de
convergência.

`[ACHADO]` Revisão posterior identificou duas lacunas, ambas apontadas pela
autora: (i) o documento não exibia **nenhuma fórmula**, apenas descrições em
prosa; (ii) mais grave, não apresentava a **formulação do modelo de simulação**,
embora o modelo da entrega exija explicitamente "Projeto e Arquitetura:
modelagem teórica da solução". A seção 1.3 descrevia a arquitetura do *pipeline*
de dados, não a do modelo.

`[DECISÃO]` As equações foram escritas com símbolos Unicode em texto formatado, e
não com o suporte a OMML do gerador. Motivo: a renderização OMML saiu vazia na
verificação, e sem poder testar no Word o risco de entregar fórmulas invisíveis
não compensava. Unicode renderiza de forma idêntica em qualquer editor.

`[DECISÃO]` A formulação do modelo foi recuperada do TCC I (seção 4.4) e
reapresentada como equações (1) a (5); o instrumental de calibração ocupa as
equações (6) a (19). Acrescentou-se a seção **1.7 — Pontos de acoplamento**,
que identifica os dois lugares exatos onde os resultados desta entrega entram no
modelo:

- o índice `Dᵢ` da equação (17) é a grandeza do numerador da equação (1),
  o esforço cognitivo exigido;
- o risco basal `F_base` da equação (19) é o termo da equação de falhas (4),
  que governa a válvula do estoque de retrabalho oculto.

Antes desta etapa, ambos seriam parâmetros arbitrados. É esse acoplamento que
define o escopo da entrega e justifica tê-la segurado até aqui.

Conteúdo final do documento `docs/entrega1_metodologia_resultados_iniciais.docx`:
17 páginas, 6 figuras, 4 tabelas, 19 equações numeradas, 13 referências.

| seção | conteúdo |
|---|---|
| 1.1–1.4 | metodologia: classificação, materiais, processo, procedimentos |
| 1.5 | modelagem do sistema: agentes, equações (1)–(5), árvore de decisão |
| 1.6 | instrumental de calibração: equações (6)–(19) |
| 1.7 | pontos de acoplamento entre a calibração e o modelo |
| 2.1 | arquitetura (Figura 1) |
| 2.2 | indicadores dos ensaios (Tabela 1, 17 linhas) |
| 2.3 | discussão: qualidade dos dados, fidelidade da base, complexidade × tamanho (Figuras 2, 3 e 4) |
| 2.4 | caracterização do J60 (Tabela 2) |
| 2.5 | índice `Di` (Figura 5) |
| 2.6 | transferência ordinal (Tabela 3, Figura 6) |
| 2.7 | cronograma (Tabela 4) |

**Pendente para as etapas seguintes**, fora do escopo desta entrega: fixação da
âncora `F_ancora` por dado do domínio; inferência difusa; simulador ABM +
Dinâmica de Sistemas; ensaios de sensibilidade do modelo integrado; redação da
monografia.

---

## 15. Métrica de retrabalho — defeito encontrado e corrigido (`ACHADO 6` e `ACHADO 7`)

> Os números desta seção são **gerados a partir de**
> `outputs/tables/modelo_03_experimento_bruto.csv` e
> `outputs/tables/modelo_03_experimento_resumo.csv`, e não transcritos à mão.

### 15.1 Como o problema apareceu

No primeiro experimento pareado (16 instâncias × 12 sementes = 384 execuções),
cinco das seis métricas favoreciam fortemente o cenário adaptativo. A sexta,
`retrabalho_sobre_esforco`, movia-se em **sentido contrário**, com efeito pequeno
e menos da metade dos pares favoráveis.

`[DEC]` Um resultado isolado que contraria todos os demais é tratado como
suspeita de defeito de medida até prova em contrário, e não como achado. A
investigação confirmou o defeito.

### 15.2 Defeito (i) — o termo de dívida latente era estruturalmente nulo

A métrica era `(TR + S_UR) / (TW + TL + TU + TR)`. O laço de simulação só termina
quando `divida_pendente` está vazia; logo `S_UR_final = 0` ao final de **384
de 384** execuções (resíduo máximo 1.1e-13, compatível com erro de ponto
flutuante). A métrica prometia somar dívida oculta e nunca somava nada:
reduzia-se exatamente a `TR / esforço_realizado`.

### 15.3 Defeito (ii) — o denominador era inflado pela disfunção sob estudo

O esforço realizado inclui `TU`, o tempo ocioso ou bloqueado.

| componente | centralizada | adaptativa |
|---|---|---|
| `TW` (trabalho) | 696,80 | 547,19 |
| `TL` (aprendizado) | 0,00 | 10,49 |
| `TU` (ocioso/bloqueado) | 126,27 | 5,94 |
| `TR` (retrabalho) | **68,87** | **52,51** |
| total realizado | 891,93 | 616,13 |

O braço centralizado gasta 45% mais esforço total, quase todo
improdutivo. Isso **dilui** seu retrabalho: ele parecia melhor na razão enquanto
seu retrabalho **absoluto é 23,8% maior**. A razão invertia o sinal do
efeito por artefato de auto-normalização — um cenário podia melhorar a métrica
piorando o projeto.

### 15.4 Correção

`[DEC]` A base passa a ser o **esforço planejado** `E_plano = Σ_j duração_j`,
propriedade da instância e portanto **idêntica nos dois braços** (verificado:
`nunique == 1` em todos os pares; média 339,25 períodos). A razão só pode se
mover pelo numerador.

`[DEC]` A métrica conflacionada é substituída por duas, reportadas separadamente:

    retrabalho_sobre_plano     = TR            / E_plano
    divida_latente_sobre_plano = max_t S_UR(t) / E_plano

A separação é **necessária**, não cosmética: os cenários diferem justamente em
`p_reporte` (0,15 contra 0,75). O adaptativo converte dívida oculta em
retrabalho visível; um agregado que soma as duas parcelas não distingue
**conversão** de **redução**. Usa-se o **máximo** de `S_UR(t)`, e não o valor
final, porque o final é nulo por construção — o que interessa é a exposição de
pico.

`retrabalho_sobre_esforco_realizado = TR / esforço_realizado` é mantida como
**diagnóstico de eficiência alocativa** e explicitamente rotulada como tal.

### 15.5 Efeito da correção

| métrica | central. | adapt. | dif % | p (Wilcoxon) | d Cohen | % pares |
|---|---|---|---|---|---|---|
| `retrabalho_sobre_plano` | 0,2031 | 0,1545 | -23,9% | 2.38e-17 | -0,729 | 77,1% |
| `divida_latente_sobre_plano` | 0,0741 | 0,0201 | -72,8% | 3.78e-33 | -2,046 | 98,4% |
| `TR` (absoluto) | 68,87 | 52,51 | -23,8% | 3.08e-17 | -0,720 | 77,1% |
| `TU` (absoluto) | 126,27 | 5,94 | -95,3% | 2.98e-33 | -2,252 | 99,5% |
| `…_esforco_realizado` *(diagnóstico)* | 0,0770 | 0,0846 | 9,9% | 2.40e-04 | 0,288 | 39,6% |

O sinal se inverte e passa a concordar com todas as demais métricas. A
divergência remanescente do diagnóstico é agora **explicada pelo mecanismo**, e
não uma anomalia.

### 15.6 `ACHADO 7` — incompatibilidade de unidades na validação externa

A verificação 9 comparava `retrabalho/esforço` (razão de **esforço**) contra a
faixa de Love (razão de **custo sobre valor de contrato**). A seção 10.1 da
especificação já recusava exatamente essa confusão ao descartar Love como base
de `F_ancora`, e o teste a reintroduzia um parágrafo adiante.

`[DEC]` O alvo passa a ser a referência medida na **mesma unidade**:

> BOEHM, B.; BASILI, V. R. *Software Defect Reduction Top 10 List*. **Computer**,
> v. 34, n. 1, p. 135-137, jan. 2001. DOI 10.1109/2.962984 — item 2: *"Current
> software projects spend about 40 to 50 percent of their effort on avoidable
> rework."*
> `https://www.cs.umd.edu/~basili/publications/journals/J81.pdf`

As cifras de Love são retidas como **piso de ordem de grandeza**, com a
diferença de unidade declarada:

> LOVE, P. E. D. et al. *Quantifying the Costs of Field Rework in Construction*.
> **JCEM**, v. 152, n. 1, 2026. DOI 10.1061/JCEMD4.COENG-17026 — 0,38% do valor
> de contrato (máx. 3,67%); 0,76% incluindo pós-conclusão (máx. 7,34%).
> `https://ascelibrary.org/doi/10.1061/JCEMD4.COENG-17026`
>
> LOVE, P. E. D.; LI, H. *Quantifying the causes and costs of rework in
> construction*. **Construction Management and Economics**, v. 18, n. 4,
> p. 479-490, 2000 — 3,15% e 2,40%.

Faixa admitida: **1% a 50% do esforço planejado**. Resultado corrente: mediana
0,1913; **0 de 24** execuções fora da faixa.

`[LIMITACAO]` **Este é um teste fraco e deve ser apresentado como tal.** A faixa
cobre uma ordem e meia de grandeza porque as duas literaturas medem construtos
diferentes (custo × esforço) em domínios diferentes (construção × software). Ele
rejeita desalinhamento grosseiro e nada mais; não é confirmação empírica do
modelo nem substitui calibração. A verificação 9c — dívida latente mediana > 0 —
foi acrescentada para garantir que o estoque `S_UR` não volte a ficar inerte sem
que um teste o detecte.

### 15.7 Estado das verificações

15 de 15 aprovadas (eram 14; a verificação 9 foi desdobrada em 9a, 9b e 9c).

### 15.8 Figuras do experimento (`src/modelo/05_figuras_modelo.py`)

| figura | conteúdo |
|---|---|
| `fig7_efeitos_pareados.png` | floresta de `d` de Cohen pareado, com IC 95% por bootstrap sobre os 192 pares (4000 réplicas); eixo orientado de modo que **negativo = vantagem do arranjo adaptativo** |
| `fig8_decomposicao_esforco.png` | painel A: composição do esforço realizado contra a linha do esforço planejado; painel B: o **mesmo** retrabalho sob as duas bases, mostrando a inversão de sinal |
| `fig9_trajetorias.png` | trajetórias médias de `S_UR`, `B(t)`, `P(t)` e `S_PV` nos dois braços, com faixa interquartil |

`[DEC]` A fig7 reporta **tamanho de efeito com incerteza**, e não valor-p. Com
192 pares, o valor-p não distingue diferença relevante de diferença apenas
detectável — os IC bootstrap distinguem.

`[DEC]` A fig8 existe para tornar o `ACHADO 6` **auditável pela banca**: mostra
lado a lado a quantidade absoluta e as duas razões, de modo que a inversão de
sinal possa ser conferida visualmente e não apenas aceita no texto.

`[OBS]` A fig9 exibe graficamente o defeito (i): a curva de `S_UR` do braço
centralizado sobe, atinge o pico e **drena até zero** antes do fim da execução.
É a confirmação visual de que o valor final do estoque não carrega informação e
de que o pico é a estatística correta.

| IC 95% do `d` pareado (bootstrap, 4000 réplicas) | `d` | IC |
|---|---|---|
| tarefas concluídas com defeito | -2,400 | [-2,729; -2,136] |
| taxa de omissão | -2,400 | [-2,729; -2,130] |
| dívida latente de pico | -2,046 | [-2,306; -1,837] |
| atraso relativo | -1,988 | [-2,224; -1,822] |
| eficiência alocativa `E_total` | -1,901 | [-2,194; -1,661] |
| retrabalho pago / plano | -0,729 | [-0,908; -0,563] |
| *diagnóstico:* retrabalho / esforço realizado | 0,288 | [0,150; 0,433] |

Nenhum intervalo cruza zero. Os seis primeiros favorecem o arranjo adaptativo; o
sétimo é o diagnóstico cujo mecanismo está explicado em 15.3.

---

## 16. Monotonicidade do sistema difuso — teorema aplicável (`ACHADO 8` e `ACHADO 9`)

### 16.1 O problema

A saída do sistema difuso é um **multiplicador de produtividade**. Monotonicidade
não é preferência estética: produtividade não pode SUBIR quando a fadiga ou a
pressão sobem. A implementação fiel ao TCC I — Mamdani com inferência **Max-Min**,
agregação por máximo e defuzzificação por centroide — apresentava regiões de
derivada positiva.

O refinamento de malha mostrou que o efeito é de **inclinação**, não de
discretização: a violação escala linearmente com o passo e a razão converge para
≈ 0,26. Ou seja, não desaparecia refinando a malha.

Na ausência da fonte, a verificação havia sido escrita com um **invariante
inventado por nós** — "a maior derivada positiva não pode alcançar metade da
inclinação média da superfície". Era defensável, mas era um critério nosso.

### 16.2 A fonte

> VAN BROEKHOVEN, E.; DE BAETS, B. *Only Smooth Rule Bases Can Generate Monotone
> Mamdani–Assilian Models Under Center-of-Gravity Defuzzification.* **IEEE
> Transactions on Fuzzy Systems**, v. 17, n. 5, p. 1157-1174, out. 2009.
> DOI 10.1109/TFUZZ.2009.2023328.
> `https://ieeexplore.ieee.org/document/4957084/`

A **Tabela IX** enumera as **cinco únicas** configurações de modelo
Mamdani–Assilian sob defuzzificação por centroide para as quais a monotonicidade
é garantida:

| # | entradas `m` | t-norma | base de regras | exigência extra |
|---|---|---|---|---|
| 1 | 1 | mínimo `T_M` | monótona | consequentes não usam os termos extremos; intervalos de transição de igual comprimento |
| 2 | 1 | produto `T_P` | monótona | — |
| 3 | 1 | Łukasiewicz `T_L` | monótona | idem linha 1 |
| 4 | **2** | **produto `T_P`** | **monótona e suave** | **—** |
| 5 | 3 | produto `T_P` | monótona e suave | várias |

Este sistema tem **duas** entradas. A combinação (`m = 2`, `T_M`) **não aparece
na tabela**. O artigo conclui textualmente: *"when designing a monotone model
with more than one input variable, one should opt for the product `T_P` and use
a monotone smooth rule base"*.

**A não-monotonicidade não era defeito de implementação nem ruído numérico: era
o comportamento previsto pela teoria para a configuração que o TCC I escolheu.**

### 16.3 Verificação das premissas do artigo, por código

Duas premissas foram testadas em `_base_de_regras_monotona_e_suave()` e no
autoteste de `fuzzy.py`, e não por inspeção visual:

1. **Base de regras monótona (Def. 2.1) e suave (Def. 2.2).** A matriz 3×3
   satisfaz ambas — as diferenças de índice de consequente entre regras vizinhas
   são todas 0 ou +1. Esta condição **já era atendida**.
2. **Termos de saída formando partição difusa** (Seção II do artigo, premissa
   dos teoremas). Os conjuntos originais — centros 0,30 / 0,65 / 0,95 com
   meia-base 0,30 — somam entre 0 e 1. **Não** constituem partição. Esta
   condição **não era atendida**.

### 16.4 `ACHADO 9` — erro de implementação revelado pela correção

A implementação aplicava `mínimo` para modificar o consequente **qualquer que
fosse a t-norma**. As equações (2), (5) e (6) do artigo usam a **mesma** t-norma
`T` na conjunção do antecedente e na modificação do consequente:
`A'_i(y) = T(α_i, A_i(y))`.

Com `T_M` isso é truncamento, e coincidia com o que estava escrito — o erro era
invisível. Com `T_P` é **escala**. Na primeira tentativa de troca, o produto
reduziu a violação de 0,258 para 0,092 mas **não** a eliminou, o que contrariava
o teorema; a discrepância levou à releitura das equações e à identificação do
erro. Corrigido, a violação foi a zero. *O teorema funcionou como teste do
código.*

### 16.5 Medição — malha de 161 × 161 pontos

| configuração | pior derivada positiva |
|---|---|
| `T_M` (mínimo) + conjuntos originais — **especificação do TCC I** | 0,258112 |
| `T_P` (produto) + conjuntos originais | 0,000000 |
| `T_M` (mínimo) + partição difusa | 0,420881 |
| `T_P` (produto) + partição difusa — **Tabela IX, linha 4** | 0,000000 |

### 16.6 Decisão

`[DEC]` Adota-se a configuração da **linha 4 da Tabela IX**: t-norma **produto**
e **partição difusa uniforme** na saída. A configuração do TCC I permanece
disponível como `fuzzy.t_norma: minimo` e entra na varredura, de modo que a
diferença seja **medida e não decretada**.

`[DEC]` O critério do autoteste deixa de ser o invariante inventado por nós e
passa a ser a **previsão do teorema**: derivada positiva nula. Medido:
`2,7 × 10⁻¹⁴`, isto é, zero a menos do erro de ponto flutuante.

`[DEC]` O autoteste também **exige que a configuração max-min viole** a
monotonicidade (medido: 0,242085). Se algum dia não violar, o diagnóstico desta
seção está errado e o teste falha — a troca de t-norma deixa de ser justificada.
É um teste do raciocínio, não só do código.

`[DEC]` A partição uniforme torna os centros de saída **estruturais** (núcleos em
0, 0,5 e 1). Com isso `consequentes` e `largura_saida` **deixam de ser premissas
numéricas** — dois parâmetros arbitrados a menos no inventário. A faixa bruta
muda de [0,300; 0,867] para [0,165; 0,835], absorvida pelo reescalonamento para
[μ_mín, 1] do `ACHADO 5`: o sistema difuso fornece a FORMA da degradação e a
magnitude é parâmetro declarado.

### 16.7 Efeito sobre os resultados

Todas as conclusões do experimento se mantêm; as diferenças são de terceira casa.

| métrica | antes (max-min) | depois (produto) |
|---|---|---|
| `retrabalho_sobre_plano` — variação | −23,9% (d = −0,724) | −23,9% (d = −0,729) |
| `divida_latente_sobre_plano` — variação | −73,6% (d = −2,127) | −72,8% (d = −2,046) |
| `atraso_relativo` — variação | −35,0% (d = −2,161) | −36,2% (d = −1,988) |
| verificação 8a (dívida × pressão) | ρ = +0,900, p = 0,037 | **ρ = +1,000, p < 0,001** |
| verificações aprovadas | 15 de 15 | 15 de 15 |

`[OBS]` A robustez é ela própria um resultado a reportar: as conclusões sobre
governança **não dependem** da escolha da t-norma. E a verificação 8a melhorou
de ρ = 0,900 para ρ = 1,000 — com o sistema difuso exatamente monótono, a
relação entre pressão e dívida técnica deixou de ter inversões locais.

---

## 17. Calibração e teste do gêmeo idêntico (`src/modelo/04_gemeo_identico.py`)

Responde às duas perguntas que a banca fará sobre qualquer modelo com parâmetros
não observados: **existe procedimento de calibração?** e **há evidência de que
ele funcione?** Sem a segunda, a primeira é só um algoritmo rodando.

### 17.1 Método e fontes

`[LIT]` **History Matching.** Em vez de buscar um ponto ótimo, descarta-se do
espaço de parâmetros tudo o que é implausível à luz dos dados. A saída é um
conjunto — o **NROY** (*Not Ruled Out Yet*) — e não uma estimativa pontual.

> ANDRIANAKIS, I. et al. *Bayesian History Matching of Complex Infectious Disease
> Models Using Emulation: A Tutorial and a Case Study on HIV in Uganda.*
> **PLoS Computational Biology**, v. 11, n. 1, e1003968, 2015.
> DOI 10.1371/journal.pcbi.1003968
> `https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003968`

`[LIT]` **Gêmeo idêntico e identificabilidade em modelos baseados em agentes.**

> McCULLOCH, J.; GE, J.; WARD, J. A.; HEPPENSTALL, A.; POLHILL, J. G.;
> MALLESON, N. *Calibrating Agent-Based Models Using Uncertainty Quantification
> Methods.* **JASSS**, v. 25, n. 2, artigo 1, 2022. DOI 10.18564/jasss.4791
> `https://www.jasss.org/25/2/1.html`

`[LIT]` **Corte de implausibilidade em 3.** Pela desigualdade de
Vysochanskii–Petunin, para qualquer distribuição unimodal ao menos 95% da massa
está a menos de três desvios da média — descartar `I > 3` raramente descarta o
verdadeiro. Não é número escolhido por nós.

> PUKELSHEIM, F. *The Three Sigma Rule.* **The American Statistician**, v. 48,
> n. 2, p. 88-91, 1994. DOI 10.1080/00031305.1994.10476030
> `https://www.tandfonline.com/doi/abs/10.1080/00031305.1994.10476030`

    I_j(x) = | z_j − f̄_j(x) | / sqrt( V_obs,j + V_sim,j + V_mod,j )
    I(x)   = max_j I_j(x)        x ∈ NROY  ⟺  I(x) ≤ 3

### 17.2 Decisões de desenho

`[DEC]` **History Matching sem emulador.** O emulador existe para substituir um
simulador caro; o nosso custa 0,108 s por execução e o desenho completo (3.200
execuções) roda em minutos. Avalia-se o simulador **diretamente**, o que
**elimina** o termo de erro de emulação da implausibilidade — uma aproximação a
menos, não uma a mais. Se o modelo crescer a ponto de encarecer, o emulador entra
sem alterar o restante do procedimento.

`[DEC]` **Cinco dos treze parâmetros `[ABERTO]`**, escolhidos por terem efeito
direto sobre grandezas que um projeto real reporta. Calibrar treze parâmetros
contra quatro observáveis seria garantir não-identificabilidade por construção.
Os outros oito permanecem premissa declarada, e isso é dito, não omitido.

| calibrados | observáveis |
|---|---|
| `F_ancora`, `f_retrabalho`, `tau_sat`, `k_heuristico`, `mu_minimo` | `taxa_omissao`, `atraso_relativo`, `retrabalho_sobre_plano`, `E_total` |

`[DEC]` **Vetor verdadeiro deliberadamente fora do centro das faixas.** Um gêmeo
cujo alvo esteja no meio do espaço é fácil demais e não testa as bordas.

`[DEC]` **Sementes das observações (100–109) disjuntas das do simulador (0–3).**
Sem isso o teste compararia ruído idêntico consigo mesmo e passaria trivialmente.

`[LIMITACAO]` **`V_mod = 0` neste teste, e isso é decisivo.** No gêmeo idêntico o
modelo **é** a verdade: não há discrepância entre modelo e realidade. O teste é
portanto **otimista por construção** — mede se o procedimento identifica
parâmetros no melhor cenário concebível. Falhar aqui condenaria o procedimento;
passar aqui **não** garante que ele funcione com dados reais, onde `V_mod > 0` e
precisa ser especificado. Apresentar assim na entrega.

### 17.3 Resultado — o teste passa

Duas ondas de 400 pontos por hipercubo latino; a onda 2 amostra dentro da caixa
envolvente do NROY da onda 1.

| | onda 1 | onda 2 |
|---|---|---|
| pontos avaliados | 400 | 400 |
| NROY | 40 (10,0%) | 115 (28,75%) |
| implausibilidade mediana | 8,392 | 4,479 |

| critério | resultado |
|---|---|
| NROY não vazio | **OK** (115 pontos) |
| NROY contém o vetor verdadeiro nos **cinco** parâmetros | **OK** |
| o espaço foi efetivamente reduzido | **OK** (volume da caixa: 14,8% do a priori) |

### 17.4 Identificabilidade — o que os dados realmente determinam

`[DEC]` Critério: redução da largura marginal do NROY em relação à faixa a
priori. Abaixo de 25%, a calibração praticamente não informou o parâmetro e ele é
reportado como **não identificado**, não como "estimado". Apresentar como
resultado um número que os dados não sustentam seria vender artefato de desenho
como achado.

| parâmetro | redução | veredito |
|---|---|---|
| `fuzzy.mu_minimo` | 70,3% | identificado |
| `risco.F_ancora` | 36,8% | parcialmente identificado |
| `agentes.tau_sat` | 10,9% | **não identificado** |
| `retrabalho.f_retrabalho` | 6,0% | **não identificado** |
| `agentes.k_heuristico` | 5,8% | **não identificado** |

### 17.5 `ACHADO 10` — a crista tem explicação estrutural, e ela é útil

A correlação de Spearman **dentro** do NROY revelou uma crista forte:

    risco.F_ancora  ×  retrabalho.f_retrabalho     rho = −0,840

Não é acidente amostral. O esforço de retrabalho gerado por tarefa é, em
esperança, `p_falha × f_retrabalho × duração`, e `p_falha` é proporcional a
`F_ancora`. **Os observáveis agregados só enxergam o produto.** Separar
frequência de severidade exigiria observar a taxa de defeito e o custo unitário
de correção separadamente — dado que o desenho atual não contém.

Hipótese testada, e confirmada:

| grandeza | verdade | NROY | redução |
|---|---|---|---|
| `F_ancora` | 0,1800 | [0,1118; 0,2383] | 36,8% |
| `f_retrabalho` | 0,4200 | [0,3036; 0,7737] | 6,0% |
| **`F_ancora × f_retrabalho`** | **0,0756** | **[0,0572; 0,1041]** | **74,7%** |

O **produto** é muito mais bem determinado do que qualquer um dos fatores.

`[DEC]` **Recomendação para a calibração com dados reais:** tratar o produto como
o parâmetro a estimar — um "esforço esperado de retrabalho por tarefa" — e
declarar a divisão entre frequência e severidade como não identificada, em vez de
reportar dois números que os dados não sustentam.

`[OBS]` As larguras marginais praticamente não mudaram da onda 1 para a onda 2.
As ondas **convergiram**: uma terceira não reduziria o espaço, porque o limite é
**identificabilidade estrutural** e não tamanho de amostra. Isso é o oposto de um
problema — é o método informando corretamente onde está o teto.

### 17.6 Figura

`fig10_nroy_identificabilidade.png` — painel A: a crista, com a hipérbole de
produto constante passando pelo vetor verdadeiro; painel B: redução marginal por
parâmetro, com os cortes de 25% e 50%.

## 18. MVP: alternativas preservadas e decisões explícitas — 16/09/2026

- **C4 [DEC]:** duração `ceil(duração × fator_omissão / (μ_cog μ_rede))`,
  piso de um período. Família declarada {0,50; 0,75; 1,00}; 0,75 é candidato
  central, não estimativa ou solução ótima. Severidade continua referida à
  duração original; não compensamos risco para obter um resultado.
- **C1 [DEC]:** falha reportada entra na fila após fim original; falha oculta
  entra quando detectada, nunca antes do fim original. Reparo FIFO elegível
  ocupa um agente e demanda os mesmos recursos da tarefa. Esforço fracionário
  paga até uma unidade por período; a capacidade fica reservada durante
  `ceil(esforço)`. Não gera reparos recursivos. Não desfaz trabalho sucessor já
  iniciado nem apaga a contagem histórica de omissões. Generalizações são
  alternativas futuras, não consequências implícitas desta correção.
- **Contabilidade:** esforço gerado = TR pago + oculto + reparos pendentes.
  `TW` na alternativa conta períodos realizados, inclusive em censura. O
  legado continua disponível com seus números e sua contabilidade original.
- **Ajuda:** ambos participantes ficam indisponíveis no período da interação;
  TL conserva a unidade legada de serviço de ajuda, não duas pessoa-horas.
  O controle de motor separa essa correção do fator de C4. `E_total` permanece
  índice contábil; não deve ser interpretado como eficiência nem como fração
  exaustiva do calendário de todos os agentes.
- **C3 [DEC]:** por evento de ajuda, os dois participantes recebem sucesso;
  por recusa com colega fisicamente elegível, só o solicitante recebe recusa.
  Na lei `media_eventos`, τ ← τ + 0,05(y−τ), y ∈ {0,1}; na lei
  `saldo_eventos`, τ ← clip(τ+0,02 em sucesso ou τ−0,01 em recusa).
  Atualização no fim do período, limitada a [0,1]. Sem evento, τ não muda.
  São leis candidatas distintas. O TCC I não escolhe nenhuma delas; a escolha
  aguarda orientação, não o melhor resultado no experimento.
- **A10/B6:** horizonte inicial dobra preservando estado e RNG; término somente
  em estado absorvente sem tarefas, agentes ou dívida pendentes. Limite de
  segurança 256×CPM, explicitamente censurado se atingido. Estabilidade não
  significa uma janela de média aparentemente plana. Recursos impossíveis
  falham antes da execução.
- **A11:** os quatro esquemas de pesos declarados no YAML alimentam Di e novos
  quartis globais. Controle 1/3 exato usa o arquivo histórico sem recalcular;
  a diferença para 0,3333/0,3333/0,3334 fica medida em braço próprio.
- **Governança:** família finita de políticas e pontos plausíveis, sem função
  objetivo, busca adaptativa ou ranking. G e N separados no fatorial 2⁵;
  interações permanecem explícitas. Rede não é o canal cognitivo direto.
- **Regra de sequência:** robustez no MVP; depois, V_obs/V_mod, perfil de
  implausibilidade e fragilidades. Não executar novas ondas de HM nesta fase.


## 16/09/2026 — correção estrutural após pareceres 12–18

Implementação anterior preservada em efd81b7 e no simulador legado. Ordem:
compatibilidade; C4 qualidade; contrafactual negativo; Crowder/reset; registro
por tarefa; congelamento; reexecução. Detalhes e evidências em
[PLANO_CORRECAO_ESTRUTURAL](../research/PLANO_CORRECAO_ESTRUTURAL.md).

[DEC] Crowder usa dC na escala original 0–5 no multiplicador de confiança,
mas dC/5 no incremento de competência normalizada. Mantém-se destinatário
único e TL legado; não se alega reprodução integral do protocolo do artigo.
Reset é de competência por subtarefa, não de confiança (divergência D-01 do
parecer 18 resolvida pela instrução direta da autora e pelo PDF p. 1431).

Nenhum parâmetro foi escolhido por melhorar o contraste. O contraste de
E_total inverteu no nominal corrigido e deve aparecer explicitamente nos
resultados; a razão contábil não será renomeada produtividade calibrada.


## 17/09/2026 — teste discriminante de TL

A Eq3 entra como alternativa, sem substituir unitário. O contraste nominal
de E_total troca de sinal mantendo estados físicos/RNG idênticos. Retirada a
interpretação da inversão como conclusão de governança. C4_C1_comunicacao
combina protocolo/escala/teto, conforme [resposta21](../projeto/21_TESTE_DISCRIMINANTE_TL_2026-09-17.md).

## 22. Observáveis antes de V_obs/V_mod — 17/09/2026

[DEC] E_total retirada das conclusões de governança e excluída do vetor externo z.
Diagnóstico interno sempre nas duas convenções TL; soma de unidades distintas
sem ponte de interpretação. Governança interna apoiada nos três indicadores
independentes de TL, com evidência e limites no
[contrato de medição](../projeto/22_OBSERVAVEIS_VOBS_VMOD.md).
Atraso relativo ao CPM não é crescimento de prazo; ainda não admitido em z externo.
V_obs/V_mod iniciados pela especificação, sem atribuir variâncias nem executar HM.

## 23. Bloqueio de premissas e portão — 17/09/2026

[DEC] V_obs/V_mod pausado. Protocolo anterior às execuções em
`research/PLANO_T1_T2_T3.md`; resultados, IC95, limites e controles no
[relatório 24](../projeto/24_TESTES_ARRANJO_T1_T2_T3.md).
Confiança em T2 é o bloco tau_inicial e tau_min; reporte inclui p_reporte e
p_deteccao. Interações impedem atribuição percentual causal única.
Taxa_falha_efetiva adicionada como campo puramente observacional; nominal e
artefatos históricos preservados. Razão de retrabalho com TL excluída de z.
Pico de dívida exige controlar número de amostras e horizonte, além da cadência.
Plano B orientado a padrões registrado no parecer 22, ainda sem avaliação externa.

## 38. Controle C3 da ordem 37 — 17/09/2026

[DEC] Preservar parâmetros e alvos publicados. Controle reprovado em 13/27
frequências e nos três chi²; causa não estabelecida. Nenhuma integração ao
simulador nem avanço aos demais itens. Algoritmos e identidade bit a bit passam,
mas não substituem o controle científico. Evidências e comando de reprodução no
[relatório 38](../projeto/38_CONTROLE_C3_BLOQUEADO.md).

## 40. Reconciliação C3 com a regra 39 — 18/09/2026

[DEC] Regra vigente é propagação da precisão impressa, alpha/beta canônicos;
BB8 registrada como exceção autorizada. Preservadas todas as saídas. A frequência
BB0 publicada continua fora do intervalo exato [67,481624506;67,484608392], mesmo
considerando arredondamento da saída. A incerteza de mu/CV não foi usada no lugar
da incerteza dos parâmetros canônicos. B1 não iniciado; detalhes no
[relatório 40](../projeto/40_RECONCILIACAO_C3_REGRA39.md).

## Especificação 41 — C3 e retomada T4 — 18/09/2026

[DEC] Substituído o critério retratado por teste discriminante em k=0..4.
Cinco negativos separam ≥10×; candidato desvio máximo 0,104318%, amplitude
0,116347%, não monotônico. A-16 confirmado em 5.329 pontos; alpha/beta
operacionais impressos preservados. Inversos não calibram o simulador.
C3 validado; fonte internamente inconsistente. Saídas antigas preservadas.

B1/T4: 1.536 execuções, 768 controles de diagonal exatos, T2 arquivado
reproduzido. Portão e rede contribuem para falha efetiva; interação separada.
P0 depende de mu_cog, não de mu_rede; rede tem caminho indireto por duração,
pressão e bateria. Crowder mantém realimentação entre os canais após o início;
T4 não congela mediadores. Identidade neutra passou após C3 e B1.
[Resultados e controles](../projeto/RESPOSTA_41_C3_T4.md).

### B2 — canal direto desligado e censura estrutural

Alternativa preservada `canal_erro_direto`, ativo default; desligado=R_error zero.
1.344 execuções; contrastes negativos sobrevivem no nominal com canal desligado.
Grade: 36 incompletas, 24 sem tarefas; seleção da tarefa pronta mais difícil pode
bloquear tarefas executáveis quando assistência está fechada e P1 é rara.
Não alterar parâmetros para eliminar a censura. Runner corrigido para fração
indefinida e gravação incremental; dinâmica dessa política preservada. Investigar
alternativa de seleção antes de afirmar robustez da grade. Lote não fechado.
[Relatório B2](../projeto/RESPOSTA_41_B2_ROBUSTEZ.md). Suíte final: 59 testes passaram.
