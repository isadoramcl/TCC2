# C4 — sensibilidade local da seleção P1 aos extremos de pressão

Análise sem modificar o simulador. Estados Di/B das 23.040 tarefas executadas
no nominal; contrafactual local substitui apenas P por 0,30 e 1,00, limites reais
do código. Piso de B=0,05. Malha tau_sat=[0,7;1;1,4], s=[0,01;0,25;0,6].
Não recalcula a trajetória endógena após a intervenção: mede a sensibilidade
local da probabilidade de seleção, condicional à população de estados nominal.

`noturno_nominal/C4_extremos_pressao.csv` publica os 18 resultados. Razão entre
frações esperadas P1 no extremo superior/inferior:

| Braço | tau=1, s=0,25 | Mínimo na malha | Máximo na malha |
|---|---:|---:|---:|
| Adaptativa | 1,574522 | 1,277388 | 1,921917 |
| Centralizada | 1,389209 | 1,226904 | 1,563834 |

Essas são **frações esperadas de seleções de estratégia**, não frações observadas
de tarefas executadas pela P1 em trajetórias contrafactuais completas. A última
leitura exigiria reexecutar a grade e permanece pendente; não substituir por esta
conta local. P2 e fuga podem separar seleção de estratégia de execução efetiva.

Comparação apenas descritiva com 44,4/19,4≈2,3 de Rieskamp: naquele estudo a unidade
é participante classificado; aqui é decisão de tarefa. Estudo 1 do mesmo artigo
não encontrou efeito (chi²=0,10; p=0,75), conforme fonte já arquivada no projeto.
P do modelo nunca fica abaixo de 0,30. Nenhum parâmetro foi ajustado contra essas
percentagens. Identidade neutra: três testes aprovados. Item C4 parcialmente
respondido, sem promover esta análise local a resultado da varredura dinâmica.
