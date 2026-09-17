# A-13 · CRÍTICO — Quanto do contraste entre arranjos é premissa e quanto é modelo

**Data:** 17/09/2026 (v2, reescrito) · **Revisor:** Claude
**Verificação:** contadores de `outputs/diagnosticos/correcao_estrutural_20260916/correcao/nominal_corrigido.csv`,
`config/parametros.yaml` e leitura de `simulador_mvp.py`. Médias sobre 16 instâncias × 12 sementes.

---

## 1. A decomposição

| Grandeza | Centralizada | Adaptativa | Razão C/A |
|---|---:|---:|---:|
| `taxa_omissao` | 0,312500 | 0,084288 | **3,708** |
| taxa de falha real (falhas/tarefas) | 0,361979 | 0,318924 | **1,135** |
| `divida_latente_sobre_plano` | 0,103272 | 0,025458 | **4,057** |
| `atraso_relativo` | 3,060802 | 2,037381 | **1,502** |
| fração de execuções via Porta 1 | 0,636979 | 0,520486 | **1,224** |

`taxa_omissao` = tarefas com falha **não reportada** / tarefas. `p_reporte` é premissa
declarada: 0,15 centralizada, 0,75 adaptativa. A razão da premissa sozinha é
(1 − 0,15)/(1 − 0,75) = **3,400**.

| Indicador | Contraste observado | Parcela da premissa `p_reporte` | Parcela do modelo |
|---|---:|---:|---:|
| `taxa_omissao` | 3,708 | 3,400 (**93,4%** em escala log) | 1,135 (6,6%) |
| `divida_latente_sobre_plano` | 4,057 | 3,400 (**87,4%**) | 1,193 (12,6%) |
| `atraso_relativo` | 1,502 | — (não é função direta de `p_reporte`) | 1,502 |

**Consequência imediata:** das três métricas eleitas para sustentar a conclusão de
governança (decisão D-14), duas são majoritariamente reenunciados de uma premissa.
Afirmar "o arranjo adaptativo produz menos falhas não reportadas" é, em 93%,
afirmar "atribuímos a ele probabilidade de reporte cinco vezes maior".

**O que o modelo de fato produz**, e que é defensável: 1,502× em atraso; 1,135× na
taxa de falha efetiva; 1,224× na fração de decisões tomadas pela Porta 1. Menores
que o anunciado, mas são efeitos de mecanismo — o que o simulador tem a oferecer.

## 2. A porta de confiança é degenerada — agora medido, não inferido

Contadores do nominal, por execução:

| Contador | Centralizada | Adaptativa |
|---|---:|---:|
| `hiato_encontrado` | 140,78 | 152,38 |
| `hiato_colega_capaz_sem_confianca` | **130,56** | **0,02** |
| `N_req` (pedidos enviados) | **0,00** | 141,97 |
| `N_success` / `p2_ajuda` | **0,00** | 102,86 |

O hiato de competência é encontrado ~141 vezes por execução no braço centralizado.
Em 130,6 delas havia colega capaz, e a porta barrou. `N_req = 0`: **nenhum pedido
jamais foi enviado**. No braço adaptativo o mesmo bloqueio ocorre 0,02 vez.

A causa está em `config/parametros.yaml`, l. 199–205, e é aritmética fechada. A porta
é `confianca_do_colega > tau_min`, e todos começam em `tau_inicial`:

- centralizada: `0,25 > 0,60` → falso, sempre;
- adaptativa: `0,80 > 0,25` → verdadeiro, sempre.

Os dois parâmetros diferem entre arranjos **em sentidos opostos**, o que garante que
nenhum dos braços fique perto do limiar: as folgas são 0,35 e 0,55.

E τ nunca se move no braço centralizado: em `comunicar`, sem elegíveis a função
contabiliza o bloqueio e retorna **antes** de `atualizar_confianca`. Sem elegíveis
não há evento; sem evento não há atualização. Daí `TL = 0,000000` exato.

**Consequências:**

1. O contraste de assistência não é graduado — é assistência contra nenhuma. Não
   existe, no espaço varrido, regime em que a confiança importe marginalmente.
2. Toda a maquinaria de Crowder (lei de confiança, aprendizado eq. 1, teto eq. 2,
   reset C6) está **inerte** no braço centralizado. A escada incremental
   `C4_completo` → … → `C4_C1_Crowder_C6` altera **um único braço**; o outro é
   constante ao longo dela.
3. A ablação B9 "sem assistência" não altera o braço centralizado, que já estava sem
   assistência. Os 86,91% do contraste de atraso que sobrevivem à ablação medem a
   dependência do braço adaptativo, não uma comparação simétrica.

Isso é coerente com o fatorial do parecer 19: **57,73%** do contraste de atraso vem
de termos sem G nem N — isto é, de `p_reporte` e `p_deteccao`.

