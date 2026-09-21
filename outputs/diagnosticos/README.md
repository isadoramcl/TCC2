# Índice dos diagnósticos

Cada diretório é **um experimento executado**, com as saídas brutas, os controles
e, quando aplicável, o `manifesto.json` que registra a configuração e o SHA-256
do código que o produziu.

> **Os nomes destes diretórios não são renomeados.** Vinte dos trinta e dois são
> lidos por caminho fixo em scripts que afirmam identidade bit a bit contra eles
> — `noturno_nominal` é lido por **oito** scripts. E o nome do diretório integra
> a cadeia de custódia entre o manifesto e a evidência: renomear um experimento
> depois de executado é reetiquetar a amostra. Este índice resolve a legibilidade
> sem tocar na evidência.

---

## Ordem cronológica

| diretório | data | o que é | execuções | arq. | MB |
|---|---|---|---:|---:|---:|
| `mvp_20260915` | 15/09 | Primeira execução completa do MVP | | 6 | 6,3 |
| `hm_20260915` | 15/09 | Diagnóstico do History Matching, ondas iniciais | | 8 | 0,04 |
| `revisao_20260915` | 15/09 | Saídas da primeira revisão independente | | 8 | 0,5 |
| `correcao_estrutural_20260916` | 16/09 | Correção estrutural do MVP e teste de tempo de aprendizado | | 9 | 10,3 |
| `arranjo_20260917` | 17/09 | Experimento de arranjo de governança, T1/T2/T3 | | 13 | 1,1 |
| `observaveis_20260917` | 17/09 | Verificação de independência de TL | | 3 | 0,002 |
| `teste_TL_20260917` | 17/09 | Teste discriminante da convenção de TL | | 9 | 0,2 |
| `lote37_C3_20260917` | 17/09 | Controle C3 de Stewart, primeira execução (reprovou) | | 5 | 0,005 |
| `lote37_C3_regra39_20260918` | 18/09 | C3 sob a regra do parecer 39 | | 3 | 0,004 |
| `lote37_C3_regra39_20260918_final` | 18/09 | C3, versão final daquela regra | | 3 | 0,004 |
| `lote41_C3_20260918` | 18/09 | C3 sob o critério discriminante do parecer 41 | | 4 | 0,5 |
| `lote41_T4_piloto_20260918` | 18/09 | T4 piloto — portão × rede | | 7 | 0,03 |
| `lote41_T4_20260918` | 18/09 | T4 completo, quatro células | | 7 | 0,5 |
| `lote41_B2_20260918` | 18/09 | B2, primeira tentativa (falha de runner) | | 2 | 0,001 |
| `lote41_B2_censura_20260918` | 18/09 | B2 com censura declarada — canal de erro direto desligado | | 9 | 0,3 |
| `lote41_verificacoes_20260918` | 18/09 | Verificações do lote | | 3 | 0,01 |
| `TB2_20260918` | 18/09 | Horizonte dobrado e seleção por conclusão | | 20 | 0,8 |
| `TB23_20260918` | 18/09 | Varredura de `tau_inicial` — o portão de assistência | | 10 | 0,2 |
| `noturno_nominal` | 19/09 | **Nominal de referência**, 384 execuções | 384 | 12 | 29,8 |
| `noturno_D1` | 19/09 | Readout de retrabalho, controle antes/depois | | 5 | 7,1 |
| `noturno_D2` | 19/09 | Cobertura repetida do History Matching | | 2 | 0,06 |
| `noturno_D2_execucao` | 19/09 | Execução da cobertura, B = 500 | | 9 | 1,7 |
| `noturno_E1` | 19/09 | Gradiente por linhas de código, dados NASA | | 7 | 0,01 |
| `A1_20260919` | 19/09 | Rota de fuga dependente de estado | 320 | 15 | 0,3 |
| `B2_rotulagem_20260919` | 19/09 | Rotulagem de rotas do B2 | | 10 | 0,09 |
| `C1_20260919` | 19/09 | Ancoragem linear de `F_ancora` em Stewart & Melchers | 96 | 15 | 0,03 |
| `C2_20260919` | 19/09 | Pré-controle do C2 — precisão dos momentos | | 7 | 0,003 |
| `C2_fechamento_20260919` | 19/09 | Heterogeneidade Beta entre agentes, CV = 1,13 | | 18 | 0,1 |
| `SAT_GOV_20260919` | 19/09 | **Saturação e 81 perfis de governança**, 2 592 execuções | 2 592 | 27 | 25,7 |
| `GOV2_CROWDER1_20260919` | 19/09 | Localização das inversões e escalares de aprendizagem | | 20 | 3,1 |
| `fechamento_20260919` | 19/09 | Fechamento das entregas obrigatórias | | 5 | 0,008 |
| `20260920_fora_da_amostra` | 20/09 | **Validação fora da amostra**, 48 instâncias novas | 1 536 | 11 | 1,2 |

---

## Os que não podem ser movidos nem renomeados

| diretório | lido por | o que quebra se mudar |
|---|---:|---|
| `noturno_nominal` | **8 scripts** | controles de identidade bit a bit de todo o lote noturno e da validação fora da amostra |
| `SAT_GOV_20260919` | 3 | análise das inversões e dos regimes de saturação |
| `GOV2_CROWDER1_20260919` | 3 | relatórios do T-GOV.2 e do T-CROWDER.1 |
| `arranjo_20260917` | 3 | geração do relatório de arranjo |
| `20260920_fora_da_amostra` | 3 | análise da validação fora da amostra |
| `teste_TL_20260917` | 2 | controle nominal em `26_testes_arranjo.py` |
| `A1_20260919`, `correcao_estrutural_20260916`, `hm_20260915` | 2 cada | relatórios e reanálises correspondentes |

O restante é lido por um script ou por nenhum, mas continua sendo evidência
datada com manifesto próprio.

---

## Convenção para diretórios novos

A partir de 20/09: `<AAAAMMDD>_<assunto>`. O `20260920_fora_da_amostra` é o
primeiro. Os anteriores ficam como estão, indexados aqui.
