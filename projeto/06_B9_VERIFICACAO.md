# B9 — verificação metodológica antes de usar qualquer número no texto

> **Atribuição revista no MVP:** A = τ_inicial move o portão de ajuda **e**
> a entrada do multiplicador de rede. O fatorial 2⁵ separa G (portão), N (rede),
> B (limiar), C (reporte) e D (detecção). N não é o multiplicador cognitivo
> direto: este recebe fadiga e pressão. Há efeitos indiretos entre canais.
> Percentuais abaixo descrevem o legado; não são participação da assistência.
> As tabelas ANTES/DEPOIS ficam em `outputs/diagnosticos/mvp_20260915/`.

Scripts: `src/modelo/09_sensibilidade_tau_min.py`, `src/modelo/10_decomposicao_fatorial.py`
Tabelas: `modelo_09_sensibilidade_tau_min.csv`, `modelo_10_fatorial_celulas.csv`,
`modelo_10_fatorial_decomposicao.csv`
Execuções acrescentadas: 2.112 (sensibilidade) + 3.072 (fatorial) = 5.184.
Registro histórico da análise anterior ao MVP; o mecanismo legado foi preservado no Git.

---

## 1. Auditoria dos percentuais — o que a B9 mediu, e o que não mediu

### 1.1 Fórmula que produziu os percentuais da B9

    fração(b, m) = 100 · média_i[ y_i(b) − y_i(centralizada) ]
                       / média_i[ y_i(adaptativa) − y_i(centralizada) ]

`i` indexa as 16 instâncias; `y_i` é a média das 12 sementes daquela instância;
`b` é o braço com **um** parâmetro trocado pelo valor adaptativo.

**O que isso é:** a fração do contraste nominal que uma substituição isolada
reproduz. **O que isso não é:** uma decomposição de contribuição. As parcelas
não são ortogonais e não somam o todo.

### 1.2 Prova de que não é aditivo

Fatorial completo 2⁴ dos quatro parâmetros (16 células, 0000 = centralizada,
1111 = adaptativa), com modelo **saturado** ajustado por instância:

    y = b0 + Σ b_k x_k + Σ b_kl x_k x_l + … + b_ABCD x_A x_B x_C x_D

16 termos para 16 células ⇒ ajuste exato, sem escolha de modelo e sem resíduo.
Vale a identidade `y(1111) − y(0000) = Σ termos − b0`, verificada com erro
máximo de **7,1e-15** em todas as métricas. **Essa sim é uma decomposição
aditiva.** A = τ_inicial, B = τ_mín, C = p_reporte, D = p_detecção.

| métrica | efeitos principais | interações | maior interação |
|---|---|---|---|
| TL | 99,0% | +1,0% | ACD +1,1% |
| TW | 97,2% | +2,8% | AD +1,6% |
| TU | 102,6% | −2,6% | AC −2,4% |
| E_total | 104,5% | −4,5% | AD −2,6% |
| TR | 105,5% | −5,5% | ACD +9,4% |
| retrabalho/plano | 107,2% | −7,2% | ACD +10,1% |
| n_com_erro · taxa_omissão | 112,3% | −12,3% | AC −11,7% |
| atraso_relativo | 118,9% | −18,9% | **CD −26,2%** |
| dívida latente · S_UR_máx | 161,8% | **−61,8%** | **CD −45,5%** |

Para a família da dívida oculta, **as interações carregam mais de 60% do
contraste**. Qualquer frase da forma "p_reporte explica 82% da redução da
dívida" está errada por construção. A interação dominante é `CD`
(p_reporte × p_detecção), **antagônica**: os dois parâmetros fazem em grande
parte o mesmo trabalho — converter dívida oculta em retrabalho visível — e
juntos entregam muito menos que a soma dos isolados.

### 1.3 Linguagem corrigida após separação dos canais

| não escrever | escrever |
|---|---|
| "τ_inicial explica 99% da redução de ociosidade" | "a ablação mede o contraste sob a intervenção na Porta 2; τ_inicial também atua na rede. Relatar TU e TL separadamente e usar a decomposição G/N para atribuição" |
| "p_reporte explica 82% da dívida" | "no fatorial 2⁴, o efeito principal de p_reporte vale −0,0444 sobre um contraste de −0,0540; as interações valem +0,0334, das quais −45,5% do contraste vêm da interação com p_detecção" |
| "X% do efeito vem de Y" | "substituir isoladamente Y reproduz Z% do contraste nominal (não é decomposição: ver interações)" |

