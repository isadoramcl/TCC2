"""Leitura integral da malha, regiões de sinal e censura explícitas."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'outputs/diagnosticos/SAT_GOV_20260919'
p=pd.read_csv(out/'GOV_perfis.csv');d=pd.read_csv(out/'bruto.csv');x=pd.read_csv(out/'GOV_contrastes_IC95.csv')
f=['tau_inicial','tau_min','p_reporte','p_deteccao']
x=x.merge(p.rename(columns={'celula':'perfil_adaptativa',**{k:k+'_A' for k in f}}),on='perfil_adaptativa').merge(p.rename(columns={'celula':'perfil_centralizada',**{k:k+'_C' for k in f}}),on='perfil_centralizada')
ordered=(x.tau_inicial_A>=x.tau_inicial_C)&(x.tau_min_A<=x.tau_min_C)&(x.p_reporte_A>=x.p_reporte_C)&(x.p_deteccao_A>=x.p_deteccao_C)
x['regiao']=np.where(ordered,'ordenacao_historica','inclui_inversao_de_premissa');x.loc[x.perfil_adaptativa==x.perfil_centralizada,'regiao']='perfis_identicos'
x.to_csv(out/'GOV_regioes_IC95.csv',index=False)
z=x[x.estimando=='observado'];summary=z.groupby(['regiao','metrica','sinal','evidencia','estatuto']).size().rename('N_contrastes').reset_index();summary.to_csv(out/'GOV_sinais_resumo.csv',index=False)
# All sign reversals, not just illustrative cases. Zero is retained separately.
z[z.media>0].to_csv(out/'GOV_regioes_contraste_positivo.csv',index=False)
nom=z[(z.tau_inicial_A==.8)&(z.tau_min_A==.25)&(z.p_reporte_A==.75)&(z.p_deteccao_A==.12)&(z.tau_inicial_C==.25)&(z.tau_min_C==.6)&(z.p_reporte_C==.15)&(z.p_deteccao_C==.03)]
nom.to_csv(out/'GOV_nominal_IC95.csv',index=False)
rows=[]
for (reg,met),g in z.groupby(['regiao','metrica']):
 rows.append(dict(regiao=reg,metrica=met,N=len(g),negativos=int((g.media<0).sum()),zeros=int((g.media==0).sum()),positivos=int((g.media>0).sum()),IC_negativo=int((g.ic95_sup<0).sum()),IC_positivo=int((g.ic95_inf>0).sum())))
r=pd.DataFrame(rows);r.to_csv(out/'GOV_sinais_contagens.csv',index=False)
# Examples are first lexicographic cells with an entirely positive CI.
ex=z[(z.ic95_inf>0)&(z.regiao=='ordenacao_historica')].sort_values(['perfil_adaptativa','perfil_centralizada']).groupby('metrica').head(1)
ex.to_csv(out/'GOV_exemplos_inversao_ordenada.csv',index=False)
def table(df):
 return '| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'+'\n'.join('| '+' | '.join(str(v) for v in row)+' |' for row in df.itertuples(index=False,name=None))
sat=pd.read_csv(out/'SAT1_resumo.csv');q=pd.read_csv(out/'SAT1_q_suplementar.csv');v=json.loads((out/'verificacoes.json').read_text())
s='''# T-SAT.1 e T-GOV.1 — caracterização de regime, nominal preservado

## T-SAT.1 — 384 execuções nominais, 192 por braço

Fonte congelada: `outputs/diagnosticos/noturno_nominal/tarefas.csv` e `bruto.csv`.
79.327 oportunidades de decisão, das quais 13.334 selecionaram P1. Denominador
é decisão, não tarefa única; repetições por bloqueio integram a distribuição.
Tabela abaixo em frações (multiplicar por 100 para porcentagens):

'''+table(sat)+'''

[Histograma](../outputs/diagnosticos/SAT_GOV_20260919/SAT1_histograma.png),
[100 intervalos e contagens](../outputs/diagnosticos/SAT_GOV_20260919/SAT1_histograma.csv).
Último intervalo inclui 1; demais são fechados à esquerda e abertos à direita.

**A hipótese operacional não se confirma pelo limiar proposto de menos de 10%
no meio:** há 14,95% de todas as decisões e 17,95% das seleções P1 em [0,1;0,9].
Não há massa abaixo de 0,01. A distribuição é bimodal, mas a massa inferior
fica acima desse extremo; não descrevê-la como empilhada em 0 e 1.

A conclusão sobre q exige outra distinção: 92,33% das seleções P1 têm q<0,01
ou q>0,99 e apenas 5,07% estão em [0,1;0,9]. q é quase binário neste sentido,
pois a transformação q=max(0,2*p_heu−1) zera todo p_heu<=0,5. Isso sustenta
concentração de q a montante da fuga, mas não atribui causalmente o degrau do
A1 somente à saturação de p_heu. O comparador individual também é binário.
[Leitura suplementar de q](../outputs/diagnosticos/SAT_GOV_20260919/SAT1_q_suplementar.csv).

## T-SAT.2 — condicional não disparada

O gatilho pré-declarado de T-SAT.1 não foi atingido; não se executou a varredura
condicional. Além disso, há impedimento independente da saturação: no limite
nominal 0,60, omega=0,50 e 0<=q<=1 implicam omega*q<=0,50<0,60 para qualquer
s_transicao. Logo nenhuma suavização pode ativar a fuga nesse limite. Não há
valor de s que torne a fuga graduada mantendo esses parâmetros. O A1 anterior
ativou fuga em limites menores; não confundir esses ensaios com o nominal.
A caracterização “só opera fora do regime saturado” não é sustentada aqui.

## T-GOV.1 — fatores de robustez, desenho declarado

81 perfis = produto cartesiano de três níveis por fator:
- tau_inicial: 0,25 / 0,525 / 0,80;
- tau_min: 0,25 / 0,425 / 0,60;
- p_reporte: 0,15 / 0,45 / 0,75;
- p_deteccao: 0,03 / 0,075 / 0,12.

Extremos históricos e ponto médio, não estimativas calibradas. Cada perfil
roda nos dois rótulos: 4 instâncias x 4 sementes x 2 braços = 32 execuções.
Todos os 81 perfis adaptativos são comparados aos 81 centralizados: 6.561
contrastes por indicador. Os mesmos resultados são reutilizados; não são
6.561 experimentos independentes. Demais fatores e horizonte 256xCPM nominais.
Esta família dedicada promove efetivamente os quatro fatores, preservando
as famílias históricas e sem eleger a combinação mais favorável.

IC95 t sobre quatro médias por instância de diferenças pareadas por semente.
Intervalos pontuais exploratórios, sem ajuste para multiplicidade. Baixa
precisão com quatro instâncias; não extrapolar a malha à faixa contínua.
“Atraso relativo” aqui é makespan/CPM sem recursos, não crescimento de prazo
externo. Fração P1 é omissões/(omissões+inícios analíticos); fuga é contada
separadamente. Nenhum dos cinco usa TL no denominador.

'''+f'Execuções: **{v["N"]}**, completas **{v["completas"]}**, violações **{v["violacoes"]}**.\n'+'''
Todas as linhas finais levam estatuto de censura/conclusão; contrastes
condicionais em pares completos também estão exportados. Nenhum NaN vira zero.

### Contraste nominal nesta subamostra (adaptativa − centralizada)

'''+table(nom[['metrica','media','ic95_inf','ic95_sup','estatuto']].round(6))+'''

### Sinais em toda a malha

“Ordenação histórica” exige tau_inicial_A>=C, tau_min_A<=C, p_reporte_A>=C e
p_deteccao_A>=C. Perfis iguais são separados. A região restante contém pelo
menos uma premissa com ordenação invertida.

'''+table(r)+'''

A estabilidade em toda a faixa **não se sustenta**: o desenho contém os dois
sentidos de atribuição das premissas, e os contrastes trocam de sinal. Perfis
idênticos dão diferença exatamente zero: o rótulo de arranjo, isoladamente,
não acrescenta efeito. As conclusões devem especificar as combinações de
premissas e seu domínio, em vez de atribuir um sinal universal à governança.
As contagens acima também permitem distinguir inversões dentro da ordenação
histórica das inversões obtidas trocando a ordem das premissas.

[Regiões completas, parâmetros dos dois braços, sinal e IC95](../outputs/diagnosticos/SAT_GOV_20260919/GOV_regioes_IC95.csv).
[Todos os contrastes positivos](../outputs/diagnosticos/SAT_GOV_20260919/GOV_regioes_contraste_positivo.csv).
[Indicadores absolutos por braço](../outputs/diagnosticos/SAT_GOV_20260919/indicadores_por_braco_IC95.csv).
[Dados por execução](../outputs/diagnosticos/SAT_GOV_20260919/bruto.csv).

## Controles e continuidade

Perfis iguais reproduzem resultados exatamente nos dois rótulos. O subconjunto
nominal reproduz TW, TL, TU, TR, makespan e contadores históricos com resíduo
zero. Hashes da dinâmica/configuração nominal inalterados antes/depois.
A suíte bit a bit é registrada separadamente. Não houve recalibração, ajuste
de V_mod, eleição de alternativa ou alteração de conclusão por conveniência.
C4 e N da bancada F continuam parciais; lote 37 permanece encerrado com a
emenda anterior. Este diagnóstico adicional limita a leitura de regime e de
premissas; não demonstra validade externa do modelo.
'''
examples=ex[['metrica','tau_inicial_A','tau_min_A','p_reporte_A','p_deteccao_A','tau_inicial_C','tau_min_C','p_reporte_C','p_deteccao_C','media','ic95_inf','ic95_sup']].round(6)
s+='''
## Inversões mantendo a ordenação histórica

Não é apenas efeito de trocar as premissas entre os nomes dos braços. Nos
1.215 pares não idênticos que mantêm a ordenação histórica há contrastes
positivos nos cinco indicadores. Para atraso: 105 médias positivas, 3 com
IC95 inteiramente positivo; omissão: 112 e 3; dívida: 70 e 1; falha efetiva:
260 e 4; fração P1: 372 e 11. São resultados exploratórios desta grade,
não evidência confirmatória após correção de multiplicidade.

Abaixo, a primeira célula em ordem lexicográfica com IC95 positivo por
indicador, não a de maior efeito. A/C identificam os dois braços; a tabela
completa inclui todas as regiões, inclusive as de intervalo cruzando zero.

'''+table(examples)+'''

## Registro dos controles de execução

A primeira chamada da suíte teve 2 testes aprovados e 1 erro de importação
(`test_mvp` fora do caminho de módulos). Com PYTHONPATH=research, passaram
os 3 testes, incluindo a identidade bit a bit. Ambos os logs foram preservados.
A primeira comparação memória/CSV reprovou a igualdade exata em TR: o parser
padrão difere do round-trip em até 2,842170943040401e-14. A leitura round_trip
preserva o float gravado e produziu resíduo zero, sem relaxar o alvo. A análise
foi refeita a partir dos mesmos dados; nenhuma simulação precisou ser repetida.
Logs originais e controle_leitura_csv.json preservam o diagnóstico. O manifesto
de execução conserva o hash do runner daquela execução; manifesto_final.json
registra o runner corrigido para leitura round-trip e os hashes dos artefatos.
'''
(ROOT/'projeto/71_REGIMES_DE_SATURACAO_E_GOVERNANCA.md').write_text(s)
print(r.to_string(index=False));print('nominal',nom[['metrica','media','ic95_inf','ic95_sup']].to_string(index=False));print('exemplos ordenados',ex.to_string(index=False))
