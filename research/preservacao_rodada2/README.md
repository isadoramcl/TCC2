# TCC2 — Modelagem e simulação da gestão de equipes de engenharia

Desenvolvimento computacional do Trabalho de Conclusão de Curso II: dados,
modelo híbrido de agentes e dinâmica de sistemas, experimentos e análise.

- **Autora:** Isadora Maria Carvalho Lopes
- **Orientador:** Prof. André Costa Batista
- **Curso:** Engenharia de Sistemas — UFMG

---

## Objetivo

Investigar a gestão de equipes em projetos de engenharia por modelagem e
simulação, dando continuidade ao modelo conceitual do TCC I.

A camada NASA MDP fornece um gradiente ordinal de risco, sem estabelecer efeito
causal independente da complexidade. O PSPLIB J60 fornece redes de tarefas,
durações e restrições de recursos. O simulador combina esses elementos com
premissas sobre cognição, assistência e governança. A taxa basal absoluta de
retrabalho em engenharia permanece aberta; não foi estimada pela NASA.

---

## Estrutura do repositório

```
data/
├── raw/                      arquivos originais — NUNCA modificados
│   ├── nasa_promise/         versões brutas do repositório PROMISE (10 arquivos)
│   ├── nasa_dp_reference/    versão D' — usada para validar o D'' (13 arquivos)
│   ├── nasa_dpp_reference/   versão D'' — base de análise (13 arquivos)
│   └── psplib/               480 instâncias do PSPLIB J60
└── processed/                bases derivadas, geradas exclusivamente por código
    ├── nasa/
    └── psplib/

src/
├── nasa/                     scripts do pipeline NASA MDP
├── psplib/                   scripts do pipeline PSPLIB
└── modelo/                   simulador, verificações e experimentos

outputs/
├── tables/                   tabelas de resultado
├── figures/                  figuras
└── logs/                     logs de execução do pipeline

docs/                         especificação, entrega e registro de decisões
projeto/                      orientações, auditoria e backlog
```

---

## Princípios metodológicos

1. **Imutabilidade dos brutos.** Nenhum arquivo em `data/raw/` é editado. Se um
   arquivo precisa ser corrigido, a correção é feita por código e o resultado
   vai para `data/processed/`.
2. **Toda transformação é código.** Não há edição manual de dados. Cada etapa de
   limpeza registra quantas linhas foram removidas e por qual critério.
3. **Rastreabilidade.** As bases derivadas preservam `project`, `source_file` e
   `source_row`, permitindo retornar qualquer observação ao arquivo de origem.
4. **Separação de origens.** A documentação distingue explicitamente: (i) o que
   vem da literatura; (ii) o que é decisão metodológica deste trabalho; e
   (iii) o que é apenas exploração.

---

## Inventário dos dados NASA

### `data/raw/nasa_promise/` — versões brutas

Nomes de atributo curtos (`loc`, `v(g)`, `ev(g)`), 22 colunas, rótulo `defects`
(`problems` no KC2).

| conjunto | linhas de dados |
|---|---|
| cm1 | 498 |
| jm1 | 10.885 |
| kc1 | 2.109 |
| kc2 | 522 |
| pc1 | 1.109 |

### `data/raw/nasa_dpp_reference/` — versões D''

Nomes de atributo por extenso (`CYCLOMATIC_COMPLEXITY`), rótulo `Defective`.

| conjunto | linhas | colunas |
|---|---|---|
| CM1 | 327 | 38 |
| JM1 | 7.782 | 22 |
| KC1 | 1.183 | 22 |
| KC3 | 194 | 40 |
| KC4 | 0 | 1 |
| MC1 | 1.988 | 39 |
| MC2 | 125 | 40 |
| MW1 | 253 | 38 |
| PC1 | 705 | 38 |
| PC2 | 745 | 37 |
| PC3 | 1.077 | 38 |
| PC4 | 1.287 | 38 |
| PC5 | 1.711 | 39 |

---

## Questões registradas na entrada dos dados

Observações feitas por inspeção direta dos arquivos, antes de qualquer
processamento. O estado de cada uma está indicado.

