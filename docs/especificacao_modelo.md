# Especificação do modelo de simulação — versão 1.0

> **MVP — atualização de 16/09/2026:** a alternativa está em
> [`simulador_mvp.py`](../src/modelo/simulador_mvp.py), preservando o legado.
> C4 reduz a duração da omissão; C1 põe reparos na fila com agente e recurso;
> C3 oferece duas leis candidatas, sem eleger uma. Robustez entra no MVP;
> calibração e fragilidades vêm depois, juntas. Nenhuma nova onda de HM.
> As premissas e a sequência de controles estão em
> [PLANO_MVP](../research/PLANO_MVP.md); números anteriores abaixo são históricos.

> **Resposta à revisão científica:** a [reanálise e os pilotos](../projeto/10_RESPOSTA_REVISAO_2026-09-15.md)
> refutaram a suficiência do produto F_ancora × f_retrabalho para todas as saídas.
> A interpretação histórica abaixo foi superada; a crista empírica permanece,
> mas não prova identificabilidade estrutural. Confiança afeta portão e rede.
> Consulte a resposta para o alcance dos resultados e a prioridade atual.

> **Nota de atualização — 15/09/2026:** este arquivo contém registros anteriores
> à auditoria atual. Consulte o [estado auditado e as divergências](../projeto/08_AUDITORIA_AUTONOMA_2026-09-15.md)
> antes de reutilizar conclusões. A análise preliminar oficial é o DOCX local
> `docs/entrega1_metodologia_resultados_iniciais.docx`, por indicação da autora.
> Em particular, convergência das ondas e identificabilidade estrutural ainda
> não estão demonstradas; o simulador contabiliza TR sem ocupar agentes, embora
> a especificação histórica descreva retorno do retrabalho à fila.

Documento normativo. **Nenhuma linha do simulador deve ser escrita antes desta
especificação estar revisada**, e nenhum valor numérico deve ser embutido no
código: todos vêm de `config/parametros.yaml`.

Cada item indica sua **origem**:

| marca | significado |
|---|---|
| `[TCC1]` | fixado na fase conceitual (TCC I, seção 4.4) — não se altera sem justificar |
| `[LIT]` | vem de fonte publicada externa |
| `[CALIB]` | estimado empiricamente nesta fase (scripts 01–05 e psplib 01–03) |
| `[DEC]` | decisão metodológica desta fase — arbitrada, com justificativa, sujeita a sensibilidade |
| `[ABERTO]` | ainda não decidido |

---

## 1. Escopo do MVP

`[DEC]` O produto mínimo viável simula **um projeto** (uma instância do PSPLIB
J60), com **uma equipe fixa** de agentes engenheiros e um agente gestor, ao
longo do tempo discreto, até que todas as 60 tarefas estejam concluídas ou o
horizonte máximo seja atingido.

**Dentro do escopo:** os três estoques, as cinco equações do TCC1, as três
portas de decisão, o sistema difuso, a transição estocástica para o modo
heurístico, e a comparação entre os dois cenários de governança.

**Fora do escopo do MVP**, a registrar como trabalho posterior: múltiplos
projetos simultâneos, contratação ou saída de agentes, aprendizado entre
projetos, e calibração de `F_ancora` por dado de campo.

---

## 2. Estoques e fluxos

`[TCC1]` A Figura 4.2 do TCC I nomeia três estoques. O modelo opera sobre eles:

| estoque | símbolo | significado | cresce quando | decresce quando |
|---|---|---|---|---|
| Desgaste cognitivo | `S_DC(t)` | fadiga acumulada da equipe | tarefas são processadas | há recuperação entre períodos |
| Progresso validado | `S_PV(t)` | trabalho concluído sem erro | uma tarefa é `Concluída_Limpa` | nunca decresce |
| Dívida técnica latente | `S_UR(t)` | retrabalho oculto não detectado | uma tarefa é `Concluída_com_Erro` | o erro é detectado e refeito |

`[TCC1]` A tensão entre `S_PV` e `S_UR` é o mecanismo central do trabalho: o
projeto parece próximo do fim porque `S_PV` cresce, enquanto `S_UR` cresce em
silêncio.

