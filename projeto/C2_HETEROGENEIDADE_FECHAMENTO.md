# C2 — heterogeneidade Beta implementada e comparada

Nova ordem de fechamento: controle aproximado, sem exigência de igualdade na
terceira casa. O ensaio anterior estrito e sua reprovação permanecem arquivados.
A fórmula e os parâmetros operacionais de C3 não foram alterados para passar.

## Controle numérico e estatuto da aproximação

mu=0,0163/CV=1,13 literais dão **alpha=0,754081392435** e
**beta=45,508580720130**. Impressos:0,7546/45,4563. Diferenças relativas:
−0,068726%/+0,115013%. Não afirmar igualdade na terceira casa ou que a fórmula
produz45,46 exatamente. A reconstrução independente dos momentos confirma a
fórmula; os impressos dão mu=0,016329480707/CV=1,129581318086, ambos dentro dos
intervalos de arredondamento de0,0163/1,13. Esse é o contrato aproximado declarado
antes da rodada, não um ajuste aos parâmetros. Ver `controle_aproximado.csv`.

## Implementação e desenho

`heterogeneidade_erro='nenhuma'` é default, bit a bit com efd1248.
`beta_cv113`: quatro taxas fixas por agente, uma por nível ordinal, com média
F_base(nível) da alternativa histórica ou C1. [DEC] Independência entre níveis
é hipótese, não medição. Não redesenhar por tarefa. p0 soma essa taxa basal ao
canal cognitivo existente; demais decisões/reporte/portas permanecem.

RNG auxiliar derivado de SeedSequence([semente,20260919,2]), independente do
fluxo da dinâmica. A opção nenhuma não consome sorteio extra. Todos os níveis
são validados antes de inicializar agentes ou RNG. O nominal histórico continua
com nenhuma e fuga constante0,60; os dois mapas C1 são alternativas, não eleitos.

Grade: sete bases ×duas opções ×quatro instâncias ×quatro sementes ×dois braços.
**448 células planejadas;352 executadas e completas;96 recusadas por domínio**.
Zero violações. Rejeição não é censura por horizonte nem observação com valor0.
Cada tentativa recusada tem motivo explícito em `bruto.csv`; os contrastes dela
são REJEITADA_DOMINIO, sem números inventados. Horizonte256×CPM.

## Domínio estrito e células incompatíveis

Beta própria exige0<mu<1/(1+1,13²)=**0,439193640476086**, estrito no extremo.
Nenhum clipping, redução de CV ou ajuste do risco para fazer a célula caber.
As seguintes combinações impedem a opção Beta das respectivas bases históricas:

| Base | Nível | F_base |
|---|---|---:|
| historica_0.15 | muito alta | 0.447750 |
| historica_0.2 | alta | 0.473400 |
| historica_0.2 | muito alta | 0.597000 |
| historica_0.25 | media | 0.483750 |
| historica_0.25 | alta | 0.591750 |
| historica_0.25 | muito alta | 0.746250 |

As bases históricas0,15/0,20/0,25 são recusadas na Beta; os dois mapas C1 e as
históricas0,05/0,10 são admissíveis. A opção nenhuma continua executável em todas.

## Momentos empíricos

20 médias admissíveis,200.000 agentes sintéticos por média, sementes fixadas
antes: maior erro relativo de média=0.3969% e de
CV=0.5946%, ambos abaixo do controle pré-declarado de3%.
Não repetir sementes até passar. Na amostra que de fato entrou nos experimentos
há24 agentes únicos por base/nível (mesmos sorteios reutilizados entre instâncias
e braços); os CV observados variam de0.6892 a1.6754.
Esses CV pequenos-amostrais são descritivos, não outro alvo a ajustar.
Taxas individuais preservadas em `taxas_agentes_unicas.csv`.

## Cinco indicadores com IC95, nas duas opções

Diferença adaptativa−centralizada. IC t sobre médias por instância (n=4),
16 pares por configuração admissível. Não generalizar essa grade pequena para
todo o espaço contínuo nem selecionar a base mais favorável.

