# Parecer 25 — Estamos reduzindo os parâmetros arbitrários?

**Data:** 17/09/2026 · **Revisor:** Claude
**Base:** contagem em `config/parametros.yaml`, contadores do nominal, e o PDF de Crowder et al. (2012)

---

## 1. A contagem, sem interpretação

39 parâmetros declarados. Classificação pelo campo `condicao` do próprio arquivo:

| condicao | n | % |
|---|---:|---:|
| `premissa` | 21 | 54% |
| `aberto` (com varredura ou faixa) | 14 | 36% |
| `literatura` | 2 | 5% |
| `calibrado` | 1 | 3% |
| `tcc1` | 1 | 3% |

Os dois `literatura` são **escolhas estruturais**, não magnitudes: t-norma produto e
partição difusa uniforme (Van Broekhoven & De Baets, 2009). O único `calibrado` é o
gradiente de complexidade da NASA — que já sabemos carregar só informação ordinal e
cujo eixo está em disputa (D-06).

**Nenhuma magnitude do modelo está ancorada externamente hoje.** Zero de 39.

## 2. Mas a resposta honesta não é "não estamos conseguindo"

O número de parâmetros arbitrários caiu pouco. O que caiu muito foi outra coisa, e
essa é a conquista real:

**(a) Arbitrário e oculto → arbitrário e declarado com varredura.** Catorze
parâmetros hoje carregam `varredura` ou `faixa` e são efetivamente varridos nos lotes
de robustez. Um parâmetro arbitrário que é varrido e reportado deixa de ser grau de
liberdade escondido e vira sensibilidade declarada. Não é ancoragem, mas é a
diferença entre um resultado que se sustenta e um que não se defende em banca.

**(b) Parâmetros eliminados por escolha estrutural.** A decisão D6 — partição
uniforme, justificada em Van Broekhoven & De Baets — **dispensou** `consequentes` e
`largura_saida`, que deixaram de existir como premissas. Esse é o único mecanismo que
de fato reduz arbitrariedade: não estimar melhor um parâmetro, e sim tornar
desnecessário estimá-lo. Foi feito uma vez e deveria ser procurado ativamente em
outros pontos.

**(c) Duração do retrabalho deixou de ser parâmetro.** Com a fila de reparos (C1), o
tempo de cada retrabalho passou a ser **emergente** — sai da ocupação de agente e
recurso, com invariante de conservação verificado em tempo de execução. Antes era
uma fração aplicada. Isso é redução genuína, do tipo (b).

**(d) Conclusões rebaixadas em vez de defendidas.** `E_total` retirada, nível
absoluto de `F_ancora` retirado da camada NASA, `Di` redescrito, `atraso_relativo`
não admitido como crescimento de prazo externo. Cada uma dessas é um parâmetro ou
afirmação arbitrária que parou de sustentar conclusão.

**(e) `ρ_omissão` ganhou faixa empírica.** [0,20; 0,50], derivada de dados humanos
depositados que eu reanalisei. Continua `aberto`, mas a faixa não é palpite.

## 3. Onde a redução **não** aconteceu — e é onde mais importa

Os quatro parâmetros que definem o contraste entre arranjos são todos `premissa`:

| Parâmetro | Centralizada | Adaptativa | Origem declarada |
|---|---:|---:|---|
| `tau_inicial` | 0,25 | 0,80 | "confiança mútua baixa / alta" |
| `tau_min` | 0,60 | 0,25 | "limiar alto / baixo para conceder ajuda" |
| `p_reporte` | 0,15 | 0,75 | "ocultação / reporte imediato" |
| `p_deteccao` | 0,03 | 0,12 | "segurança psicológica restrita / elevada" |

O parecer 23 mediu que `p_reporte` responde por **93,4%** do contraste de
`taxa_omissao` e **87,4%** do de dívida latente. E `tau_inicial`/`tau_min` deixam a
porta de confiança travada nos dois sentidos.

