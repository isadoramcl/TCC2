# Teste local da correção da Porta 1 — 16/09/2026

**Revisor:** Claude · 256 execuções · 4 instâncias × 8 sementes × 2 cenários × 4 variantes
**Código:** cópia isolada do checkout Windows (`revisao-auditoria`), fora do repositório da autora.
**Controle positivo:** V0 reproduz o nominal exatamente
(`j6010_1`, centralizada, semente 0 → makespan 214, TW 663,0, TU 118,0, TR 55,2, taxa_omissão 0,15).
O patch é neutro com `F_ATALHO=1,0` e `OMISSAO_SEMPRE_ERRA=False`, e não altera o consumo do RNG.

## Variantes

| | atalho de tempo na P1 | omissão produz erro |
|---|---|---|
| V0 | — (nominal) | não |
| V1 | 0,70 | não |
| V2 | 0,70 | sim |
| V3 | 0,87 | sim |

---

## [A] A diferença aparente entre as portas, hoje, é seleção — não mecanismo

| variante | duração média P1 | duração média P3 | p(falha) P1 | p(falha) P3 |
|---|---|---|---|---|
| **V0 nominal** | **12,466** | **7,538** | **0,297** | **0,190** |
| V1 atalho 0,70 | 8,776 | 7,486 | 0,271 | 0,185 |
| V2 atalho 0,70 + erra | 8,793 | 7,439 | 1,000 | 0,197 |
| V3 atalho 0,87 + erra | 10,897 | 7,542 | 1,000 | 0,199 |

No nominal, tarefas executadas pela Porta 1 duram **65% mais** e falham **56% mais** que as da
Porta 3. Isso parece o arquétipo funcionando. Não é.

A fórmula de `dur_efetiva` e de `p_falha` é idêntica nas duas portas — o CRITICAL-6. A diferença
agregada é **efeito de composição**: `p_heu = σ((E − τ_sat)/s)` com `E = Di·P/B`, então o modo
heurístico é sorteado mais em tarefas **mais difíceis**, que são mais longas e têm `F_base` maior.
O subconjunto P1 é uma amostra enviesada de tarefas duras.

**Consequência prática:** qualquer verificação que compare agregados P1 × P3 será enganada do mesmo
jeito. O teste correto condiciona na tarefa, ou compara contra o contrafactual da mesma tarefa.

## [B] C4 sozinho não restaura o arquétipo — confirmado empiricamente

Centralizada:

| variante | makespan | atraso | TW | TR | taxa_omissão | retrab/plano |
|---|---|---|---|---|---|---|
| V0 nominal | 253,2 | 3,060 | 647,2 | 64,7 | 0,2031 | 0,1952 |
| **V1 atalho só** | **212,2** | **2,588** | **503,7** | **54,8** | **0,2031** | **0,1652** |
| V2 atalho + erra | 221,3 | 2,692 | 502,8 | 152,1 | 0,5115 | 0,4587 |
| V3 atalho 0,87 + erra | 239,8 | 2,911 | 580,1 | 158,9 | 0,5271 | 0,4792 |

Com **apenas** o atalho de tempo (V1), tudo melhora: makespan −16%, TW −22%, retrabalho −15%.
Alívio sem custo nenhum. Isso não é Soluções Sintomáticas — é um desconto.

Com atalho **e** erro (V2), aparece a troca: TW cai 22% e `TR` sobe **135%**, retrabalho sobre plano
sobe de 0,195 para 0,459. Aí sim há ganho imediato pago depois.

## [C] Mas a leitura literal do TCC1 produz taxa de defeito implausível

Em V2, a centralizada fica com `taxa_omissão = 0,51` e retrabalho de **46% do esforço planejado**.
A faixa empírica da literatura de engenharia é de ~4% a ~11% do custo. Mesmo com a ressalva de que
custo e esforço não são a mesma grandeza, 46% está fora de qualquer leitura razoável.

A causa é conhecida: a B9 mediu **38,64 de 60 tarefas (64%) roteadas pela Porta 1** no braço
centralizado. Fazer toda omissão virar defeito, com 64% das tarefas omitindo, dá metade do projeto
defeituosa.

**Portanto: ou `p_heu` está mal calibrado, ou a ligação omissão → erro precisa ser probabilística.**
A leitura literal do pseudocódigo do TCC1 não sobrevive ao confronto com ordem de grandeza empírica.

## [D] O contraste de governança sobrevive — e fica mais forte

Pareado por instância e semente, adaptativa − centralizada:

| variante | Δ atraso | Δ omissão | Δ TR | Δ retrab | Δ makespan |
|---|---|---|---|---|---|
| V0 nominal | −1,1084 | −0,1406 | −15,47 | −0,0464 | −91,72 |
| V1 atalho 0,70 | −0,9564 | −0,1453 | −12,35 | −0,0369 | −76,91 |
| **V2 atalho 0,70 + erra** | **−1,0858** | **−0,4052** | **−68,84** | **−0,2074** | **−88,19** |
| **V3 atalho 0,87 + erra** | **−1,1233** | **−0,4203** | **−71,92** | **−0,2168** | **−91,69** |

O sinal nunca inverte. E, com a correção estrutural completa, os contrastes de **omissão** e de
**retrabalho** ficam ~3× e ~4,5× maiores. A conclusão de governança não depende do defeito que
estava sendo corrigido — ela ficava **subestimada** por ele.

## [E] `f_atalho` move níveis, não move o contraste

V2 (0,70) e V3 (0,87) diferem bastante em nível — makespan centralizado 221,3 contra 239,8 — e
quase nada em contraste: Δ atraso −1,086 contra −1,123, Δ omissão −0,405 contra −0,420.

**O único parâmetro genuinamente novo desta correção não afeta a afirmação principal do trabalho.**
Declará-lo `[ABERTO]` com análise de sensibilidade é suficiente, e barato.

---

## Recomendações

1. Implementar C4 **com as duas propriedades** — tempo reduzido e maior risco. Só tempo piora o modelo.
2. **Não** adotar a leitura literal "toda omissão vira erro": produz 46% de retrabalho. Usar a forma
   probabilística `p_falha,P1 > p_falha,P3`, e calibrar o excesso para que a taxa agregada caia na
   faixa empírica.
3. Reexaminar `p_heu`: 64% das tarefas pela Porta 1 no braço centralizado é alto, e é o que
   amplifica qualquer ligação omissão → erro.
4. `f_atalho` como `[ABERTO]` com sensibilidade — já demonstrado que não move o contraste.
5. Substituir qualquer verificação que compare agregados P1 × P3 por uma que condicione na tarefa.
