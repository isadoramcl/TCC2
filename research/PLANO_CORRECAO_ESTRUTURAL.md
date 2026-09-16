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

### Etapa 4 — lei, eventos e reset (implementação alternativa)

- Eq. (4) conferida no PDF local de Crowder et al. (2012), p. 1431,
  DOI 10.1109/TSMCA.2012.2199304. Estado original dos agentes em escala 0–5.
  Com C normalizada: dC_original=clip((15+3*(5*Cp-5*Cr))/100,0,0.30).
  Competência recebe dC_original/5; confiança normalizada recebe tau*dC_original
  no sucesso ou -0.01 no insucesso. Não dividir o multiplicador dC novamente.
- Removidas as leis media_eventos e saldo_eventos do código ativo; preservadas
  no commit efd81b7. Constante permanece como controle.
- N_req conta destinatários efetivamente acionados; N_fail conta destinatários
  acionados mas ocupados; N_blocked conta tentativas barradas pelo limiar.
  N_success fecha N_req=N_success+N_fail. Somente o respondente recebe a
  atualização correspondente; bloqueio e ausência de candidato não alteram tau.
- [DEC] Mantida uma pessoa contatada por tentativa (política do modelo anterior),
  não o broadcast de Crowder: melhor elegível disponível; se todos ocupados,
  contato com o melhor elegível ocupado, registrado como insucesso. Portanto,
  adota-se a Eq. (4), sem alegar reprodução integral do protocolo do artigo.
  Atualização acontece no evento; pode afetar pedidos posteriores no período.
  TL continua uma unidade por sucesso; Eq. (3) não foi transplantada silenciosamente.
- [DEC] Reset C6 restaura competência inicial ao completar tarefa e ao trocar
  a tarefa-alvo durante aprendizado. Repetir pedido para a mesma tarefa conserva
  o aprendizado. Confiança não é reiniciada. Flag separada isola essa alteração.
- Sob Crowder, tau_portao/tau_rede representam condições iniciais separadas;
  ambas evoluem pelos mesmos eventos. Assim o fatorial não congela acidentalmente
  um canal. Sem override, ambos leem a mesma confiança individual.
- Alternativas registradas separadamente: protocolo, lei, reset e horizonte;
  nenhuma execução de resultados foi iniciada nesta etapa.
- Cinco testes de eventos/reset/canais passaram; suíte total 30 testes passou,
  incluindo compatibilidade neutra. Ainda é necessário verificar integração
  completa e resultados nas etapas seguintes antes de concluir o MVP.

Revisão independente da etapa 4 conferiu as equações no PDF e encontrou duas
fronteiras adicionais: reset no último período e override unilateral de portão
vazando para rede. Ambas receberam regressões reproduzidas antes da correção.
Reset agora ocorre na conclusão, inclusive para quem aprendeu sobre tarefa
executada por outro agente. Um override unilateral mantém o outro canal na
condição inicial do cenário e ambos evoluem por eventos. Teste no laço real
compara diagonais com execução nominal, contadores e reset final nos dois cenários.

### Etapa 5 — registro por oportunidade de decisão

`registros_tarefas` contém uma linha por tentativa sobre tarefa elegível com
recursos disponíveis, inclusive P1_fuga e P2 sem execução. Campos de risco e
duração efetiva ficam nulos quando a tarefa não é executada; não se confundem
probabilidades hipotéticas com falhas observadas. Registra E, margem E-tau_sat,
p_heu, q, Di, P, B, mu_cog, mu_rede, porta, p0, p_fail, excesso, duração-base,
duração analítica contrafactual, duração efetiva, agente/tarefa/período, seleção
P1 e sorteios efetivamente consumidos. Nenhum sorteio adicional.

A análise P(P1|D,P,B) terá como denominador essas oportunidades, não todos os
períodos de calendário nem somente tarefas executadas. A amostra condicionada
em P1 seleciona p_heu maior e amplifica a sensibilidade a rho por q; registrar
média q geral e condicional sem recalibrar a logística para uma taxa-alvo.
A opção de desligar instrumentação permite verificar identidade dos resultados
e do estado RNG. Os 64% anteriores permanecem quantidade a validar externamente.

### Etapa 6 — congelamento antes de reexecutar

B1/B3/B7/B9, tabelas modelo_/entrega_ e todo o lote mvp_20260915 estão
inventariados por SHA-256 em CONGELAMENTO_PRE_CORRECAO.json. Os CSV antigos
não foram alterados. Relatório 11 e documentos B9 receberam aviso explícito;
README retirou a alegação de MVP concluído. Nenhum número anterior será usado
como conclusão final sem reexecução. Etapa 5 verificada por 34 testes, inclusive
identidade com instrumentação desligada. Próximo passo: desenho declarado da
reexecução, sem escolher políticas ou valores pelo resultado.

### Etapa 7 — desenho registrado antes de executar

Pasta nova: outputs/diagnosticos/correcao_estrutural_20260916; não sobrescrever
mvp_20260915. Dez alternativas em sequência, 16 instâncias espaçadas fixas e
12 sementes em ambos os cenários (3.840 execuções). Robustez: família já
registrada de âncora, retrabalho, piso fuzzy, pesos, políticas, fator temporal,
controle constante e horizonte duplicado, cruzada com rho={0.20,0.35,0.50}.
Fatorial 2^5 mantém G,N,B,C,D separados, 16 instâncias e 12 sementes; legado
e corrigido são reexecutados. B9: três políticas de ablação nas mesmas chaves.
Sem ranking, minimização de função objetivo ou escolha de parâmetros.

B1/B3/B7 antigos continuam congelados; conclusões finais novas limitar-se-ão
aos experimentos reexecutados. Auditorias e calibração ficam após o MVP.
Instrumentação detalhada: amostra fixa das quatro primeiras instâncias do
desenho, quatro sementes, ambos os cenários, nominal corrigido; resumos
condicionais de seleção, sem comparar médias P1×P3 como evidência causal.


### Fechamento da reexecução

3.840 alternativas + 4.128 robustez + 6.144 canais corrigidos + 6.144 canais
legados + 1.152 B9 = 21.408 execuções principais. Mais 32 instrumentadas:
21.440 no total, sem incompletas/violações. Diagonais corrigidas384 e
legadas3072 conferem; três pares de horizonte rho conferem (32 cada).
Revisão independente verificou tabelas incrementais, denominadores e sinais.
O primeiro empacotamento do suplemento falhou por caminho relativo; a saída
parcial foi preservada em /private/tmp, caminho corrigido e reprodução integral
fora do repositório produziu CSV idênticos. Não houve mudança de simulação.
Relatório19 registra inversão de E_total e limites; relatório11 permanece congelado.
Próxima prioridade: V_obs/V_mod e ponte de observação, sem novas ondas HM.