1. **KC4 está vazio.** `KC4.arff` contém apenas cabeçalho (49 bytes, 0 linhas de
   dados). **RESOLVIDA:** Shepperd et al. (2013), nota de rodapé 1, registram que
   o KC4 não está presente no repositório PROMISE. Excluído da consolidação, com
   registro em log.
2. **JM1 do D'' tem estrutura distinta** — 22 colunas contra 37-40 dos demais, e
   rótulo `label` em vez de `Defective`. **RESOLVIDA:** a Tabela I do artigo
   reporta que o JM1 no MDP possui 24 atributos, contra 43 do CM1. A diferença é
   inerente aos dados de origem, não é erro de download.
3. **KC2 não possui contraparte D''.** **RESOLVIDA:** mesma nota de rodapé —
   *"KC2 was not present on the MDP website"*.
4. **Divergência entre `jm1.arff` e `jm1.csv`** — 10.885 contra 13.204 registros.
   **RESOLVIDA:** a Tabela I do artigo lista 10.885 para a versão Promise do JM1,
   coincidindo com o ARFF. O CSV não corresponde a nenhuma versão catalogada e
   foi descartado.
5. **Proveniência dos arquivos.** Os arquivos do PROMISE vieram de um espelho
   público no GitHub; os arquivos D'/D'' têm data de 2011, anterior ao artigo.
   **EM ABERTO:** conferir contra a coleção oficial no Figshare comparando os
   resumos SHA-256 já registrados pelo script 01.

Ver `docs/registro_de_decisoes.md` para o registro completo de decisões,
achados e justificativas.

## Pipeline

| script | função |
|---|---|
| `src/nasa/01_auditar_raw.py` | auditoria dos arquivos brutos, hashes, comparação ARFF/CSV |
| `src/nasa/02_consolidar_dpp.py` | base única com rastreabilidade |
| `src/nasa/03_validar_dpp.py` | validação da versão D'' contra o algoritmo publicado |
| `src/nasa/04_modelos_logisticos.py` | modelos logísticos aninhados, razões de chances, VIF |
| `src/nasa/05_faixas_complexidade.py` | faixas de risco, F_base, sensibilidade, leave-one-project-out |
| `src/nasa/06_figuras.py` | figuras a 300 dpi |
| `src/psplib/01_auditar_j60.py` | auditoria das 480 instâncias, reconstrução da grade NC/RF/RS |
| `src/psplib/02_indice_dificuldade.py` | CPM, índice de dificuldade `Di`, níveis ordinais |
| `src/psplib/03_transferencia_ordinal.py` | razões de risco NASA → J60, com bootstrap por projeto |

Execução em sequência, a partir da raiz do projeto, com o ambiente virtual ativo.
Cada script encerra com verificações automáticas e sai com código de erro se
alguma falhar, de modo que uma etapa defeituosa não alimente a seguinte.

## Principais resultados até aqui

**Validação da base de análise.** Aplicando ao conjunto D' os dois passos do
algoritmo de Shepperd et al. que o separam do D'', o conjunto de módulos
preservados foi reproduzido em 12 de 12 bases. O resíduo — 46 registros, 0,26% —
restringe-se a qual rótulo foi mantido em grupos com rótulos conflitantes, ponto
em que os arquivos distribuídos **não seguem literalmente o pseudocódigo
publicado**, que determina remover ambos os membros do par.

**Complexidade não sobrevive ao controle por tamanho.** Isolada, a complexidade
ciclomática tem razão de chances 1,90 sobre a ocorrência de defeito. Controlando
`LOC_TOTAL`, cai para 0,944 com IC 95% [0,870; 1,024] e p = 0,17 — o intervalo
contém o valor nulo. O tamanho, ao contrário, sobrevive ao controle pela
complexidade (LR = 431,2; p ≈ 9 × 10⁻⁹⁶). Nenhuma métrica candidata apresenta
efeito positivo independente do tamanho. A complexidade é preservada no trabalho
como **marcador ordinal** de risco, não como fator causal independente.

