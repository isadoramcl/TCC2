# Alternativas da noite — desenho declarado antes dos testes

Cada item terá commit próprio e identidade neutra verificada. Sem mudar o YAML
nominal histórico. Ensaios pequenos: quatro instâncias espaçadas da lista ordenada,
quatro sementes (0–3), ambos os braços, pareados, salvo indicação explícita.
Resultados de censura permanecem identificados; não tratar par incompleto como
contraste final. Nenhum ranking ou escolha automática de parâmetro.

## C1

Alternativa de ancoragem histórica (default) e `stewart_linear`.
Mapas sintéticos declarados dificuldade ordinal→número de passos:
`curto`: baixa=1, média=2, alta=3, muito alta=4;
`longo`: baixa=1, média=2, alta=4, muito alta=8.
Sob essa alternativa F_base=k×0,0128 substitui a composição âncora×razão NASA;
empilhar os dois gradientes contaria dificuldade duas vezes. Não se afirma que
uma tarefa PSPLIB tenha esses passos observados. Varrer ambos, preservar nominal.

## C2

Default nenhuma; alternativa beta_cv113. Para cada agente e cada nível ordinal,
sortear uma taxa basal fixa da Beta com média F_base(nível), CV=1,13.
[DEC] Quatro suscetibilidades independentes por agente, não redesenhadas por tarefa.
Não implica covariância empírica conhecida entre tarefas de níveis diferentes.
Validar todos os parâmetros antes de consumir RNG. Domínio estrito
0<mu<1/(1+1,13²); fronteiras degeneradas rejeitadas explicitamente.
Varrer âncoras históricas 0,05;0,10;0,15;0,20;0,25. Registrar rejeições, não alterar
CV. Controles de momentos usarão 200.000 agentes sintéticos e sementes fixas.
O controle de mu=0,0163 publica a diferença entre momentos arredondados e
alpha/beta impressos, conforme A-16; não recalibrar para números impressos.

## A1

Default constante, alternativa dependente_estado: omega*q>limite.
Malha limite=[0,10;0,20;0,30;0,40], omega nominal, com controle constante para
cada limite (inclusive as novas constantes). Não tentar obter curva contínua
por ajuste. O limiar é determinístico condicional a q; no agregado pode ter
platôs/saltos. Quatro pontos não provam continuidade matemática.

## E2/E3

Nominal intacto, 16 instâncias ×12 sementes ×2 braços. Exportar trajetórias por
execução e distribuição de mu por decisão executada e por período (unidades
distintas). Primeiro cruzamento da média de confiança 0,95 por execução;
percentual que nunca cruza também é resultado. Não presumir saturação.

## C4

Análise local contrafactual sem alterar o simulador: mesma distribuição de Di e
bateria de decisões nominais, substituir somente P por 0,30 ou 1,00 (limites
confirmados no código), tau_sat=[0,7;1;1,4], s=[0,01;0,25;0,6]. Integrar a
probabilidade P1: fração esperada de seleções (não taxa empírica de execuções).
Separar esse readout da fração observada em tarefas executadas no nominal.
Se os limites do código diferirem, corrigir declaração antes de executar.
Comparação com 2,3× de Rieskamp é descritiva e unidades não coincidem.

## E1

Reexecutar o script NASA existente em novo diretório de saída, preservando
cortes de LOC por quartis. Publicar tabela LOC ao lado de complexidade, versão
D'' de Shepperd do repositório com SHA256. Não promover automaticamente ao YAML.
