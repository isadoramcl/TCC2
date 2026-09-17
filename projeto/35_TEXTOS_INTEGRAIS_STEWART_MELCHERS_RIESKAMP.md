# Parecer 35 — Os três textos integrais: G-02 fecha, e o modelo precisa mudar

**Data:** 17/09/2026 · **Revisor:** Claude
**Fontes:** três PDFs obtidos pela autora e lidos integralmente por mim
**Estado das três: TEXTO LIDO.** Todos os números abaixo têm página.

---

## 1. Stewart & Melchers (1988) — **a regra de composição está publicada, e é linear**

*Simulation of human error in a design loading task.* Structural Safety **5**(4), 285–297.

**Tabela 1, p. 290 — taxas de erro por microtarefa:**

| Microtarefa | Taxa |
|---|---:|
| PTE — consulta a tabela | 0,0126 |
| PME₁ — cálculo de 1 passo | **0,0128** |
| PME₂ — cálculo de 2 passos | 0,0256 |
| PME₃ — 3 passos | 0,0384 |
| PME₄ — 4 passos | 0,0512 |
| PME₅ — 5 passos | 0,0640 |
| PME₈ — 8 passos | 0,1024 |

**0,0256 = 2 × 0,0128. 0,0384 = 3 × 0,0128. 0,1024 = 8 × 0,0128.** Exato, em todos.

A regra de composição é **linear no número de passos**:

```
p_erro(k passos) = k × 0,0128
```

### O que isso faz com `F_ancora` — o G-02 fecha

| `F_ancora` (varredura atual) | k passos implícitos |
|---:|---:|
| 0,05 | **3,9** |
| 0,10 | 7,8 |
| 0,15 | 11,7 |
| 0,20 | 15,6 |
| 0,25 | **19,5** |

**A faixa que o trabalho já varre corresponde a atividades de 4 a 20 passos elementares de
cálculo**, à taxa de 0,0128 por passo medida em engenheiros civis profissionais.

E o mais importante: **a regra é publicada, não sintetizada.** A autorização do orientador
para sintetizar dados **não é necessária aqui**. Continua guardada.

### Retratação R-10

No parecer 30 eu propus compor por independência, `F_ancora = 1 − (1 − p)^k`. **Está errado
como reconstrução do que a fonte faz.** Stewart & Melchers usam composição **linear**. Para
k = 8 a diferença é pequena (0,0982 contra 0,1024, 4%), mas a regra a citar é a deles, não
a minha.

---

## 2. O achado maior: **omissão domina comissão por uma ordem de grandeza**

Ainda na Tabela 1, p. 290 — as taxas de **omissão**:

| Microtarefa de omissão | Taxa |
|---|---:|
| PRFO — omitir fatores de redução de parede e telhado | **0,8000** |
| POPL — omitir carga concentrada de telhado | 0,4167 |
| PCPIE — colocação da abertura dominante | 0,4000 |
| PG10 — ângulo de telhado maior que 10° | 0,4000 |

Contra **0,0126 a 0,1024** para as microtarefas de comissão. **Trinta a sessenta vezes mais
frequente.**

### E a estrutura da árvore de eventos é a da sua Porta 1

Figura 1, p. 287, e texto da p. 286:

> *"A typical element of an event tree that incorporates an error of omission (i.e. failure
> to perform a task) and an error of commission (i.e. incorrect performance of a task)...
> The element operates by first considering a binary decision section that introduces the
> probability of the occurrence of an error of omission. If such an error does occur, then
> the task is omitted and the algorithm proceeds to the next task. Otherwise, an error of
> commission may occur at this task."*

Primeiro um nó binário de **omissão**; se não omitiu, então **comissão**. É exatamente o
desenho das portas do seu modelo — publicado, em projeto de engenharia, com taxas para os
dois ramos.

### A consequência é dura

**O ramo que o seu modelo tem desligado é o que carrega o modo de erro dominante.**
`p1_fuga = 0,000000` nos dois arranjos (achado A-14). A literatura do domínio diz que a
omissão é 30 a 60× mais frequente que a comissão, e o seu simulador nunca a executa.

E isso **converge com a bancada de fatores humanos**: nos árbitros da NBA, **87,1% dos erros
são omissões**. Dois domínios completamente independentes — projeto estrutural e arbitragem
esportiva — com o mesmo achado. Isso é evidência convergente forte, e é material de
discussão de primeira linha.

---

## 3. Stewart (1992) — o 0,0163 confirmado, e três parâmetros novos

