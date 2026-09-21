# 74 — Portões suaves: proposta testada para os itens 5, 6 e 7

**Data:** 21/09/2026 · **Executado por:** Claude (revisor), a pedido da autora.
**Sem auditoria independente** — mesma ressalva do parecer 45. O Codex deve
refazer a análise quando voltar.
**Estado:** implementado como **opção desligada**. O nominal publicado não mudou.
Adotar como nominal é decisão da autora com o orientador (§7).

Código: `src/modelo/simulador_mvp.py` (opções `portao_assistencia`,
`regra_fuga='logistica'`, `efeito_fuga`, `s_portoes`) ·
Testes: `research/test_portoes_suaves.py` ·
Scripts: `research/validacao/portoes_suaves/` ·
Evidência: `outputs/diagnosticos/20260921_portoes_suaves/`

---

## 1. O problema, em uma frase

O TCC I especifica três decisões como **comparação dura entre dois números**
(`E > τsat`, `Ω > Limite`, `τk > τmin`). O TCC2 já tinha trocado a primeira por
uma probabilidade suave, `p_heu = σ((E − τsat)/s)`. As outras duas ficaram duras,
e são exatamente as duas que degeneram: a fuga nunca dispara (A-14) e o pedido de
ajuda no arranjo centralizado nunca abre (A-13).

## 2. A proposta

Aplicar às duas decisões restantes **a mesma forma que o modelo já usa na Porta 1**.

| decisão | TCC I | proposta |
|---|---|---|
| aceitar colega *k* como apoio (Porta 2) | `τk > τmin` | aceita com probabilidade `σ((τk − τmin)/s_p)` |
| adiar a tarefa (fuga, Porta 1) | `Ω > Limite` | adia com probabilidade `σ((ω·q − Limite)/s_p)` |

- **`s_p = 0,25`** `[DEC]`: a inclinação nominal da transição cognitiva, fixada e
  **não varrida** junto com `s_transicao`. Confiança e aversão à perda são
  construtos distintos da seleção heurística. É o **único parâmetro novo**, e não
  tem fonte.
- **Confiança continua com a lei de Crowder, Eq. (4)**, que já está no nominal:
  sobe com ajuda bem-sucedida, cai 0,01 com pedido frustrado. A mudança é só que
  agora ela tem como ser exercida.
- **Fuga continua drenando a bateria**, como manda a linha 3 do algoritmo da
  Porta 1 no TCC I. A variante com alívio foi testada (F2 e GF) e **descartada**:
  não é necessária para o projeto terminar e se afastaria do TCC I.
- Os sorteios novos vêm de um **fluxo aleatório auxiliar**; o fluxo principal fica
  intacto, e com as opções desligadas o fluxo auxiliar nem é criado.

**Base conceitual.** A confiança cognitiva é definida no próprio TCC I como crença
sobre a competência técnica dos pares, construída na interação. A fuga é o
adiamento por falta de tempo documentado por Ball et al. (2014). As fontes dão o
construto, não os valores.

## 3. Verificação

- Opções desligadas: **nominal reproduzido bit a bit**, 384 execuções, 45 campos,
  zero divergentes, rodado a partir do código principal já modificado.
- Suíte completa: **31 arquivos, 101 testes, todos aprovados**.
- Os testes novos foram checados contra implementações erradas: sem o portão
  logístico, a chave travada do B2 não termina; com a fuga por limiar, a fuga
  não dispara. Os dois testes separam o certo do errado.

## 4. Resultado no nominal (16 instâncias × 12 sementes)

Contraste adaptativo − centralizado, IC95 sobre instâncias:

| indicador | publicado | portões suaves (GF1) | variação |
|---|---:|---:|---:|
| atraso relativo | −1,0234 [−1,114; −0,933] | −0,9429 [−1,086; −0,799] | −8% |
| taxa de omissão | −0,2282 [−0,243; −0,214] | −0,2016 [−0,214; −0,189] | −12% |
| dívida latente | −0,0778 [−0,086; −0,069] | −0,0694 [−0,076; −0,063] | −11% |
| taxa de falha efetiva | −0,0431 [−0,057; −0,029] | −0,0229 [−0,035; −0,011] | −47% |
| fração Porta 1 | −0,1165 [−0,137; −0,096] | −0,0511 [−0,070; −0,033] | −56% |

