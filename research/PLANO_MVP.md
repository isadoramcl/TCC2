# MVP — plano e registro de execução, 15/09/2026

A instrução da autora nesta rodada é a especificação: fechar software e robustez;
calibração e fragilidades depois, juntas. Não otimizar políticas nem parâmetros.
Implementação em branch isolada; nunca editar o checkout da autora.

## Arquitetura e entregas

1. Instrumentação: preservar três documentos (feito, manifesto em preservacao_rodada2),
   commit da auditoria (7fd2e48 antes do rebase), rebase sobre dc8721f (feito).
   Reconciliar por comparação integral. Verificador do DOCX exige caminho vivo,
   confere snapshot E vivo contra hash fixado, sai com erro em divergência.
2. `src/modelo/simulador_mvp.py`: alternativa à classe legada, sem alterar seu
   comportamento. `SimulacaoMVP(..., opcoes: OpcoesMVP)` compartilha inicialização,
   fuzzy e resultado, mas tem laço explícito de atividades e retrabalho. Legado
   continua em `simulador.py`. Fila de reparo ocupa agente e demanda original;
   reparo só inicia após término original e tem prioridade FIFO entre elegíveis.
   Conserto não gera conserto recursivo (premissa [DEC]); dívida é removida da
   conta oculta quando detectada, esforço pago somente por trabalho realizado.
   Retrabalho não apaga contagem histórica de omissões nem S_PV histórico.
3. C4: fator de duração da omissão declarado 0,75, família {0,5; 0,75; 1};
   mesma produtividade, risco e severidade, sem compensação calibrada. C3:
   constante, aprendizado por ajuda (EMA de sucesso/recusa), saldo de eventos
   (incremento limitado por ajuda e decréscimo por recusa). Taxas em YAML,
   valores candidatos, nenhuma escolha após olhar resultados. Recusa só quando
   existe colega elegível fisicamente, para não confundir ocupação com confiança.
4. Horizonte: continuação do MESMO estado/RNG ao cruzar horizonte inicial,
   até estado terminal absorvente (tarefas, dívida, fila e agentes concluídos).
   Limite de segurança explícito produz resultado censurado e pendências, nunca
   sucesso. Comparar duplicação do horizonte inicial; estabilidade é término,
   não curva média temporariamente plana. Detectar recursos inviáveis cedo.
5. `src/modelo/20_experimento_mvp.py`: etapas alternativas, robustez, canais;
   saídas novas, manifestos de entradas e configuração. Di recalculado para
   quatro pesos já declarados no YAML, quartis globais pelo mesmo procedimento
   legado. Manter controle 1/3 exato para ANTES; registrar pequeno arredondamento
   YAML 0,3333/0,3333/0,3334 separadamente.
6. Antes/depois: mesmas 16 instâncias e 12 sementes do experimento nominal,
   todas as métricas numéricas disponíveis; resultados antigos preservados.
   Modelos legado, C4, C4+C1, duas leis C3. Sem selecionar pelo desempenho.
7. Robustez: desenho declarado pequeno sobre 8 vértices de F_ancora [0,05;0,25],
   f_retrabalho [0,30;0,80], mu_min [0,40;0,70], mais centro; 4 esquemas Di;
   4 instâncias equiespaçadas e 4 sementes, 2 cenários. Complementos no centro:
   família Porta 2 {nominal, sem_assistencia, assistencia_universal,
   sem_filtro_competencia}, duas leis τ, fatores C4; sem otimização. Reportar
   contrastes por célula, sinais, intervalos por instância e censura, não garantia
   em todo espaço contínuo. Bateria, risco e confiança são mantidos declarados;
   seus valores não explorados são limitação do domínio.
8. Canais: 2^5 com portão G, rede N, tau_min B, reporte C, detecção D; mesmos
   níveis nominais; 16 instâncias/12 sementes. Controles G=N reproduzem 2^4.
   Modelo saturado por instância; 31 termos; agrupar termos com G, N, ambos,
   nenhum. Rede não é μ_cognitivo: o canal cognitivo direto segue fadiga/pressão.
   Comparar percentuais publicados do fatorial com marginais diagonais e
   decomposição expandida. Corrigir B9, sem universalizar piloto 2×2.

## Verificação e decisões

- Testes antes do código: redução de duração, fila usa recurso e agente sem
  sobreposição, conservação gerado=pago+pendente, horizonte censurado não conclui,
  confiança limitada/constante e mudança por eventos, ajuda não usa agente ocupado.
- Testar hash vivo igual/diferente/ausente. Reexecutar testes de auditoria.
- Preservar todos os números publicados como históricos; tabelas novas incluem
  ANTES/DEPOIS. Não regenerar documento oficial.
- Revisão independente do diff antes de publicar branch. Não mergear main.
- Após MVP: V_obs/V_mod, perfil de implausibilidade, fragilidades. Nenhuma nova
  onda HM ou troca de método nesta entrega.

## Estado

- Preservação e rebase concluídos. Plano registrado antes de simulações do MVP.
