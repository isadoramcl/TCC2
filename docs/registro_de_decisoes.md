# Registro de decisões metodológicas, achados e problemas

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
