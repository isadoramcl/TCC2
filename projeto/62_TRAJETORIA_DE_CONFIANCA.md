# E2 — trajetória de confiança no nominal

384 execuções completas, 16 instâncias ×12 sementes ×2 braços. Código e
parâmetros históricos preservados, hashes conferidos ao término. Trajetórias
por período e por execução publicadas em `outputs/diagnosticos/noturno_nominal/`.

| Braço | Execuções | Cruzam média ≥0,95 | Nunca cruzam | Primeiro cruzamento, mediana [mín;máx] | Média final |
|---|---:|---:|---:|---|---:|
| Adaptativa | 192 | 161 (83,85%) | 31 | 9 [1;62] períodos | 0,936396 |
| Centralizada | 192 | 0 | 192 | não observado | 0,250000 |

A mediana é condicional às que cruzam. t começa em zero, conforme o simulador.
A média temporal por execução é 0,943519 no adaptativo e 0,250000 no centralizado.
Cruzar uma vez não equivale a permanecer saturado: média final adaptativa abaixo
de 0,95. O dado **não sustenta** chamar confiança de mera condição inicial em
ambos os braços. No centralizado ela fica congelada pelo portão; no adaptativo
há dinâmica, cruzamentos e quedas. Não se transformou a interpretação esperada
na ordem em alvo. Ver cruzamentos individuais e trajetórias completas.

Três controles de identidade executados após o item; modelo não alterado.
