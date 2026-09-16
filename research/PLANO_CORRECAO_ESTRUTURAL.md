# Correção estrutural após pareceres 12–18 — sequência obrigatória

Instrução da autora prevalece: passos 1–7 na ordem, sem nova onda HM,
sem ajustar p_heu ou risco para atingir retrabalho desejado. Baseline efd81b7
permanece preservado no Git. Main remoto ainda dc8721f no fetch desta execução;
pareceres incorporados de revisao-auditoria bcf39db (somente documentos).

1. Compatibilidade no próprio laço MVP: opções neutras; comparar todos os campos
   legados do Resultado, trajetórias, contadores, estado RNG e estados finais.
   Novos campos de diagnóstico separados. Teste proíbe delegação executar ao legado.
   Corrigir diferenças por causa, registrando cada uma antes do próximo passo.
2. Qualidade C4: rho no YAML com fonte e faixa instruídas; manter p0, q e forma
   multiplicativa no complemento; rho=0 usa p0 exato, sem cancelamento numérico.
3. Contrafactual mesma tarefa/estado/sorteios, P1 forçada/P3 forçada; controle
   negativo fator1/rho0 não deve detectar efeito. Sem comparar médias selecionadas.
4. Ler Eq4 de Crowder no PDF; substituir leis experimentais por Crowder,
   reset de competência por subtarefa; responder distingue pedido/insucesso/bloqueio.
   Nenhum bloqueio pré-pedido diminui confiança, nenhum solicitante recebe crédito.
5. Instrumentar tentativas e execuções por tarefa: E, margem, p_heu,q,Di,P,B,mu,
   porta,p0,p_fail,excesso,durações e sorteios; observar seleção sem alterar p_heu.
6. Congelar B1/B3/B7/B9 e relatório11 como pré-correção. Não apagar dados antigos.
7. Só após testes anteriores: reexecutar etapas isoladas, experimento, robustez
   incluindo rho{.20,.35,.50}, canais e publicar ANTES/DEPOIS com resultados novos.
   Valores antes servem somente como controles históricos, não conclusão final.

## Registro de execução

- Pareceres12–17 lidos; §9 de12 retira comparação direta custo/esforço.
- Etapa1 iniciada: teste de compatibilidade antes de modificar o laço.
- Etapa1 concluída: antes, 30/32 pares divergiam; depois, 32/32 coincidem nos
  campos legados, trajetórias, RNG, agentes e tarefas, sem delegar executar.
  Causas corrigidas: reserva extra do solicitante, liberação do ajudante no fim
  do período, estado_final de reporte; no modo sem fila, pré-contagem de TW e
  dívida zero seguem o legado. Com C1, TW continua realizado e término completo.
  Os nove testes anteriores de conservação/censura também passam.
- Etapa2: risco adicional no complemento implementado conforme fórmula pedida;
  rho aberto0,35/faixa0,20–0,50 em parametros.yaml, sem consumo extra do RNG.
  Dois testes de forma/extremos passaram; compatibilidade rho0 manteve32/32.
- Etapa3: contrafactual real P1/P3 forçadas no mesmo estado e mesmos sorteios
  controlados. Detecta menor duração/maior risco e falha realizada diferencial.
  Controle negativo fator1/rho0 não detecta diferença e não produz falha.
  Testes passaram e compatibilidade32/32 permanece. Não se usaram médias P1×P3.

### Reabertura do controle após revisão independente — 16/09/2026

A revisão repetida encontrou um limite omitido pelos 32 pares nominais:
com horizonte fixo 257 ou 300 × CPM, o MVP cortava em 256 × CPM.
O teto de segurança da extensão automática vazava para o modo fixo.
Novo teste reproduziu divergência nos horizontes 0, 257 e 300 antes da
correção; os controles 1 e 256 já coincidiam. A implementação agora usa
integralmente o horizonte legado quando a extensão automática está desligada.
O contrato também compara diretamente a fila `divida_pendente`.

Documento 18 lido: D-01 escreve “reset da confiança por subtarefa”. Isso
conflita com a instrução direta da autora e com o parágrafo após a Eq. (2)
de Crowder (p. 1431), que estabelece reset da **competência**. A etapa 4
seguirá competência; não reiniciará confiança a cada tarefa. O documento
original foi preservado. As fontes apenas catalogadas em 18 não passam a
ser consideradas verificadas por esta leitura do catálogo.

Verificação após correção do horizonte: 25 testes passaram (incluindo 32 pares
nominais e cinco horizontes de fronteira); `git diff --check` sem erros.
