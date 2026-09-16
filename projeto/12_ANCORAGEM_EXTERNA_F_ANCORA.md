# Nota de pesquisa — ancoragem externa de `F_ancora` e do produto `F × f`

**Data:** 15/09/2026 · **Origem:** pergunta 4 da lista para a orientação
**Estado:** proposta com fontes parcialmente verificadas; ver a seção de ressalvas

---

## 1. O que a pergunta é

`F_ancora` fixa o **nível absoluto** da probabilidade basal de falha por tarefa.
A camada NASA fornece o **gradiente ordinal** — quanto o risco cresce entre faixas
de complexidade — mas não o nível. O README declara isso: *"A taxa basal absoluta
de retrabalho em engenharia permanece aberta; não foi estimada pela NASA."*

No simulador:

```
p_falha = clip( F_base(nível) + R_error · (1 − μ_cognitivo) , 0 , 1 )
F_base(nível) = F_ancora × multiplicador_de_risco(nível)
```

Faixa a priori usada na calibração: `F_ancora ∈ [0,05 ; 0,25]`. É palpite.

**Por que importa:** é o parâmetro com maior sinal identificável do conjunto
(r = 0,950 com `taxa_omissao`), multiplica toda quantidade de retrabalho do modelo,
e é um dos cinco que a calibração tenta estimar. Fixá-lo por evidência de domínio
remove um parâmetro aberto **e** alivia a calibração, que hoje é o gargalo.

---

## 2. Por que a literatura não responde diretamente

Levantei a literatura empírica de retrabalho em engenharia e construção. Ela mede
**custo**, não **frequência**. O documento compilado pela CMAA é explícito: não
apresenta números sobre a proporção de itens de trabalho que sofrem retrabalho —
apenas impacto em custo e prazo.

Ou seja: ninguém publica `P(tarefa sai com defeito)`, que é exatamente o que
`F_ancora` é. Por isso a busca direta falha, e por isso o parâmetro ficou aberto.

---

## 3. A saída: duas fontes, duas restrições, dois parâmetros

A chave é notar **o que cada literatura restringe**.

No modelo, o observável de retrabalho é, em esperança,

```
retrabalho_sobre_plano  =  TR / E_plano  ≈  p_falha × f_retrabalho × severidade
```

Portanto:

| fonte | restringe | parâmetro do modelo |
|---|---|---|
| Confiabilidade humana (HEART e similares) | probabilidade de erro **por tarefa** | `F_ancora` |
| Literatura de custo de retrabalho (CII, Love, Hwang) | **fração de esforço** gasta em retrabalho | o produto `F_ancora × f_retrabalho` |

**Duas restrições externas independentes, dois parâmetros.** O sistema fecha.

E isso conversa diretamente com o CRITICAL-1: os observáveis agregados veem o
produto, e a separação dos fatores exige um canal à parte. A literatura fornece
exatamente esse canal à parte — só que de fora do modelo, não de dentro dos dados.
O que a calibração não consegue separar, a ancoragem externa separa.

---

## 4. Números levantados

### 4.1 Custo de retrabalho — restringe o produto

Compilação da CMAA, com os estudos primários nomeados:

| estudo | custo direto de retrabalho |
|---|---|
| CII Research Summary 10-1 (1989) | 12% total — projeto 9,5%, construção 2,5% |
| Burati, Farrington & Ledbetter (1992) | projeto 9,5%, construção 2,5%, fabricação 0,3%, operabilidade 0,1% |
| Benchmarking & Metrics Data Report (1997) | 3,4% |
| Love (2002), por grupo respondente | projetistas 8,0%, contratantes 5,8%, gerentes 4,3% |
| Hwang et al. (2009), por setor | edificações 4,6%, industrial leve 9,3%, infraestrutura 5,7%, industrial pesado 4,5% |
| CII Research Report 153-11 (2011) | 4,4% |

Síntese da compilação: mediana direta **4,03%**; corrigindo subnotificação, faixa
**4,03%–6,05%** com mediana 5,04%. Custos indiretos ≈ 80% dos diretos, levando o
total a **7,25%–10,89%**, mediana **9,07%**.

Também reporta impacto de prazo: atraso médio de 18,85% da duração planejada, do
qual o retrabalho responde por 52,1% — ou seja, **≈ 9,8% de crescimento de prazo
atribuível a retrabalho**.

### 4.2 Confiabilidade humana — restringe o fator

HEART (*Human Error Assessment and Reduction Technique*) estrutura a estimativa como
**confiabilidade nominal por tipo genérico de tarefa** multiplicada por
**condições produtoras de erro** com multiplicadores tabelados.

A correspondência estrutural com o simulador é quase termo a termo:

| HEART | simulador |
|---|---|
| confiabilidade nominal por tipo genérico de tarefa | `F_base(nível)` |
| condições produtoras de erro, multiplicativas | `μ_cognitivo`, pressão de prazo, fadiga |
| probabilidade de falha da tarefa | `p_falha` |

