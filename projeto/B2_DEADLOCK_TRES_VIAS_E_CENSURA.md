# B2 — bloqueio conjunto, duas saídas verificadas e censura na tabela final

## Localização exata

36/576 incompletas na grade: **centralizada E s_transicao=0,01 E tau_sat nos
níveis testados 1,0 ou 1,4**. Não há incompletas em s=0,25 ou 0,60, nem no
adaptativo. No nominal há 192/192 completas em cada braço por estado do canal
direto; 384 por canal e 768 considerando os dois estados. Não extrapolar a
afirmação para todo tau_sat≥1 contínuo, que não foi varrido.

## Mecanismo conjunto e validação cruzada

O bloqueio reúne três condições, com o seletor priorizando maior Di antes de
verificar competência:

1. Tarefa escolhida acima da maior competência disponível: no caso j6021_1,
   semente0, tarefa3, Di=0,689416916 > Cmax=0,626850718.
2. Assistência fechada: tau_inicial=0,25 não satisfaz tau>tau_min=0,60.
3. Seleção heurística praticamente inacessível no horizonte: p_heu máximo da
   **tarefa escolhida**=3,24749e-14 em tau_sat=1, s=0,01, bateria1, P=1.
   O valor 3,02786e-29 pertence à tarefa2 (Di=0,343328875), disponível mas não
   escolhida. Não juntar Di de uma tarefa com p_heu de outra.

T-B2.3 testa a saída por assistência: tau=0,60 dá 0/36 completas; tau=0,600001
completa36/36, assim como os níveis superiores. O controle só-portão confirma
36/36, enquanto só-rede dá0/36. A condição relevante é **tau_inicial>tau_min**.

A grade B2 testa a saída heurística: mesmas 36 chaves (instância, semente, braço,
canal e tau_sat), com apenas s mudado, dão **36/36 completas em s=0,25** e
**36/36 em s=0,60**, mantendo N_req=0 no centralizado. São 72 contrapartes
publicadas em `B2_rotulagem_20260919/validacao_cruzada_rotas.csv`.
Duas intervenções distintas validam conjuntamente o diagnóstico; o portão
fechado isoladamente NÃO basta, pois o nominal com ele fechado conclui.

A terceira saída, tornar a tarefa compatível ou mudar a seleção, é uma
consequência local das regras, mas não foi varrida nas 36 execuções. Não se
alega que uma terceira intervenção completa já tenha sido demonstrada.

## P1 — estatuto de s_transicao=0,01

**[LIMITACAO] Manter como teste de degeneração, não como evidência do regime
estocástico regular.** Nesse canto da grade, o caminho heurístico torna-se
praticamente inacessível e o modelo opera efetivamente no caminho analítico
(com tentativas de P2); com os outros dois bloqueios, entra em deadlock prático.
Não é globalmente "só Porta3": em tau_sat=0,7 há conclusões e a probabilidade
ainda depende de Di/P/B. Não elevar o extremo nem alterar nominal para ocultar
isso; rotular a região em cada leitura de robustez.

Precisão numérica: 3e-29 e 3e-14 são representáveis em float64. Não há subfluxo
aritmético a zero; é inacessibilidade probabilística na escala do horizonte.
No exemplo publicado, limite superior por união para ao menos uma seleção P1
em 6 agentes×19.456 períodos é 3,79e-9 (tarefa escolhida). Não é prova de
impossibilidade em tempo infinito. Chamar apenas "subfluxo" confundiria causa
numérica com limiar logístico quase determinístico.

## P2 — censura acompanha o valor até a tabela final

`research/lote41/b2.py` passa a exportar CSV e Markdown com `estatuto` e
`valor_rotulado`. Qualquer linha com censura recebe `CENSURADO: N execucoes;
nao terminal` junto à média; fração sem denominador recebe também
`INDEFINIDO/PARCIAL`. NaN continua NaN, nunca zero. Colunas numéricas originais
preservadas para auditoria, com estatuto adjacente; a tabela de apresentação usa
o valor rotulado. Não usar a média diagnóstica como desfecho terminal.

Novas tabelas canônicas de apresentação:
`outputs/diagnosticos/B2_rotulagem_20260919/contraste_A_menos_C_IC95.md` e CSV,
mais `celulas_IC95.md` e CSV. Os CSVs históricos permanecem congelados, já com
contagens de censura; não devem ser usados diretamente como tabela final.
Os contrastes condicionais de T-B2.2 continuam identificados como condicionais
à conclusão, com perda de pares e de potência; não corrigem seleção.

Testes: censura/indefinição preservadas, recusa de tabela sem contagem, números
inalterados; reanálise verifica todos os rótulos e as72 contrapartes. Identidade
neutra também verificada. A1 segue prioridade; C1/C2 vêm depois.

### Valores críticos com rótulo

| Canal | tau_sat | Indicador | Valor |
|---|---:|---|---|
| ativo | 1.0 | atraso_relativo | -112.291506 [CENSURADO: 7 execucoes; nao terminal] |
| ativo | 1.0 | fracao_porta1 | -0.161458 [CENSURADO: 7 execucoes; nao terminal; INDEFINIDO/PARCIAL: 4 sem denominador] |
| ativo | 1.4 | atraso_relativo | -174.504547 [CENSURADO: 11 execucoes; nao terminal] |
| ativo | 1.4 | fracao_porta1 | NA [CENSURADO: 11 execucoes; nao terminal; INDEFINIDO/PARCIAL: 8 sem denominador] |
| desligado | 1.0 | atraso_relativo | -112.355713 [CENSURADO: 7 execucoes; nao terminal] |
| desligado | 1.0 | fracao_porta1 | -0.158333 [CENSURADO: 7 execucoes; nao terminal; INDEFINIDO/PARCIAL: 4 sem denominador] |
| desligado | 1.4 | atraso_relativo | -174.610857 [CENSURADO: 11 execucoes; nao terminal] |
| desligado | 1.4 | fracao_porta1 | NA [CENSURADO: 11 execucoes; nao terminal; INDEFINIDO/PARCIAL: 8 sem denominador] |
