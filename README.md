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
│   ├── nasa_dpp_reference/   versões D'' — apenas referência de comparação (13 arquivos)
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

## Questões abertas registradas na entrada dos dados

Estas observações foram feitas por inspeção direta dos arquivos, antes de
qualquer processamento. Nenhuma foi resolvida ainda.

1. **KC4 está vazio.** `KC4.arff` contém apenas cabeçalho (49 bytes, 1 atributo,
   0 linhas de dados). Comportamento confirmado no arquivo de origem.
2. **JM1 do conjunto D'' tem estrutura distinta.** Possui 22 colunas, contra
   37–40 dos demais arquivos D'', e o rótulo chama-se `label` em vez de
   `Defective`. Não é erro de download: os nomes seguem o padrão MDP, mas o
   subconjunto de métricas é menor (ausentes `CALL_PAIRS`, `NODE_COUNT` e todas
   as métricas de densidade). Implicação: o conjunto de métricas disponível
   **varia por projeto**, o que exige uma decisão explícita ao consolidar a base.
3. **KC2 não possui contraparte D''.** Existe apenas a versão bruta. A hipótese
   de que KC2 não integra o conjunto limpo publicado ainda **não foi verificada**
   no artigo original.
4. **Proveniência dos arquivos D'' a confirmar.** Os arquivos têm data de
   2011-11-08, anterior ao artigo de 2013 e à migração para o Figshare em 2018.
   A fonte exata do download precisa ser identificada e registrada antes de a
   comparação ser tratada como referência.

---

## Estado atual

Estrutura inicial do projeto criada. Pipeline ainda não implementado.