`[DEC]` **Detecção de retrabalho.** O TCC I não especifica quando a dívida
oculta se torna visível. Adota-se: a cada período, cada unidade em `S_UR` tem
probabilidade `p_deteccao` de ser detectada; ao ser detectada, a tarefa
correspondente retorna à fila com duração residual `f_retrabalho · duração
original`, e o tempo gasto é contabilizado em `TR_i`. Sem esse mecanismo o
estoque de dívida nunca se realizaria e o modelo não teria laço de retrabalho —
o que contrariaria o próprio arquétipo de Kim (1994) que o trabalho formaliza.

---

## 3. Agentes e variáveis de estado

### 3.1 Agente Gestor `[TCC1]`

| símbolo | variável | natureza |
|---|---|---|
| `P(t)` | pressão de cronograma | dinâmica |
| `Ω` | restrição orçamentária / ameaça | constante no cenário |
| `W` | topologia do fluxo de trabalho | fixa, vem da instância J60 |
| `D_i` | dificuldade técnica de cada nó | fixa `[CALIB]`, vem de `tarefas_j60_com_di.csv` |

`[DEC]` **Evolução de `P(t)`.** O TCC I não a especifica. Adota-se pressão
proporcional ao atraso relativo em relação ao cronograma de referência:

```
P(t) = P_min + (P_max − P_min) · clip( atraso_relativo(t), 0, 1 )
atraso_relativo(t) = ( t − t_esperado(progresso) ) / makespan_CPM
```

onde `t_esperado(progresso)` é o instante em que aquele nível de progresso
ocorreria no cronograma sem restrição de recursos. Justificativa: a pressão é
uma resposta do gestor ao desvio observado, não uma constante exógena — é o que
torna o laço de realimentação possível. Alternativa considerada e descartada:
`P(t)` crescente com o tempo independentemente do progresso, que produziria
pressão mesmo num projeto adiantado.

### 3.2 Agente Engenheiro `[TCC1]`

| símbolo | variável | faixa |
|---|---|---|
| `C(t)` | competência técnica | [0, 1] |
| `B(t)` | bateria cognitiva | [0, `B_max`] |
| `a(t)` | disponibilidade | {0, 1} no MVP |
| `R(t)` | taxa de resposta na rede | [0, 1] |
| `τ(t)` | confiança mútua | [0, 1] |
| `τ_sat` | limiar de saturação da atenção | escalar |

`[DEC]` **Dinâmica de `B(t)`.** Não especificada no TCC I. Adota-se drenagem
proporcional ao esforço exigido, com taxa distinta por modo de processamento,
e recuperação parcial a cada período de descanso:

```
modo analítico :  B ← B − k_analitico  · E(t)
modo heurístico:  B ← B − k_heuristico · E(t)          com k_heuristico > k_analitico
fim de período :  B ← min( B_max , B + r_recuperacao · B_max )
```

`[TCC1]` A taxa heurística é "acelerada" em relação à analítica — daí a
restrição `k_heuristico > k_analitico`, que o código deve verificar ao carregar
os parâmetros.

`[DEC]` `C(t)` evolui apenas pela equação (2) do TCC I, na Porta 2. Não há
aprendizado por execução no MVP; registrado como simplificação.

---

## 4. Equações herdadas do TCC I

`[TCC1]` Reproduzidas sem alteração:

```
(1)  E(t)        = D_i · P(t) / B(t)
(2)  ΔC          = [ 15 + 3 ( C_k − C ) ] / 100
(3)  PR_efetiva  = PR_nominal · μ_cognitivo · μ_rede
(4)  TGE         = PR_efetiva · ( F_base + R_error · ( 1 − μ_cognitivo ) )
(5)  E_total     = Σ TW_i / Σ ( TW_i + TL_i + TU_i + TR_i )
```

`[CALIB]` `F_base` vem da transferência ordinal: `F_base(ℓ) = F_ancora · RR(ℓ)`,
com `RR` = 1,000 / 1,935 / 2,367 / 2,985 e intervalos por bootstrap de projetos.

---

## 5. Sistema de inferência difusa

