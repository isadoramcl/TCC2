# 75 — Critério de adoção dos portões suaves como nominal

**Escrito em 21/09/2026, antes da execução da varredura de `s_portoes`.**
Regra 11 do projeto: o critério nasce antes do resultado.

## Por que 0,25 — o que existe hoje e o que falta

`s_portoes = 0,25` **não veio de dado nem de busca.** Foi reaproveitado do valor
nominal de `s_transicao`, a inclinação da transição cognitiva que o modelo já usa
na Porta 1 — que também é premissa, sem fonte, varrida em {0,01; 0,25; 0,60}.
O argumento é de parcimônia (uma escala só para as três decisões), não empírico.

Há dois limites lógicos que qualquer valor precisa respeitar:

- **`s` muito pequeno** recupera o limiar duro do TCC I — e com ele o travamento.
- **`s` muito grande** achata a curva: a chance de aceitar ajuda fica perto de 50%
  qualquer que seja a confiança, e a confiança deixa de governar o pedido de ajuda,
  contrariando a premissa do TCC I de que é ela quem decide.

O que falta é mostrar **onde, entre esses dois limites, a conclusão se sustenta.**
É isso que a varredura mede.

## Varredura

`s_portoes` ∈ {0,05; 0,10; 0,25; 0,50; 1,00}; nominal completo (16 instâncias ×
12 sementes × 2 arranjos) e as 36 chaves que travavam no B2, para cada valor.
Faixa de decisão: **0,10 a 0,50** (0,25 dividido e multiplicado por ~2).
Os extremos 0,05 e 1,00 são descritivos: mostram onde a proposta deixa de valer.

## Critério — adota se TODOS passarem

1. **Identidade.** Com as opções desligadas, o código reproduz o nominal arquivado
   bit a bit.
2. **Testes.** Suíte completa aprovada.
3. **Ponto proposto (0,25).** Dentro (16) e fora (48) da amostra: os cinco
   contrastes com o mesmo sinal do nominal publicado e IC95 excluindo zero; todas
   as execuções terminam; zero violações.
4. **Faixa 0,10–0,50.** Os cinco contrastes mantêm o sinal em todos os valores;
   todas as execuções do nominal terminam; as 36 chaves do B2 terminam.
5. **Plausibilidade.** Confiança final média do centralizado acima da inicial
   (0,25) e abaixo da do adaptativo; a fração de fuga cresce com a sobrecarga.

Se algum item falhar, **o nominal publicado continua valendo** e a proposta fica
como opção documentada, com o motivo da recusa.

---

## Resultado (acrescentado depois da execução, 21/09/2026)

| critério | resultado |
|---|---|
| 1. Identidade | **passou** — 384 execuções, 45 campos, zero divergentes |
| 2. Testes | **passou** — 31 arquivos, 101 testes (102 com o teste de regressão da v2) |
| 3. Ponto 0,25 | **passou** — cinco contrastes negativos com IC excluindo zero, dentro (16) e fora (48); 1 536 execuções completas, zero violações |
| 4. Faixa 0,10–0,50 | **passou** — sinal mantido nos cinco em todos os valores; 384/384 completas por valor; B2 36/36 por valor. Em 0,50 o IC da falha efetiva inclui zero (−0,0119 [−0,0272; 0,0034]) — o critério pedia sinal, não significância |
| 5. Plausibilidade | **passou** — na faixa 0,10–0,50 a confiança final do centralizado vai de 0,34 a 0,69, sempre entre a inicial (0,25) e a do adaptativo (≈ 0,95); fuga cresce com a sobrecarga. Fora da faixa, em 0,05, fica em 0,251 — praticamente parada, como no limiar duro |

Os extremos descritivos também mantêm o sinal: 0,05 e 1,00. Tabelas em
`outputs/diagnosticos/20260921_portoes_suaves/varredura_s/`.

**O que a varredura diz sobre o 0,25.** Não escolhe o valor — a conclusão de
direção vale em toda a faixa testada. O que ela mostra é que a **magnitude** de
falha efetiva e de fração via Porta 1 depende da inclinação:

| inclinação | falha efetiva | fração Porta 1 | chance inicial de aceitar ajuda (centralizado / adaptativo) |
|---:|---:|---:|---|
| 0,05 | −0,0450 | −0,1159 | 0,001 / 1,000 — praticamente o limiar duro |
| 0,10 | −0,0431 | −0,1056 | 0,029 / 0,996 |
| **0,25** | **−0,0229** | **−0,0511** | **0,198 / 0,900** |
| 0,50 | −0,0119 | −0,0431 | 0,332 / 0,750 |
| 1,00 | −0,0168 | −0,0269 | 0,413 / 0,634 — a confiança quase não importa |

0,25 fica na região em que a confiança **ainda decide** (20% contra 90%) sem que
a decisão vire um corte seco. É uma escolha declarada, não uma estimativa.

**Decisão: adotado como nominal v2.** `config/mvp.yaml` passa a ligar os portões
suaves; `config/mvp_v1.yaml` congela a versão anterior.

### Teste que não estava no critério — e que enfraquece um indicador

Pela regra 9, depois da adoção foi rodada também a varredura de governança de 81
perfis sob a v2 (2 592 execuções, mesmo desenho do SAT_GOV de 19/09). Na região
em que o adaptativo tem premissas pelo menos tão favoráveis (1 215 pares):

| indicador | v1: pares a favor do adaptativo | v2 |
|---|---:|---:|
| atraso relativo | 89% | 93% |
| dívida latente | 92% | 91% |
| taxa de omissão | 88% | 76% |
| fração via Porta 1 | 66% | 66% |
| **taxa de falha efetiva** | **75%** | **46%** |

A reconstrução da contagem v1 bate exatamente com o parecer 71. **Na v2, a
vantagem do adaptativo em falha efetiva deixa de ser robusta ao espaço de
governança.** Isso não reverte a adoção: o critério foi escrito antes e passou, e
a v1 só parecia robusta nesse indicador porque o centralizado estava proibido de
pedir ajuda. Mas muda o que se pode afirmar: falha efetiva vale no ponto nominal,
não como conclusão geral. A causa das inversões não foi investigada — fica para a
auditoria.

### Auditoria (22/09/2026) — item 9 marcado DIVERGENTE

O auditor leu o critério de plausibilidade **por execução**; o critério 5 acima foi
escrito sobre a **média**. A média passa (0,605). Por execução, a confiança final
do centralizado fica abaixo da inicial em 2 de 192 execuções do nominal (mínimo
0,238) e em 10 de 576 fora da amostra (mínimo 0,211).

**Causa verificada:** nessas execuções, em média 23 a 27 dos cerca de 30 pedidos
de ajuda falham porque o colega está ocupado, e a Eq. (4) de Crowder desconta
0,01 da confiança a cada pedido frustrado. É o comportamento previsto pela lei que
já estava no nominal: confiança que se desgasta quando a ajuda não chega. Não é
defeito. A ambiguidade foi do enunciado que o revisor passou ao auditor — a ordem
dizia "fica entre 0,25 e a do adaptativo" sem dizer "em média". O README passou a
declarar a fração e o mínimo.
