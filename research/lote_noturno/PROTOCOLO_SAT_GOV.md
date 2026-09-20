# T-SAT / T-GOV — protocolo antes da execução

Nenhuma alteração da dinâmica ou dos parâmetros nominais. Diagnósticos novos
em pasta permanente separada; fonte SAT1: nominal histórico de 384 execuções.
SAT1 exporta histograma de 100 intervalos e frações estritas <0,01 e >0,99,
e inclusiva [0,1;0,9], em todas as oportunidades da Porta 1 e nas seleções P1.
Os denominadores são decisões repetidas, não tarefas únicas ou execuções.
Gatilho SAT2: massa intermediária pooled de todas as decisões abaixo de 10%.
A seleção P1 também é reportada, para não confundir saturação com seleção.

SAT2, se habilitado: s em [0,25;0,5;1;2], dependente_estado, limite nominal
0,60. Restrição analítica prévia: omega=0,50 e q<=1 implicam fuga impossível
em toda a faixa; a varredura não poderá demonstrar graduação nesse limite.
Não alterar limite, omega ou nominal para obter fuga. Quatro instâncias
ordenadas [::120] e sementes 0..3, mesmos sorteios iniciais (sem alegar
alinhamento de eventos depois que as trajetórias divergem).

GOV: os quatro parâmetros deixam de ser constantes por arranjo na família
experimental. Cada um assume os dois extremos históricos e o ponto médio;
produto cartesiano 3^4=81 perfis, executados nos dois rótulos de arranjo.
Cada perfil adaptativo é contrastado com cada perfil centralizado: 81^2=6561
pares de perfis, incluindo configurações iguais, nominal e inversão das
premissas. São 2592 execuções (81x2x4x4), reutilizadas nos contrastes.
Esse desenho inclui regiões que invertem a ordenação histórica das premissas;
a análise deve separá-las das regiões de ordenação histórica. Não extrapolar
estabilidade de uma malha finita a toda a faixa contínua. Outros fatores
permanecem nominais; esta é uma extensão dedicada do desenho de robustez.

Cinco indicadores: atraso_relativo=makespan/CPM, taxa_omissao,
divida_latente_sobre_plano, taxa_falha_efetiva, fracao_porta1 (omissões entre
inícios P1/P3; fugas e pedidos não são inícios). IC95 t sobre médias por
instância das diferenças pareadas por instância/semente (4 instâncias).
ICs pontuais exploratórios, sem correção para multiplicidade; não tratar
os milhares de contrastes dependentes como réplicas independentes.
Conservar censura/NaN e exportar também contrastes em pares completos.
Controles: nominal reproduz os resultados arquivados sem resíduo; perfis
iguais nos dois rótulos produzem identidade. Hashes do modelo antes/depois.
