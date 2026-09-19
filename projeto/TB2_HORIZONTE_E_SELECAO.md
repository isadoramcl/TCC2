# T-B2.1 e T-B2.2 — horizonte dobrado e seleção por conclusão

> Leitura causal atualizada por [T-B2.3](TB23_PORTAO_E_INCOMPLETUDE.md):
> abrir só o portão completa 36/36; a rede sozinha completa 0/36.
> As incompletas são desfecho de A-13 neste desenho, não limitação da família.


18/09/2026. Pedido executado antes de avançar ao bloco C. Código e resultados
anteriores publicados em `d54283b`; árvore movida de `/private/tmp` para
`TCC2/.worktrees/integracao-main-tl`, dentro do repositório permanente.

## Veredito

**0/36 execuções incompletas concluíram com o horizonte dobrado.**
Nenhuma executou tarefas adicionais: a contagem de tarefas permanece idêntica
em todas as 36. Os resultados são compatíveis com bloqueio estrutural das regras
de seleção/assistência neste desenho, não com truncamento resolvido dobrando
apenas o horizonte. Não se deduz impossibilidade matemática em horizonte infinito.

A incompletude está concentrada no braço centralizado e não deve ser tratada
como ausência ao acaso. Os contrastes da grade nas células afetadas foram
recalculados **condicionais à conclusão dos dois braços**, com redução da amostra
explícita. Não estimam o efeito incondicional da governança nessa região.

## T-B2.1 — desenho e resultados

Reexecutadas exatamente as 36 chaves incompletas do B2: mesmos arquivo, semente,
cenário, canal direto, tau_sat e s_transicao. A única alteração de execução foi
`limite_horizonte_fator: 256 → 512`. Horizonte automático mantido; início do
zero com a mesma semente. Nenhuma política ou parâmetro ajustado para concluir.

| Canal | tau_sat | s_transicao | Reexecutadas | Concluíram no dobro | Sem tarefas no dobro |
|---|---:|---:|---:|---:|---:|
| ativo | 1.0 | 0.01 | 7 | 0 | 4 |
| ativo | 1.4 | 0.01 | 11 | 0 | 8 |
| desligado | 1.0 | 0.01 | 7 | 0 | 4 |
| desligado | 1.4 | 0.01 | 11 | 0 | 8 |

- Horizonte em períodos: de 256×CPM para 512×CPM, por instância.
- 36 atingiram novamente o limite de segurança.
- 24 permaneceram sem executar tarefa alguma.
- 0 executaram tarefas adicionais.
- Agentes ocupados no estado final: 0–0.
- Violações: 0. As 1.308 linhas completas anteriores
  (nominal e grade) foram preservadas e conferidas por igualdade de dataframe.

[36 resultados antes/depois](../outputs/diagnosticos/TB2_20260918/horizonte_dobrado_36.csv).
As mesmas contagens e os mesmos contrastes condicionais persistem após substituir
as 36 linhas pelos resultados de horizonte dobrado.

## T-B2.2 — localização da incompletude

**N total da grade=576**; nominal é amostra separada com N=768, toda completa.
Os marginais abaixo são estratificações da mesma grade; não somá-los entre si.

| Parâmetro | Nível | N do grupo | Incompletas | Percentual no grupo | N total da grade |
|---|---|---:|---:|---:|---:|
| cenario | adaptativa | 288 | 0 | 0.000% | 576 |
| cenario | centralizada | 288 | 36 | 12.500% | 576 |
| canal | ativo | 288 | 18 | 6.250% | 576 |
| canal | desligado | 288 | 18 | 6.250% | 576 |
| tau_sat | 0.7 | 192 | 0 | 0.000% | 576 |
| tau_sat | 1.0 | 192 | 14 | 7.292% | 576 |
| tau_sat | 1.4 | 192 | 22 | 11.458% | 576 |
| s_transicao | 0.01 | 192 | 36 | 18.750% | 576 |
| s_transicao | 0.25 | 192 | 0 | 0.000% | 576 |
| s_transicao | 0.6 | 192 | 0 | 0.000% | 576 |

