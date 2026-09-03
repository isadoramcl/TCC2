# TCC2 — Calibração NASA MDP e dificuldade técnica no PSPLIB J60

Implementação do pipeline de dados do Trabalho de Conclusão de Curso II.

- **Autora:** Isadora Maria Carvalho Lopes
- **Orientador:** Prof. André Batista
- **Curso:** Engenharia de Sistemas — UFMG

---

## Objetivo

Reproduzir em Python, a partir dos dados brutos, o procedimento de limpeza
**D''** proposto por Shepperd et al. para os conjuntos NASA MDP; validar o
resultado contra os arquivos D'' publicados pelos autores; e, em etapa
posterior, construir o proxy de dificuldade técnica sobre o PSPLIB J60.

O objetivo **não** é construir o melhor classificador de defeitos de software,
e sim obter uma relação interpretável e transferível ordinalmente entre
complexidade e risco basal.

---

## Estrutura do repositório

```
data/
├── raw/                      arquivos originais — NUNCA modificados
│   ├── nasa_promise/         versões brutas do repositório PROMISE (10 arquivos)
│   ├── nasa_dp_reference/    versão D' — usada para validar o D'' (13 arquivos)
│   ├── nasa_dpp_reference/   versão D'' — base de análise (13 arquivos)
│   └── psplib/               instâncias J60 (etapa posterior)
└── processed/                bases derivadas, geradas exclusivamente por código
    ├── nasa/
    └── psplib/

src/
├── nasa/                     scripts do pipeline NASA MDP
└── psplib/                   scripts do pipeline PSPLIB

outputs/
├── tables/                   tabelas de resultado
├── figures/                  figuras
└── logs/                     logs de execução do pipeline

docs/                         guia metodológico e registro de decisões
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

Execução em sequência, a partir da raiz do projeto, com o ambiente virtual ativo.

## Estado atual

Pipeline NASA MDP concluído e verificado (17.377 observações, 12 projetos).
Entrega 1 ao orientador gerada em `docs/`. Etapa PSPLIB J60 ainda não iniciada.
