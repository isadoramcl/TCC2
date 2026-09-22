# Teste aleatório do nominal v2 — critério escrito antes da execução (22/09/2026)

Amostra: 24 instâncias do PSPLIB J60 sorteadas ao acaso entre as 416 nunca
usadas (fora das 16 do nominal e das 48 da validação fora da amostra), com semente
de sorteio gerada pelo relógio e registrada. Sementes de simulação 100 a 111 —
nunca usadas antes. Configuração: `config/mvp.yaml` sem alteração.

Passa se:
1. todas as execuções terminam, com zero violações;
2. os cinco contrastes (adaptativo − centralizado) têm média negativa;
3. atraso, omissão e dívida latente têm IC95 excluindo zero (os três robustos na
   varredura de governança). Falha efetiva e fração Porta 1 são só reportadas.
