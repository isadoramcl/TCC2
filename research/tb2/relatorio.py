"""Produz relatório do teste sem alterar a dinâmica ou resultados brutos."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
o=ROOT/'outputs/diagnosticos/TB2_20260918'
v=json.loads((o/'verificacoes.json').read_text());novo=pd.read_csv(o/'horizonte_dobrado_36.csv')
marg=pd.read_csv(o/'marginais_h256.csv');cond=pd.read_csv(o/'contrastes_pares_completos_h256.csv')
a=pd.read_csv(ROOT/'outputs/diagnosticos/lote41_B2_censura_20260918/contraste_A_menos_C_IC95.csv')
x=a.merge(cond,on=['etapa','canal','tau_sat','s_transicao','metrica'],suffixes=('_observado_censurado','_pares_completos'))
x.to_csv(o/'antes_depois_contrastes.csv',index=False)
r=pd.read_csv(o/'pares_retidos_h512_seletivo.csv');r=r[r.metrica=='atraso_relativo'];r.groupby(['etapa','canal','tau_sat','s_transicao','arquivo']).size().rename('N_pares_retidos').to_csv(o/'amostra_por_instancia_h512_seletivo.csv')
posterior=pd.read_csv(o/'contrastes_pares_completos_h512_seletivo.csv')
pd.testing.assert_frame_equal(cond,posterior)
s=f'''# T-B2.1 e T-B2.2 — horizonte dobrado e seleção por conclusão

18/09/2026. Pedido executado antes de avançar ao bloco C. Código e resultados
anteriores publicados em `d54283b`; árvore movida de `/private/tmp` para
`TCC2/.worktrees/integracao-main-tl`, dentro do repositório permanente.

## Veredito

**{v['completaram']}/36 execuções incompletas concluíram com o horizonte dobrado.**
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
'''
for (c,tau,esc),g in novo.groupby(['canal','tau_sat','s_transicao']):
 s+=f'| {c} | {tau} | {esc} | {len(g)} | {int(g.concluiu.sum())} | {int((g.n_executadas==0).sum())} |\n'
s+=f'''
- Horizonte em períodos: de 256×CPM para 512×CPM, por instância.
- {int((~novo.concluiu).sum())} atingiram novamente o limite de segurança.
- {int((novo.n_executadas==0).sum())} permaneceram sem executar tarefa alguma.
- {int((novo.n_executadas>novo.n_executadas_antes).sum())} executaram tarefas adicionais.
- Agentes ocupados no estado final: {int(novo.agentes_ocupados_final.min())}–{int(novo.agentes_ocupados_final.max())}.
- Violações: {int(novo.violacoes.sum())}. As 1.308 linhas completas anteriores
  (nominal e grade) foram preservadas e conferidas por igualdade de dataframe.

[36 resultados antes/depois](../outputs/diagnosticos/TB2_20260918/horizonte_dobrado_36.csv).
As mesmas contagens e os mesmos contrastes condicionais persistem após substituir
as 36 linhas pelos resultados de horizonte dobrado.

## T-B2.2 — localização da incompletude

**N total da grade=576**; nominal é amostra separada com N=768, toda completa.
Os marginais abaixo são estratificações da mesma grade; não somá-los entre si.

| Parâmetro | Nível | N do grupo | Incompletas | Percentual no grupo | N total da grade |
|---|---|---:|---:|---:|---:|
'''
for _,r in marg.iterrows():s+=f'| {r.parametro} | {r.valor} | {r.N_grupo} | {r.incompletas} | {100*r.fracao_incompleta:.3f}% | {r.N_grade} |\n'
s+='''
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
'''
sel=cond[(cond.etapa=='grade')&(cond.N_pares_excluidos>0)]
for _,r in sel[sel.metrica=='taxa_falha_efetiva'].iterrows():s+=f'| {r.canal} | {r.tau_sat} | {r.N_pares_retidos}/{r.N_pares_previstos} | {100*r.N_pares_excluidos/r.N_pares_previstos:.2f}% | {r.n_instancias}/4 |\n'
s+='''
A perda de réplicas reduz precisão e potência; com tau=1,4 perde-se também uma
instância (IC t com apenas dois graus de liberdade). Não foi estimada uma
percentagem formal de potência. Os IC não corrigem viés de seleção nem tornam
esses resultados representativos das execuções que não concluem.

### Cinco indicadores nas quatro células afetadas

Todos usam s=0,01. Valores A−C, média [IC95].

| Canal | tau_sat | Indicador | Média [IC95] |
|---|---:|---|---|
'''
for _,r in sel.iterrows():s+=f'| {r.canal} | {r.tau_sat} | {r.metrica} | {r.media:+.6f} [{r.ic95_inferior:+.6f}; {r.ic95_superior:+.6f}] |\n'
s+='''
### Antes/depois da leitura da taxa de falha efetiva

A coluna anterior incluía observações ao horizonte nas execuções censuradas;
não representava desfechos finais. O recálculo não escolhe sinais favoráveis.

| Canal | tau_sat | Média anterior com censura | Média nos pares completos | IC95 dos pares completos |
|---|---:|---:|---:|---|
'''
for _,r in x[(x.N_pares_excluidos>0)&(x.metrica=='taxa_falha_efetiva')].iterrows():
 s+=f'| {r.canal} | {r.tau_sat} | {r.media_observado_censurado:+.6f} | {r.media_pares_completos:+.6f} | [{r.ic95_inferior_pares_completos:+.6f}; {r.ic95_superior_pares_completos:+.6f}] |\n'
s+='''
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
'''
(ROOT/'projeto/49_HORIZONTE_DOBRADO_E_SELECAO.md').write_text(s)