*Modelling human error rates for human reliability analysis of a structural design task.*
Reliability Engineering & System Safety **36**(2), 171–180.

**Tabela 1, p. 173 — confirmação na fonte primária:**

| Nº de erros | Respondentes | Erros | Microtarefas |
|---:|---:|---:|---:|
| 0 | 68 | — | 1 683 |
| 1 | 18 | 18 | 445 |
| 2 | 5 | 10 | 125 |
| 3 | 2 | 6 | 50 |
| 4 | 1 | 4 | 24 |
| **Total** | **94** | **38** | **2 327** |

`p_av = 38 / 2 327 = ` **0,0163**. Confirmado. 260 engenheiros civis contatados, 65
organizações responderam. O instrumento tinha 32 microtarefas; 25 foram retidas após
descartar sete de ordenação e as de quatro e cinco passos, para igualar dificuldade.

### 3.1 A independência entre erros é **REJEITADA** pelos dados

Tabela 2, p. 175 — ajuste dos três modelos:

| Modelo | χ² | g.l. | χ²₀,₀₅ | Veredito |
|---|---:|---:|---:|---|
| Binomial (independência) | **10,174** | 2 | 5,991 | **rejeitado** |
| Beta-binomial | 0,162 | 1 | 3,841 | melhor ajuste |
| Binomial p-dependente | 0,583 | 1 | 3,841 | aceito |

> *"the binomial distribution is significantly different from the data at the α = 0,05 level
> of significance"* (p. 176)

**Isso invalida a composição por independência** — inclusive a minha do parecer 30, e
inclusive qualquer `1 − Π(1 − p)`. A composição linear de Stewart & Melchers permanece
válida porque não assume independência: é uma taxa medida por número de passos.

### 3.2 Variação entre indivíduos — **parâmetro novo, com valor**

Beta-binomial ajustada: μ = 0,0163, σ² = 0,00034, e o **coeficiente de variação
V = σ/μ = 1,13**, que o autor declara poder ser assumido constante para qualquer taxa média.
Parâmetros: α = 0,7546, β = 45,4563.

**O seu modelo não tem heterogeneidade nenhuma na taxa de erro entre agentes.** `F_base` é
por nível de tarefa e `R_error` é global. Este é um parâmetro empírico, do domínio certo,
para uma dimensão que o modelo simplesmente não tem.

### 3.3 Correlação intraindividual — **segundo parâmetro novo**

Binomial p-dependente: `p_x = φ · p_av · x`, com **φ = 0,845**. Quem errou antes tende a
errar de novo.

### 3.4 E a consequência está quantificada

> *"Results of the HRA using BB and p-DB models of error occurrence increased the probability
> of failure by approximately **20–30% and 50%**, respectively, when compared to the values
> reported by Stewart and Melchers and Stewart"* (p. 176)

Ou seja: **assumir independência subestima a probabilidade de falha em 20% a 50%.** O seu
simulador assume independência.

### 3.5 Pressão de tempo: **efeito nulo**

Metade dos respondentes foi instruída a *"complete the tasks in the shortest possible time"*.

> *"An analysis of response times indicated a negligible difference between response times
> for the two sub-samples... dividing the general total sample into the two sub-samples is a
> redundant measure"* (p. 173)
>
> *"It was also found that **response time and experience had a negligible effect upon error
> rates**... It would appear that the variation of response times is only indicative of the
> behaviour of the individual designers, and does not represent a measure of time pressure."*
> (p. 175)

E Stewart & Melchers (1988), p. 289, hipótese (v): *"No microtask completion time constraints
(i.e. no time pressure)."*

**Este é o quinto achado independente sem efeito de pressão sobre erro**, e agora na
população mais próxima possível do modelo — engenheiros civis profissionais em microtarefas
de projeto. Somando: tênis (sinal oposto), NBA (nulo), Go (nulo), Stewart 1992 (negligível),
Stewart & Melchers 1988 (excluído por hipótese).

---

## 4. Rieskamp & Hoffrage (2008) — os 19% → 44% **estão corretos**, e eu errei ao suspeitar

*Inferences under time pressure.* Acta Psychologica **127**(2), 258–276.

Achei a origem dos números, no Estudo 2 (n = 36, p. 266–267):

> *"11 of the 29 participants who were classified as selecting a compensatory strategy under
> low time pressure were classified as switching to a noncompensatory strategy under high
> time pressure. In contrast, only 2 of the 7 participants who were classified as selecting
> a noncompensatory strategy under low time pressure were classified as switching to a
> compensatory strategy under high time pressure; **p = 0,02 according to a McNemar test**."*

