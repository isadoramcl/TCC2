# CRITICAL-6 — a Porta 1 não implementa satisficing

**Revisor:** Claude · **Data:** 16/09/2026 · **Verificado no código, checkout Windows**

---

## 1. O que o código faz

`simulador.py`, bloco de execução (linhas 451–520):

```
E        = tar.dificuldade * P / b                      # dificuldade = Di
mu_cog, mu_rede = self.multiplicadores(a, P)            # linha 456
p_heu    = 1/(1+exp(-(E - tau_sat)/s_tr))
heuristico = rng.random() < p_heu                       # linha 460
...
produtividade = max(1e-6, mu_cog * mu_rede)
dur_efetiva   = ceil(tar.duracao / produtividade)
p_falha       = clip(F_base(tar.nivel) + R_err*(1 - mu_cog), 0, 1)
tar.porta     = "P1_omissao" if heuristico else "P3_analitica"
```

E `multiplicadores(a, P)` devolve `(fuzzy(fadiga, P), fuzzy(desconfianca, carga))`.

Três consequências, todas verificáveis por leitura:

1. **`mu_cog` não depende de `heuristico`.** É calculado na linha 456, **antes** de a
   Porta 1 ser sorteada, a partir de fadiga e pressão.
2. **`p_falha` é idêntico nas duas portas.** Mesma fórmula, mesmo `mu_cog`,
   mesmo `F_base`.
3. **`dur_efetiva` é idêntica nas duas portas.** Mesma produtividade.

A única diferença efetiva entre Porta 1 e Porta 3 é o rótulo e a taxa de drenagem:
`k_heuristico = 0,10` contra `k_analitico = 0,04`.

## 2. Portanto a Porta 1 é estritamente dominada

| dimensão | Porta 1 (omissão) | Porta 3 (analítica) |
|---|---|---|
| tempo da tarefa | igual | igual |
| probabilidade de falha | igual | igual |
| drenagem de bateria | **0,10 · E** | 0,04 · E |

A omissão **não economiza tempo** (é o item C4), **não muda a qualidade da tarefa
executada**, e **gasta 2,5× mais bateria**. Não há nenhum ganho de curto prazo.

O arquétipo de Soluções Sintomáticas exige alívio imediato com custo diferido.
Aqui há custo imediato e custo diferido, e alívio nenhum. **O que está implementado
não é satisficing: é uma penalidade de fadiga com outro nome.**

## 3. Divergência entre texto e código

A docstring do próprio `simulador.py`, linhas 29–30, afirma:

> "Sob a Porta 3, μ_cognitivo é alto e p_falha aproxima-se de F_base; sob a Porta 1,
> μ_cognitivo cai e p_falha cresce."

O código não faz isso. `mu_cog` é o mesmo nos dois ramos. Pela regra 5 do
`00_INSTRUCOES`, é preciso decidir qual dos dois está errado — e aqui o texto
descreve o modelo pretendido e o código é que diverge.

## 4. O efeito da omissão existe, mas é indireto e defasado

Modo heurístico drena 2,5× mais → bateria menor → fadiga maior → `mu_cog` menor
→ `p_falha` maior **nas tarefas seguintes**. O laço existe, mas atua por realimentação
ao longo do tempo, não sobre a tarefa que foi omitida.

Isso também reinterpreta a "dupla contagem" de `Di` levantada na discussão: o segundo
caminho (`Di → E → heurístico → erro`) é indireto e mediado pela bateria, não uma
segunda seta direta. A única entrada direta de `Di` em `p_falha` é `F_base(nível)`.

## 5. Composição do `Di` — confirmada

`02_indice_dificuldade.py`, linha 314 e 334:

```
Di = (1/3)·duracao_norm + (1/3)·intensidade_norm + (1/3)·criticidade_folga
```

`criticidade_sucessores` é calculada, gravada no CSV e **nunca usada no índice**.
Ou seja, `Di` não tem nenhuma componente estrutural ou de coordenação: é duração,
carga de recursos e folga — escala e posição.

E a varredura de pesos declarada no YAML produz `psplib_02_sensibilidade_pesos.csv`
mas não alimenta nada: `reais["Di"] = referencia`, pesos 1/3 fixos. É o A11,
agora caracterizado com precisão.

## 6. Work content — computável hoje, e não é o mesmo que `Di`

`intensidade_recursos = média_k(r_ik / R_k)`. Logo:

```
WC_i = duracao × intensidade_recursos
```

é a fórmula de conteúdo de trabalho a menos da constante 1/K, e sai de colunas que
já existem em `tarefas_j60_com_di.csv`. Medido:

| | correlação com WC |
|---|---|
| `Di` | +0,647 |
| `intensidade_recursos` | +0,719 |
| `duracao` | +0,578 |
| `criticidade_folga` | +0,119 |
| `criticidade_sucessores` | +0,030 |

**Concordância de faixa entre `Di` e WC: 49,7%.** Metade das tarefas mudaria de
faixa. Trocar `Di` por WC é mudança real de ordenação, não renomeação — o que
responde à ressalva de que poderia ser só rótulo outra vez.

## 7. Impacto e ordem

O CRITICAL-6 é anterior a tudo que estava na fila. Enquanto a Porta 1 não tiver
alívio, o modelo não contém o mecanismo que dá nome à tese, e nenhuma análise de
robustez, ablação ou calibração sobre ele responde à pergunta de pesquisa.

Correção mínima, que é o C4 já previsto no backlog: a omissão executa com tempo
reduzido. Com isso a Porta 1 passa a ter alívio imediato (menos tempo) e custo
diferido (mais drenagem, e o defeito oculto que já existe). O arquétipo fecha.

**Confiança:** alta. Verificado por leitura direta do código e da configuração.
