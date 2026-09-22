# 76 — Auditoria independente do nominal v2

Data: 22/09/2026. Auditoria feita sobre uma cópia extraída de `origin/main`
(74f67bb), sem alterar `config/mvp.yaml`, `config/mvp_v1.yaml` ou executar
operações Git. Os artefatos produzidos por esta auditoria estão em
`outputs/diagnosticos/20260922_auditoria_v2/`.

## Veredictos

| Item | Veredicto | Evidência independente |
|---|---|---|
| 1. Mudança no código | **CONFIRMADO** | Revisão do diff contra 09710d7 e testes de construção: `rng_aux=None` quando as opções suaves estão desligadas; o fluxo principal continua em `self.rng`; drenagem permanece em `efeito_fuga='drena'`; o portão logístico de assistência é aplicado somente quando `politica_porta2='nominal'`. O fluxo auxiliar ainda é criado quando a opção logística é ligada junto a outra política, mas não é consumido pelo filtro logístico de assistência. |
| 2. Identidade v1 | **CONFIRMADO** | Reexecução independente de 384 células com `config/mvp_v1.yaml`: zero campos divergentes por `float.hex()`. `a1.py`, `sat_gov.py` e `crowder1.py` foram conferidos quanto à leitura da configuração congelada e aos controles de identidade; os artefatos de controle registram resíduos nulos (exceto `TR=1,42e-14` no CSV decimal do A1). |
| 3. Suíte | **CONFIRMADO** | `python -m unittest discover -s research -p 'test_*.py' -v`, com `GIT_DIR` somente para permitir os testes históricos que usam `git show`: **Ran 102 tests ... OK** (`suite2.log`). |
| 4. Nominal v2 do zero | **CONFIRMADO** | Reexecuções independentes: 384 nominais e 1.152 fora da amostra; zero divergências campo a campo por `float.hex()` contra `bruto_nominal.csv` e `bruto_fora_da_amostra.csv`. IC95 próprio, média das sementes por instância e t sobre instâncias: nominal atraso −0,942878 [−1,086353;−0,799404], omissão −0,201563 [−0,213702;−0,189423], dívida −0,069431 [−0,076063;−0,062799], falha efetiva −0,022917 [−0,034693;−0,011140], P1 −0,051128 [−0,069652;−0,032605]. Fora: −0,985950; −0,207378; −0,072682; −0,021267; −0,049884, todos com IC95 negativo. Os 50 estratos foram recalculados; 50/50 excluem zero. |
| 5. Validação v1 fora da amostra | **CONFIRMADO** | Reanálise própria dos dados brutos reproduziu a tabela: atraso −1,138673 [−1,208643;−1,068704], omissão −0,225289 [−0,233210;−0,217369], dívida −0,081554 [−0,086510;−0,076599], falha −0,037037 [−0,044635;−0,029439], P1 −0,096672 [−0,109217;−0,084128]. A perda de precisão descrita no §8 é de até `3e−14` em campos derivados e não altera nenhum número publicado nem os sinais/ICs. |
| 6. Varredura `s_portoes` | **CONFIRMADO** | Reagregação própria de `s=0,10` e `s=0,25`: em ambos os pontos os cinco contrastes são negativos e todas as 384 células estão completas. Os valores coincidem com os CSVs round-trip; ver `s_varredura_IC95_indep.csv`. |
| 7. Governança v2 | **CONFIRMADO** | Recalculo próprio a partir de `governanca/bruto.csv` usando somente o braço adaptativo e médias por instância: 1.215 pares na região de ordenação histórica. Falha efetiva favorece o adaptativo em 643/1.215 = **46,42%**, contra 75% na v1; os demais percentuais independentes são atraso 92,84%, dívida 90,62%, omissão 76,21% e P1 66,01%. As células positivas de falha estão espalhadas por muitos perfis, embora haja concentração descritiva em `tau_inicial_A=0,80`; isso não identifica mecanismo. Teste discriminante proposto: para as células positivas e seus pares nominais, reexecutar um fatorial pareado `portao_assistencia ∈ {limiar, logistico}` mantendo perfil, instância, semente e demais opções; decompor a mudança em pedidos, sucesso/bloqueio, P1, erro efetivo e bateria/confiança, com contrastes dentro da mesma célula. Não foi executado nesta auditoria. |
| 8. Sensibilidade à pressão | **CONFIRMADO** | O ponto `tau_sat=1, s_transicao=0,25` foi localizado e reagregado nos dois arquivos. Ambos têm 256 células completas. Na v1, P1 médio por braço/pressão: centralizada 0,3732 (P=0,3) e 0,8221 (P=1); adaptativa 0,2742 e 0,8068. Na v2: centralizada 0,2779 e 0,8036; adaptativa 0,2680 e 0,7943. A diferença é esperada pela mudança de portões; os CSVs foram reproduzidos, não tratados como equivalentes. |
| 9. Plausibilidade | **DIVERGENTE** | Confiança média final v2: adaptativa 0,953699, centralizada 0,605003; a hierarquia média é plausível, mas o mínimo centralizado observado foi **0,238389**, abaixo da inicial 0,25. A fuga aumenta com a pressão no ponto C4 (P=0,3→1), e não há término rápido ou explosão de adiamentos: todas as 384 células concluem, makespan v2 vai de 96 a 254 (adaptativa) e 141 a 469 (centralizada). A divergência é localizada no requisito “sempre entre 0,25 e adaptativa”; não foi corrigida. |

## Arquivos e comandos

- Reexecução e cálculos independentes: `outputs/diagnosticos/20260922_auditoria_v2/`.
- Suíte: `python -m unittest discover -s research -p 'test_*.py' -v`.
- Os CSVs foram lidos com `float_precision='round_trip'` em todas as comparações.
- Nenhum parâmetro foi ajustado e nenhum resultado foi escolhido por conveniência.

## Limite da auditoria

Não foi feita nova simulação para o teste discriminante causal do item 7; ele é
uma proposta de identificação para a causa da queda de 75% para 46,42%. A
auditoria confirma a divergência de robustez, não afirma seu mecanismo.