O cruzamento completo por braço e **todos** os parâmetros varridos está em
[cruzamento_h256.csv](../outputs/diagnosticos/TB2_20260918/cruzamento_h256.csv).
Por combinação afetada há 16 execuções por braço: no centralizado, 7/16
incompletas com tau=1 e 11/16 com tau=1,4, sempre s=0,01, em cada estado do canal;
no adaptativo, nenhuma. A concentração é estrutural ao desenho observado.

## Contrastes somente sobre pares completos

Pareamento por arquivo/semente. Um par só entra quando ambos os braços
concluíram; não comparar sementes diferentes nem usar um braço inteiro contra
um subconjunto do outro. Primeiro calcular A−C por par; depois a média das
sementes retidas em cada instância; IC95 t sobre as instâncias retidas, com
peso igual por instância. Esse estimando é **condicional à conclusão conjunta**.
Número desigual de sementes por instância está publicado nos arquivos de amostra.

| Canal | tau_sat | Pares retidos/previstos | Perda de pares | Instâncias retidas/previstas |
|---|---:|---:|---:|---:|
| ativo | 1.0 | 9/16 | 43.75% | 4/4 |
| ativo | 1.4 | 5/16 | 68.75% | 3/4 |
| desligado | 1.0 | 9/16 | 43.75% | 4/4 |
| desligado | 1.4 | 5/16 | 68.75% | 3/4 |

A perda de réplicas reduz precisão e potência; com tau=1,4 perde-se também uma
instância (IC t com apenas dois graus de liberdade). Não foi estimada uma
percentagem formal de potência. Os IC não corrigem viés de seleção nem tornam
esses resultados representativos das execuções que não concluem.

### Cinco indicadores nas quatro células afetadas

Todos usam s=0,01. Valores A−C, média [IC95].

| Canal | tau_sat | Indicador | Média [IC95] |
|---|---:|---|---|
| ativo | 1.0 | atraso_relativo | -1.793585 [-4.977522; +1.390351] |
| ativo | 1.0 | taxa_omissao | -0.265625 [-0.302490; -0.228760] |
| ativo | 1.0 | divida_latente_sobre_plano | -0.108378 [-0.166687; -0.050068] |
| ativo | 1.0 | taxa_falha_efetiva | -0.062500 [-0.162025; +0.037025] |
| ativo | 1.0 | fracao_porta1 | -0.268750 [-0.457018; -0.080482] |
| ativo | 1.4 | atraso_relativo | -0.817008 [-1.619492; -0.014523] |
| ativo | 1.4 | taxa_omissao | -0.297222 [-0.446978; -0.147466] |
| ativo | 1.4 | divida_latente_sobre_plano | -0.103601 [-0.213155; +0.005952] |
| ativo | 1.4 | taxa_falha_efetiva | -0.102778 [-0.263573; +0.058017] |
| ativo | 1.4 | fracao_porta1 | -0.225000 [-0.422476; -0.027524] |
| desligado | 1.0 | atraso_relativo | -2.040745 [-4.986258; +0.904769] |
| desligado | 1.0 | taxa_omissao | -0.247917 [-0.299130; -0.196703] |
| desligado | 1.0 | divida_latente_sobre_plano | -0.115729 [-0.160243; -0.071214] |
| desligado | 1.0 | taxa_falha_efetiva | -0.080208 [-0.195220; +0.034804] |
| desligado | 1.0 | fracao_porta1 | -0.262500 [-0.461697; -0.063303] |
| desligado | 1.4 | atraso_relativo | -1.327902 [-3.129692; +0.473888] |
| desligado | 1.4 | taxa_omissao | -0.219444 [-0.251066; -0.187823] |
| desligado | 1.4 | divida_latente_sobre_plano | -0.087252 [-0.184982; +0.010479] |
| desligado | 1.4 | taxa_falha_efetiva | -0.050000 [-0.140234; +0.040234] |
| desligado | 1.4 | fracao_porta1 | -0.191667 [-0.286531; -0.096802] |