### 1.4 Achado: τ_mín é **inerte** em todo o fatorial

Testadas as 8 comparações que trocam só B, as células são **idênticas linha a
linha** nas 192 execuções de cada uma. Todo termo do modelo saturado que contém
B é exatamente zero e o fatorial 2⁴ colapsa num 2³ replicado.

Não é propriedade do parâmetro. É consequência de τ ser constante e igual para
todos os agentes: o portão `confiança > τ_mín` compara sempre τ_inicial com
τ_mín, e os dois níveis testados de τ_mín (0,60 e 0,25) caem do mesmo lado dos
dois níveis testados de τ_inicial (0,25 e 0,80).

---

## 2. Sensibilidade local de τ_mín (item 2 do pedido)

Cenário centralizado, tudo o mais constante. 16 instâncias × 12 sementes por
ponto; 11 pontos; 2.112 execuções. `τ_inicial = 0,25` é 2⁻², exatamente
representável em binário — o empate é igualdade exata, não arredondamento.

| τ_mín | ajudas | bloqueios | atraso_rel | TU | TL | TR | E_total |
|---|---|---|---|---|---|---|---|
| 0,2000 | 9,97 | 6,45 | 2,8600 | 6,45 | 9,97 | 59,64 | 0,8980 |
| 0,2250 | 9,97 | 6,45 | 2,8600 | 6,45 | 9,97 | 59,64 | 0,8980 |
| 0,2400 | 9,97 | 6,45 | 2,8600 | 6,45 | 9,97 | 59,64 | 0,8980 |
| 0,2490 | 9,97 | 6,45 | 2,8600 | 6,45 | 9,97 | 59,64 | 0,8980 |
| 0,2499 | 9,97 | 6,45 | 2,8600 | 6,45 | 9,97 | 59,64 | 0,8980 |
| **0,2500** | **0,00** | **126,27** | **3,1345** | **126,27** | **0,00** | **68,87** | **0,7839** |
| 0,2501 | 0,00 | 126,27 | 3,1345 | 126,27 | 0,00 | 68,87 | 0,7839 |
| 0,2510 | 0,00 | 126,27 | 3,1345 | 126,27 | 0,00 | 68,87 | 0,7839 |
| 0,2600 | 0,00 | 126,27 | 3,1345 | 126,27 | 0,00 | 68,87 | 0,7839 |
| 0,2750 | 0,00 | 126,27 | 3,1345 | 126,27 | 0,00 | 68,87 | 0,7839 |
| 0,3000 | 0,00 | 126,27 | 3,1345 | 126,27 | 0,00 | 68,87 | 0,7839 |

**Diagnóstico: (b), descontinuidade — não (a), mudança gradual.**

- 11 pontos, **2 regimes**. Dentro de cada regime os sete indicadores são
  idênticos até a sexta casa. Não existe faixa intermediária.
- Salto único, no intervalo (0,2499; 0,2500], de largura **1e-4**, contendo
  exatamente τ_inicial.
- A variação de 0,20 a 0,249 — 490 vezes maior — não produz efeito nenhum.

**Por que não pode ser gradual.** O script verifica: o número de valores
distintos de confiança dentro da equipe é **1**, em todas as execuções. Todos os
agentes nascem com confiança = τ_inicial e ela não evolui (τ constante, item
C3). O portão é portanto a mesma comparação para todos: uma função degrau
global de τ_mín. Com esta parametrização o modelo **não tem como** produzir
resposta gradual a τ_mín. A descontinuidade não é uma escolha ruim de valor —
é a única forma que τ_mín pode assumir enquanto τ for constante.

**Validação cruzada entre dois instrumentos independentes.** O regime 1
(τ_mín < 0,25) reproduz exatamente o braço `centralizada__assistencia_universal`
da B9: 9,97 ajudas, 6,45 TU, 2,8600 de atraso, 0,8980 de E_total. A varredura
de parâmetro e a ablação de mecanismo, construídas separadamente, chegam ao
mesmo ponto.

---

## 3. Origem documental da regra `confiança > τ_mín` (item 3 do pedido)