**Risco basal por faixa, robusto.** Sobre faixas adaptadas do requisito NASA
SWE-220, o risco cresce monotonicamente: 0,147 → 0,285 → 0,348 → 0,439. Tendência
de Cochran-Armitage z = 25,6. Monotonicidade preservada em 5 de 5 esquemas
alternativos de corte e em 12 de 12 reamostragens por exclusão de projeto.

**Delineamento do J60 reconstruído.** Recalculando NC, RF e RS pelas definições
de Kolisch, Sprecher e Drexl (1995) e agrupando os valores obtidos, recupera-se
um fatorial completo e balanceado 3 × 4 × 4 = 48 células com 10 instâncias cada.
Como os níveis foram derivados dos arquivos e não supostos, o resultado valida
simultaneamente a leitura e as três formulações.

**Índice `Di` com componentes ortogonais.** Correlações de Spearman entre duração
normalizada, intensidade de recursos e criticidade: −0,004, 0,003 e 0,193. Cada
componente carrega informação distinta. A criticidade é medida por folga total do
CPM; a contagem de sucessores, prevista inicialmente, mostrou correlação de
apenas 0,116 com a folga e foi descartada como medida (mantida como variável
alternativa na base).

**Transferência ordinal por razão de risco.** Uma tarefa de dificuldade muito
alta carrega 2,99 vezes o risco basal de uma tarefa de dificuldade baixa
(IC 95% [1,878; 4,156], bootstrap por projeto). A correspondência direta de
rótulos foi descartada com evidência numérica: inflaria o risco médio em 1,74
vezes por artefato do tamanho dos estratos.

---

## Estado atual e ponto de entrada

O simulador já está implementado. Há experimentos de cenários, calibração com
gêmeo sintético, ablações de governança, análise fatorial, sensibilidades e
reanálise por instância. O resultado preliminar não deve ser confundido com
validação empírica do comportamento humano de equipes.

A [auditoria de 15/09/2026](projeto/08_AUDITORIA_AUTONOMA_2026-09-15.md) reúne
arquitetura, inventário dos resultados, verificações existentes, divergências e
backlog priorizado. Ela descreve o **estado local auditado**: parte desse código
e dos resultados está em um merge ainda não concluído no checkout principal.
Esta branch publica a documentação e o diagnóstico; não incorpora esse merge.
As seções históricas acima descrevem principalmente a camada de dados.

### Documento oficial

Por indicação da autora, a análise preliminar oficial é a **cópia local** de
`docs/entrega1_metodologia_resultados_iniciais.docx`. A versão no Git pode estar
atrasada em relação a ela. O gerador `docs/gerar_entrega.js` deve ser comparado
com essa cópia antes de qualquer regeneração, preservando ajustes locais.

O documento local já ressalva a conclusão sobre identificabilidade e declara
que o retrabalho contabilizado não ocupa agentes. Algumas afirmações antigas
no registro e na especificação ainda divergem desse conteúdo; ver a auditoria.

### Prioridades científicas

- Corrigir e reavaliar o desenho das ondas de calibração: o diagnóstico
  confirmou repetição das coordenadas normalizadas com a semente legada.
- Verificar horizonte e término completo no espaço de calibração antes de
  expandir os experimentos.
- Investigar a representação do retrabalho e distinguir término das tarefas de
  encerramento da dívida no indicador de prazo.
- Avaliar dependência dos resultados em relação à confiança constante,
  parametrização, seleção de instâncias e transferência ordinal de risco.

A alternativa de desenho testada permanece um piloto: não demonstra
convergência nem resolve identificabilidade estrutural. Os resultados anteriores
foram preservados, e as limitações constam do registro.

### Continuidade e execução

Leia as [orientações atuais da autora](projeto/07_AUTONOMIA.md) e a auditoria
antes de escolher a próxima tarefa. Não use o backlog histórico como prova de
que um defeito continua presente: várias correções já existem no estado local.

Diagnóstico pequeno, sem sobrescrever resultados publicados:

```sh
python3 src/modelo/15_diagnostico_hm.py --saida /tmp/tcc2_hm_diagnostico
```

A pasta de saída deve ainda não existir. Versões do ambiente, sementes, hashes,
resultados por execução e controles são registrados pelo script. Isso não
substitui a validação do ambiente completo definido em `requirements.txt`.
