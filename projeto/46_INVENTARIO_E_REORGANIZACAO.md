# Parecer 46 — Inventário do `projeto/` e proposta de reorganização

**Data:** 20/09/2026 · **Revisor:** Claude
**Nada foi movido.** Este documento é o levantamento pedido antes de qualquer mudança.

---

## 1. O diagnóstico em uma frase

`projeto/` tem **71 arquivos** de **quatro naturezas diferentes**, e nenhuma
delas é a entrega. A entrega é a monografia mais o código; `projeto/` é o
**registro de processo** de uma revisão entre implementador e revisor.

| natureza | quantos | exemplo |
|---|---:|---|
| Instruções e estado do projeto | 5 | `00_INSTRUCOES_DO_PROJETO.md` |
| Pareceres do revisor | 33 | `41_C3_VEREDITO_CORRIGIDO.md` |
| Relatórios do implementador | 25 | `69_SENSIBILIDADE_DOS_ESCALARES_DE_APRENDIZAGEM.md` |
| Catálogo de fontes | 1 | `04_FONTES.md` |

---

## 2. Defeitos estruturais encontrados

**Colisões de número** — dois arquivos disputando o mesmo prefixo:

| número | arquivos |
|---|---|
| `00` | `42_AUTONOMIA_E_CONTINUIDADE.md` e `00_INSTRUCOES_DO_PROJETO.md` |
| `10` | `10_RESPOSTA_REVISAO_2026-09-15.md` e `44_REVISAO_INDEPENDENTE_RODADA2.md` |

**Lacunas na numeração:** faltam **42** e **44**.

**25 arquivos sem número nenhum**, todos relatórios de execução, com convenção
própria e inconsistente entre si.

**Vocabulário de processo no nome do arquivo**, que é o que a autora não pode
entregar:

| termo | ocorrências |
|---|---:|
| `NOTURNO` | 10 |
| `AUDITORIA` | 5 |
| `RESPOSTA` | 4 |
| `LOTE` | 3 |
| `TB2` / `TGOV` / `TSAT` / `TCROWDER` | 7 |

**33 arquivos com zero referências de entrada** — ninguém os cita, nem documento
nem script.

---

## 3. Classificação

### FICA — documentação do modelo (vai para `docs/`)

| arquivo | por quê |
|---|---|
| `04_FONTES.md` | catálogo de fontes com estado de verificação; **20 referências**, o mais citado do repositório |
| `00_INSTRUCOES_DO_PROJETO.md` | regras metodológicas e lições; serve de apêndice de método |

### PROCESSO — trilha de revisão (vai para `revisao/`)

Tudo o que não está nas outras três listas. É evidência legítima para a defesa e
deve ser preservada, mas fora do caminho da entrega. Subdivide em:

- `revisao/pareceres/` — os documentos do revisor
- `revisao/execucao/` — os relatórios do implementador
- `revisao/superados/` — os abaixo

### SUPERADOS — substituídos por versão posterior

| arquivo | substituído por |
|---|---|
| `02_ORDEM_DE_SERVICO.md` | 32, depois 37 |
| `32_ORDEM_DE_SERVICO_FINAL_MVP.md` | **37** (o próprio 37 declara: "Substitui e consolida a ordem 32") |
| `38_CONTROLE_C3_BLOQUEADO.md` | 40, depois 41 |
| `39_C3_NAO_ESTA_BLOQUEADO.md` | **41** (retratado nas seções 1 e 5) |
| `12_ANCORAGEM_EXTERNA_F_ANCORA.md` | 36 e `53_ANCORAGEM_LINEAR_DE_F_ANCORA` |
| `01_ESTADO_DO_TRABALHO.md` | datado de 06/09, dois meses de trabalho depois |
| `09_REVISAO_INDEPENDENTE`, `10_REVISAO_RODADA2` | rodadas posteriores |
| `13`, `14`, `15`, `16` | achados iniciais, 0 referências, incorporados adiante |
| `NOTURNO_*` (8 arquivos, 0–2 KB) | `66_RELATORIO_CONSOLIDADO_19_A_20.md` |
| `65_ORDEM_DE_SERVICO_19_A_20.md` | ordem executada, resultado no relatório |

**Superado não é descartável.** Vai para `revisao/superados/` com um índice
dizendo o que substituiu o quê — é isso que permite reconstruir a cadeia de
decisão se a banca perguntar.

### DESCARTÁVEL

Nenhum. Não achei arquivo sem uso nem histórico. Os 33 sem referência de entrada
são todos pareceres ou relatórios legítimos que simplesmente ninguém cita.

---

## 4. Estrutura proposta

```
docs/        especificação, registro de decisões, fontes, entrega
src/         modelo e pipeline
data/        dados
config/      parâmetros
research/    experimentos e testes
outputs/     evidência — CONGELADO, ver §5
revisao/
  INDICE.md  mapa número → assunto → o que substituiu o quê
  pareceres/ documentos do revisor
  execucao/  relatórios do implementador
  superados/ versões substituídas
```

Nomenclatura para o que for renomeado: `<NN>_<ASSUNTO>.md`, numeração contínua,
sem vocabulário de processo no nome. Diretórios de saída **novos** seguem
`<AAAAMMDD>_<item>` — o `20260920_fora_da_amostra` já nasceu assim.

---

## 5. A armadilha — ler antes de executar

**`outputs/` não se toca.** Vários scripts recarregam saídas arquivadas por
caminho fixo e afirmam identidade bit a bit contra elas:

```
crowder1.py           -> outputs/diagnosticos/noturno_nominal/bruto.csv
26_testes_arranjo.py  -> outputs/diagnosticos/teste_TL_20260917/bruto.csv
fora_da_amostra.py    -> outputs/diagnosticos/noturno_nominal/bruto.csv
```

Renomear esses diretórios quebra os controles **em silêncio** — o teste não falha,
ele deixa de existir. `outputs/` é trilha de evidência e fica como está, com o
nome feio. Ninguém entrega `outputs/`; ele é anexo de reprodutibilidade.

**Segunda armadilha:** mover `projeto/X.md` para `revisao/pareceres/X.md` quebra
os links relativos dentro dos documentos (`../outputs/...` passa a apontar um
nível errado). A reorganização precisa reescrever os links e verificar depois.

---

## 6. A decisão que é sua

**Os pareceres entram na entrega?**

- **Não entram** — o repositório entregue tem `docs/`, `src/`, `data/`,
  `config/`, `research/`, `outputs/`. A trilha de revisão fica no histórico do
  git e você a usa na arguição se precisar. Repositório limpo.
- **Entram como apêndice** — `revisao/` vai junto, com índice. Mostra o
  processo, que neste trabalho é forte: 21 retratações registradas, controles
  publicados, bateria de controles negativos.

Eu recomendaria a segunda. O processo é o melhor ativo deste trabalho, e um
apêndice de revisão independente com índice é raro numa monografia de graduação.
Mas quem entrega é você.
