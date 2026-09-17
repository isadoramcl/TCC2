# B9 — Ablação do experimento de governança

> **PRÉ-CORREÇÃO ESTRUTURAL — congelado em 16/09/2026.** Números históricos preservados; não constituem resultado do MVP corrigido nem alimentam conclusão final sem reexecução. Ver `research/CONGELAMENTO_PRE_CORRECAO.json` e `research/PLANO_CORRECAO_ESTRUTURAL.md`.

Execução: 07/09/2026 · 2.880 execuções · 16 instâncias × 12 sementes × 15 braços
Unidade inferencial: **instância** (n = 16). Menor valor-p bilateral atingível no
Wilcoxon pareado: 3,05e-05. Nenhum p abaixo disso é interpretável.

Tabelas: `outputs/tables/modelo_07_ablacao_{bruto,parametros,mecanismo,portas,p_reporte}.csv`
Log: `outputs/logs/modelo_07_ablacao.log`
Scripts: `src/modelo/07_ablacao_governanca.py`, `src/modelo/08_verificar_ablacao.py`

---

## 0. O que foi mexido no modelo

`simulador.py` recebeu **contadores observacionais** e um parâmetro
`ablacoes` **vazio por padrão**. Com o padrão, nenhuma linha de decisão muda.
Conferido por impressão digital SHA-256 sobre 32 execuções pareadas
(makespan, TW, TL, TU, TR, n_com_erro, S_UR_máx, E_total):

```
antes  640e78e0d3ff41e857cd744fc9b90b1a72a31e59e41f16c787024236a3da0915
depois 640e78e0d3ff41e857cd744fc9b90b1a72a31e59e41f16c787024236a3da0915
```

E as 192 execuções nominais de cada braço reproduzem linha a linha o
`modelo_03_experimento_bruto.csv` já publicado. **Nenhuma alteração estrutural
foi feita.**

---

## 1. Contagem por porta (média por execução; 60 tarefas por instância)

| braço | P1 omissão | P3 analítica | P2 ajuda | P2 bloqueio | hiato |
|---|---|---|---|---|---|
| centralizada | 38,64 | 21,36 | **0,00** | 126,27 | 126,27 |
| adaptativa | 19,17 | 40,83 | 10,49 | 5,94 | 16,43 |
| centralizada sob assistência universal | 24,99 | 35,01 | 9,97 | 6,45 | 16,42 |
| adaptativa sob sem assistência | 35,11 | 24,89 | **0,00** | 145,20 | 145,20 |

`P1 omissão + P3 analítica = 60` em toda execução (verificado): são **tarefas**.
`P2 ajuda`, `P2 bloqueio` e `hiato` contam **eventos agente-período**, não
tarefas — o mesmo agente reencontra o mesmo hiato a cada período em que fica
bloqueado. Não somar com as outras duas colunas.

**Hiato estrutural:** 14,54 de 60 tarefas (24,2%) têm dificuldade acima da
**maior** competência inicial da equipe. É idêntico entre todos os braços —
depende só de instância e semente —, portanto é controle, não resultado.

**Por que a ajuda não foi concedida, no braço centralizado:**

| motivo | eventos | fração |
|---|---|---|
| havia colega livre mais competente, mas τ ≤ τ_mín | 81,42 | 64,5% |
| não havia colega livre mais competente | 44,84 | 35,5% |

Ou seja: em quase dois terços dos bloqueios do braço centralizado **existia quem
pudesse ajudar** e a regra de confiança impediu.

## 1.1 Achado de fragilidade numérica — o empate exato

A Porta 2 testa `confiança > τ_mín`, com desigualdade estrita.
`τ_inicial` da centralizada = **0,25**; `τ_mín` da adaptativa = **0,25**.
São o mesmo número. Por isso trocar **só** `τ_mín` na centralizada não muda
absolutamente nada — `0,25 > 0,25` é falso.

Sondagem (6 instâncias × 4 sementes):

| τ_mín na centralizada | TL médio | ajudas | atraso relativo |
|---|---|---|---|
| 0,60 (nominal) | 0,000 | 0,00 | 3,6841 |
| 0,2500 | 0,000 | 0,00 | 3,6841 |
| **0,2499** | **8,042** | **8,04** | **3,5360** |
| 0,20 | 8,042 | 8,04 | 3,5360 |

`TL = 0,00` no braço centralizado **não é uma propriedade robusta do arranjo**:
é uma descontinuidade sobre um empate exato entre dois parâmetros declarados em
seções diferentes do YAML. Isso precisa estar no documento.

---

## 2. BLOCO 1 — fração do contraste reproduzida por substituição isolada

> **ATENÇÃO — leitura corrigida.** Estes percentuais **não são uma decomposição
> do efeito** e não podem ser lidos como "X% do resultado vem do parâmetro Y".
> São a fração do contraste nominal que uma substituição isolada reproduz, e
> elas não somam 100% porque os parâmetros interagem. A decomposição aditiva
> legítima está em `06_B9_VERIFICACAO.md` (fatorial 2⁴ saturado), e as
> conclusões válidas são as de lá, não as desta seção.

Fórmula exata usada nesta tabela:

    fração(b, m) = 100 · média_i[ y_i(b) − y_i(centralizada) ]
                       / média_i[ y_i(adaptativa) − y_i(centralizada) ]

