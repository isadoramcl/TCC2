# Parecer 45 — Validação fora da amostra: o contraste se sustenta

**Data:** 20/09/2026 · **Revisor:** Claude
**Saídas:** `outputs/diagnosticos/20260920_fora_da_amostra/`
**Scripts:** `research/validacao/fora_da_amostra.py`, `parte2.py`, `analise.py`

---

## 0. Declaração de independência — ler antes do resultado

**Este experimento foi executado pelo revisor, não pelo Codex.** A separação
AUTOR/REVISOR não vale para este item, porque o Codex esgotou a cota de execução
e o congelamento é em sete dias. Isso tem de constar no capítulo de V&V.

A mitigação disponível foi aplicada e passou: antes de qualquer execução nova, o
runner reproduziu o nominal arquivado (`noturno_nominal/bruto.csv`, 384
execuções) e foi conferido campo a campo por `float.hex()`.

> **45 campos numéricos conferidos, zero divergentes, identidade exata.**

Ou seja: os números fora da amostra foram produzidos pela mesma máquina que
produziu os números publicados. O que falta é auditoria independente da
*análise*, não da execução.

---

## 1. A pergunta

> O modelo está certo, ou só está certo nos números em que ele já rodou?

A pergunta é da autora e é a certa. O contraste publicado vem de **16 instâncias
do PSPLIB J60**, de um conjunto de 480. Nunca ninguém olhou fora delas.

---

## 2. Desenho

| | |
|---|---|
| Amostra fora | **48 instâncias**, uma por combinação de desenho, sorteio estratificado |
| Semente do sorteio | 20260920, registrada em `amostra_estratificada.csv` |
| Exclusão | todas as 16 instâncias usadas em qualquer experimento publicado |
| Sementes de execução | 0 a 11, as mesmas do nominal |
| Execuções | **1 152**, zero violações, todas concluíram |
| IC95 | pareado por arquivo e semente, média das sementes por instância, t sobre instâncias — a mesma construção do pipeline |

Cobertura de desenho: o nominal usa **16 das 48 combinações**; a amostra fora
usa **as 48**. Triplica a cobertura.

---

## 3. Resultado — A2

| indicador | dentro (16 inst.) | fora (48 inst.) | sinal | IC95 exclui zero | ICs se sobrepõem |
|---|---:|---:|:---:|:---:|:---:|
| atraso relativo | −1,0234 [−1,1139; −0,9330] | **−1,1387** [−1,2086; −1,0687] | igual | sim | sim |
| taxa de omissão | −0,2282 [−0,2428; −0,2136] | **−0,2253** [−0,2332; −0,2174] | igual | sim | sim |
| dívida latente | −0,0778 [−0,0862; −0,0694] | **−0,0816** [−0,0865; −0,0766] | igual | sim | sim |
| taxa de falha efetiva | −0,0431 [−0,0568; −0,0293] | **−0,0370** [−0,0446; −0,0294] | igual | sim | sim |
| fração Porta 1 | −0,1165 [−0,1366; −0,0964] | **−0,0967** [−0,1092; −0,0841] | igual | sim | sim |

**Os cinco mantêm o sinal, os cinco excluem zero, e os cinco intervalos se
sobrepõem aos de dentro da amostra.** Nenhum indicador precisou de ressalva.

O atraso sai **mais forte** fora da amostra (−1,139 contra −1,023), não mais
fraco — o que é o oposto do que o encolhimento típico de generalização produziria.

---

## 4. Resultado — A3, estratificado

Dez estratos, cinquenta combinações indicador × estrato:

| fator | níveis | resultado |
|---|---|---|
| NC (complexidade da rede) | 1,500 / 1,806 / 2,113 | **5/5 em cada** |
| RF (fator de recursos) | 0,250 / 0,504 / 0,754 / 1,000 | **5/5 em cada** |
| RS (força de recursos, tercis) | baixo / médio / alto | **5/5 em cada** |

**Não há um único estrato em que algum indicador perca significância ou troque
de sinal.** Incluindo `RF = 0,25`, o regime de baixa contenção de recursos, que
a grade de robustez nunca havia tocado.

---

## 5. Retratação R-21 — eu exagerei a lacuna de cobertura

Eu disse à autora que **`RF = 0,25` nunca foi testado**. Isso vale para a
**grade de robustez** do T-GOV e do T-CROWDER, que roda em 4 instâncias
(`sat_gov.py:60`, `sorted(...)[::120]`) e cobre RF em 3 de 4 níveis.

**Não vale para o nominal.** As 16 instâncias do experimento principal cobrem
NC 3/3 e **RF 4/4**. Eu li a cobertura da grade e falei como se fosse a do
nominal.

A lacuna real, e ela é legítima, era de **combinações**: 16 de 48 no nominal.
É essa que a amostra fora da amostra fecha.

---

## 6. O que isto autoriza a escrever

> O contraste entre os arranjos foi replicado fora da amostra sobre 48
> instâncias do PSPLIB J60 sorteadas de forma estratificada, uma por combinação
> de desenho, excluindo as 16 instâncias dos experimentos originais. Os cinco
> indicadores mantiveram sinal e significância, com intervalos de confiança
> sobrepostos aos originais, e a estratificação por complexidade de rede, fator
> de recursos e força de recursos não revelou nenhum estrato em que o resultado
> se dissolvesse. A replicação foi precedida da reprodução exata, por comparação
> de representação binária em 45 campos, do experimento nominal arquivado.

E a ressalva obrigatória, que não é opcional:

> Esta replicação foi executada pelo revisor e não dispõe da auditoria
> independente aplicada aos demais experimentos.

---

## 7. O que continua fora do alcance

O que a validação fora da amostra **não** testa: os parâmetros de governança
continuam `premissa`, sem fonte. Instância nova não ancora parâmetro. O que este
resultado mostra é que a conclusão não depende da **escolha de instâncias** — não
que ela seja independente da escolha de parâmetros. Essa segunda questão foi
tratada separadamente pelo T-GOV.1, com 81 perfis, e está reportada lá.
