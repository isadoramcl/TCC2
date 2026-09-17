# Parecer 33 — Avaliação da matriz de fontes e da proxy de bateria

**Data:** 17/09/2026 · **Revisor:** Claude
**Objeto:** matriz rastreável de decisão proposta em conversa paralela, com nove fontes
**Método:** verificação das referências na origem e auditoria do mapeamento construto → parâmetro

---

## 1. Veredito em uma linha

A matriz é boa e o formato é o certo. **Oito das nove fontes entram sem risco, como
justificativa estrutural.** A nona — a proxy de bateria a partir de Zhao — **não deve ser
implementada**, por três razões técnicas, e não por falta de qualidade da fonte.

---

## 2. Verificação das referências

### Zhao, Qi & Chen (2026) — **CONFIRMADA na origem**

*Job demands, job resources, and burnout among metro site management personnel in China:
a cross-sectional study based on the JD-R model.* Frontiers in Psychology, publicado em
23/07/2026. DOI [10.3389/fpsyg.2026.1856402](https://doi.org/10.3389/fpsyg.2026.1856402) ·
PubMed 42564107 · PMC13441851.

Conferido no texto integral:

| Item | Valor confirmado |
|---|---|
| Amostra | **274 respostas válidas**, gestão de obras de metrô na China |
| Perfil | 81,8% homens; 37,6% com 5–10 anos de casa; 88,3% com jornada > 8 h |
| Carga de trabalho | 3 itens, Likert de 5 pontos, α = 0,838 |
| Complexidade | 5 itens, Likert de 5 pontos, α = 0,859 |
| Exaustão | MBI-GS, **6 itens**, α = 0,925 |
| Coeficientes | carga **β = 0,608**; complexidade **β = 0,349** |
| Desenho | **transversal** ("a two-stage cross-sectional survey was conducted") |
| Limitação declarada | *"because all variables were collected through self-report questionnaires, common method variance cannot be entirely excluded"* |

**Divergência de DOI a corrigir.** O artigo declara os dados em
`10.5281/zenodo.21153010`. A matriz cita `10.5281/zenodo.21153011`. Provavelmente é o par
normal do Zenodo — DOI de conceito e DOI de versão — mas **cite o que está no artigo** e
confirme ao baixar.

### Stewart (1992) e Stewart & Melchers (1988) — **CONFIRMADAS** (parecer 30)

### Melchers (1989), JSE 115(7), 1795–1807 — **autoria a conferir**

O artigo existe. Mas a literatura adjacente é assinada **Stewart & Melchers** em conjunto
(1988 Structural Safety; 1989 Error control in member design). A matriz atribui este a
Melchers sozinho. Conferir a folha de rosto antes de citar — errar autoria é o tipo de
detalhe que a banca nota.

### Rieskamp & Hoffrage (2008) — **NÃO VERIFICADA**, e é a mais promissora do G-03

*Inferences under time pressure: how opportunity costs affect strategy selection.* Acta
Psychologica 127(2), 258–276. DOI 10.1016/j.actpsy.2007.05.004.

Se ela reportar **proporção de escolhas descritas por cada estratégia**, é melhor candidata
que Payne, Bettman & Luce (1996), que eu trouxe no parecer 30 — porque ali o deslocamento de
estratégia apontou na direção certa mas **não foi significativo** (F(1,70) = 0,67). Obter e
conferir: é a melhor chance aberta de fechar o G-03.

### Ball et al. (2014), White et al. (2019), Lee et al. (2020), Jarratt et al. (2011) — **NÃO VERIFICADAS**

Plausíveis e bem descritas. Obter antes de citar, pela regra do projeto.

---

## 3. A proxy de bateria — três razões para não implementar

A proposta é `B_i = 1 − norm(exaustão_i)`. A matriz já marca como hipótese a auditar, o que
está certo. Auditando: **não sobrevive.**

### 3.1 Transversal não informa variável de estado

No modelo, `B` é **recurso que se esgota e se recupera ao longo do projeto**: parte de
`b_inicial = 1,00`, drena `k·E` por período e recupera `r_recuperacao`. Zhao é **uma
medição por pessoa, sem dimensão temporal**. Um escore transversal não pode informar uma
dinâmica de depleção.

E também não serve como `b_inicial`: `b_inicial = 1,00` é declarado como "bateria plena no
início", enquanto Zhao mede exaustão de regime em profissionais com 5–10 anos de casa e
jornada acima de 8 horas. São pontos diferentes da trajetória, e mapear um no outro exige
declarar a que instante do projeto a medição de Zhao corresponde — o que ninguém consegue
fazer com dado transversal.

### 3.2 A dupla contagem é pior do que a matriz sinaliza

A matriz alerta para o risco. A magnitude é o problema.

Em Zhao, **exaustão é o desfecho** predito por carga (β = 0,608) e complexidade (β = 0,349).
No modelo, `E = D·P/B`, com `D` ≈ complexidade e `P` ≈ carga. Se `B := 1 − norm(exaustão)`,
então `B` passa a ser função de `D` e `P`, e o índice vira:

```
E = D·P / f(D, P)
```

`D` e `P` entram **duas vezes**, com forma funcional implícita e não controlada. E como a
carga domina (0,608 contra 0,349), `B` seria majoritariamente o inverso da pressão, tornando
`E` explosivo em `P`. Não é um risco a monitorar — é uma alteração estrutural da equação
central do modelo, feita por acidente.

### 3.3 Escala afetiva não é capacidade mecânica

A exaustão do MBI-GS são 6 itens Likert sobre **exaustão emocional sentida**. O `B` do
modelo é uma capacidade que **multiplica duração e probabilidade de erro**. A transformação
`1 − norm(·)` não tem base empírica: é escolhida por conveniência de escala.

E isto é o ponto decisivo: hoje `b_inicial` é **um parâmetro arbitrário**. A proposta o
substituiria por **uma função arbitrária**. Função tem mais graus de liberdade que
parâmetro, e eles ficam escondidos dentro da normalização. **Trocaria arbitrariedade
declarada por arbitrariedade oculta** — o oposto do que o trabalho vem fazendo.

---

## 4. O que Zhao faz de valioso — e é mais do que parece

Zhao **sustenta estruturalmente a direção** `carga, complexidade → desgaste`, **na população
certa**: gestão de obras de engenharia, não enfermagem, não esporte, não software.

E isso responde parcialmente ao desafio que a bancada de fatores humanos levantou. A bancada
não encontrou apoio de campo para "mais pressão → mais erro" (tênis com sinal oposto, NBA e
Go nulos). Mas esse é **outro elo da cadeia**. Montando:

| Elo | Fonte | População | Estado |
|---|---|---|---|
| `D, P → exaustão` | **Zhao (2026)**, β = 0,608 / 0,349 | gestão de obras | **apoiado, domínio certo** |
| `exaustão → omissão` | White (2019), OR ≈ 4,97 | enfermagem | apoiado, domínio distante |
| `omissão → pior desfecho` | — | — | **suposição do modelo** |

O primeiro elo passou a ter apoio de campo no domínio certo. É ganho real para o capítulo de
justificativa, e **não custa uma linha de código.**

---

## 5. O achado mais útil da matriz: Ball e White sustentam a porta errada

Em enfermagem, *care left undone* é **a tarefa necessária NÃO ter sido realizada** por falta
de tempo. Na Porta 1 do modelo, a tarefa **é realizada** — mais rápido e com mais risco. São
construtos diferentes.

O construto do modelo que corresponde à omissão de enfermagem é a **rota de fuga (`P1_fuga`)
— o adiamento**. E essa rota **nunca executa**: `p1_fuga = 0,000000` nos dois arranjos,
porque `omega > limite_aversao_perda` é `0,50 > 0,60`, falso por construção (achado A-14,
parecer 29).

**Portanto Ball e White, usados corretamente, são evidência para corrigir a rota de fuga —
não para sustentar a Porta 1.** Isso torna as duas fontes mais úteis do que a matriz propõe,
e reforça a prioridade 1 da ordem de serviço 32.

Sobre o OR = 4,97 de White: é enorme, vem de autorrelato transversal com viés de método
comum declarado, e mapear razão de chances para incremento de probabilidade exige uma linha
de base. A matriz diz "não transportar literalmente" — correto —, mas "usar para limitar
faixa de sensibilidade" ainda é uso quantitativo. Recomendo: **direção apenas**. Se uma faixa
for derivada, a derivação tem que estar escrita e ser auditável.

---

## 6. Sobre a autorização para dados sintéticos

Vale notar: **esta proposta quase não usa a autorização.** Todas as nove fontes são dados
reais publicados. Isso é melhor que síntese, e significa que a permissão do orientador
continua disponível, não gasta.

Guarde-a para o único lugar onde ela resolve algo que fonte nenhuma resolve: o **`k` da
composição de Stewart** — quantas microtarefas elementares compõem uma atividade do J60.
Sintetizar uma decomposição de tarefa a partir de procedimentos de projeto documentados,
declarada como sintética e varrida, é uso legítimo e fecha a ponte de agregação do G-02.
Esse é o uso de alto valor da autorização.

---

## 7. O que cabe antes de 27/09 e o que não cabe

### Cabe — texto, zero código, zero reexecução

- Citar Zhao, Lee, Ball, White, Rieskamp e Stewart/Melchers como **justificativa estrutural**
  no capítulo de modelo. Fortalece muito o trabalho sem alterar um número sequer.
- **A própria matriz vira apêndice.** O formato — fonte, o que mede de verdade, como entra,
  pode parametrizar, status — é exatamente o que uma banca quer ver. Acrescentar a coluna de
  estado de verificação do `04_FONTES` e migrar as entradas para lá.
- Reenquadrar Ball e White como evidência da rota de fuga (§5).
- Obter os primários: Rieskamp, Ball, White, Lee, Melchers 1989.

### Não cabe

- **A proxy de bateria.** Baixar o Zenodo, auditar microdados, reconstruir escalas, decidir
  transformação, testar dupla contagem, implementar, rerrodar tudo e reauditar são semanas.
  E altera a dinâmica: com `b_inicial` heterogêneo, o nominal muda e o capítulo de resultados
  precisa ser reescrito a 10 dias do congelamento. Somado às três razões da §3, a recomendação
  é **não fazer**, não apenas adiar.

### O que fazer com o pacote do Zenodo, se ela quiser baixar mesmo assim

Não é desperdício — só não vai para dentro do modelo. Serve para: (a) confirmar os números
citados no artigo, o que sustenta a citação; (b) descrever a distribuição de exaustão na
população, o que é material de justificativa; (c) verificar se carga e complexidade são
separáveis empiricamente, o que informa se `D` e `P` do modelo são construtos distintos ou
colineares no mundo real. **Esse terceiro item é interessante por si só** e é barato.

---

## 8. Créditos

O formato da matriz é o certo, e três decisões dela merecem registro:

- a coluna **"pode parametrizar?"**, que separa apoio estrutural de valor numérico — é a
  mesma disciplina do `04_FONTES`, aplicada a um problema novo;
- a recusa explícita a transportar os 86% de Ball, o OR 4,97 de White e os coeficientes de
  Lee;
- a instrução de **não alterar código antes de auditar o mapeamento**. É exatamente a ordem
  certa, e foi ela que permitiu que esta auditoria encontrasse a dupla contagem antes de
  custar uma rodada.
