# Parecer 27 — Auditoria de T1/T2/T3 (commit `ee76fb6`)

**Data:** 17/09/2026 · **Revisor:** Claude
**Verificação:** recomputação da decomposição e das interações a partir das tabelas do parecer 24.

---

## 1. Veredito

O parecer 24 é o melhor documento produzido até agora neste trabalho, e o resultado
**recupera a conclusão de governança** — realocada para outros indicadores. Também
me corrige num ponto de método, que registro na seção 5.

## 2. T2 — a decomposição, recomputada

Referência = arranjo centralizado. Bloco `confianca` = `tau_inicial` **e** `tau_min`;
bloco `reporte` = `p_reporte` **e** `p_deteccao`. Parcelas sobre o contraste total,
com a interação fechando exatamente 100% (conferido linha a linha):

| Indicador | Confiança | Reporte | Interação | Total |
|---|---:|---:|---:|---:|
| `atraso_relativo` | 31,2% | **57,7%** | 11,1% | −1,023421 |
| `taxa_omissao` | 18,1% | **97,5%** | −15,6% | −0,228212 |
| `divida_latente_sobre_plano` | 19,7% | **95,5%** | −15,1% | −0,077815 |
| `taxa_falha_efetiva` | **118,5%** | 19,8% (n.s.) | −38,3% | −0,043056 |
| `fracao_porta1` | **115,6%** | −2,2% (n.s.) | −13,4% | −0,116493 |

Significância dos blocos isolados (IC95):

| Bloco | `taxa_falha_efetiva` | `fracao_porta1` |
|---|---|---|
| confiança | −0,051042 [−0,0669; −0,0352] — **significativo** | −0,134635 [−0,158; −0,111] — **significativo** |
| reporte | −0,008507 [−0,0229; +0,0059] — **inclui zero** | +0,002517 [−0,0060; +0,0110] — **inclui zero** |

**O achado central, e é o inverso do que eu antecipei:** a premissa de reporte domina
`taxa_omissao` e dívida latente — que contam falhas **não reportadas** —, mas **não
tem efeito detectável sobre a taxa de falha efetiva nem sobre a seleção de porta**.
Esses dois são governados pelo bloco de confiança.

## 3. O teste que mais importa: confiança **depois** de igualar o reporte

A tabela "ambos − reporte" isola o efeito de acrescentar confiança quando o bloco de
reporte **já está** no nível adaptativo:

| Indicador | Ambos − reporte | IC95 | Veredito |
|---|---:|---|---|
| `atraso_relativo` | −0,432614 | [−0,491; −0,374] | **significativo** |
| `taxa_falha_efetiva` | −0,034549 | [−0,049; −0,021] | **significativo** |
| `fracao_porta1` | −0,119010 | [−0,139; −0,099] | **significativo** |
| `divida_latente_sobre_plano` | −0,003527 | [−0,0061; −0,0010] | significativo, magnitude pequena |
| `taxa_omissao` | −0,005816 | [−0,0136; +0,0020] | inclui zero |

**Isto é o que salva o capítulo de governança.** O arranjo de confiança reduz prazo,
taxa de falha real e uso da porta heurística **mesmo depois de neutralizada a
premissa de reporte**. Não é tautologia: é mecanismo.

## 4. O que a monografia pode e não pode afirmar

| Pode afirmar | Não pode afirmar |
|---|---|
| O arranjo de confiança reduz `atraso_relativo` em 0,433 (IC95 [0,374; 0,491]) com reporte igualado | Que o arranjo adaptativo reduz falhas não reportadas — isso é 97,5% premissa de reporte |
| Reduz a taxa de falha **efetiva** em 0,035 [0,021; 0,049] | Que a premissa de reporte reduz defeitos gerados — IC inclui zero |
| Reduz a fração de decisões pela Porta 1 em 0,119 [0,099; 0,139] | Que dívida latente demonstra efeito de governança — 95,5% premissa |
| Que reporte e confiança **interagem**, com subaditividade nas reduções | Somar as parcelas como percentuais causais independentes |

Redação sugerida para o achado principal: *"Igualadas as premissas de reporte e
detecção, o arranjo de confiança ainda reduz prazo, taxa de falha efetiva e uso da
rota heurística. O contraste em falhas não reportadas e dívida latente, por outro
lado, é majoritariamente atribuível à premissa de reporte e não constitui evidência
independente de efeito de governança."*

## 5. Correção que o parecer 24 faz no parecer 23 — e eu aceito

Eu decompus `taxa_omissao` em escala logarítmica pela razão das premissas de não
reporte (3,400 contra contraste observado 3,708), concluindo 93,4% de parcela da
premissa. O parecer 24 observa, corretamente, que **essa comparação não identifica
parcela causal**, porque reporte e detecção também afetam filas, duração, pressão e
sorteios futuros. A decomposição por intervenção (T2) mede o regime explicitamente,
com as interações.