**Ou seja: a redução de arbitrariedade avançou nos parâmetros de pouca consequência
e não avançou nos de maior consequência.** Isso não é acaso — os quatro acima são os
mais difíceis de ancorar, e por isso ficaram por último. Mas o esforço de pesquisa
está hoje apontado para `F_ancora` (G-02, bloqueado pela ponte de agregação do HEART),
que responde por menos desfecho do que `p_reporte`. **A prioridade está invertida.**

## 4. Frequência de erro

| Parâmetro | Estado | Obstrução |
|---|---|---|
| `F_ancora` | `aberto`, varrido em [0,05 … 0,25] | G-02: a probabilidade do HEART é por passo elementar; uma atividade J60 agrega muitos. Sem regra de composição, o número não pode ser lido como `F_ancora`. |
| `R_error` | `aberto`, varrido em [0,05; 0,15; 0,30] | sem fonte |
| Produto `F_ancora × f_retrabalho` | não identificável dos agregados (A-01) | ancoragem externa é a única saída |

**O que mudou para melhor:** a taxa de falha **efetiva** do modelo agora está medida —
0,362 centralizada, 0,319 adaptativa. Antes ninguém sabia qual `p_falha` o modelo
produzia; era dedução a partir de agregados (parecer 12, §5). Hoje é observação
direta. O instrumento existe; falta o comparador.

**Recomendação:** promover a taxa de falha efetiva a desfecho de primeira classe
(T3 do parecer 23). É o indicador menos contaminado por premissa de reporte e é o
alvo natural de qualquer ancoragem futura de frequência de erro.

## 5. Custo ou duração de cada retrabalho

Aqui a situação é melhor do que parece, e vale separar duas coisas:

- **Duração de cada reparo: resolvida estruturalmente.** A fila C1 faz o tempo de
  reparo emergir da ocupação, não de um parâmetro. Não precisa de fonte.
- **Magnitude do retrabalho gerado por falha: aberta.** `f_retrabalho` e `f_corrup`
  continuam premissas, e o observável agregado só enxerga o produto com `F_ancora`.
- **Comparador externo: existe em unidade, não em domínio.** Boehm & Basili (2001)
  medem esforço, como o modelo — é a única referência na mesma unidade, e já está
  verificada em `04_FONTES`. O problema é domínio (software × projeto de engenharia),
  não unidade. A literatura de construção mede custo sobre valor de contrato, outro
  denominador ainda (Love 2026: 0,38%; Love & Li 2000: 3,15% e 2,40%).

**Posição defensável hoje:** comparar com Boehm & Basili declarando o empréstimo de
domínio, tratando a cifra como ordem de grandeza e não como validação. Isso é
escrevível agora e melhora a monografia. A busca por cifra em esforço fora de
software continua aberta (G-01) — Rodrigues (2000, SYDPIM), já catalogado, trabalha
nativamente em esforço e ninguém olhou ainda com essa pergunta.

## 6. Dá para medir bateria cognitiva, confiança e segurança psicológica?

Resposta direta: **como o modelo as usa, não.** E o precedente do próprio trabalho
mostra por quê.

### 6.1 O que Crowder et al. fizeram — e é instrutivo

Eles mediram confiança, competência e motivação com questionário psicométrico em
escala Likert de cinco pontos (216 respondentes, 35 equipes), e usaram os resultados
como **valores de entrada definidos pelo usuário** — não como alvos de calibração.
A validação deles correlacionou o desempenho previsto com avaliações independentes
dos líderes: **r = −0,02 para qualidade; r = 0,10 para tempo de conclusão; r = 0,31
para tempo de trabalho.** E declaram explicitamente que o modelo *"does not yield
absolute information"*, examinando sensibilidade a mudanças, não valores absolutos.

Isto é o artigo em que o trabalho se apoia. Ele não calibrou essas variáveis: mediu
como insumo de cenário e validou fracamente no desfecho. A posição honesta deste TCC
é, portanto, **bem precedentada** — e o precedente também limita o que se pode
prometer.