**Onde a regra aparece:** em um único lugar do repositório inteiro —
`src/modelo/simulador.py:478`. `grep -rn tau_min` em todo o repositório confirma.

| documento | o que diz sobre o portão |
|---|---|
| `docs/especificacao_modelo.md` §6 "Portas de decisão" | declara que "duas precisões são necessárias para tornar o pseudocódigo executável" e detalha **apenas** a transição estocástica da Porta 1 e a ordem de avaliação. **A Porta 2 não é especificada.** |
| `docs/especificacao_modelo.md` linha 298 | apenas `τ_mín, limiar para conceder ajuda` — verbal, **sem operador** |
| `docs/registro_de_decisoes.md` | **nenhuma entrada** sobre τ_mín ou Porta 2 |
| `config/parametros.yaml` | `condicao: premissa` para os quatro; `fonte` é a frase qualitativa "limiar alto/baixo para conceder ajuda". Nenhuma justificativa para 0,25 nem para 0,60 |
| Crowder et al. (2012), fonte citada do mecanismo | **não tem portão de confiança nenhum.** O agente difunde o pedido porque sua competência é menor que a dificuldade; os outros respondem ou declinam por **disponibilidade**. τ ali é variável de **saída**, em [0; 5], que evolui a partir dos eventos de comunicação (eq. 4 do artigo) — não é pré-condição em [0; 1] |

### 3.1 RESOLVIDO — a monografia do TCC1

A monografia foi consultada. **A desigualdade estrita é do TCC1.** Seção 4.4.3,
"Regra de Transição Lógica", Porta 2 — Hiato de competência: requisição pull,
linha 4 do pseudocódigo:

```
1   se ∆D > 0 então
2         Muda estado para Espera_por_Suporte;
3         Transmite Request(∆D) à rede;
4         se ∃ agente k com a_k > 0 e τ_k > τ_min então      <-- ESTRITA, no TCC1
5               ∆C ← [15 + 3(C_k − C)]/100;
6               Atualiza C;
7               Adiciona TL_i ao relógio global;
8               Drena a_k;
9         senão
10              Adiciona TU_i ao relógio global;
11        fim
12  fim
```

E na lista de símbolos (p. 15): `τ_min — Limiar mínimo de confiança para
transferência de conhecimento`.

**Classificação, das três hipóteses levantadas:** não é artefato de
implementação. O código reproduz fielmente a formulação conceitual. O que resta
é **escolha arbitrária de parametrização** — `τ_inicial = 0,25` e
`τ_min = 0,25` são `condicao: premissa` sem justificativa registrada, e
coincidem exatamente sobre o único ponto em que o resultado depende de `>`
contra `≥`. Nenhum outro valor de τ_min em [0; 1] tem essa propriedade.

### 3.2 Divergências entre o TCC1 e o código, encontradas na conferência

| item | TCC1 §4.4.3 | código `simulador.py:474-478` | situação |
|---|---|---|---|
| confiança do apoiador | `τ_k > τ_min` | `k.confianca > tau_min` | **fiel** |
| disponibilidade | `a_k > 0`, atributo contínuo do vetor de estado, drenado na linha 8 | `k.tarefa_atual is None`, booleano; drena um período | operacionalização; declarar como `[DEC]` |
| competência do apoiador | **nenhuma condição** | `k.competencia > a.competencia` | **restrição acrescentada, não declarada** |
| Porta 2 só fora da saturação | portas independentes na árvore | `if not heuristico and dD > 0` | já declarado como `[DEC]` (ordem de avaliação) |

O terceiro item é achado novo e precisa entrar no registro. O TCC1 permite que
**qualquer** colega disponível e confiável conceda ajuda: a equação (4.2)
continua positiva mesmo com `C_k < C`, porque `3(C_k − C) ≥ −3 > −15`. O código
exige que o apoiador seja mais competente, o que torna a ajuda **mais rara** do
que a formulação prevê.

Quanto isso pesa, pelos contadores já medidos (média por execução): no braço
adaptativo há 16,43 eventos de hiato, 10,49 recebem ajuda e **5,94 são
bloqueados por não haver colega livre mais competente** — exatamente os casos
que a regra do TCC1 poderia ter atendido. No braço centralizado o filtro é
irrelevante, porque τ já bloqueia tudo. **Ressalva:** o contador atual conflaciona
"não havia colega livre" com "havia, mas não era mais competente"; separar as
duas exige um contador a mais. Não medi ainda.