com i indexando as 16 instâncias e cada y_i sendo a média das 12 sementes.

| métrica | só τ_inicial | só τ_mín | só p_reporte | só p_detecção | par τ | sem par τ |
|---|---|---|---|---|---|---|
| atraso_relativo | 52,6% | 0,0% | 27,8% | 38,4% | 52,6% | 40,1% |
| E_total | **98,4%** | 0,0% | 4,3% | 1,8% | 98,4% | 3,8% |
| TL | **99,0%** | 0,0% | 0,0% | 0,0% | 99,0% | 0,0% |
| TU | **99,8%** | 0,0% | 2,7% | 0,0% | 99,8% | 2,4% |
| TW | **98,4%** | 0,0% | −0,3% | −0,9% | 98,4% | −0,6% |
| TR | **91,3%** | 0,0% | 10,1% | 4,1% | 91,3% | 5,7% |
| retrabalho_sobre_plano | **91,5%** | 0,0% | 10,7% | 5,1% | 91,5% | 6,7% |
| n_com_erro · taxa_omissão | 10,6% | 0,0% | **100,6%** | 1,0% | 10,6% | 99,5% |
| dívida_latente · S_UR_máx | 22,6% | 0,0% | **82,2%** | 57,1% | 22,6% | 93,8% |

As frações **não somam 100%**: os parâmetros não são aditivos (p_reporte e
p_detecção juntos entregam 93,8% da dívida latente, isoladamente 82,2% e 57,1%).
Valores acima de 100% e negativos são ruído em torno de efeito nulo ou
sub-aditividade, não erro de conta.

**Leitura direta:** o experimento mede duas coisas diferentes que estavam
somadas numa conclusão só.

- Tudo que é **tempo e ocupação** (TL, TU, TW, E_total, TR) é essencialmente
  `τ_inicial`: 91% a 99,8%.
- Tudo que é **defeito oculto** (n_com_erro, S_UR) é essencialmente `p_reporte`
  e `p_detecção`; τ responde por 10% a 23%.
- Só o **atraso relativo** é genuinamente misto (53% τ, 28% p_reporte,
  38% p_detecção).

## 3. BLOCO 2 — nominal × ablação de mecanismo

Efeito = média(adaptativa) − média(centralizada), por instância.
`sem_assistência`: a Porta 2 nunca concede ajuda, nos dois braços.
`assistência universal`: a Porta 2 ignora τ_mín, nos dois braços.

| métrica | nominal | sem assistência | assist. universal | resta (sem/univ) | veredito |
|---|---|---|---|---|---|
| atraso_relativo | −1,1354 | −0,8240 | −0,8608 | 73% / 76% | diminui |
| **E_total** | **+0,1046** | **−0,0477** | **−0,0095** | −46% / −9% | **INVERTE** |
| TL | +10,49 | 0,00 | +0,52 | 0% / 5% | desaparece |
| **TU** | **−120,32** | **+18,93** | −0,51 | −16% / 0,4% | **INVERTE** |
| TR | −16,36 | −4,26 | −7,13 | 26% / 44% | diminui muito |
| TW | −149,60 | −123,81 | −118,54 | 83% / 79% | diminui pouco |
| retrabalho_sobre_plano | −0,0486 | −0,0130 | −0,0211 | 27% / 43% | diminui muito |
| n_com_erro | −9,198 | −8,995 | −8,620 | 98% / 94% | permanece |
| taxa_omissão | −0,1533 | −0,1499 | −0,1437 | 98% / 94% | permanece |
| dívida_latente_sobre_plano | −0,0540 | −0,0505 | −0,0458 | 94% / 85% | permanece |
| S_UR_máximo | −18,29 | −17,11 | −15,53 | 94% / 85% | permanece |

Todos com p = 3,05e-05 (o mínimo atingível com n = 16), exceto TU sob
assistência universal (p = 0,214, sem efeito) e TL sob assistência universal
(p = 0,007, efeito residual).

## 4. BLOCO 3 — varredura de p_reporte

Demais parâmetros na centralizada.

| p_reporte | n_com_erro | taxa_omissão | TR | retrab/plano | atraso_rel | E_total |
|---|---|---|---|---|---|---|
| 0,15 | 13,02 | 0,2170 | 68,87 | 0,2031 | 3,1345 | 0,7839 |
| 0,30 | 10,63 | 0,1772 | 67,70 | 0,1997 | 3,0525 | 0,7860 |
| 0,45 | 8,49 | 0,1416 | 68,31 | 0,2009 | 3,0054 | 0,7862 |
| 0,60 | 6,13 | 0,1022 | 68,73 | 0,2020 | 2,8942 | 0,7857 |
| 0,75 | 3,77 | 0,0628 | 67,21 | 0,1979 | 2,8183 | 0,7884 |

Gradiente monótono e praticamente linear em `n_com_erro` e `taxa_omissão`;
`TR` e `retrabalho_sobre_plano` **não respondem** (variação < 2,5%, sem
significância). Razão mecânica prevista só por p_reporte:
`(1−0,75)/(1−0,15) = 0,2941`. Razão observada trocando só p_reporte: **0,2892**.
98,3% da diferença é o parâmetro reaparecendo na saída — confirma o item B11:
**manipulation check, não achado independente.**
