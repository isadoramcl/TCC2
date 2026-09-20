# D1 — readout de retrabalho sem mudança dinâmica

Adicionado `retrabalho_sobre_esforco_total=TR/(E_plano+TR)` ao Resultado comum
e às linhas exportadas pelos runners; runners que serializam Resultado herdam
o campo. Não entrou no vetor de HM. Os indicadores históricos permanecem.

Controle ANTES/DEPOIS: **64 execuções** (legado e MVP, quatro instâncias, quatro
sementes, dois braços), todos os campos preexistentes, estados e RNG idênticos
por float.hex; resíduo máximo **zero**. Snapshot anterior arquivado e comparador
reexecutável em `research/lote_noturno/readout.py`. Três testes gerais de
compatibilidade também aprovados. Nenhuma decisão, sorteio ou estado alterado.

No nominal de 384 execuções completas (16 instâncias ×12 sementes ×2 braços):

| Braço | Esperado aproximado pela ordem | Observado |
|---|---:|---:|
| Adaptativa | 0,190 | 0,186605 |
| Centralizada | 0,224 | 0,221795 |

A aproximação numérica não foi usada como alvo: amostra declarada e taxas por
execução, depois média. `nominal_384.csv` publica numerador e denominador.
O readout não contém TL; E_plano é esforço nominal, não prazo observado externo.
A admissibilidade externa ainda exige compatibilidade da fronteira/contagem.

Saídas: `outputs/diagnosticos/noturno_D1/`. A rodada nominal que fornece os
componentes foi executada antes da edição do readout; o campo foi derivado dos
componentes, coerente com a prova de ausência de alteração dinâmica.
