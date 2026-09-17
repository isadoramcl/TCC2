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
backlog priorizado. O merge auditado foi concluído em `dc8721f`; a preservação
da rodada 2 foi registrada antes do rebase e reconciliada depois dele.
As seções históricas acima descrevem principalmente a camada de dados.

### Documento oficial

Por indicação da autora, a análise preliminar oficial é a **cópia local** de
`docs/entrega1_metodologia_resultados_iniciais.docx`. O snapshot versionado
[`analise_preliminar_oficial_2026-09-15.docx`](docs/snapshots/analise_preliminar_oficial_2026-09-15.docx)
é um ponteiro imutável para a cópia conferida, com SHA-256
`d5a658f1cdf03d99e6bdc0b5d03cb4aaa9420853ec7ebc2bb3f55e85a728c57d`.
Antes de qualquer regeneração, confira uma cópia viva explicitamente, sem editá-la:

```sh
python3 research/verificar_documento_oficial.py --vivo /caminho/para/analise_preliminar.docx
```

O documento local já ressalva a conclusão sobre identificabilidade e declara
que o retrabalho contabilizado não ocupa agentes. Algumas afirmações antigas
no registro e na especificação ainda divergem desse conteúdo; ver a auditoria.

### Resposta à revisão independente

A [resposta de 15/09/2026](projeto/10_RESPOSTA_REVISAO_2026-09-15.md) classifica
cada crítica, preserva os resultados negativos e atualiza o backlog. O piloto
com produto constante refutou a interpretação de que as saídas só observam
`F_ancora × f_retrabalho`. A confiança atua no portão e no multiplicador de rede;
o legado permanece preservado.

O [relatório 11](projeto/11_MVP_RESULTADOS_2026-09-16.md) e suas 17.920
execuções estão **congelados como pré-correção estrutural**. C4 estava sem o
excesso de risco; o controle neutro revelou deriva do laço e as leis de
confiança foram substituídas. Esses números não são resultados do MVP corrigido.

A [sequência de correção](research/PLANO_CORRECAO_ESTRUTURAL.md) registra
compatibilidade bit a bit, risco da omissão, contrafactual com controle negativo,
Crowder, reset de competência e instrumentação por tarefa. A [reexecução e análise corrigidas](projeto/19_CORRECAO_ESTRUTURAL_MVP_2026-09-16.md)
terminaram: 21.440 execuções e 34 testes, sem violações. O [teste discriminante de TL](projeto/21_TESTE_DISCRIMINANTE_TL_2026-09-17.md)
mostrou que o sinal de E_total depende da convenção de contagem; não sustenta
conclusão de governança. Unitário permanece como default, Eq3 como alternativa.

Os [comandos de reprodução](research/REPRODUCAO.md) recuperam evidências históricas
por commit e hash, sem depender de arquivos da máquina da autora. As
[fontes verificadas](research/SOURCES.md) distinguem apoio bibliográfico e inferência.
Há snapshots fiéis da [análise preliminar oficial](docs/snapshots/analise_preliminar_oficial_2026-09-15.docx)
e do [TCC I](docs/snapshots/TCC_I_referencia_2026-09-15.pdf). Preservar as cópias locais;
os snapshots não autorizam regenerá-las sobre edições da autora.

### Prioridade vigente

- MVP corrigido e robustez concluídos; consultar o relatório 19 e as tabelas incrementais.
- B1/B3/B7/B9 e relatório 11 só podem ser usados como controles históricos até reexecução.
- Depois do MVP: V_obs/V_mod, implausibilidade perfilada e fragilidades restantes.
- Sem novas ondas de History Matching, substituição do método ou busca de melhor política.

Os hashes das saídas congeladas estão no
[manifesto de congelamento](research/CONGELAMENTO_PRE_CORRECAO.json).

### Continuidade e execução

Leia as [orientações atuais da autora](projeto/07_AUTONOMIA.md) e a [sequência de correção estrutural](research/PLANO_CORRECAO_ESTRUTURAL.md)
antes de escolher a próxima tarefa. Não use o backlog histórico como prova de
que um defeito continua presente: várias correções já existem no estado local.

Diagnóstico pequeno, sem sobrescrever resultados publicados:

```sh
python3 src/modelo/15_diagnostico_hm.py --saida /tmp/tcc2_hm_diagnostico
```

A pasta de saída deve ainda não existir. Versões do ambiente, sementes, hashes,
resultados por execução e controles são registrados pelo script. Isso não
substitui a validação do ambiente completo definido em `requirements.txt`.

### Observáveis e calibração — decisão vigente

`E_total` foi retirada das conclusões de governança: é diagnóstico interno com
unidades distintas no denominador, reportado nas duas convenções TL. A evidência
de governança interna e a especificação inicial de V_obs/V_mod estão no
[contrato de medição](projeto/22_OBSERVAVEIS_VOBS_VMOD.md).
`atraso_relativo` usa CPM sem recursos e não equivale a crescimento de prazo externo.
Nenhuma nova onda de History Matching foi iniciada.

### Prioridade vigente: arranjo e portão — V_obs/V_mod pausado

[T1/T2/T3 concluídos](projeto/24_TESTES_ARRANJO_T1_T2_T3.md): a resposta não se
reduz a degrau puro; portão e canal fuzzy devem ser distinguidos. O bloco de
reporte/detecção explica grande parte da redução das falhas não reportadas,
sem evidência conclusiva de redução da taxa de falha efetiva por esse bloco.
A nova taxa efetiva é desfecho explícito. Nominal preservado; alternativa próxima
ao limiar apenas proposta. V_obs/V_mod continua pausado por instrução da autora.