Verifiquei que a técnica trata a confiabilidade nominal como probabilidade de falha
por tarefa, e conferi multiplicadores reais de condições: falta de tempo ×11,
desconhecimento de situação infrequente ×17, sobrecarga de capacidade de canal ×6.
As probabilidades de falha calculadas nos exemplos do documento consultado são
0,16, 0,09 e 0,02 conforme o tipo de tarefa.

**Esses valores caem dentro da faixa a priori `[0,05 ; 0,25]` hoje usada.** O palpite
não era absurdo — mas pode deixar de ser palpite.

---

## 5. Alerta de validade externa que este levantamento revelou

No vetor verdadeiro do gêmeo sintético, o modelo produz
`retrabalho_sobre_plano = 0,196` — 19,6% do esforço planejado gasto em retrabalho.
Nos vértices da caixa de calibração o valor vai de 0,043 a 0,628.

A literatura empírica põe o retrabalho **direto** entre ~3,4% e ~9,5%, e o total
entre ~7% e ~11%. Custo e esforço não são a mesma grandeza, mas para retrabalho
dominado por mão de obra servem como checagem de ordem de grandeza.

**O modelo está operando de duas a quatro vezes acima da faixa empírica.**

Isso é consistente com o que se deduz do encadeamento: com `F_ancora = 0,18` e
`f_retrabalho = 0,42`, o produto é 0,0756, e o observável dá 0,196 — cerca de 2,6×
o produto. A diferença vem do termo cognitivo aditivo em `p_falha` e da severidade.
Isso implica uma taxa efetiva de falha por tarefa da ordem de 0,47, quase metade
das tarefas falhando — valor que, nas tabelas de confiabilidade humana, só aparece
em tarefas totalmente não familiares executadas sob pressão.

**Isto é dedução a partir de agregados, não medição.** O teste discriminante é
trivial e deve ser feito antes de qualquer conclusão: **instrumentar a taxa de
falha realizada por execução** (contador puramente observacional, como os da B9) e
compará-la com as tabelas. Hoje ninguém sabe qual `p_falha` o modelo efetivamente
produz.

---

## 6. Segundo alerta: `atraso_relativo` não é comparável a "crescimento de prazo"

`atraso_relativo = makespan / makespan_cpm`, e a coluna usada é
`makespan_sem_recursos` — o limite inferior de CPM, **sem restrição de recursos**.
Um cronograma viável sempre fica bem acima desse limite, então a razão de 1,5 a 2,3
que o modelo produz não é comparável aos ~9,8% de crescimento de prazo da literatura.

Correção barata: o PSPLIB publica soluções ótimas ou melhores conhecidas para o
conjunto J60, e elas **não estão** nos dados processados
(`instancias_j60.csv` traz apenas `makespan_sem_recursos`). Incorporá-las dá uma
linha de base viável, e o atraso medido contra ela passa a ser comparável à
literatura — abrindo um segundo alvo de validação externa que hoje não existe.

---

## 7. Ressalvas de verificação

| item | estado |
|---|---|
| Estrutura do HEART e multiplicadores de condições | **verificado** em documento de aplicação |
| Tabela de tipos genéricos do HEART com valores nominais | **NÃO verificado** — obter da fonte primária antes de citar |
| Números de custo de retrabalho | **verificados** numa compilação secundária (CMAA), com estudos primários nomeados |
| Estudos primários (CII 10-1, 153-11, Burati et al., Love, Hwang et al.) | **NÃO lidos** — citar apenas após obter cada um |
| Love & Li (2000) | metadados conferidos; conteúdo não lido |
| PSPLIB publica ótimos para J60 | plausível e amplamente sabido; **conferir na fonte** antes de depender |

Nada aqui deve entrar na monografia antes de a fonte primária correspondente ser
obtida e conferida, pela regra 4 do projeto.

---

## 8. A pergunta reescrita para a orientação

Em vez de *"o senhor tem fonte para `F_ancora`?"* — que ele já respondeu que não —
levar a proposta:

> Proponho ancorar a probabilidade basal de falha por tarefa em literatura de
> **confiabilidade humana** (HEART e similares), e ancorar o produto
> `F_ancora × f_retrabalho` na **literatura empírica de custo de retrabalho**
> (CII, Love, Hwang). São duas restrições externas independentes para dois
> parâmetros, e substituem a transferência do gradiente da NASA como fonte do
> nível absoluto. Vê problema nessa ancoragem, ou conhece alguém em confiabilidade
> humana que possa validar a escolha dos tipos genéricos de tarefa?

Isso também reformula a pergunta 3: a transferência NASA → PSPLIB deixa de carregar
o nível absoluto e passa a carregar **apenas o gradiente ordinal entre faixas**, que
é o que ela de fato mede e o que o trabalho sempre afirmou que ela media.