`[TCC1]` Pertinências triangulares, modelo de Mamdani–Assilian com agregação por
máximo, defuzzificação por centroide.
`[LIT]` Liu, Triantis e Sarangi (2011).

`[ACHADO 8]` **A t-norma especificada pelo TCC I (mínimo, "Max-Min") foi
substituída pelo produto.** O motivo não é conveniência numérica: é um teorema.

> VAN BROEKHOVEN, E.; DE BAETS, B. *Only Smooth Rule Bases Can Generate Monotone
> Mamdani–Assilian Models Under Center-of-Gravity Defuzzification.* **IEEE
> Transactions on Fuzzy Systems**, v. 17, n. 5, p. 1157-1174, out. 2009.
> DOI 10.1109/TFUZZ.2009.2023328.

A Tabela IX do artigo enumera as cinco únicas configurações com monotonicidade
garantida sob defuzzificação por centroide. Para **duas** entradas há uma só
(linha 4): **t-norma produto com base de regras monótona e suave**. A combinação
(2 entradas, t-norma mínimo) não consta — e de fato viola a monotonicidade, com
derivada positiva local medida de 0,258.

A monotonicidade é requisito, não estética: a saída é um multiplicador de
produtividade, que não pode crescer quando a fadiga ou a pressão crescem.

`[DEC]` Adota-se a linha 4 da Tabela IX. A base de regras da seção 5.1 **já era**
monótona e suave (verificado por código, Definições 2.1 e 2.2). Foi preciso ainda
tornar os termos de saída uma **partição difusa** — premissa da Seção II do
artigo, que os conjuntos originais não satisfaziam. Resultado: derivada positiva
de 2,7 × 10⁻¹⁴, isto é, monotonicidade exata a menos de erro de ponto flutuante.

`[DEC]` `fuzzy.t_norma` é parâmetro declarado com varredura `[produto, minimo]`.
A configuração do TCC I é executada e medida, não descartada. As conclusões do
experimento de governança **não mudam** entre as duas — ver seção 16.7 do
registro de decisões.

`[DEC]` O TCC I não define entradas, termos nem regras. Adota-se um sistema com
**duas entradas por saída**, para que haja de fato "combinações de variáveis"
como o TCC I exige:

### 5.1 `μ_cognitivo` — degradação individual

Entradas: `fadiga = 1 − B(t)/B_max` e `pressao = P(t)` normalizada em [0,1].
Termos: `baixa`, `media`, `alta`, triangulares, vértices em 0 / 0,5 / 1 com
sobreposição nos pontos médios.

Base de regras (9), sendo o consequente o nível de `μ_cognitivo`
(1 = sem degradação):

| fadiga \ pressão | baixa | media | alta |
|---|---|---|---|
| **baixa** | alto | alto | medio |
| **media** | alto | medio | baixo |
| **alta** | medio | baixo | baixo |

### 5.2 `μ_rede` — atrito da rede

Entradas: `desconfianca = 1 − τ(t)` e `carga = fração de agentes ocupados`.
Mesma estrutura de termos e mesma matriz de regras.