| Base | Heterogeneidade | Indicador | Média A−C | IC95 | Estatuto |
|---|---|---|---:|---|---|
| curto | beta_cv113 | atraso_relativo | -0.840772 | [-1.409561; -0.271984] | COMPLETO |
| curto | beta_cv113 | taxa_omissao | -0.119792 | [-0.144820; -0.094764] | COMPLETO |
| curto | beta_cv113 | divida_latente_sobre_plano | -0.052740 | [-0.070445; -0.035035] | COMPLETO |
| curto | beta_cv113 | taxa_falha_efetiva | -0.094792 | [-0.133969; -0.055614] | COMPLETO |
| curto | beta_cv113 | fracao_porta1 | -0.166667 | [-0.263808; -0.069526] | COMPLETO |
| curto | nenhuma | atraso_relativo | -1.069970 | [-1.887648; -0.252293] | COMPLETO |
| curto | nenhuma | taxa_omissao | -0.132292 | [-0.182894; -0.081690] | COMPLETO |
| curto | nenhuma | divida_latente_sobre_plano | -0.061573 | [-0.099069; -0.024078] | COMPLETO |
| curto | nenhuma | taxa_falha_efetiva | -0.089583 | [-0.143310; -0.035856] | COMPLETO |
| curto | nenhuma | fracao_porta1 | -0.191667 | [-0.282735; -0.100598] | COMPLETO |
| historica_0.05 | beta_cv113 | atraso_relativo | -1.259394 | [-2.007897; -0.510890] | COMPLETO |
| historica_0.05 | beta_cv113 | taxa_omissao | -0.173958 | [-0.223684; -0.124233] | COMPLETO |
| historica_0.05 | beta_cv113 | divida_latente_sobre_plano | -0.069928 | [-0.108448; -0.031408] | COMPLETO |
| historica_0.05 | beta_cv113 | taxa_falha_efetiva | -0.100000 | [-0.187121; -0.012879] | COMPLETO |
| historica_0.05 | beta_cv113 | fracao_porta1 | -0.144792 | [-0.241080; -0.048503] | COMPLETO |
| historica_0.05 | nenhuma | atraso_relativo | -0.912373 | [-1.233897; -0.590849] | COMPLETO |
| historica_0.05 | nenhuma | taxa_omissao | -0.155208 | [-0.214355; -0.096062] | COMPLETO |
| historica_0.05 | nenhuma | divida_latente_sobre_plano | -0.064205 | [-0.088254; -0.040156] | COMPLETO |
| historica_0.05 | nenhuma | taxa_falha_efetiva | -0.061458 | [-0.119606; -0.003311] | COMPLETO |
| historica_0.05 | nenhuma | fracao_porta1 | -0.163542 | [-0.219897; -0.107186] | COMPLETO |
| historica_0.1 | beta_cv113 | atraso_relativo | -1.038215 | [-1.521528; -0.554903] | COMPLETO |
| historica_0.1 | beta_cv113 | taxa_omissao | -0.227083 | [-0.282687; -0.171480] | COMPLETO |
| historica_0.1 | beta_cv113 | divida_latente_sobre_plano | -0.078240 | [-0.085129; -0.071351] | COMPLETO |
| historica_0.1 | beta_cv113 | taxa_falha_efetiva | -0.072917 | [-0.144017; -0.001817] | COMPLETO |
| historica_0.1 | beta_cv113 | fracao_porta1 | -0.159375 | [-0.265232; -0.053518] | COMPLETO |
| historica_0.1 | nenhuma | atraso_relativo | -1.050750 | [-1.891816; -0.209684] | COMPLETO |
| historica_0.1 | nenhuma | taxa_omissao | -0.207292 | [-0.244552; -0.170031] | COMPLETO |
| historica_0.1 | nenhuma | divida_latente_sobre_plano | -0.067985 | [-0.089434; -0.046536] | COMPLETO |
| historica_0.1 | nenhuma | taxa_falha_efetiva | -0.047917 | [-0.114107; +0.018274] | COMPLETO |
| historica_0.1 | nenhuma | fracao_porta1 | -0.108333 | [-0.117710; -0.098957] | COMPLETO |
| historica_0.15 | beta_cv113 | atraso_relativo | NA | NA | REJEITADA_DOMINIO |
| historica_0.15 | beta_cv113 | taxa_omissao | NA | NA | REJEITADA_DOMINIO |
| historica_0.15 | beta_cv113 | divida_latente_sobre_plano | NA | NA | REJEITADA_DOMINIO |
| historica_0.15 | beta_cv113 | taxa_falha_efetiva | NA | NA | REJEITADA_DOMINIO |
| historica_0.15 | beta_cv113 | fracao_porta1 | NA | NA | REJEITADA_DOMINIO |
| historica_0.15 | nenhuma | atraso_relativo | -1.005448 | [-1.550835; -0.460061] | COMPLETO |
| historica_0.15 | nenhuma | taxa_omissao | -0.246875 | [-0.329219; -0.164531] | COMPLETO |
| historica_0.15 | nenhuma | divida_latente_sobre_plano | -0.075544 | [-0.120198; -0.030890] | COMPLETO |
| historica_0.15 | nenhuma | taxa_falha_efetiva | -0.012500 | [-0.130235; +0.105235] | COMPLETO |
| historica_0.15 | nenhuma | fracao_porta1 | -0.137500 | [-0.299633; +0.024633] | COMPLETO |
| historica_0.2 | beta_cv113 | atraso_relativo | NA | NA | REJEITADA_DOMINIO |
| historica_0.2 | beta_cv113 | taxa_omissao | NA | NA | REJEITADA_DOMINIO |
| historica_0.2 | beta_cv113 | divida_latente_sobre_plano | NA | NA | REJEITADA_DOMINIO |
| historica_0.2 | beta_cv113 | taxa_falha_efetiva | NA | NA | REJEITADA_DOMINIO |
| historica_0.2 | beta_cv113 | fracao_porta1 | NA | NA | REJEITADA_DOMINIO |
| historica_0.2 | nenhuma | atraso_relativo | -1.036765 | [-1.348284; -0.725246] | COMPLETO |
| historica_0.2 | nenhuma | taxa_omissao | -0.297917 | [-0.347679; -0.248154] | COMPLETO |
| historica_0.2 | nenhuma | divida_latente_sobre_plano | -0.088918 | [-0.112441; -0.065394] | COMPLETO |
| historica_0.2 | nenhuma | taxa_falha_efetiva | -0.016667 | [-0.082746; +0.049413] | COMPLETO |
| historica_0.2 | nenhuma | fracao_porta1 | -0.093750 | [-0.216302; +0.028802] | COMPLETO |
| historica_0.25 | beta_cv113 | atraso_relativo | NA | NA | REJEITADA_DOMINIO |
| historica_0.25 | beta_cv113 | taxa_omissao | NA | NA | REJEITADA_DOMINIO |
| historica_0.25 | beta_cv113 | divida_latente_sobre_plano | NA | NA | REJEITADA_DOMINIO |
| historica_0.25 | beta_cv113 | taxa_falha_efetiva | NA | NA | REJEITADA_DOMINIO |
| historica_0.25 | beta_cv113 | fracao_porta1 | NA | NA | REJEITADA_DOMINIO |
| historica_0.25 | nenhuma | atraso_relativo | -1.015427 | [-1.687959; -0.342896] | COMPLETO |
| historica_0.25 | nenhuma | taxa_omissao | -0.348958 | [-0.444942; -0.252974] | COMPLETO |
| historica_0.25 | nenhuma | divida_latente_sobre_plano | -0.109107 | [-0.152760; -0.065455] | COMPLETO |
| historica_0.25 | nenhuma | taxa_falha_efetiva | -0.025000 | [-0.073419; +0.023419] | COMPLETO |
| historica_0.25 | nenhuma | fracao_porta1 | -0.050000 | [-0.135594; +0.035594] | COMPLETO |
| longo | beta_cv113 | atraso_relativo | -0.984419 | [-1.679254; -0.289583] | COMPLETO |
| longo | beta_cv113 | taxa_omissao | -0.126042 | [-0.155877; -0.096206] | COMPLETO |
| longo | beta_cv113 | divida_latente_sobre_plano | -0.056237 | [-0.085183; -0.027291] | COMPLETO |
| longo | beta_cv113 | taxa_falha_efetiva | -0.069792 | [-0.116163; -0.023420] | COMPLETO |
| longo | beta_cv113 | fracao_porta1 | -0.173958 | [-0.276296; -0.071620] | COMPLETO |
| longo | nenhuma | atraso_relativo | -1.076609 | [-1.451730; -0.701488] | COMPLETO |
| longo | nenhuma | taxa_omissao | -0.132292 | [-0.177055; -0.087528] | COMPLETO |
| longo | nenhuma | divida_latente_sobre_plano | -0.059681 | [-0.099923; -0.019440] | COMPLETO |
| longo | nenhuma | taxa_falha_efetiva | -0.092708 | [-0.127106; -0.058311] | COMPLETO |
| longo | nenhuma | fracao_porta1 | -0.189583 | [-0.232380; -0.146786] | COMPLETO |

`efeito_beta_menos_nenhuma.csv` fornece ANTES/DEPOIS em cada braço e IC95 da
diferença de opção pareada, sem confundir efeito de heterogeneidade com A−C.
`completude.csv` e `dominio.csv` preservam todas as células planejadas.

## Verificação

Quatro testes de integração: p0 usa taxa sorteada fixa; nenhuma exata/default;
rejeição antes de RNG; mapas C1 admissíveis/opções inválidas. Controle contra
a implementação anterior efd1248:16 pares de execuções, campos/trajetórias,
estados de agentes/tarefas/eventos/reparos e RNG bit a bit. Suíte de identidade
legado/MVP também aprovada. Manifesto e hashes conferidos no término.

Reprodução: `python3 research/lote_noturno/c2_fechamento.py`; script recusa
sobrescrever brutos existentes. Protocolo: `PROTOCOLO_C2_FECHAMENTO.md`.
Saídas: `outputs/diagnosticos/C2_fechamento_20260919/`.
