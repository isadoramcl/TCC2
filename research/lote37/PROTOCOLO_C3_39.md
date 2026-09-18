# C3 — reconciliação pelo parecer 39 (18/09/2026)

Antes da execução: aplicar a seção 5, mantendo as saídas anteriores intactas.
Origem canônica beta-binomial: alpha=0,7546 e beta=45,4563; intervalos de
arredondamento [0,75455;0,75465] e [45,45625;45,45635]. Binomial:
p∈[0,01625;0,01635]. P-dependente: mesmo p e phi∈[0,8445;0,8455].
Aprovação por inclusão do valor publicado no intervalo propagado. A célula BB8
é exceção explicitamente autorizada pelo parecer, registrada sem apagá-la.

Para binomial e beta-binomial, provar monotonicidade de cada massa no pequeno
retângulo por limites das derivadas logarítmicas, depois avaliar os extremos.
Para p-dependente, propagar limites não negativos pela recorrência (envoltória
conservadora, não intervalo estatístico nem necessariamente faixa atingível).
Para chi² propagar os intervalos dos quatro grupos por (O-E)^2/E; esses limites
são conservadores por ignorar dependência entre células. Não ajustar parâmetros.

Se outra célula falhar, registrar e não retomar B1. Passar um intervalo marginal
não prova que um único vetor de parâmetros reproduz simultaneamente a tabela.
Executar identidade bit a bit depois do item. A tolerância antiga fica disponível
explicitamente para reprodução histórica, mas não rege a decisão atual.
