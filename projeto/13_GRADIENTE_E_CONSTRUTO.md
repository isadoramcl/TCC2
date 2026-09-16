# CRITICAL-5 — o gradiente transferido é de tamanho, não de complexidade

**Revisor:** Claude · **Data:** 16/09/2026
**Origem:** pergunta da autora sobre o resíduo da transferência NASA → PSPLIB

---

## 1. O achado

O multiplicador de risco transferido ao J60 vem das frequências **brutas** de
defeito por faixa de `CYCLOMATIC_COMPLEXITY` (cortes SWE-220 adaptados):

| nível | n | frequência bruta | multiplicador |
|---|---|---|---|
| baixa | 14.986 | 0,1470 | 1,000 |
| média | 1.079 | 0,2845 | 1,935 |
| alta | 503 | 0,3479 | 2,367 |
| muito alta | 809 | 0,4388 | 2,985 |

Confirmado: os multiplicadores em `tarefas_j60_com_risco.csv` são exatamente as
razões dessas frequências brutas.

**Mas os modelos logísticos ajustados por tamanho, na mesma base, dizem outra
coisa** (`04_sobrevivencia_ao_controle_de_tamanho.csv`):

| métrica | OR ajustado | IC 95% | p | sentido | sobrevive ao controle | sobrevive Holm |
|---|---|---|---|---|---|---|
| CYCLOMATIC_COMPLEXITY | 0,944 | [0,870; 1,024] | 0,166 | negativo | **não** | não |
| ESSENTIAL_COMPLEXITY | 0,941 | [0,883; 1,003] | 0,063 | negativo | **não** | não |
| DESIGN_COMPLEXITY | 1,098 | [1,010; 1,194] | 0,028 | positivo | sim | **não** (p_holm 0,084) |
| HALSTEAD_DIFFICULTY | 0,771 | [0,704; 0,844] | 1,7e-08 | **negativo** | não | não |
| HALSTEAD_EFFORT | 0,904 | [0,867; 0,943] | 4,3e-06 | **negativo** | não | não |

**Nenhuma métrica de complexidade apresenta efeito positivo sobre risco de defeito
que sobreviva ao controle por tamanho e à correção de Holm.** A única positiva
morre no Holm, e as de Halstead ficam significativamente **negativas** — assinatura
clássica de colinearidade com tamanho.

E o mesmo arquivo `05_fbase.csv` traz o eixo alternativo, por quartis de
`LOC_TOTAL`:

| nível | frequência bruta | multiplicador implícito |
|---|---|---|
| baixa | 0,0634 | 1,00 |
| média | 0,1205 | 1,90 |
| alta | 0,1797 | 2,84 |
| muito alta | 0,3401 | **5,37** |

Gradiente **mais forte** que o de complexidade, com estatística de tendência
maior (z = 34,3 contra 25,6).

## 2. E o lado do PSPLIB também é tamanho

O `Di` que define `nivel_dificuldade` no J60 é dominado pela duração:

| componente | correlação com Di |
|---|---|
| `duracao_norm` | **+0,710** |
| `criticidade_folga` | +0,646 |
| `intensidade_norm` | +0,472 |
| `criticidade_sucessores` | +0,068 |

Duração é o análogo de tamanho na rede de projeto. E `criticidade_sucessores`,
que seria a componente mais genuinamente "de coordenação", quase não entra.

## 3. O que isso significa

Ninguém falsificou nada. O gradiente bruto por complexidade é real, monótono e
altamente significativo (p ≈ 1,8e-144). O problema é **de interpretação**:
sem ajuste, complexidade e tamanho são colineares; com ajuste, a contribuição
independente da complexidade desaparece.

Portanto:

- a afirmação **"complexidade → risco"** não é sustentada pelos próprios modelos
  ajustados do trabalho;
- a afirmação **"tamanho → risco"** é fortemente sustentada, dá gradiente mais
  íngreme, e é o que o pipeline de fato transfere;
- do lado do alvo, o `Di` também está dominado por tamanho.

**Os dois lados já medem a mesma coisa. Só que não é a coisa que o texto diz.**

## 4. A saída mais simples é também a mais honesta

Renomear o eixo: o que a camada NASA fornece é um **gradiente ordinal de escala**,
não de complexidade. Isso:

- passa a ser sustentado pelos dados de origem, e pelo eixo mais forte dos dois;
- torna os dois lados da transferência o mesmo construto;
- dispensa a defesa mais difícil do trabalho, que era justificar complexidade de
  módulo de software como proxy de complexidade de tarefa de engenharia.

Não é remendo: é a descrição correta do que o pipeline já faz.

## 5. Se a autora quiser manter "complexidade"

Aí é preciso **definir o construto** em vez de assumi-lo, e depois mostrar que o
`Di` o mede. As referências canônicas:

- WOOD, R. E. Task complexity: definition of the construct. *Organizational
  Behavior and Human Decision Processes*, v. 37, n. 1, p. 60–82, 1986.
  Separa complexidade **de componente**, **de coordenação** e **dinâmica**.
- LIU, P.; LI, Z. Task complexity: a review and conceptualization framework.
  *International Journal of Industrial Ergonomics*, 2012.

Pelo enquadramento de Wood, `duracao_norm` seria complexidade de componente e
`intensidade_norm` com `criticidade_sucessores` seriam de coordenação. Mas para
sustentar "complexidade" o trabalho teria que mostrar que **as componentes de
coordenação** carregam o gradiente — e hoje os dados mostram o contrário:
`criticidade_sucessores` quase não entra no `Di`, e na NASA o efeito independente
de complexidade não sobrevive ao tamanho.

Metadados das duas referências conferidos; conteúdo não lido nesta rodada.

## 6. Por onde levar a pesquisa

Em ordem de retorno:

1. **Tamanho de pacote de trabalho → retrabalho, em engenharia.** É a linha que
   sustenta o eixo renomeado, e conecta com a nota 12: Zhang et al. (2012) mede
   retrabalho em horas, e a relação com tamanho do pacote é o que falta conferir.
2. **Construto de complexidade de tarefa** (Wood; Liu e Li), caso a autora queira
   preservar o termo. Serve também para *definir* o que o `Di` mede, que hoje é
   afirmado sem fonte.
3. **Tipos genéricos de tarefa do HEART** como escada ordinal alternativa: daria
   nível e gradiente de uma fonte só, no mesmo construto — sujeito ao problema de
   agregação registrado na nota 12, §9.1.

## 7. Impacto e teste discriminante

Impacto: afeta o capítulo da camada de dados, a justificativa do `Di` e a
descrição da transferência. **Não muda nenhum número do simulador** — os
multiplicadores continuam os mesmos; muda o que eles são chamados e como são
defendidos.

Teste discriminante, barato: reestimar o gradiente por faixa usando o eixo
`LOC_TOTAL` e comparar o contraste de governança resultante com o atual. Se a
conclusão do experimento não mudar, o trabalho ganha a versão defensável sem
perder nada. Se mudar, isso por si é um achado.

**Confiança:** alta quanto ao fato; alta quanto à recomendação.