### 6.2 Por variável

| Variável do modelo | Mensurabilidade externa | Instrumento |
|---|---|---|
| **Confiança (τ)** | Sim, como escore de escala, transversal, por equipe | Gillespie, *Behavioural Trust Inventory* — é a referência [18] do próprio Crowder, verificada no PDF |
| **Segurança psicológica** (operacionalizada em `p_reporte`/`p_deteccao`) | **Sim, e é o alvo mais promissor** | Escala de Edmondson (1999) — construto é literalmente disposição a reportar erro |
| **Bateria cognitiva (B)** | **Não, na forma usada** | Instrumentos de carga (NASA-TLX) e fadiga medem estado momentâneo, não recurso que se esgota ao longo de um projeto |

**A obstrução comum** não é falta de instrumento, é **resolução temporal**. O modelo
trata as três como trajetórias que evoluem por período de projeto. Os instrumentos
produzem escore transversal, ordinal, por pessoa, em um ou poucos momentos. Não
existe medição de τ(t) ou B(t) na frequência que a calibração exigiria. Por isso a
rota realista é a de Crowder: **insumo de cenário em escala declarada**, não alvo
de estimação.

### 6.3 A consequência prática, e é uma redireção

`p_reporte` e `p_deteccao` são, pela própria descrição no YAML, operacionalizações de
segurança psicológica. O parecer 23 mostrou que respondem pela maior parte do
contraste. E segurança psicológica é, das três, a que tem instrumento validado,
literatura empírica ampla e escores publicados por equipe.

**Portanto: o esforço de ancoragem externa deveria migrar de `F_ancora` para
`p_reporte`/`p_deteccao`.** `F_ancora` está bloqueado por um problema de agregação
sem solução à vista e responde por menos desfecho. Segurança psicológica tem
instrumento, tem dados, e governa a maior parte do contraste que o trabalho quer
explicar.

Isso não fecha o problema — continua sendo preciso mapear um escore de escala Likert
para uma probabilidade por tarefa, o que é uma ponte de unidade como todas as outras
deste trabalho, e precisa ser declarada como tal. Mas é uma ponte sobre um vão menor
do que a do HEART, e com dados do outro lado.

## 7. Veredito em três linhas

1. **Redução de contagem: pouca.** 35 de 39 parâmetros seguem premissa ou aberto;
   nenhuma magnitude está ancorada externamente.
2. **Redução de arbitrariedade oculta: substancial.** Varreduras declaradas,
   dois parâmetros eliminados por escolha estrutural, duração de reparo tornada
   emergente, e quatro conclusões rebaixadas em vez de defendidas. É o ganho real,
   e é o que se defende em banca.
3. **A prioridade está invertida.** O esforço está em `F_ancora`, bloqueado e de
   baixa consequência; deveria estar em `p_reporte`/`p_deteccao`, que governam o
   resultado e têm instrumento.

## 8. Estado de verificação das fontes citadas neste parecer

| Fonte | Estado |
|---|---|
| Crowder et al. (2012) — método de medição, validação r = −0,02 / 0,10 / 0,31 | **TEXTO LIDO** — PDF nos arquivos do Projeto |
| Gillespie, *Behavioural Trust Inventory* | **METADADOS** — referência [18] de Crowder, conferida na lista dele; texto não lido |
| Van Broekhoven & De Baets (2009) | já catalogada e verificada em `04_FONTES` |
| Boehm & Basili (2001); Love (2026); Love & Li (2000); Rodrigues (2000) | já catalogadas e verificadas em `04_FONTES` |
| Edmondson (1999), escala de segurança psicológica | **NÃO VERIFICADA** — citada de memória do revisor. Obter e conferir antes de qualquer uso na monografia. |
| NASA-TLX (Hart & Staveland) e escalas de fadiga | **NÃO VERIFICADAS** — mencionadas apenas para dizer que não servem na resolução exigida |
