# Parecer 30 — G-02 resolvido; G-01 e G-03 com rota nova; e o que é o problema da calibração

**Data:** 17/09/2026 · **Revisor:** Claude
**Origem:** proposta da autora de buscar Stewart/Melchers em nível de macrotarefa

---

## 1. G-02 — A intuição da autora estava certa, e a lacuna fecha

Existe uma literatura inteira, no domínio certo, que **construiu exatamente a ponte de
agregação que faltava** — e usa a mesma palavra: microtarefa e macrotarefa.

### 1.1 O número

> Stewart obteve uma **taxa média de erro de 0,0163 por microtarefa de projeto**,
> a partir de levantamento de 25 microtarefas de complexidade comparável.

Fonte: revisão *Human and organizational factors influencing structural safety*,
[repositório TU Delft](https://repository.tudelft.nl/file/File_d99d9e9d-813f-4ea8-a169-7463a502dd9d),
citando Stewart (1992). **Estado: número lido numa revisão; obter o primário antes de citar.**

### 1.2 Por que isso fecha a lacuna

A obstrução do G-02 era: *o HEART dá probabilidade por passo elementar, o modelo precisa
de probabilidade por atividade, e não há regra de composição justificável.*

Stewart e Melchers resolveram esse problema em 1988–1993, para tarefas de projeto
estrutural:

- **microtarefas** — consulta a tabela, cálculo numérico, ordenação de números,
  determinação de fator de redução de vento;
- **macrotarefas** — o processo de projeto completo, encadeando microtarefas;
- e a validação: o modelo de macrotarefa foi comparado com **dados de levantamento da
  mesma tarefa**.

Ou seja: não é preciso inventar uma camada. Existe precedente publicado, no domínio de
engenharia (não nuclear, não aviação), que compõe microtarefas em macrotarefa e valida
o resultado contra observação.

### 1.3 O que isso faz com `F_ancora` — e é o ganho maior

Compondo com independência, `F_ancora = 1 − (1 − 0,0163)^k`, onde `k` é o número de
microtarefas por atividade:

| k microtarefas | F_ancora |
|---:|---:|
| 3 | 0,048 |
| 5 | 0,079 |
| 7 | 0,109 |
| 10 | 0,151 |
| 13 | 0,192 |
| 15 | 0,218 |
| 18 | 0,256 |
| 20 | 0,280 |
| 30 | 0,389 |

**A varredura que o trabalho já usa — [0,05; 0,10; 0,15; 0,20; 0,25] — corresponde a
k ≈ 3 a 17,5 microtarefas por atividade.**

Isso transforma `F_ancora` de palpite em parâmetro com interpretação declarada. A frase
que entra na monografia deixa de ser *"faixa a priori escolhida"* e passa a ser:

> A faixa de `F_ancora` corresponde a atividades compostas por 3 a 18 microtarefas
> elementares de projeto, à taxa de erro por microtarefa de 0,0163 levantada por
> Stewart junto a engenheiros profissionais, sob composição por independência.

Um parâmetro dos 39 sai de "arbitrário" e vira "ancorado com hipótese de composição
declarada". **É o primeiro.**

### 1.4 O que ainda falta, e é honesto declarar

- A hipótese de **independência** entre microtarefas. Stewart mediu correlação de taxas
  de erro dentro de indivíduos, então a independência é aproximação — e ele próprio
  fornece o vocabulário para discuti-la.
- O valor de `k` para uma atividade do J60. O PSPLIB não traz decomposição de tarefa.
  Mas agora `k` é uma quantidade **interpretável e varrida**, não um parâmetro oculto.
- O número 0,0163 veio de revisão, não do primário.

### 1.5 As seis fontes a obter, em ordem de prioridade

| # | Referência | Por que |
|---|---|---|
| 1 | **Stewart, M. (1992).** *Modelling human error rates for human reliability analysis of a structural design task.* Reliability Engineering & System Safety **36**(2), 171–180. DOI [10.1016/0951-8320(92)90097-5](https://doi.org/10.1016/0951-8320(92)90097-5) | É a fonte do 0,0163. Dados de **engenheiros profissionais** em tarefas cognitivas de cálculo, consulta a tabela e ordenação. Examina efeito de **tempo de resposta** e de experiência, e reporta **variação entre indivíduos** — que é exatamente a heterogeneidade que um modelo baseado em agentes precisa. |
| 2 | **Stewart, M. G.; Melchers, R. E. (1988).** *Simulation of human error in a design loading task.* Structural Safety **5**(4), 285–297. DOI [10.1016/0167-4730(88)90029-X](https://doi.org/10.1016/0167-4730(88)90029-X) | O modelo de macrotarefa e a comparação com **dados de levantamento da mesma tarefa**. É o precedente da composição. |
| 3 | **Stewart, M. G.; Melchers, R. E. (1989).** *Error control in member design.* Structural Safety **6**(1), 11–24 | Dimensionamento de membro — o nível de macrotarefa que a autora identificou. |
| 4 | **Stewart, M. G.; Melchers, R. E. (1989).** *Human error in structural design tasks.* Journal of Structural Engineering **115**(7), 1795 | Artigo-síntese na ASCE. |
| 5 | **Stewart, M. (1992).** *Simulation of human error in reinforced concrete design.* Research in Engineering Design **4**(1), 51–60 | Projeto de viga de concreto — outro caso de macrotarefa. |
| 6 | **Stewart, M. (1992).** *A human reliability analysis of reinforced concrete beam construction.* Civil Engineering Systems **9**(3), 227–250 | HRA completa de uma macrotarefa. |

Todas **NÃO VERIFICADAS** exceto os resumos de (1) e (2), que eu li na origem.

### 1.6 Bônus: isso também ataca o G-01 e o G-03

- O item (1) examina **efeito do tempo de resposta sobre a taxa de erro em engenheiros
  profissionais**. Não é seleção de estratégia, mas é o compromisso esforço–acurácia na
  população certa — muito mais próximo do modelo que o estudo de leitura.
- Os modelos de macrotarefa de Stewart simulam **processo de projeto com retrabalho**,
  o que os torna candidatos a comparador para o G-01 **em esforço, dentro de engenharia**.

---

## 2. G-01 — Sim, a pasta paralela é a abordagem certa

A ideia da autora está correta e é boa prática, não gambiarra. Justificativa:

1. **Isola o risco.** Se a análise não fechar, nada no simulador foi tocado.
2. **Não polui o controle de identidade bit a bit.** Qualquer alteração em `src/modelo/`
   obriga a rerrodar a suíte inteira; uma pasta separada não.
3. **Vira artefato citável por si.** Uma busca documentada que não encontra a fonte
   **é** a evidência de insuficiência — e isso é material de capítulo, não desperdício.

### Estrutura sugerida

```
research/ancoragem_retrabalho/
├── README.md              # pergunta, critério de aceitação, log de busca
├── fontes.csv             # uma linha por fonte: numerador, denominador,
│                          # unidade, fronteira, domínio, veredito, link
├── conversao.py           # se houver conversão custo→esforço, aqui e só aqui
├── comparar.py            # lê outputs/.../nominal_corrigido.csv e confronta
└── resultado.md           # veredito com IC, ou declaração de insuficiência
```

**Regra de ouro:** `comparar.py` **lê** os CSV do lote publicado e não escreve nada em
`src/` nem em `outputs/`. A integração posterior, se houver, é uma linha no texto e uma
entrada em `04_FONTES.md` — não código no simulador.

**Critério de aceitação**, escrito antes de buscar: uma fonte só fecha o G-01 se declarar
numerador, denominador, unidade, unidade amostral independente, fronteira do sistema e
domínio. Se faltar qualquer um, é ilustração, não ancoragem.

Mesma estrutura serve para `research/ancoragem_selecao_p1/` (G-03).

---

## 3. G-03 — Fora da engenharia, e achei fonte melhor que a atual

A autora está certa: são fatores humanos, e a literatura certa não é de engenharia.

### 3.1 A fonte

**Payne, J. W.; Bettman, J. R.; Luce, M. F. (1996).** *When time is money: Decision
behavior under opportunity-cost time pressure.* Organizational Behavior and Human
Decision Processes **66**(2), 131–152.
[PDF acessível](https://people.duke.edu/~jrb12/bio/Jim/46.pdf) · **TEXTO LIDO (resumo e resultados)**

**Por que é melhor que o estudo de leitura que descartamos:** ali o prazo era uma parede
imposta (30/60/90 s), e o sujeito não escolhia nada — por isso a direção causal se
invertia. Aqui a pressão é **custo de oportunidade**: um relógio de 30 s corre e o
pagamento é multiplicado pela proporção de tempo restante. **O sujeito escolhe quanto
tempo gastar, trocando pagamento por acurácia.** Isso é a estrutura do modelo: o agente
escolhe o atalho e o tempo é consequência.

### 3.2 Os números

| Medida | Sem pressão | Sob pressão severa | Teste |
|---|---:|---:|---|
| Aquisições de informação | 24,6 | 15,4 | F(1,70) = 20,4; p < 0,0001 |
| Tempo por aquisição (s) | 0,52 | 0,42 | F(1,70) = 15,9; p < 0,0003 |
| Índice de padrão (→ processamento por atributo) | −0,14 | −0,23 | F(1,70) = 0,67, **n.s.** |
| Variância entre alternativas | 0,018 | 0,023 | F(1,70) = 3,03; p < 0,09 |

**Leitura honesta:** a **aceleração** é forte e significativa (−37% de aquisições). O
**deslocamento de estratégia** aponta na direção esperada mas **não é significativo**.
Então esta fonte sustenta que a pressão reduz o processamento; **não** sustenta uma
proporção de seleção heurística que se possa comparar aos 67,4% / 57,9% do modelo.

**G-03 continua aberto para o valor.** Mas ganhou suporte de construto muito melhor
ancorado, na população e na estrutura causal certas.

### 3.3 A tensão que essa fonte revela — e que vale um parágrafo da discussão

O resultado central do artigo é: sob pressão de custo de oportunidade, as escolhas por
estratégia **lexicográfica (heurística)** correlacionam positivamente com o pagamento
(r = 0,23; p < 0,0001), enquanto as maximizadoras de valor esperado não (r = −0,02, n.s.).
**Sem** pressão o padrão se inverte.

Isto é: na literatura de decisão, recorrer à heurística sob pressão é **adaptativo**, não
falha. O modelo, ao pôr `ρ_omissão > 0`, codifica o oposto — a Porta 1 é mais rápida **e**
pior.

As duas coisas podem ser verdadeiras, porque medem coisas diferentes: o modelo mede
**qualidade do produto**; Payne et al. medem **pagamento ajustado pelo custo do tempo**.
Mas a tensão precisa aparecer no texto, porque é o tipo de coisa que uma banca de fatores
humanos vai levantar. E conecta com D-04, onde já se concluiu que a Porta 1 não instancia
o arquétipo de Soluções Sintomáticas.

### 3.4 Sobre a ideia do banco de dados separado

Faz sentido, com uma ressalva. Montar `research/ancoragem_selecao_p1/fontes.csv` como
base estruturada — uma linha por estudo, com população, manipulação de pressão (imposta
ou por custo), medida reportada, e se traz proporção de estratégia — é útil e barato.

O que **não** vale a pena: tentar meta-análise própria. Com o prazo de 29/11, uma
meta-análise mal-feita é pior que nenhuma. A base serve para **decidir se a fonte
existe**, não para produzir um número novo.

---

## 4. O que é, exatamente, o problema da calibração

A pergunta foi direta, então a resposta é direta. Calibrar significa: *achar quais valores
dos parâmetros desconhecidos fazem o modelo reproduzir o mundo real.* Para isso são
necessárias três coisas, e o trabalho falha nas três.

### 4.1 Primeiro: não há alvo (`z`)

Calibração compara um número do mundo com o número correspondente do modelo. O trabalho
não tem nenhum número do mundo que sirva:

| Saída do modelo | Por que não serve como alvo |
|---|---|
| `E_total` | soma no denominador coisas em unidades diferentes; o sinal depende da convenção de contagem |
| `atraso_relativo` | a linha de base é o CPM sem recursos, que nenhum projeto real usa |
| `taxa_omissao` | é 97,5% reenunciado da premissa `p_reporte`; calibrar contra ela é calibrar a própria premissa |
| `divida_latente` | é por definição **latente** — ninguém observa o estoque oculto de um projeto real |
| `retrabalho_sobre_plano` | existe comparador em esforço, mas de outro domínio (G-01) |

**Sem alvo não há calibração.** Não é dificuldade técnica; é ausência de um dos lados
da comparação.

### 4.2 Segundo: o instrumento está desregulado

O método é History Matching: calcula-se a implausibilidade

```
I(x) = max_j |z_j − f̄_j(x)| / √(V_obs + V_sim + V_mod)
```

e descarta-se tudo com `I > 3`, sobrando a região NROY.

No teste sintético — em que o vetor verdadeiro é **conhecido**, porque nós o escolhemos —
a implausibilidade do **próprio vetor verdadeiro** tende a **3,594**. Acima do corte de 3.
Ou seja: **o método rejeitaria a resposta certa.** E `V_obs` responde por 74% a 86% do
denominador, o que significa que a incerteza da observação domina tudo o mais.

Um instrumento que reprova o gabarito não pode ser usado para corrigir prova.

### 4.3 Terceiro: dois parâmetros não são separáveis

Os observáveis agregados só enxergam o **produto** `F_ancora × f_retrabalho`. Correlação
de `taxa_omissao` com `F_ancora`: r = 0,950. Com `f_retrabalho`: r = 0,022.

Isso é **não identificabilidade estrutural** (Raue et al., 2009): nenhuma quantidade de
dados separa os dois, porque eles não aparecem separados na saída. A única saída é
ancoragem externa de um deles — que é justamente o que o Stewart agora permite fazer
com `F_ancora`.

### 4.4 Por que isso não é fracasso

Três obstruções independentes, cada uma suficiente sozinha para impedir a calibração.
Nenhuma se resolve com mais tempo de computador.

O que o trabalho pode entregar, e é contribuição real: **o mapa preciso da obstrução.**
Uma monografia que diz *"calibramos"* sem alvo é indefensável. Uma que diz *"não é
calibrável hoje, e estas são as três razões, cada uma com o critério que uma fonte teria
de satisfazer"* é honesta, defensável e útil para quem vier depois.

A adequação do modelo, então, é argumentada por **reprodução simultânea de múltiplos
padrões qualitativos** (Grimm et al., 2005 — já catalogado), não por ajuste numérico.

---

## 5. Recomendação

1. **Obter Stewart (1992) RESS e Stewart & Melchers (1988) Structural Safety.** É a
   prioridade máxima. Se o 0,0163 se confirmar no primário, `F_ancora` deixa de ser
   arbitrário e o trabalho ganha seu primeiro parâmetro ancorado.
2. Criar `research/ancoragem_retrabalho/` e `research/ancoragem_selecao_p1/` como pastas
   independentes, com critério de aceitação escrito **antes** da busca.
3. Registrar Payne, Bettman & Luce (1996) em `04_FONTES.md` como suporte de construto
   para a seleção de porta — com a linha explícita do que **não** sustenta: não fornece
   proporção de seleção heurística comparável aos 67,4% / 57,9% do modelo.
4. Escrever o parágrafo de tensão da §3.3 na discussão. É um ponto forte, não uma
   fragilidade.
