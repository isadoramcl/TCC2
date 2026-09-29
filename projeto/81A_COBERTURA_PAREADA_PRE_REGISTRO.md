# 81A — Correção de desenho da cobertura, pré-registro complementar

28/09/2026. Registrado após as ondas do HM e antes de qualquer execução desta cobertura complementar. A cobertura inicialmente prevista ainda está em curso; nenhuma de suas taxas foi utilizada para esta decisão.

A revisão estática independente do runner 81 encontrou: o alvo e as propostas HM usam a mesma semente nas duas instâncias do bloco; a cobertura herdou sementes independentes por instância do desenho D2. Ambos estimam a média do conjunto fixo, mas têm covariâncias e distribuições de I diferentes. A taxa do segundo não deve ser atribuída ao primeiro.

Decisão: preservar integralmente a cobertura inicial como diagnóstico de desenho independente e acrescentar B=500 réplicas com sementes PAREADAS entre instâncias, iguais às do desenho HM em sua estrutura. Esta é a cobertura principal a confrontar com 5%. Não haverá escolha entre as duas taxas pela conveniência do resultado.

Sementes complementares: 20000000+14*b+j, com j=0..9 para observação, j=10..13 para predição; ambas as instâncias recebem a mesma semente em cada bloco. Réplicas, observação e predição são disjuntas; 7000 sementes distintas, 14000 execuções. Mantêm-se todas as escolhas da 81: parâmetros/verdade/faixas, opções v3, instâncias, observáveis, estimador por bloco, corte 3, V_mod=0, Wilson e p95. Nenhuma alteração do HM nem novas ondas. A adição eleva o total de simulações científicas deste lote de 20428 para 34428.

Validade: zero violações; igualdade hex dos coeficientes em toda execução; nenhum descarte de réplica ou ajuste posterior. Incompletas serão publicadas e limitam interpretação. Critério é validade, não atingir 5%. Testes de sementes devem detectar tanto sobreposição entre blocos quanto uso de sementes diferentes dentro de um bloco. Resultados antigos e ambas as coberturas novas serão publicados lado a lado com rótulo do desenho.

Proveniência: o runner original congelou código/configuração e verificará os hashes finais, mas não congelou dados PSPLIB. O complemento registrará e copiará os dois CSVs de entrada, conferindo hashes antes/depois; a igualdade com os hashes históricos do manifesto 78 será explicitamente verificada. A cópia posterior não será apresentada como captura anterior ao primeiro lote.
