# Atualização 19/09 — B2, A1, C1 e controle C2

> **Registro histórico superado.** A autora auditou 29f7fbf e fechou o lote.
> C2: implementação validada, fonte internamente inconsistente em 0,012% (A-16).
> Vigora o parecer 41, §5, conforme emenda à ordem 37. As menções abaixo a
> reprovação ou lote aberto descrevem o estado anterior.
> Ver [fechamento vigente](56_FECHAMENTO_DAS_ENTREGAS_OBRIGATORIAS.md).

**Lote não fechado.** Código nominal preservado; alternativas não eleitas como
substitutas. Publicações separadas por item em origin/main.

## T-B2.3 e D1 — números explícitos

Malha principal, 36 chaves historicamente incompletas; hiato/N_req são médias
acumuladas por execução (a exposição temporal difere entre pontos):

| tau_inicial | Incompletas/36 | Hiato sem confiança | N_req |
|---:|---:|---:|---:|
| 0,25 | 36 | 106925,777778 | 0 |
| 0,59 | 36 | 106919,333333 | 0 |
| 0,60 | 36 | 106919,333333 | 0 |
| 0,600001 | 0 | 14,361111 | 329,416667 |
| 0,61 | 0 | 14,250000 | 329,416667 |
| 0,65 | 0 | 3,583333 | 325,277778 |
| 0,80 | 0 | 0,083333 | 325,833333 |
| 1,00 | 0 | 0,083333 | 338,583333 |

Primeiro ponto sem incompletas=0,600001; desigualdade estrita
**tau_inicial>tau_min=0,60**, sem escolher um novo nominal. A conclusão é
condicional à amostra e à configuração; não propriedade universal do arranjo.
D1 nominal: **0,186605 adaptativa**, **0,221795 centralizada**, contra aproximações
esperadas0,190/0,224. Resíduo ANTES/DEPOIS dos campos antigos/estados/RNG=zero.

## B2/P1/P2 — caracterização corrigida

Incompletas somente em centralizada + s=0,01 + tau_sat=1 ou1,4 na grade testada.
Nominal:192/192 completas em cada braço por estado do canal direto. Não basta
assistência fechada: o bloqueio combina tarefa acima da competência disponível,
assistência fechada e rota heurística praticamente inacessível.

Duas saídas verificadas: assistência aberta36/36; mesmas36 chaves com s=0,25
ou0,60 completam36/36 em cada nível (72 contrapartes), N_req permanece0.
A tarefa escolhida no exemplo tem p_heu máximo3,25e-14; o3e-29 é de outra tarefa
mais fácil, não escolhida. Ambos são representáveis: **não é subfluxo a zero**.

[Limitação] Manter s=0,01 como teste de degeneração nesse canto, não regime
regular. Não generalizar "só P3" para toda a grade: com tau_sat=0,7 há conclusões.
Tabelas finais agora exportam `estatuto` e `valor_rotulado`: −112,291506 e
−174,504547 aparecem como CENSURADOS; a fração indefinida aparece como NA com
censura/indefinição. Valores antigos preservados, não transformados em desfechos
terminais. Ver [diagnóstico e tabelas](52_DEADLOCK_DE_TRES_VIAS_E_CENSURA.md).

## A1 — implementado, continuidade não aprovada

`regra_fuga=constante` default; `dependente_estado` alternativa com omega*q>limite.
320 execuções;117 completas,203 censuradas; zero violações. Baseline preservado.
Robustez dedicada inclui limite_aversao_perda. No estado dependente:

| Limite | Completas centralizada/16 | Completas adaptativa/16 | Fuga/P1 centralizada | Fuga/P1 adaptativa |
|---:|---:|---:|---:|---:|
| 0,10 | 0 | 8 | 0,999887 | 0,795624 |
| 0,20 | 0 | 8 | 0,999885 | 0,792429 |
| 0,30 | 0 | 8 | 0,999884 | 0,764938 |
| 0,40 | 0 | 9 | 0,999875 | 0,728281 |
| 0,60 (controle) | 16 | 16 | 0 | 0 |

Frações acima são médias por execução e **incluem censura**, não resultados
terminais. O agregado centralizado satura em fuga quase total; o adaptativo
varia, com seleção por conclusão. A regra individual continua interruptor por
estado, não mecanismo contínuo validado. Não se reformulou ou escolheu limite
para obter a curva esperada. Cinco indicadores/IC95 e ANTES/DEPOIS completos em
[A1](50_FUGA_DEPENDENTE_DE_ESTADO.md). A-13 e A-14 são os dois portões encontrados
independentemente; remover a degeneração de um não garante ausência de bloqueio.

## C1 — alternativa testada

Seis pontos com maior resíduo6,94e-18 (<1e-12). Mapas sintéticos curto/longo
comparados com histórico em96 execuções, todas completas. Nenhum mapa eleito.
Na alternativa o gradiente de passos substitui o NASA: decisão declarada, sem
empilhar transporte de dificuldade. Histórico permanece default.
Mapa reverso:0,05→3,90625 passos;0,10→7,8125;0,15–0,25 requerem k>8 e são
**cenários de sensibilidade**, não valores ancorados. Ver [C1](53_ANCORAGEM_LINEAR_DE_F_ANCORA.md).

## C2 — interrompido no controle publicado

Fórmula literal mu=0,0163/CV=1,13 retorna alpha=0,754081392435,
beta=45,508580720130; não reproduz0,7546/45,4563 na terceira casa exigida pela
ordem37. Os impressos implicam momentos que arredondam para os publicados:
problema de contrato de precisão, não prova de erro da fórmula. Nenhum ajuste.

Seguindo a regra de parada do item, Beta não foi inserida no simulador e não
houve sorteio de agentes. Matemática/domínio conferidos independentemente;
seis células históricas excedem o domínio e estão tabuladas. Critério C2 precisa
de reconciliação antes de continuar. Ver [resíduos e domínio](54_CONTROLE_DE_MOMENTOS_ARREDONDADOS.md).

C4/F permanecem parciais conforme autorizado. Próximo passo não é uma onda HM:
é resolver o critério C2 e revisar cientificamente a saturação de A1. Não há
aprovação implícita por teste de software nem pelo push.

## Verificação de software

80 testes de `research/test_*.py` passaram na árvore final; logs por item e
`outputs/diagnosticos/verificacao_final_20260919.log`. Isso inclui identidade
bit a bit do nominal e controles locais. **Não equivale** a aprovação do
controle científico de continuidade A1 ou do controle publicado C2, ambos
explicitamente não aprovados acima.