**Fora da amostra (48 instâncias):** −0,9860 / −0,2074 / −0,0727 / −0,0213 /
−0,0499, **todos com IC excluindo zero**.

**Leitura.** Os cinco indicadores continuam favorecendo o arranjo adaptativo, com
significância, dentro e fora da amostra. O que encolhe é a parte do efeito que
vinha de **o centralizado estar proibido de pedir ajuda por construção** —
sobretudo falha efetiva e fração Porta 1, as mais dependentes do portão. O que sobra é atribuível a reporte, detecção e
confiança que cresce mais devagar.

## 5. Testes de estresse — onde o modelo antes travava

| caso | antes (limiar) | portões suaves |
|---|---|---|
| fuga com limite 0,10–0,40 (A1, regra dependente de estado), centralizado | 0/64 terminam | **64/64** (F1) |
| fuga com limite 0,10–0,40 (A1, regra dependente de estado), adaptativo | 33/64 | **64/64** (F1) |
| as 36 chaves incompletas do B2 (`s_transicao = 0,01`) | 0/36 | **36/36** (G e GF) |

Na fuga logística a fração de adiamentos **cai de forma gradual** quando o limite
sobe (centralizado: 0,55 → 0,45 → 0,37 → 0,29). É o mecanismo contínuo que o A1
não conseguiu produzir com limiar.

Estresse rodado com teto de 16×CPM em vez de 256×, para caber no tempo de
execução. A referência por limiar (A1) reproduz as mesmas contagens do A1
publicado sob esse teto.

## 6. O resultado faz sentido? — checagens de plausibilidade

1. **A confiança no centralizado sobe, mas não alcança a do adaptativo.** Média
   final ≈ 0,60 contra ≈ 0,95. A hierarquia **atrasa** a construção de confiança
   em vez de proibi-la. É o comportamento esperado.
2. **A fuga cresce com a sobrecarga.** Entre escolhas heurísticas: ≈ 8–12% sem
   sobrecarga (q = 0) e 33–43% com sobrecarga alta (q > 0,75), contra o teórico
   de 8,3% e 40%. O mecanismo responde à variável certa.
3. **Adiar não explode o prazo.** O atraso fica próximo do nominal, porque o
   adiamento também evita parte das execuções heurísticas de risco. É um
   trade-off plausível, não um artefato.
4. **Efeito colateral a declarar.** A forma logística tem piso: com sobrecarga
   zero ainda há ≈ 8% de adiamento entre as escolhas heurísticas. É procrastinação
   leve, defensável, mas vem da forma escolhida, não de dado.

## 7. O que muda nos itens 5, 6 e 7

- **Item 6 (portão de assistência):** deixa de ser degenerado. Passa a ser
  premissa declarada — a confiança **inicial** é mais baixa no centralizado — com
  uma lei de evolução que já estava no modelo.
- **Item 5 (fuga):** passa a ser mecanismo ativo e gradual.
- **Item 7 (`s_transicao = 0,01`):** o canto **não trava mais** (36/36). A seleção
  heurística continua quase inacessível ali, porque é isso que o valor significa,
  mas o projeto termina. Vira extremo da faixa de sensibilidade, não degeneração.

**Para adotar como nominal:** trocar o default em `config/mvp.yaml`, rodar de novo
o nominal e a validação fora da amostra, regenerar as tabelas e o README, e pedir
ao Codex a auditoria. As três condições degeneradas passam a ser um **achado sobre
a especificação do TCC I** — limiar duro degenera, a forma suave que o TCC2 já
usava na Porta 1 resolve —, não uma limitação do modelo entregue.

## 8. Achado lateral — precisão do CSV fora da amostra

O arquivo `20260920_fora_da_amostra/bruto_fora_da_amostra.csv` perdeu o último
bit em campos derivados: `atraso_relativo` não é igual, bit a bit, a
`makespan/makespan_cpm` recalculado a partir do próprio arquivo. As diferenças são
≤ 3·10⁻¹⁴. A reexecução reproduz o modelo exatamente, e **os IC publicados não
mudam** em nenhuma casa reportada. Consequência: a identidade bit a bit daquela
validação se verifica contra reexecução, não contra o arquivo. O Codex deve ver
isso na auditoria.