## 3. O que isto responde

A pergunta central do trabalho é o que emerge do fenômeno e o que decorre das regras
impostas. A resposta, medida:

- `taxa_omissao` e `divida_latente`: **decorrem da premissa**, em 93% e 87%.
- `atraso_relativo`, taxa de falha efetiva e seleção de porta: **decorrem do modelo**,
  em magnitudes de 1,14× a 1,50×.
- O aparato de confiança **não gera** o contraste de assistência; transmite, já
  pronto, o resultado de duas premissas postas de lados opostos de um limiar.

Nada disso invalida o trabalho. Invalida a apresentação atual, e realoca a
contribuição: de "o arranjo adaptativo tem melhor desempenho" para "dado um
diferencial de premissas de reporte e de confiança, eis como a degradação cognitiva,
as portas de decisão e a fila de retrabalho transmitem, amplificam ou amortecem esse
diferencial". A segunda é pergunta de mecanismo, é o que o simulador investiga, e
exige que o diferencial de entrada seja declarado como entrada.

## 4. Testes discriminantes

A maquinaria existe (`tau_portao`, `tau_rede` já implementados).

**T1 — varredura de τ através do limiar.** Fixar `p_reporte` e `p_deteccao` iguais
nos dois braços e varrer `tau_inicial` continuamente através de `tau_min`. Se os
indicadores forem função degrau, a confiança é interruptor binário e o aparato
difuso não contribui com nada ao contraste — e isso tem de ser escrito. Se houver
variação contínua, o mecanismo é real e o problema é que os valores escolhidos o
puseram fora do regime informativo; a correção é reposicionar os cenários.

**T2 — decomposição por bloqueio de premissa.** Três células: (i) só τ difere;
(ii) só `p_reporte`/`p_deteccao` diferem; (iii) ambos, que é o nominal. Reportar os
cinco indicadores nas três. Isso separa premissa de mecanismo sem depender da álgebra
do fatorial, e é diretamente citável.

**T3 — instrumentar a taxa de falha efetiva como saída de primeira classe.** Hoje ela
só se obtém somando `n_com_erro + n_reportadas`. É a métrica menos contaminada por
premissa de reporte e deve estar entre os desfechos reportados.

## 5. Recomendação

Rodar T1–T3 antes de prosseguir com V_obs/V_mod. Calibrar um modelo cujo contraste
principal é imposto por premissa é calibrar a premissa. E `p_reporte`/`p_deteccao`
passam a ser as primeiras candidatas a ancoragem externa — antes de `F_ancora`,
porque respondem por mais desfecho do que ela.

---

## Apêndice — notas sobre o parecer 22 (que está bem-feito)

**(a)** `retrabalho_sobre_esforco_realizado` tem TL no denominador e mudou entre
convenções (o parecer 21 identifica), mas não está na tabela de admissibilidade do
parecer 22, embora siga sendo produzida e apareça nas figuras (`05_figuras_modelo.py`,
constante `DIAGNOSTICO`). Acrescentar linha, marcada **Excluída** pelo motivo de `E_total`.

**(b)** `divida_latente_sobre_plano` é **estatística de extremo**. O parecer 22 exige
mesma frequência de amostragem; insuficiente — a esperança de um pico cresce com o
**número** de oportunidades de amostragem, e o horizonte do modelo é endógeno.
Comparação externa exige igualar o número de amostras, não só o intervalo.

**(c)** Falta o plano B metodológico. O parecer 22 prevê corretamente declarar
insuficiência se nenhuma fonte satisfizer o contrato, mas não diz o que o trabalho
entrega então. A rota já está decidida (D-12, Grimm et al. 2005, em `04_FONTES`):
adequação por reprodução simultânea de múltiplos padrões qualitativos. Nomear os
padrões e o critério de sucesso agora, não se e quando a busca fracassar.

**(d) Concessões do revisor.** Duas. Eu afirmei que a independência de TL era
estrutural "em nenhuma configuração" — largo demais; o escopo do parecer 22 (vale
para a alternativa implementada) está certo. E a versão 1 deste parecer afirmava que
"o contraste é imposto", genérico demais: todo estudo comparativo impõe contraste de
entrada. A afirmação correta é a decomposição quantitativa da seção 1.

**(e) Créditos.** Os controles negativos do verificador de TL — adulterar cada
indicador numa réplica e confirmar detecção — são prática correta e rara; sem eles
"384/384 idênticos" poderia significar que o verificador não compara nada. E a
retirada, por iniciativa própria, da caracterização do vetor de
`04_gemeo_identico.py::OBSERVAVEIS` como grandezas registradas em projetos evita uma
afirmação insustentável na monografia.
