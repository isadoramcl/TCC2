# Parecer 43 — D-13: o delta contra o precedente híbrido ABM+SD

**Data:** 18/09/2026 · **Revisor:** Claude
**Fonte:** Pessoa, Naess, Bijos, Rebello, Colombo, Schnitman e Nogueira.
*A Hybrid Agent-Based and System Dynamics Framework for Modelling Project
Execution and Technology Maturity in Early-Stage R&D.* **TEXTO LIDO na íntegra.**

> ⚠ **Estado da referência: PREPRINT.** O próprio rodapé diz *"Preprint submitted
> to Elsevier"*. Não achei número de volume, páginas nem DOI no texto. **Confirme
> o estado de publicação e o ano antes de citar** — e, se continuar preprint,
> declare isso na citação. Não invente o ano: o texto cita Pujotomo et al. (2025),
> então é 2025 ou posterior, e é só isso que se pode afirmar.

---

## 1. Por que este item é o de maior risco

É a pergunta mais provável da banca, e a mais barata de fazer: *"modelo híbrido
ABM+SD de execução de projeto com retrabalho e pressão de cronograma já existe —
o que o seu tem de diferente?"*

Pior: o precedente reivindica a mesma lacuna. Ele abre dizendo que modelos
híbridos AB–SD *"are well established in other fields"* mas que a aplicação a
P&D *"remains limited"*. Se você não tiver a resposta pronta e específica, a
sobreposição aparente responde por você.

A boa notícia é que o delta é largo e as diferenças são **estruturais**, não de
ajuste. Três delas o próprio artigo lista como trabalho futuro dele.

---

## 2. O delta, em quatro eixos

| | Precedente (Pessoa et al.) | Este trabalho |
|---|---|---|
| **Agentes** | **Homogêneos por hipótese**: *"identical properties in terms of availability, skill level, and behavioral logic"* | Heterogêneos, com competência e estado cognitivo; dispersão **ancorada em medida de campo** (CV = 1,13, Stewart 1992) |
| **Efeito da pressão** | Multiplica a **produtividade** global por curva de lookup não linear | Muda **qual estratégia** o agente seleciona (Porta 1 heurística × Porta 3 analítica), e a estratégia muda o erro |
| **Retrabalho** | **Exógeno**: probabilidade fixa por tarefa, 0,2–0,5, definida no cenário | **Endógeno**: emerge do erro, que emerge da porta escolhida, que emerge do estado do agente |
| **Fator experimental** | Tamanho de equipe e topologia de dependências | **Arranjo de governança** — limiares de confiança, reporte e detecção |
| **Validação** | *"expert judgement and historical comparison"*; auto-declarado *"proof-of-concept rather than a predictive or diagnostic instrument"* | History Matching com NROY e taxa de falsa exclusão; reprodução de controle publicado; identidade bit a bit |

### 2.1 O eixo mais forte: heterogeneidade

O precedente não apenas assume agentes idênticos — ele **lista a remoção dessa
hipótese como trabalho futuro**, item (2) da seção de desenvolvimentos futuros:
*"integrating adaptive and learning-based decision mechanisms that enable agents
to adjust behaviour dynamically in response to changing project conditions"*.
E a seção de hipóteses diz explicitamente que os agentes seguem regra fixa
*"without modelling individual personality or cognitive variation"*.

É exatamente onde este trabalho opera. E a diferença não é de ambição: é que
aqui a dispersão entre agentes tem **origem empírica publicada**, não é parâmetro
de conveniência.

### 2.2 O eixo mais interessante para a banca: o canal causal

Esta é a diferença que vale explicar no quadro, porque não é óbvia na tabela.

No precedente, pressão → produtividade. Todo mundo fica mais rápido (ou mais
lento, passado o joelho da curva). O retrabalho não depende disso: ele é sorteado
com probabilidade fixa da tarefa.

Aqui, pressão → **seleção de estratégia** → erro → retrabalho. O retrabalho é
consequência de uma decisão, não um sorteio paralelo. Isso é o que permite
perguntar o que o precedente não pode perguntar: **se o arranjo de governança
muda o resultado, ele muda por reduzir o erro ou por redistribuir o trabalho?**
O I-8 já mostrou que, neste modelo, a resposta é a segunda — e essa é uma
pergunta que só existe quando o retrabalho é endógeno.

### 2.3 O eixo do fator experimental

O precedente varia **recurso** (1 a 10 pessoas) e **topologia** (paralelo ×
sequencial). São perguntas de dimensionamento e de cronograma.

Este trabalho varia o **arranjo organizacional** — quem reporta, com que
frequência se detecta, quanta confiança é preciso ter para pedir ajuda. É uma
pergunta sobre organização, não sobre recurso, e não encontrei nenhum trabalho
nessa linha que a faça.