### Antes/depois da leitura da taxa de falha efetiva

A coluna anterior incluía observações ao horizonte nas execuções censuradas;
não representava desfechos finais. O recálculo não escolhe sinais favoráveis.

| Canal | tau_sat | Média anterior com censura | Média nos pares completos | IC95 dos pares completos |
|---|---:|---:|---:|---|
| ativo | 1.0 | +0.076042 | -0.062500 | [-0.162025; +0.037025] |
| ativo | 1.4 | +0.160417 | -0.102778 | [-0.263573; +0.058017] |
| desligado | 1.0 | +0.062500 | -0.080208 | [-0.195220; +0.034804] |
| desligado | 1.4 | +0.147917 | -0.050000 | [-0.140234; +0.040234] |

O sinal troca nas quatro células, mas **todos os novos IC95 da taxa de falha
incluem zero**. Não se pode destacar redução de falhas como resultado detectado
nessa região, nem concluir ausência de efeito. Demais células e todos os cinco
indicadores estão nos CSV condicionais; médias marginais completas por braço,
com N, também estão publicadas separadamente e não substituem o pareamento.

### Distinção necessária: nominal versus grade

O nominal de B2 teve **768/768 execuções completas**. Recalcular por pares
completos não exclui nenhuma linha nominal. Portanto a afirmação estritamente
nominal de sobrevivência dos contrastes ao desligar R_error não depende de uma
hipótese de ausência ao acaso. **Ela não pode ser extrapolada à grade**: nesta,
a seleção diferencial exige a interpretação condicional acima. O problema não
é corrigido descartando incompletas e voltando a chamar o contraste de geral.

## Diagnóstico e precedente na literatura

No TCC, o diagnóstico anterior identifica seleção prioritária de tarefa difícil,
competência insuficiente, ajuda bloqueada e probabilidade quase nula de P1.
As 36 reexecuções acabam com agentes livres; não se demonstrou um erro numérico
ou de implementação. Classificação: **limitação estrutural das regras adotadas**,
com impacto na leitura dos resultados. Nenhuma regra foi alterada neste teste.

Pessoa et al. relatam não conclusão persistente a 600 semanas por dependências,
alocação e indisponibilidade de agentes. O precedente sustenta que estruturas de
alocação podem produzir essa assinatura; não prova mecanismo idêntico: lá há
ocupação, aqui agentes livres. Tampouco torna o bloqueio necessário em toda
família ABM+SD ou valida empiricamente nossas regras. Os períodos relativos ao
CPM não são convertidos em semanas. [Fonte primária](https://pubs.acs.org/doi/10.1021/acs.iecr.5c04351).

## Verificação, publicação e continuidade

- Dois testes novos confirmam exclusão pareada e proíbem parear sementes distintas;
  IC de uma única instância é indefinido.
- Identidade bit a bit: três testes passaram após o diagnóstico.
- Seleção de 36 chaves, N=576/768, preservação de linhas completas e hashes do
  código/configuração conferidos automaticamente.
- Não houve alteração de dinâmica, RNG, V_mod ou ajuste contra Rieskamp.
- Não se avançou ao bloco C; o lote 37 continua aberto.

[Protocolo](../research/tb2/PROTOCOLO.md) e
[saídas integrais](../outputs/diagnosticos/TB2_20260918/).

```sh
python3 research/tb2/diagnostico.py --saida outputs/diagnosticos/TB2_nova
python3 -m unittest discover -s research -p test_tb2_pares.py -v
```

A pasta de saída deve ser nova. A política atual fica preservada. Qualquer
alternativa futura de seleção/alocação exige desenho declarado e comparação;
o horizonte não deve ser aumentado repetidamente até aparecer um resultado
conveniente. Os contrastes censurados da primeira análise ficam como histórico,
substituídos pelos resultados condicionais para interpretação das células afetadas.
