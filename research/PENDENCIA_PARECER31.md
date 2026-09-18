# Parecer 31 — pendência subordinada a E-1 e T4

## Ordem explícita da autora

Nenhum dos itens abaixo deve ser implementado antes de E-1 (rota de fuga morta)
e T4. V_obs/V_mod externo continua pausado.

1. Campo puramente derivado `retrabalho_sobre_esforco_total = TR/(E_plano+TR)`,
   propagado aos runners, com controle ANTES/DEPOIS de RNG, decisões e estados.
2. Cobertura repetida do procedimento HM: B=500 (1000 se viável), novas
   pseudo-observações em cada réplica e resposta independente no vetor verdadeiro;
   quatro I_j, I_max, indicador I_max>3, falsa exclusão empírica e percentil95.
   Não ajustar V_mod nem selecionar z favorável. Se percentil95>3, reportar como
   corte conjunto empírico específico do desenho, distinguindo regra marginal.
3. Declarar estimando sintético e manter geração/estimação na mesma unidade
   amostral; renomear gêmeo para verificação interna do procedimento. Não inferir
   V_obs externo a partir da variabilidade do próprio simulador.

## Verificação de pré-requisitos — somente leitura

Após fetch, origin/main=ee76fb681220beab32264404b965bcea481e32a8. Parecer31 e especificação de T4 não encontrados
em projeto/, nas branches disponíveis, em /Users/isadoracarvalho/TCC2 nem em
/Users/isadoracarvalho/Documents/00 - Semestre Atual/TCC (documentos md/txt).
Foi solicitado à autora o caminho ou commit dos pareceres E-1/T4/31.
Não se alega que E-1/T4 foram resolvidos.

Configuração carregada pelo simulador: omega=0.5, limite=0.6,
condição omega>limite=False. Ambos são constantes neste caminho do laço.
Código: simulador_mvp.py, ramo `if heu and omega>limite`.
A ordem antiga projeto/02_ORDEM_DE_SERVICO.md já menciona esse ramo como C5.

Contagens conferidas diretamente nos CSV históricos:

| Lote | Execuções | Soma p1_fuga | Máximo p1_fuga |
|---|---:|---:|---:|
| alternativas | 3840 | 0 | 0 |
| robustez | 4128 | 0 | 0 |

Nenhuma alteração de dinâmica, parâmetro, readout ou procedimento HM foi feita
nesta verificação. Próximo passo: obter a especificação estrutural faltante,
resolver/verificar E-1 e T4, então executar os três itens nesta ordem autorizada.
Não corrigir a rota de fuga apenas mudando o limiar para obter eventos esperados.

## Atualização — documentos recuperados em 17/09/2026

O parecer 31 e a especificação T4 foram recuperados do pacote local e publicados
com os pareceres 27–37. A ausência descrita acima é registro da busca anterior,
não o estado atual. A ordem 37 substitui a 32 e exige C3 primeiro. Esse controle
falhou; ver [relatório 38](../projeto/38_CONTROLE_C3_BLOQUEADO.md). E-1/T4 e os
itens deste registro continuam pendentes, agora pelo controle científico.