---

## 3. O que o precedente tem e este trabalho não tem

Isto entra no texto como delimitação, e é melhor você dizer antes que perguntem.

1. **Maturidade tecnológica (TRL).** Eles acoplam a execução a uma CDF de
   maturidade (t de Student sobre ln da fração concluída, seguindo Kenley et al.).
   Este trabalho não tem construto de maturidade e não precisa ter — mas diga
   que não tem, e por quê: o objeto aqui é o processo de execução, não a
   progressão de prontidão tecnológica.
2. **Enquadramento setorial.** Eles têm um caso de óleo e gás com coautoria do
   CENPES/Petrobras. Este trabalho usa instâncias do PSPLIB J60 — **o que é uma
   vantagem metodológica** (rede de tarefas de benchmark, reprodutível por
   terceiros, contra 15 tarefas construídas à mão), mas é uma desvantagem de
   concretude setorial. Declare os dois lados.
3. **Camada SD explícita em estoques e fluxos.** Eles publicam quatro estoques
   (WTD, WQA, WCR, WA) e sete fluxos com as equações diferenciais. Vale conferir
   se a sua camada SD está documentada com o mesmo nível de explicitação —
   se não estiver, **é o item mais barato de melhorar antes do congelamento**,
   e é exatamente o tipo de coisa que uma banca cobra na comparação.

---

## 4. Um presente do precedente, que vale citar

Na discussão do Experimento 2 eles escrevem, sobre o próprio resultado:

> *"It remains improbable that a five-member team could complete a complex
> offshore R&D project, spanning early-phase development to commercialisation,
> within 156 weeks. This discrepancy suggests that the current parameterisation
> may overestimate agent productivity, highlighting a key avenue for future model
> calibration using empirical data."*

É o precedente declarando, em texto, que a falta de ancoragem empírica produziu
resultado implausível. Use isso para justificar o esforço de ancoragem deste
trabalho — Stewart & Melchers para o erro basal, Stewart 1992 para a dispersão,
Crowder para competência e confiança — **sem precisar criticar o artigo deles**.
É a citação mais econômica que você pode fazer: ela sustenta a sua escolha com a
palavra do autor que fez a escolha oposta.

---

## 5. O parágrafo para a monografia

Meia página, para o capítulo de posicionamento. Confira o ano antes de usar.

> Trabalhos híbridos que combinam Modelagem Baseada em Agentes e Dinâmica de
> Sistemas para execução de projetos existem, e o mais próximo deste é o de
> Pessoa et al., que acopla uma camada de agentes de tarefa e de membro de equipe
> a uma estrutura de estoques e fluxos com ciclos de retrabalho, e dela deriva
> uma distribuição de maturidade tecnológica. A diferença em relação ao presente
> trabalho é estrutural e está em três pontos. Primeiro, naquele modelo os
> membros de equipe são homogêneos por hipótese declarada, seguindo regra fixa,
> sem variação cognitiva entre indivíduos; aqui a heterogeneidade entre agentes é
> representada e sua dispersão é ancorada em medida de campo publicada. Segundo,
> naquele modelo a pressão de cronograma atua sobre a produtividade por meio de
> um fator global, enquanto o retrabalho é sorteado com probabilidade fixa
> atribuída a cada tarefa; aqui a pressão atua sobre a seleção de estratégia do
> agente, e o retrabalho é consequência endógena do erro que essa seleção produz.
> Terceiro, aquele trabalho toma como fatores experimentais o tamanho da equipe e
> a topologia de dependências, ao passo que aqui o fator experimental é o arranjo
> de governança. As duas primeiras diferenças correspondem a itens que os próprios
> autores registram como desenvolvimento futuro de seu modelo. Cabe registrar
> ainda que aquele trabalho se posiciona explicitamente como prova de conceito
> validada por julgamento de especialista, sem calibração empírica, e observa que
> sua parametrização pode superestimar a produtividade dos agentes — observação
> que motiva o esforço de ancoragem empírica adotado aqui.

---

## 6. O que fazer com isto

| | |
|---|---|
| **Agora** | Confirmar estado de publicação, ano e DOI. Entra no `04_FONTES.md` com a linha "→ não sustenta" |
| **Antes do congelamento** | Conferir o item 3.3 — explicitação da camada SD em estoques e fluxos |
| **No texto** | §5 vai no capítulo de posicionamento; §3 vai nas delimitações |

Nada aqui depende do Codex nem do lote 37. É trabalho de leitura e escrita, e
pode ser feito em paralelo ao que ele está rodando.
