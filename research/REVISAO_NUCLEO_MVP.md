# Revisão independente do núcleo MVP — 15/09/2026

Escopo: leitura do plano, simulador alternativo, legado, testes, alterações da fase 1; nenhuma alteração no código. Revisão realizada antes da execução ampliada. Linhas correspondem à versão inicialmente revisada.

## Achados

### P2 — Censura mistura trabalho futuro com esforço realizado

`src/modelo/simulador_mvp.py:179-181`: TW e períodos analíticos/heurísticos são creditados integralmente ao iniciar uma atividade; TR, por sua vez, é pago período a período. Reprodução com tarefa de duração 100, CPM 8, multiplicadores 1 e limite de segurança 8: makespan=8, TW=100, E_total=1, concluiu=False. Portanto as frações de esforço de uma execução censurada não representam o trabalho realizado até seu corte. O comportamento de TW é herdado, mas o MVP passa a explicitar e explorar censura. Corrigir contagem por período ou manter uma variável de compromisso distinta; alternativamente não interpretar essas métricas em linhas censuradas. Teste atual de censura só cobre corte após a tarefa original.

### P2 — Dívida zero impede término sem pendência real

`src/modelo/simulador_mvp.py:80-83,183-189`: defeito oculto de esforço zero é adicionado à dívida, e `_terminal` exige lista vazia, mesmo quando a soma pendente é zero. Reprodução: falha=1, f_retrabalho=0, reporte=0, detecção=0, tarefa duração8, limite16: todas tarefas encerradas, retrabalho_pendente=0, dívida=[(1,0.0)], resultado censurado. Não registrar dívida de esforço nulo ou removê-la antes da condição terminal. Fora do domínio de f_retrabalho nominal positivo, mas importante para controle de desligamento.

### P2 — Comparação C4 exige controle de motor

`src/modelo/simulador_mvp.py:126-127,164` corrige disponibilidade de ambos os participantes da ajuda; `23,98-108` também muda horizonte. C4 contra legado agrega essas diferenças além da duração. A equipe informou que está acrescentando controle neutro do motor. Separar também horizonte fixo/automático ou explicitar contraste conjunto. Comparações entre variantes do mesmo motor com opções restantes iguais são adequadas.

### P3 — Reconciliação do README ficou desatualizada

`research/RECONCILIACAO_RODADA2.md` diz que o README vivo apenas acrescenta conteúdo. Após as atualizações da fase1, comparação integral mostra quatro blocos substituídos (3→2, 3→9, 10→26, 1→1 linhas), sobretudo prioridades e status. Registrar que essas substituições são deliberadas e que a integralidade histórica está no snapshot. Os dois documentos em docs diferem do snapshot somente por inserção de seis linhas cada.

## Verificações e limites

- `python3 research/test_mvp.py`: 7 testes passaram.
- `python3 research/test_documento_oficial.py`: 3 testes passaram.
- Fila mantém exclusividade de agente, reserva recursos originais e só inicia após fim original. Pagamento fracionário versus ceil da ocupação está declarado. Conservação gerado=pago+pendente é verificada no resultado.
- Suporte marca ambos ocupados e o laço testa a ocupação novamente, evitando reutilização indevida da lista de livres do legado. Falta teste de integração específico para suporte, especialmente ajuda seguida de tentativa de atribuição no mesmo período.
- Faltam testes para detecção oculta durante tarefa e após seu término, esforço fracionário, vários recursos, repetição com horizonte inicial duplicado e igualdade de estado/resultado, e cenários sem possibilidade de progresso que devem censurar.
- Leis de confiança têm limites e opção constante, mas teste atual exercita atualização direta, não eventos de ajuda/recusa num projeto. Atribuir uma recusa ao solicitante e atualizar ambos no sucesso são decisões do modelo a declarar; não são inferências empíricas.
- `04_gemeo_identico.py` agora distingue a observação sintética fixa da média exata e não universaliza a direção do efeito; revisão textual adequada.
- Verificador exige caminho vivo, valida snapshot e vivo contra hash fixo; não escreve nos documentos. Testes negativos de snapshot adulterado/ausente ainda não existem, embora os ramos sejam explícitos.

## Parecer

Nenhum bloqueio de capacidade/precedência encontrado para execução nominal com esforço de reparo positivo. Execução exploratória pode prosseguir com controle neutro, censura explícita e sem interpretar métricas de esforço censuradas como realizadas. Não apresentar C4 versus legado como efeito isolado sem esses controles. Os testes pequenos não estabelecem robustez do domínio contínuo nem identificabilidade.

## Rechecagem após correções

A equipe corrigiu os dois bugs do núcleo: TW e períodos de execução são agora incrementados por período efetivamente trabalhado, somente em tarefas originais; dívida oculta só é enfileirada quando o esforço é positivo acima da tolerância. Li as alterações e executei novamente `python3 research/test_mvp.py`: **9 testes passaram**, incluindo os dois contraexemplos. Os primeiros dois achados estão resolvidos para os casos reproduzidos. Não vejo impedimento técnico para iniciar a execução ampliada autorizada. Controle de motor e retificação do registro de reconciliação continuam acompanhados pelos respectivos responsáveis.
