
# `ρ_omissão` a partir de dados humanos — 16/09/2026

**Revisor:** Claude · Dados: OSF `q2dm6`, `dataset/human_comprehension_data.csv`
SHA-256 declarado pelo OSF: `7808075b932c3096ba2c50ff0273b2d375607afd0ba6a3ceeb627ab353fbf171`
Artigo: *Hierarchical resource rationality explains human reading behaviour*,
Nature Human Behaviour, 2026. DOI 10.1038/s41562-026-02534-0.

---

## 1. Por que estes dados servem

A formulação acordada para a Porta 1 é

```
p_falha,P1 = 1 − (1 − p0)·(1 − ρ_omissão·q)
```

Rearranjando:

```
(p_falha,P1 − p0) / (1 − p0) = ρ_omissão · q
```

Ou seja, `ρ·q` é o **excesso de erro como fração do que ainda podia dar errado**. Não é
diferença nem razão — é excesso relativo no complemento. E essa grandeza se mede diretamente
num experimento de speed–accuracy com condição de pressão manipulada.

Definindo a condição de menor pressão como linha de base:

```
ε(c) = [ e(c) − e(90s) ] / [ 1 − e(90s) ],    e(c) = 1 − acurácia(c)
```

## 2. Estrutura dos dados

32 participantes × 9 estímulos = **288 trials**, 96 por condição, e **todas as 96 células
participante × condição têm exatamente 3 trials**. Desenho intra-sujeito contrabalançado.

As médias reproduzem o artigo: MCQ 0,5917 em 30 s e 0,8250 em 90 s, contra 0,59 e 0,83
publicados. É o dado certo.

## 3. Resultado

| condição | MCQ médio | erro `e(c)` | `ε(c)` agregado | `ε(c)` pareado | IC 95% |
|---|---|---|---|---|---|
| 30 s | 0,5917 | 0,4083 | **0,2828** | **+0,2680** | [+0,1973; +0,3387] |
| 60 s | 0,7313 | 0,2687 | 0,1136 | +0,1014 | [+0,0357; +0,1671] |
| 90 s | 0,8250 | 0,1750 | — (base) | — | — |

n = 32 pareado. Mediana de `ε(30 s)` = +0,3077. **29 de 32 participantes com `ε(30 s) > 0`.**

## 4. O que isso fixa e o que não fixa

**Fixa um piso.** Como `q ∈ [0,1]`, temos `ρ = ε/q ≥ ε`. Portanto:

```
ρ_omissão ≥ 0,268     (limite inferior do IC 95%: 0,197)
```

com igualdade apenas se a condição de 30 s corresponder a sobrecarga total (`q = 1`), o que é
improvável.

**Não fixa o valor pontual.** `ρ = ε(30)/q(30)` depende de onde a pressão experimental cai na
escala de sobrecarga do modelo, e não existe mapeamento entre "segundos de orçamento de leitura"
e o `E = D_i·P/B` do simulador. Se `q(30)` estiver entre 0,6 e 0,8, então `ρ ∈ [0,34; 0,45]`.

**Dá uma restrição de forma, que é informação nova.** Com dois pontos acima da base:

```
q(30) / q(60) = ε(30)/ε(60) = 2,49
```

Qualquer mapeamento adotado entre pressão e `q` deve reproduzir essa razão. É um segundo vínculo
empírico, independente do nível.

**Não sustenta valor pontual, e sim faixa.** `ε(30 s)` por participante varia de −0,375 a +0,643.
A dispersão é grande — mesma lição do `F_ancora` com a dispersão entre métodos de HRA. `ρ_omissão`
entra como `[ABERTO]` com faixa e análise de sensibilidade, não como constante.

## 5. Limitações declaradas

1. **Transporte de construto.** Erro de compreensão de leitura não é defeito em entrega de
   engenharia. O que transporta melhor é a **forma** — excesso relativo em escala limitada — e é
   exatamente a forma que a equação usa. Continua sendo transporte e deve ser declarado.
2. **Pressão nem sempre piora.** 3 de 32 participantes tiveram `ε(30 s) < 0`, ou seja, foram
   melhores sob pressão. É o mesmo achado de Zou et al. (2021) em examinadores profissionais. A
   formulação adotada (`q = 0` abaixo do limiar, sem ramo de benefício) não representa melhora sob
   pressão. Simplificação declarada, não omissão.
3. **A coluna `recall` do CSV é texto livre**, na redação do próprio participante — **não** é o
   `free_recall_score` normalizado que o README declara. O README está desatualizado em relação ao
   arquivo. Os valores de recall publicados no artigo (0,64 e 0,73) **não são reproduzíveis a
   partir do dado público** sem pontuar os textos. Se recall for desejado como segundo observável,
   é trabalho novo de codificação.
4. **32 participantes válidos**, não 39. O README diz "32 valid human participants" e os dados vão
   de 1 a 32. Citar o número certo.
5. **Três títulos diferentes** para a mesma obra: o nó do OSF é "A Resource-Rational Mechanism for
   Reading", o README diz "Resource-Rational Control of Eye Movements in Reading", e o publicado é
   "Hierarchical resource rationality explains human reading behaviour". Citar o publicado e o
   repositório pelo accession.
6. **Sem licença declarada** no nó do OSF (`node_license: null`). Público não é o mesmo que
   licenciado para reuso. Conferir os termos na declaração de disponibilidade do artigo antes de
   redistribuir dado derivado.
7. O arquivo **não está em UTF-8** (lido com `latin-1`). Relevante para reprodutibilidade.

## 6. O que entra no modelo

```
rho_omissao: { valor: 0.35, faixa: [0.20, 0.50], condicao: aberto,
               fonte: "excesso relativo de erro sob pressão temporal, ε(30s) = 0,268
                       [0,197; 0,339], n=32, Nature Human Behaviour 2026 / OSF q2dm6;
                       transporte de construto declarado" }
```

O valor central 0,35 corresponde a `q(30) ≈ 0,77`. A faixa cobre de `q(30) = 1` (piso, ρ = 0,20
pelo limite inferior do IC) até sobrecarga moderada. **Sensibilidade obrigatória**, e o critério
de aceitação não é o retrabalho agregado cair numa faixa desejada — é a conclusão de governança
sobreviver à varredura.