Reconstruindo: baixa pressão, **7 de 36 = 19,4%** não compensatórios. Alta pressão:
(7 − 2) + 11 = **16 de 36 = 44,4%**. Os números conferem e o deslocamento é **significativo**.

**Eu havia sinalizado isso como o padrão da retratação R-01 — valor específico atribuído a
fonte não lida. A verificação confirmou em vez de derrubar.** A desconfiança continuava
certa como procedimento; o resultado foi a favor da fonte.

### Três ressalvas que a leitura revelou

1. **O Estudo 1 não achou o efeito.** Com n = 40 e ambas as condições induzidas por custo de
   oportunidade: *"we did not observe that the proportion of participants who selected a
   noncompensatory strategy was larger in the condition with high time pressure... χ²(1) = 0,10,
   p = 0,75"* (p. 264). O efeito do Estudo 2 aparece porque lá a condição de baixa pressão era
   um limite folgado **sem incentivo nenhum para ser rápido**.
2. **O contraste é pressão × ausência de pressão.** O seu modelo varia `P` de 0,30 a 1,00 —
   **nunca tem uma condição sem pressão**. O deslocamento de 19% → 44% pode ser maior do que
   qualquer coisa que a faixa de `P` do modelo consiga gerar.
3. **A unidade continua sendo participante classificado**, não execução. Comparar com os
   67,4% / 57,9% do modelo é descasamento de denominador. Use como **mudança relativa**
   (2,3×, ou +25 p.p.), declarada.

---

## 5. O que isso muda na ordem de serviço 32 — **você estava certa**

Eu disse que o comando para o Codex não mudava. **Estava errado.** Cinco itens novos:

### N1 · Ancorar `F_ancora` pela regra publicada (prioridade alta, barato)

Substituir a faixa a priori por interpretação declarada: `F_ancora = k × 0,0128`, com `k` =
número de passos elementares por atividade, varrido em 4 a 20. Citar Stewart & Melchers
(1988), Tabela 1, p. 290. **Não sintetizar nada** — a regra é publicada.

### N2 · Heterogeneidade de taxa de erro entre agentes (novo mecanismo)

Introduzir variação entre agentes na taxa basal de erro, com distribuição **Beta de
coeficiente de variação 1,13** (Stewart 1992, p. 174). Alternativa preservada, nominal
histórico intacto. É a primeira heterogeneidade empiricamente ancorada do modelo.

### N3 · Sensibilidade à independência entre erros

O modelo assume erros independentes; a fonte **rejeita** independência (χ² = 10,174 > 5,991)
e quantifica que isso subestima a probabilidade de falha em **20–50%**. Rodar uma
alternativa com correlação intraindividual `p_x = φ·p_av·x`, φ = 0,845, e reportar o efeito
sobre os cinco indicadores.

### N4 · A rota de fuga sobe para prioridade máxima — agora com taxas

O item P1.1 da ordem 32 deixa de ser "corrigir defeito estrutural" e passa a ser "implementar
o modo de erro dominante". A literatura do domínio dá taxas de omissão de **0,40 a 0,80**
contra 0,0126–0,1024 de comissão, e a estrutura de árvore de eventos (omissão primeiro,
comissão depois) é a mesma das portas do modelo.

### N5 · O cenário com efeito de P sobre erro nulo vira **obrigatório**

Era desejável (P2.2). Com cinco fontes independentes sem efeito de pressão sobre erro — duas
delas agora em engenheiros profissionais de projeto — o modelo precisa mostrar que suas
conclusões sobrevivem a `R_error · (1 − μ_cog) = 0`. Se sobreviverem, a crítica está
respondida. Se não sobreviverem, isso precisa estar escrito.

**Distinção que o texto tem que fazer:** o modelo tem dois canais da pressão para o erro —
`p_heu = σ((E − τ_sat)/s)`, que é **seleção de estratégia** e está **apoiado** por Rieskamp;
e `R_error · (1 − μ_cog)`, que é **erro direto** e **não tem apoio de campo**. São coisas
diferentes e hoje estão embaralhadas na discussão.

---

## 6. Onde a autorização de síntese ainda serve

Depois destes três textos, ela **não é mais necessária para o G-02**. O que sobra para ela:

- o número de passos `k` por atividade do J60 — mas agora como **varredura declarada de 4 a
  20**, ancorada na regra publicada, e não como invenção livre;
- nada mais, por ora.

É um bom lugar para a permissão ficar: usada no mínimo necessário, com a regra vindo de fora.
