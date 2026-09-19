# Relatório consolidado — lote noturno 19–20

**Lote não fechado.** Este documento distingue trabalho publicado de pendências.
Todas as saídas ficam no repositório permanente, em `outputs/diagnosticos/`.
Nenhum nominal histórico substituído; não houve ajuste de V_mod ou de parâmetros
contra as percentagens de Rieskamp. Publicação em origin/main por item.

## Executado e verificado

| Item | Controle/expectativa | Observado | Estado |
|---|---|---|---|
| T-B2.3 | testar portão como causa das 36 incompletas | 0/36 até tau=0,60; 36/36 em 0,600001 e acima; só portão 36/36, só rede 0/36 | executado, baseline e identidade passam |
| D2 | 500 pseudo-observações novas, previsão independente, V_mod fixo | 31/500 falsas exclusões: 6,2%, IC95 [4,2511%;8,6853%]; p95 Imax=3,116875; 0 incompletas/14.000 | verificação interna executada |
| D1 | campos anteriores intactos; novo indicador ~0,190/~0,224 | 64 controles ANTES/DEPOIS, resíduo zero; nominal 0,186605/0,221795 A/C | identidade exata; sem ajuste ao valor aproximado |
| D3 | mesma unidade de geração e estimação | média de blocos de duas instâncias fixas; 10 blocos obs, 4 previsão independentes; variâncias recalculadas | estimando e nome corrigidos |
| E2 | testar saturação, não assumir | 161/192 adaptativas cruzam 0,95, mediana t=9; 31 nunca cruzam; final=0,936396; centralizada 0/192 e final=0,25 | hipótese de mera condição inicial nos dois braços não sustentada |
| E3 | confrontar magnitudes com ordens 0,95/0,97 de outro modelo | por tarefa: mu_cog A/C=0,809597/0,752021; mu_rede=0,916757/0,727805 | distribuições publicadas; construtos não equivalentes |
| E1 | recalcular LOC offline, preservar complexidade | N=17.377; frequências LOC=0,06336/0,12050/0,17974/0,34005; verificações do script passam | reexecutado, Dpp e hashes declarados |

Não interpretar os intervalos acima como aprovação de validade externa. D2 não
informa V_obs externo; p95 é corte conjunto empírico deste desenho, enquanto 3
é regra marginal. E_total continua diagnóstico interno e não conclusão de
governança. T-B2.3 identifica causa na amostra selecionada, não prevalência
populacional. A leitura de incompletude como limitação da família foi retirada.

## Parcial ou não executado — não aprovado por omissão

| Item | O que falta | Motivo/retomada |
|---|---|---|
| C1 | implementar alternativa F_ancora=k×0,0128, seis pontos, mapa reverso e varredura sintética | não implementado nesta execução; há somente plano declarado; próximo item |
| C2 | Beta por agente, momentos e domínio, células inválidas e varredura | não implementado; aguarda execução após C1, sem confundir A-16 com igualdade dos momentos arredondados |
| A1 | alternativa dependente de estado e varredura de limite | não implementado; regra constante histórica continua, defeito A-14 permanece |
| C4 | fração realizada de tarefas P1 nas trajetórias contrafactuais | publicada apenas análise local esperada em estados nominais; não substitui reexecução dinâmica |
| F | N de base de commits, correção dos artefatos originais da bancada | bases não localizadas no clone nem na pasta TCC; não inventar N; numeração e errata de rótulos já feitas |

No C4 local, razões alto/baixo P=1,277–1,922 no adaptativo e 1,227–1,564 no
centralizado. Unidades diferentes das de Rieskamp; sem calibrar contra 2,3×.

## Evidência, falhas operacionais e continuidade

- T-B2.3: `projeto/TB23_PORTAO_E_INCOMPLETUDE.md`, 468 execuções e controles.
- D1/D2/D3/E2/E3/E1/C4/F: relatórios `projeto/NOTURNO_*.md` e saídas respectivas.
- Snapshot ANTES de D1 preserva estados/RNG; snapshot D2 congela implementação.
- Identidade neutra repetida após cada item publicado; logs por item.
- Verificação final: 65 testes de `research/test_*.py` aprovados; dois testes
  adicionais do desenho D2 aprovados separadamente. Log `noturno_testes_finais.log`.
- D2 teve uma tentativa inicial que falhou por caminho relativo antes de simular;
  log/snapshot mantidos. Relatório TB23 inicialmente falhou por dependência de
  apresentação ausente, corrigida sem mudar dados. Validação de sintaxe foi
  feita em memória após o cache Python externo ser recusado pelo sandbox.
- Controle extra de override nominal TB23 ocorreu depois, não antes como previsto;
  quatro testes passaram. Fontes da varredura conferidas por hash no término.
- Arquivos históricos e tentativas anteriores preservados. Parecer 43 não alterado.

Próxima sessão deve iniciar em C1, continuar C2/A1 e completar C4/F. A existência
deste relatório e o push não significam que os doze itens foram concluídos.