Meu 93,4% era aproximação descritiva de uma quantidade que não é a parcela causal.
O valor medido é **97,5%**. A conclusão qualitativa sobreviveu; o método estava
errado. Registrado como **R-08**.

## 6. T1 — o que o teste sustenta, e o que não

**Sustenta**, e com evidência determinística: em estado local fixo, `mu_rede` varia
de 0,775 a 1,000 com τ sem alterar `mu_cog`. É um canal contínuo real, computado,
não estimado. A hipótese de degrau puro está refutada nesse canal.

**Não sustenta:** as tabelas de contraste local têm 4 instâncias × 4 sementes por
célula, com IC sobre 4 médias — t com 3 graus de liberdade. Dos 24 contrastes locais,
a maioria inclui zero. Isso é **baixa potência**, não ausência de efeito, e o próprio
relatório diz isso. Logo, a refutação do degrau puro apoia-se no canal determinístico,
não nas curvas estocásticas. Escrever assim no texto.

**Achado emergente que merece destaque, e o relatório subestima:** em `tau_min = 0,6`
com `p_reporte = 0,15`, abrir o portão **aumenta** o atraso (+0,2948, IC95 [0,0295;
0,5602], exclui zero). Assistência tem custo — o colega fica ocupado um período — e
com reporte baixo o benefício não se materializa. Um regime em que ajudar piora o
prazo é exatamente o tipo de resultado não óbvio que justifica um simulador. Não é
só uma ressalva; é material para a discussão.

## 7. O confundimento que resta — e o T4 que o resolve

`confianca` no T2 move `tau_inicial` **e** `tau_min` juntos, e o relatório declara
isso. Mas há uma consequência que ele não tira: `tau_inicial` alimenta **dois
caminhos** — o portão de assistência e a entrada difusa (`desconfianca = 1 − confianca`,
que produz `mu_rede`). Portanto o efeito significativo sobre `taxa_falha_efetiva`
pode vir da assistência **ou** do canal difuso, e T2 não separa os dois.

Isso importa porque o caminho é indireto e vale a pena verificá-lo: `p0` depende de
`mu_cog`, não de `mu_rede`. `mu_rede` afeta produtividade → duração → drenagem de
bateria e pressão → `mu_cog` → `p0`. Se o efeito vier por aí, a leitura correta não é
"assistência reduz defeito", e sim "confiança reduz duração, e duração reduz
degradação cognitiva".

**T4 (barato, maquinaria pronta):** `tau_portao` e `tau_rede` já existem como
overrides independentes. Rodar quatro células — portão centralizado/adaptativo ×
rede centralizada/adaptativa — com reporte igualado, e reportar os cinco indicadores.
Isso decide se o efeito sobre a taxa de falha efetiva passa pela assistência ou pelo
canal difuso.

## 8. Sobre a alternativa de reposicionamento (T1, §final)

O desenho proposto — limiar comum, confianças a +0,01 e +0,05 — está correto em
princípio e a ressalva sobre rótulos é a certa. Um alerta de potência: com margens de
+0,01 e +0,05, os braços diferem em 0,04 de τ, contra 0,55 no histórico. O contraste
vai encolher muito, e com 4 instâncias por célula provavelmente ficará indetectável.
Ou aumentar instâncias, ou incluir margens mais largas na família (por exemplo
+0,01 / +0,05 / +0,15 / +0,30), para que a ausência de efeito seja informativa e não
apenas falta de potência.

## 9. Créditos

Registro porque são práticas que devem aparecer na monografia como evidência de rigor:

- protocolo registrado **antes** de executar (`research/PLANO_T1_T2_T3.md`);
- declaração explícita de que o consumo sequencial de sorteios pode desalinhar as
  trajetórias, e de que não se alega identidade de sorteio por tarefa — honestidade
  sobre o estimando que a maioria dos trabalhos omite;
- recusa a somar parcelas como percentuais causais, com a fórmula da interação escrita;
- "inclui zero significa inconclusivo, não ausência de efeito" — dito explicitamente;
- recusa a eleger limiar pelo sinal favorável, tendo encontrado um sinal desfavorável;
- T3 implementado como campo derivado sem alterar RNG, com controle ANTES/DEPOIS
  (resíduo máximo 2,84 × 10⁻¹⁴).

## 10. Recomendação

1. **T4** (separação portão × canal difuso) — único teste que ainda falta para a
   leitura do mecanismo ficar fechada. Barato.
2. **Escrever o capítulo de governança agora**, na forma da seção 4. O resultado está
   maduro; adiar só consome prazo.
3. O reposicionamento próximo ao limiar é interessante mas **não é pré-requisito da
   monografia**. Se o prazo apertar, entra como trabalho futuro.