## 4. Reorganização dos resultados (item 4 do pedido)

**Nota sobre E_total.** Não é eficiência. Pela equação (5) do TCC1,
`E_total = ΣTW / Σ(TW+TL+TU+TR)`, é a fração do esforço realizado que foi
trabalho produtivo — uma medida de **ocupação**. Tratada como tal daqui em
diante.

### A. Robustos às ablações do mecanismo de assistência

Sobrevivem a ≥85% do contraste sob as duas ablações independentes.

| resultado | nominal | sem assistência | assist. universal |
|---|---|---|---|
| redução da dívida latente máxima (S_UR_máx) | −18,29 (−72,8%) | −17,11 (93,5%) | −15,53 (84,9%) |
| redução da dívida latente sobre o plano | −0,0540 | −0,0505 (93,6%) | −0,0458 (84,8%) |

**Ressalva obrigatória:** robusto ao mecanismo **não** quer dizer atribuível a um
parâmetro. Aqui as interações carregam −61,8% do contraste. A afirmação
defensável é: *o arranjo adaptativo reduz a dívida técnica oculta, e essa
redução persiste quando o mecanismo de assistência é neutralizado nos dois
braços; ela decorre conjuntamente de p_reporte e p_detecção, que interagem de
forma antagônica e não admitem atribuição separada.*

### B. Condicionados ao mecanismo de assistência

| resultado | nominal | sem assistência | veredito |
|---|---|---|---|
| TL (tempo de ajuda) | +10,49 | 0,00 | desaparece — por construção |
| ociosidade TU | −120,32 | +18,93 | **inverte** |
| ocupação E_total | +0,1046 | −0,0477 | **inverte** |
| retrabalho pago TR | −16,36 | −4,26 | resta 26% |
| retrabalho sobre plano | −0,0486 | −0,0130 | resta 27% |
| tempo de trabalho TW | −149,60 | −123,81 | resta 83% |
| atraso relativo | −1,1354 | −0,8240 | resta 73% |

Em todos, o efeito principal dominante no fatorial é A (τ_inicial): 91% a 99,8%.
E τ_inicial só age através do portão que a seção 2 mostrou ser um degrau de
largura 1e-4. **Estes resultados são condicionados a τ constante e à
parametrização atual, e devem ser enunciados assim.**

Além disso, `atraso_relativo` ainda tem pendente o item C2: medido até a última
tarefa concluída, e não até a dívida zerar, o valor cai de −36,2% para −22,2%.

### C. Verificações de manipulação, não achados

`taxa_omissão` e `n_com_erro` — **a mesma grandeza dividida por 60** (item B11).
Efeito principal de C (p_reporte) = 100,6% do contraste; razão mecânica prevista
`(1−0,75)/(1−0,15) = 0,2941` contra 0,2892 observada trocando só p_reporte.
Manter **uma** das duas, rotulada como verificação de que a manipulação
experimental funcionou.

---

## 5. Sobre o empate numérico — o que **não** dá para escrever ainda

A frase "metade dos resultados é sustentada por um empate acidental" foi
**retirada**. Ela pressupõe a resposta da seção 3, que ainda está em aberto.

O que os dados sustentam hoje, e só isso:

1. τ_mín é inerte em todo o fatorial 2⁴ (verificado, 8 de 8 comparações).
2. A resposta a τ_mín é um degrau de largura 1e-4 localizado exatamente em
   τ_inicial (verificado, grade de 11 pontos, 2 regimes).
3. O degrau é inevitável enquanto τ for constante e igual entre agentes
   (verificado: 1 valor distinto de confiança por equipe).
4. Os quatro valores são `premissa` sem justificativa numérica registrada
   (verificado no YAML).
5. A desigualdade estrita não aparece em nenhum documento, só no código
   (verificado por `grep` no repositório inteiro).
6. Crowder et al., fonte do mecanismo, não tem portão de confiança
   (verificado no PDF do projeto).

**Resolvido em 3.1:** a desigualdade estrita vem do TCC1 §4.4.3. A frase
retirada continua retirada, mas por outro motivo: o problema não é o operador,
é a escolha dos dois valores coincidirem sobre o ponto de fronteira.

**Aberto e novo:** o filtro `k.competencia > a.competencia`, que não existe no
TCC1 (seção 3.2).
