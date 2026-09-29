# 81 — HM e cobertura interna da v3

## Pré-registro (antes de qualquer execução deste experimento)

Data UTC: 2026-09-28T19:15:13.670298+00:00. Autorização: instrução da autora após o parecer 80. Resultados pendentes neste registro inicial.

[DEC] Espaço 5D: F_ancora [0,05;0,25], f_retrabalho [0,30;0,80], tau_sat [0,70;1,40], **k_analitico [0,02;0,08]**, mu_minimo [0,40;0,70]. Em toda proposta e na verdade, k_heuristico=k_analitico por atribuição do mesmo float; controle por float.hex(). k_fuga permanece 0,10.

[DEC] Verdade: F_ancora=0,180; f_retrabalho=0,420; tau_sat=0,850; **k_analitico=0,065**; mu_minimo=0,620. O coeficiente 0,065 ocupa 75% da faixa nova, mesma posição relativa de (0,135−0,06)/(0,16−0,06)=75% no desenho antigo. Não está no centro 0,05, não é extremo e foi escolhido sem executar o novo desenho. Nenhuma faixa será adaptada para melhorar identificabilidade.

Núcleo: SimulacaoMVP com opções de config/mvp.yaml (v3), parâmetros e derivados atuais; instrumentação por tarefa desligada apenas para reduzir armazenamento. Cenário adaptativa. Duas instâncias fixas selecionadas pelo mesmo espaçamento do runner 04; 4 sementes por proposta, 10 para o alvo. Duas ondas de 400 pontos LHS, semente de desenho 20260905 em cada onda, como no histórico; a segunda usa a caixa envolvente dos pontos com I_max<=3 da primeira. Se não houver pontos aceitos, registrar NROY vazio e não inventar faixa para a segunda onda. Os identificadores concretos das instâncias serão congelados no manifesto antes de simular.

Estimando interno: média esperada dos quatro observáveis sobre o conjunto fixo das duas instâncias, variando a aleatoriedade dos agentes. Cada bloco é a média das duas instâncias; V_obs e V_sim são variâncias amostrais dessas médias divididas pelo número de blocos (10 e 4). O HM antigo usava variância de execuções agrupadas: esta diferença também impede comparação direta. Vetor interno preservado: taxa_omissao (proporção de tarefas), atraso_relativo (makespan/CPM sem recursos, adimensional), retrabalho_sobre_plano (TR/esforço planejado) e E_total (razão contábil interna, dependente da convenção TL). E_total NÃO é observável para calibração externa; atraso não é crescimento do prazo contratual. O experimento verifica o procedimento internamente, não estima V_obs externo.

Cobertura: B=500, em cada réplica 10 blocos de observação e 4 de predição independentes; duas instâncias por bloco. Sementes 10000000+28*b+offset+2*bloco+i, offset 0 para observação e 20 para predição. I_j=abs(z_j-f_j)/sqrt(V_obs,j+V_sim,j); V_mod=0, sem ajuste. Denominador zero: I=0 se diferença zero, infinito caso contrário. Reportar I_max>3, IC95 Wilson, distância do nominal 5%, p95 de I_max e contagens de censura. Corte 3 é marginal, não garantia conjunta de 95%. Nenhuma escolha posterior de pseudo-observação.

Critério de validade (não de beleza da tabela): zero violações em TODAS as execuções; igualdade bit a bit dos coeficientes em TODA proposta; preservar todas as saídas, incluindo resultados desfavoráveis. Execução incompleta será explicitamente registrada e impedirá interpretação irrestrita. Identificabilidade é descritiva, sem passou/reprovou; reportar amplitudes e contrações sem otimizar faixas. Nenhuma mudança de V_mod para fazer o verdadeiro passar.

Comparação: resultados v3 ao lado dos históricos, sem interpretar diferenças de espaço a priori, dinâmica e estimador de variância como melhoria. A retirada de k_heuristico é POR DERIVAÇÃO, não por falta de dados. outputs/ antigos não serão sobrescritos. HM/gêmeo 6420 execuções, cobertura 14000, total previsto 20420. Avaliação adicional do vetor verdadeiro com quatro sementes independentes: +8 (20428), registrada aqui antes da execução para testar I conjunto, além das projeções marginais.

Plano: escrever teste de derivação com controle negativo; implementar runner versionado e saídas exclusivas; testar; congelar código/configuração/desenho; executar alvo, ondas e cobertura; auditar os CSVs com código de análise independente; completar inventário nominal-v3/histórico/não executado por arquivo; publicar resultados sem Git.
