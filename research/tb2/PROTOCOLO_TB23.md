# T-B2.3 — confiança inicial e incompletude (antes das execuções)

Especificação da autora: variar tau_inicial apenas na centralizada, sem escolher
valor substituto do nominal. Nenhum avanço ao bloco C.

## Desenho fixo

- População: as mesmas 36 execuções incompletas da grade B2 original (18 por
  canal ativo/desligado), mesmas instâncias e sementes. Seleção explícita por
  incompletude histórica, não amostra nova nem estimativa para toda a grade.
- Malha principal declarada: [0.25, 0.59, 0.60, 0.600001, 0.61, 0.65, 0.80, 1.00].
  Inclui nominal, vizinho inferior, igualdade estrita e vizinho superior do
  limiar tau_min=0.60. Reportar todos; não fazer busca binária de melhor valor.
- Horizonte: 256×CPM, o da grade B2 original. T-B2.1 já testou 512×CPM no nominal.
  Não misturar alteração de horizonte com alteração de confiança.
- Principal: alterar só cenarios.centralizada.tau_inicial, nenhum override.
  Isso altera simultaneamente os estados iniciais do portão e da rede difusa.
- Controle de mecanismo adicional pré-declarado: tau_portao=[0.600001,0.80,1.00],
  mantendo tau_rede inicial=0.25 e tau_inicial do cenário=0.25. Usa overrides já
  existentes; a rede continua evoluindo pelos eventos Crowder, não congelada.
  Mede intervenção inicial no portão com todas suas consequências posteriores.
- Controle negativo de rede: tau_rede inicial=[0.80,1.00], tau_portao=0.25,
  cenário tau_inicial=0.25. Portão fechado; verifica se alterar só rede resolve.
- Todos os outros parâmetros, inclusive tau_min, reporte, detecção, canal direto,
  tau_sat, s_transicao e políticas, ficam exatamente como em cada linha B2.
- Total: 36×(8+3+2)=468 execuções. Quatro processos; salvar incrementalmente.

## Critérios e leitura

Contar conclusões, tarefas executadas, TL, N_req/N_success/N_fail/N_blocked,
hiato_colega_capaz_sem_confianca, hiato_encontrado e confiança final. Reportar
hiato em contagem e por oportunidade (denominador hiato_encontrado), pois
horizontes realizados diferem. Não dar zero a uma fração sem denominador.

Reportar primeiro valor testado com 36/36 completas e se todos os valores
superiores testados também concluem. Não afirmar limiar contínuo exato: é uma
malha finita. Caso não haja valor sem incompletas, registrar isso sem ajustar
malha/parâmetros. Causalidade do portão precisa do controle com rede inicial
preservada; desaparecimento na principal sozinho não separa os canais.

Controle: baseline principal tau=.25 reproduz os campos B2 arquivados (apenas
serialização CSV até 1e-12). Comparar controle portão nominal com principal em
um caso bit a bit, incluindo RNG, antes do lote. Testar que nenhuma configuração
altera tau_min, reporte/detecção ou outro cenário. Rodar identidade neutra depois.
Resultados antigos preservados; revisão explícita da leitura B2, conforme dados.
