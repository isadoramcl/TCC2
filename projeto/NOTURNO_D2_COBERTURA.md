# D2 — verificação interna repetida do procedimento

500 réplicas, 14.000 execuções completas, 14.000 sementes distintas.
31/500 falsas exclusões do vetor verdadeiro com I_max>3: **6,2%**, IC95
binomial exato Clopper–Pearson **[4,2511%; 8,6853%]**.
Percentil 95 empírico de I_max: **3,1168746532** (interpolação linear).

O corte 3 é regra marginal, não promessa de cobertura conjunta de quatro
observáveis com variâncias estimadas. Neste desenho, 3,1169 é corte conjunto
empiricamente justificado para 95% de retenção na amostra de verificação; não
é garantia populacional, universal ou seleção de V_mod. O IC inclui 5% de
falsa exclusão: não há aqui evidência precisa de afastamento da meta de 95%.
Não alterar o corte histórico retrospectivamente nem rodar ondas de HM.
V_mod=0 em todas as réplicas. Nenhuma pseudo-observação escolhida por resultado.

## Estimando sintético

Média esperada dos quatro observáveis em duas instâncias FIXAS com peso igual,
sobre a aleatoriedade dos agentes, no vetor verdadeiro e cenário adaptativo do
simulador histórico. Unidade amostral: bloco de duas execuções, uma por instância,
com sementes independentes. z usa 10 blocos; resposta estimada usa 4 novos blocos.
V_obs=var(médias dos 10 blocos, ddof=1)/10; V_sim idem /4. Instâncias não são
réplicas intercambiáveis. Nenhuma inferência sobre V_obs externo ou validade do
MVP corrigido. E_total integra apenas este vetor histórico interno com convenção
fixa; continua excluído do vetor de calibração externa.

Protocolo prévio: `research/lote_noturno/PROTOCOLO_D2_D3.md`.
Execução: `python3 research/lote_noturno/cobertura.py --saida <diretorio-novo>`.
Saída completa: `outputs/diagnosticos/noturno_D2_execucao/`.
Snapshot de código/configuração, sementes, quatro I_j por réplica, I_max,
variâncias e observações preservados. Variâncias recalculadas independentemente
dos brutos, hashes verificados, três testes de identidade e dois de desenho.
A primeira tentativa falhou no tratamento de caminho antes de simular; log e
snapshot preservados em `outputs/diagnosticos/noturno_D2/`, sem ocultar a tentativa.

Estado: diagnóstico interno executado. HM externo permanece sem autorização
científica: este ensaio não resolve o contrato observacional. Lote não fechado.