`[DEC]` Defuzzificação por centroide. Justificativa: é o método mais usado e
produz saída contínua, requisito explícito do TCC I ("de forma contínua e não
linear").

---

## 6. Portas de decisão

`[TCC1]` As três portas estão especificadas no TCC I. Duas precisões são
necessárias para tornar o pseudocódigo executável:

`[TCC1]` **A transição para o modo heurístico é estocástica.** O texto do TCC I
afirma que o agente "transita de forma estocástica" quando a exigência supera a
capacidade. O pseudocódigo, porém, escreve `se E(t) > τ_sat`, que é
determinístico. Prevalece o texto:

```
p_heuristico = σ( ( E(t) − τ_sat ) / s )       σ = função logística
transita para heurístico com probabilidade p_heuristico
```

`[DEC]` A escala `s` controla a suavidade da transição. Com `s → 0` recupera-se
o limiar determinístico do pseudocódigo, o que permite testar as duas leituras
por sensibilidade em vez de escolher uma por decreto.

`[DEC]` **Ordem de avaliação.** Porta 1 (sobrecarga) antes de Porta 2 (hiato de
competência): um agente saturado não busca ajuda, recorre ao atalho. Segue a
ordem em que o TCC I as numera.

### 6.1 LACUNA IDENTIFICADA — o ramo de reporte de erro

`[ACHADO]` A matriz de cenários do TCC I (Tabela 5.1) distingue os arranjos de
governança pela **resposta a erros**: *"ocultação / adiamento"* no cenário
centralizado contra *"reporte imediato"* no adaptativo. A Porta 1, porém, prevê
apenas dois desfechos sob sobrecarga:

- **fuga** (`Ω > Limite_Aversao_Perda`) → tarefa adiada, tempo em `TU_i`;
- **omissão** → tarefa concluída com erro, parcela injetada em `S_UR`.

**Não existe ramo de reporte.** Sem ele, o cenário adaptativo não dispõe de
mecanismo para se comportar diferentemente do centralizado no ponto que a
matriz declara ser a distinção principal, e o experimento central compararia
dois arranjos operacionalmente idênticos.

`[DEC]` Acrescenta-se um terceiro desfecho ao ramo de omissão. Ao cometer a
falha, o agente reporta com probabilidade `p_reporte`:

```
se ocorre omissão:
    com probabilidade p_reporte  → erro REPORTADO
        a tarefa é refeita imediatamente; tempo vai para TR_i;
        nada entra em S_UR
    caso contrário               → erro OCULTO
        tarefa marcada Concluída_com_Erro;
        injeta ( E(t) − τ_sat ) · f_corrup em S_UR
```

Justificativa: é a tradução mínima e direta da linha "resposta a erros" da
matriz de cenários, e preserva a estrutura da Porta 1 em vez de reescrevê-la. O
erro reportado tem custo de tempo imediato; o oculto tem custo diferido e maior,
que é exatamente o arquétipo de "Soluções Sintomáticas" de Kim (1994) que o
trabalho formaliza.

`[DEC]` `p_reporte` é o parâmetro que mais diretamente encarna a segurança
psicológica, e é o principal contraste entre os dois cenários.

---

## 7. Dinâmica temporal

| aspecto | decisão | origem |
|---|---|---|
| passo de tempo | 1 período, mesma unidade das durações do J60 | `[DEC]` |
| horizonte máximo | derivado em `config/parametros_derivados.yaml` (hoje 9 × o makespan do CPM) | `[CALIB]`, do escalonamento de referência |
| tamanho da equipe | parâmetro `n_agentes` | `[DEC]` |
| atribuição de tarefa | tarefa elegível de maior `D_i` ao agente de maior `C(t)` disponível | `[DEC]` |
| restrição de recursos | respeitada: a soma das demandas das tarefas ativas não excede `a_k` | `[TCC1]` via J60 |
| elegibilidade | todos os predecessores concluídos | `[TCC1]` via `W` |

`[DEC]` A política de atribuição "tarefa mais difícil ao agente mais competente"
é uma heurística gulosa, declarada como tal. Alternativas a testar por
sensibilidade: atribuição aleatória, e ordem por folga crescente. A política
**não** é objeto de estudo do trabalho; é uma escolha que precisa existir para o
modelo rodar, e por isso precisa ser explícita e variada nos testes.

---

## 8. Cenários de experimentação

`[TCC1]` Matriz da Tabela 5.1 do TCC I:

| dimensão | governança centralizada | governança adaptativa |
|---|---|---|
| tomada de decisão | hierárquica e sequencial | distribuída e lateral |
| confiança mútua `τ` | baixa | alta |
| segurança psicológica | restrita | elevada |
| transferência de conhecimento | formal e vertical | informal e horizontal |
| resposta a erros | ocultação / adiamento | reporte imediato |
| pressão `P(t)` | alta, **igual nos dois** | alta, **igual nos dois** |
| dificuldade `D_i` | definida pelo grafo | definida pelo grafo |

`[DEC]` Tradução das dimensões qualitativas em parâmetros:

| dimensão | parâmetro afetado |
|---|---|
| confiança mútua | `tau_inicial` |
| segurança psicológica | `p_deteccao` — ambiente seguro detecta erro mais cedo |
| transferência de conhecimento | `tau_min`, limiar para conceder ajuda |
| resposta a erros | **`p_reporte`** — probabilidade de reportar em vez de ocultar (ver 6.1) |
| — | `f_corrup`, parcela injetada em `S_UR` quando o erro é ocultado |

`[DEC]` **`P(t)` e `D_i` permanecem idênticos entre cenários.** É o controle
experimental exigido pelo TCC I: só variam os parâmetros organizacionais.

---

## 9. Saídas

| saída | descrição |
|---|---|
| `E_total` | equação (5) |
| `S_UR(T)` | dívida técnica ao fim |
| `S_UR` máximo | pico de dívida oculta durante a execução |
| makespan realizado | contra o makespan do CPM |
| `TW/TL/TU/TR` | decomposição do tempo, por tarefa e agregada |
| trajetórias | `B(t)`, `P(t)`, `S_PV(t)`, `S_UR(t)`, `μ_cognitivo(t)` |
| taxa de omissão | fração de tarefas `Concluída_com_Erro` |

---

## 10. Verificações obrigatórias do simulador

1. Conservação: toda tarefa termina em exatamente um estado terminal.
2. Precedência: nenhuma tarefa inicia antes de todos os predecessores concluírem.
3. Recursos: em nenhum período a demanda ativa excede a disponibilidade.
4. Tempo: `Σ(TW+TL+TU+TR)` iguala o tempo total de agente alocado.
5. Faixas: `B(t) ∈ [0, B_max]`, `μ ∈ [0,1]`, `C(t) ∈ [0,1]`, `E_total ∈ [0,1]`.
6. Determinismo: mesma semente reproduz o mesmo resultado, bit a bit.
7. Caso degenerado: com `P(t)` mínima, `B_max` alto e `F_base` nulo, nenhuma
   tarefa deve ser concluída com erro e `E_total` deve tender a 1.
8. Monotonicidade esperada: aumentar `P(t)` não pode reduzir `S_UR` em média
   sobre replicações. Violação é achado, não erro.

---

## 10.1 Alvos externos de validação

`[ACHADO 7]` **Correção de uma incompatibilidade de unidades.** A versão anterior
desta seção descartava, corretamente, as cifras de Love como base para
`F_ancora` — "custo como fração do contrato e probabilidade de uma tarefa exigir
retrabalho são grandezas distintas" — e, no parágrafo seguinte, usava essas mesmas
cifras como faixa admissível para uma razão de **esforço** produzida pelo
simulador. A confusão recusada num parágrafo era reintroduzida no outro. O
critério foi refeito sobre a construção equivalente em unidade.

### Referência em ESFORÇO — mesma unidade da saída do modelo

| fonte | valor reportado |
|---|---|
| BOEHM, B.; BASILI, V. R. *Software Defect Reduction Top 10 List*. **Computer**, v. 34, n. 1, p. 135-137, jan. 2001. DOI 10.1109/2.962984 | item 2: projetos de software gastam **40% a 50% do esforço** em retrabalho evitável |

Disponível em `https://www.cs.umd.edu/~basili/publications/journals/J81.pdf`.

### Referência em CUSTO — unidade distinta, retida como piso de ordem de grandeza

| fonte | valor reportado |
|---|---|
| LOVE, P. E. D. et al. *Quantifying the Costs of Field Rework in Construction*. **JCEM**, v. 152, n. 1, 2026. DOI 10.1061/JCEMD4.COENG-17026 | 0,38% do valor de contrato (mín. 0,01%; máx. 3,67%); 0,76% incluindo pós-conclusão (máx. 7,34%) |
| LOVE, P. E. D.; LI, H. *Quantifying the causes and costs of rework in construction*. **Construction Management and Economics**, v. 18, n. 4, p. 479-490, 2000. | 3,15% e 2,40% em dois estudos de caso |

`[DEC]` **Estas cifras continuam NÃO sendo usadas como valor de `F_ancora`**, pela
razão já registrada. Também não são usadas como faixa de aceitação direta, pela
razão nova: a base é monetária, não de esforço.

### Critério adotado

`[DEC]` A saída confrontada é `retrabalho_sobre_plano = TR / E_plano`, com
`E_plano = Σ_j duração_j`. Faixa admitida: **1% a 50% do esforço planejado**. O
piso vem da ordem de grandeza das cifras de campo em construção; o teto, da cifra
de esforço em software. O critério incide sobre a **mediana**, e a cauda é
reportada como limitação, não suprimida.

`[LIMITACAO]` **É um teste fraco.** A faixa cobre uma ordem e meia de grandeza
porque as duas literaturas medem construtos diferentes (custo × esforço) em
domínios diferentes (construção × software). Ele rejeita desalinhamento
grosseiro e nada mais; não substitui calibração. Registrar assim na entrega, e
não como confirmação empírica do modelo.

`[ACHADO]` Nenhuma das fontes localizadas reporta **incidência** de retrabalho
por tarefa. Portanto `F_ancora` permanece sem base empírica direta e continua
como parâmetro varrido — mas agora com um teste de consistência externa que
restringe os valores admissíveis.

## 10.2 Métricas de retrabalho — decomposição

`[ACHADO 6]` A métrica agregada `(TR + S_UR) / esforço_realizado` foi
descartada. Dois defeitos, ambos verificados nos dados (384 execuções pareadas):

1. `S_UR_final = 0` em 384 de 384 execuções, porque o laço só termina com a
   dívida quitada. O termo de dívida latente era estruturalmente inerte.
2. O denominador incluía o tempo ocioso `TU`, que é a própria disfunção sob
   estudo. O braço centralizado (`TU = 118,2` contra `6,3`) inflava o próprio
   denominador e **parecia melhor** na razão (0,0757 contra 0,0819) enquanto seu
   retrabalho absoluto era **23,8% maior** (69,1 contra 52,7 períodos).

`[DEC]` Substituída por duas métricas de base fixa por instância, portanto
idêntica nos dois braços:

| métrica | definição | mede |
|---|---|---|
| `retrabalho_sobre_plano` | `TR / E_plano` | retrabalho efetivamente pago |
| `divida_latente_sobre_plano` | `max_t S_UR(t) / E_plano` | exposição oculta de pico |

`retrabalho_sobre_esforco_realizado = TR / esforço_realizado` é mantida apenas
como **diagnóstico de eficiência alocativa**, nunca como medida de dano. A
separação é necessária porque os cenários diferem em `p_reporte` (0,15 contra
0,75): o adaptativo converte dívida oculta em retrabalho visível, e um agregado
que soma as duas parcelas não distingue conversão de redução.

---

## 11. Decisões em aberto

- `[ABERTO]` `F_ancora` — taxa basal de retrabalho do domínio de engenharia.
- `[ABERTO]` `n_agentes` — sem base empírica; será varrido.
- `[ABERTO]` Valores numéricos de `τ_sat`, `R_error`, `f_corrup`,
  `Limite_Aversao_Perda`, `p_deteccao`, `p_reporte`, `f_retrabalho`,
  `k_analitico`, `k_heuristico`, `r_recuperacao`, `s_transicao`. Todos entram como premissas com faixa de
  varredura declarada em `config/parametros.yaml`, e nenhum resultado do
  trabalho pode depender de um valor específico sem análise de sensibilidade.

**Nenhum desses valores em aberto é estimável com os dados disponíveis.** A
consequência metodológica é que os resultados do simulador serão apresentados
como comparação **entre cenários sob os mesmos parâmetros**, e não como previsão
de valores absolutos.


---

## 11. Calibração e identificabilidade

`[LIT]` **Procedimento:** History Matching com medida de implausibilidade e corte
em 3 (Andrianakis et al., 2015; Pukelsheim, 1994). A saída é o conjunto **NROY**
— não uma estimativa pontual.

`[LIT]` **Validação do procedimento:** teste do **gêmeo idêntico** (McCulloch et
al., 2022). Observações sintéticas são geradas de um vetor de parâmetros
conhecido, com sementes disjuntas das do simulador, e verifica-se se a
calibração o recupera.

`[DEC]` History Matching **sem emulador**: o simulador custa 0,108 s por
execução, e avaliá-lo diretamente elimina o termo de erro de emulação.

### 11.1 Resultado

Duas ondas de 400 pontos. **Aprovado**: NROY não vazio (115 pontos), contém o
vetor verdadeiro nos cinco parâmetros calibrados, volume da caixa envolvente
reduzido a 14,8% do a priori.

### 11.2 O que os dados determinam — a reportar com honestidade

| parâmetro | redução da largura marginal | veredito |
|---|---|---|
| `mu_minimo` | 70,3% | identificado |
| `F_ancora` | 36,8% | parcialmente identificado |
| `tau_sat` | 10,9% | **não identificado** |
| `f_retrabalho` | 6,0% | **não identificado** |
| `k_heuristico` | 5,8% | **não identificado** |

`[ACHADO 10]` Crista de equifinalidade entre `F_ancora` e `f_retrabalho`
(ρ = −0,840), com causa **estrutural**: os observáveis agregados só enxergam o
produto `p_falha × f_retrabalho`. O produto tem redução de **74,7%**, contra
36,8% e 6,0% dos fatores isolados.

`[DEC]` Com dados reais, estimar o **produto** — esforço esperado de retrabalho
por tarefa — e declarar a divisão entre frequência e severidade como não
identificada.

`[CORREÇÃO — rodada 2]` `V_mod = 0` não torna o critério otimista: a
observação sintética fixa contém erro amostral. Reduzir `V_sim` estreita o
denominador e pode excluir o vetor gerador. Isso ocorreu no piloto K=64; o
limite formal usa a média exata, ainda desconhecida. A incerteza de observação
e a cobertura serão tratadas depois do MVP; não escolher discrepância para
forçar aprovação.


## Alternativa estrutural de 16/09/2026 — implementação separada

O código legado deste documento permanece em `simulador.py`. A alternativa
`simulador_mvp.py` incorpora C4 completo (tempo e excesso de risco dependente
de sobrecarga), fila C1, Crowder normalizado, reset C6 e horizonte terminal.
Fórmulas, decisões de protocolo, unidades e testes estão no
[relatório 19](../projeto/19_CORRECAO_ESTRUTURAL_MVP_2026-09-16.md) e no
[registro de execução](../research/PLANO_CORRECAO_ESTRUTURAL.md).

O relatório 11 e B1/B3/B7/B9 anteriores foram congelados. Resultados da
alternativa devem ser identificados pela pasta e manifesto de reexecução;
a formulação nova não substitui silenciosamente a evidência histórica.


### Alternativa de contagem TL — 17/09/2026

`lei_tempo_aprendizado=unitario` preserva o nominal. `crowder_eq3` conta
0,5*dC_original por sucesso e0,05 por pedido não atendido; bloqueio não conta.
Não muda ocupação/relógio. O [teste21](../projeto/21_TESTE_DISCRIMINANTE_TL_2026-09-17.md)
mostra troca de sinal de E_total sem mudança física; a razão não sustenta
conclusão de governança independente dessa convenção.

## Alternativas preservadas de 19/09/2026

[DEC] `regra_fuga='constante'` continua padrão. `dependente_estado` usa
`omega*max(0,2*p_heu-1)>limite_aversao_perda`, sem sorteio extra. O limite
é varrido na família dedicada `config/robustez_a1.yaml`. A grade mostrou
saturação/censura; não tratar como mecanismo contínuo validado.

[DEC] `ancoragem_erro='historica'` continua padrão, com F_ancora×razão NASA.
`stewart_linear` usa F_base=k×0,0128 e `mapa_passos=curto|longo`, sintéticos.
O gradiente de passos substitui NASA somente nessa alternativa, não os empilha.
C2: `heterogeneidade_erro='nenhuma'` default; `beta_cv113` sorteia taxa fixa
por agente/nível, média F_base e CV=1,13, validando domínio antes de RNG.
A emenda à ordem 37 aplica a regra discriminante do parecer 41, §5:
implementação C2 validada; fonte internamente inconsistente em 0,012% (A-16),
com resíduos publicados e fórmula inalterada. Ver [C2 de fechamento](../projeto/C2_HETEROGENEIDADE_FECHAMENTO.md).

Estado e controles: [atualização de 19/09](../projeto/ATUALIZACAO_B2_A1_C1_C2_20260919.md).
