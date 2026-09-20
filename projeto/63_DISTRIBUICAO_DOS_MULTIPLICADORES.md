# E3 — distribuição nominal dos multiplicadores

384 execuções completas; 23.040 tarefas executadas. Observações por tarefa e
por período publicadas separadamente em `noturno_nominal/E3_distribuicoes.csv`.
A média por execução dá peso igual a cada execução; a pooled por período dá
mais peso às execuções longas. Não são o mesmo estimando.

| Unidade: tarefa executada | mu_cog médio | mu_rede médio |
|---|---:|---:|
| Adaptativa | 0,809597 | 0,916757 |
| Centralizada | 0,752021 | 0,727805 |

Médias temporais com peso igual por execução: mu_cog 0,792401/0,740646 e
mu_rede 0,890499/0,719159, adaptativa/centralizada. Quantis 5/50/95%, extremos e
N constam da tabela; piso observado 0,55. Esses valores não coincidem com as
ordens de 0,95 (pressão) e 0,97 (fadiga) citadas na ordem para Reichelt & Lyneis.
Não se ajustou mu_minimo para fazê-los coincidir.

Os benchmarks são **saídas de outro modelo de Dinâmica de Sistemas da mesma
linhagem**, não medição empírica independente. Além disso, mu_cog aqui combina
pressão/bateria e mu_rede é canal de rede/confiança: não correspondem um a um
aos fatores pressão/fadiga daquele modelo. A comparação mostra diferença de
magnitude e de construto; não autoriza validar ou rejeitar isoladamente uma
faixa de mu_minimo. Identidade neutra: três testes aprovados.
