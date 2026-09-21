"""Localização das inversões existentes; nenhuma nova simulação."""
from pathlib import Path
import pandas as pd
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/diagnosticos/GOV2_CROWDER1_20260919'
x=pd.read_csv(ROOT/'outputs/diagnosticos/SAT_GOV_20260919/GOV_regioes_IC95.csv')
x=x[x.estimando=='observado'];opp=x[x.ic95_inf>0].sort_values(['metrica','perfil_adaptativa','perfil_centralizada']);opp.to_csv(OUT/'GOV2_todas_inversoes_IC95.csv',index=False)
y=opp[opp.regiao=='ordenacao_historica'].copy();assert len(y)==22
d=pd.read_csv(ROOT/'outputs/diagnosticos/SAT_GOV_20260919/bruto.csv',float_precision='round_trip')
sigs=[]
for r in y.itertuples():
 a=d[(d.celula==r.perfil_adaptativa)&(d.cenario=='adaptativa')].set_index(['arquivo','semente'])[r.metrica].sort_index()
 c=d[(d.celula==r.perfil_centralizada)&(d.cenario=='centralizada')].set_index(['arquivo','semente'])[r.metrica].sort_index()
 sigs.append(hashlib.sha256('|'.join(float(v).hex() for v in a-c).encode()).hexdigest())
y['assinatura_vetor_diferencas']=sigs;y.to_csv(OUT/'GOV2_inversoes_ordenacao_historica.csv',index=False)
rows=[]
for m,g in x.groupby('metrica'):
 z=g[g.regiao=='ordenacao_historica'];q=y[y.metrica==m]
 rows.append(dict(metrica=m,N_total=len(g),IC_oposto_total=int((g.ic95_inf>0).sum()),N_ordenacao_historica=len(z),IC_oposto_ordenado=len(q),vetores_distintos=q.assinatura_vetor_diferencas.nunique(),perfis_A=q.perfil_adaptativa.nunique(),perfis_C=q.perfil_centralizada.nunique()))
s=pd.DataFrame(rows);s.to_csv(OUT/'GOV2_concentracao.csv',index=False)
def table(df):
 return '| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'+'\n'.join('| '+' | '.join(str(v) for v in row)+' |' for row in df.itertuples(index=False,name=None))
f=['tau_inicial','tau_min','p_reporte','p_deteccao']
y['A (tau, limiar, reporte, detecção)']=y.apply(lambda r:', '.join(f'{r[k+"_A"]:g}' for k in f),axis=1)
y['C (tau, limiar, reporte, detecção)']=y.apply(lambda r:', '.join(f'{r[k+"_C"]:g}' for k in f),axis=1)
r='''# T-GOV.2 — localização das inversões e leitura da multiplicidade

Nenhuma simulação nova. Base: T-GOV.1, 81 perfis, quatro instâncias e quatro
sementes; contrastes adaptativa−centralizada. Sinal oposto ao contraste médio
nominal negativo: IC95 inteiramente positivo. A taxa de falha efetiva nominal
já tinha IC cruzando zero; seu sinal de referência é apenas o da média.
Todos os resultados abaixo são completos, sem censura.

## Denominadores: 3/1.215, não 3/6.561

'''+table(s)+'''

Os três casos de atraso pertencem à região com ordenação histórica das quatro
premissas: 1.215 pares não idênticos. Na malha total há 1.602 ICs positivos
para atraso, incluindo os 1.599 em regiões que invertem ao menos uma premissa.
Os 81 perfis idênticos têm diferença exatamente zero. Misturar o numerador de
uma sub-região com o denominador total produz a comparação “55x menos”.

Sob n hipóteses todas nulas e ICs marginais com cobertura e caudas corretas,
a expectativa de exclusões numa direção seria 0,025*n: 164,025 para 6.561
ou 30,375 para 1.215. Linearidade da esperança não exige independência, mas
uma interpretação binomial das contagens exigiria hipóteses adicionais.
Aqui as hipóteses não são todas nulas, há fortes efeitos negativos, perfis
idênticos degenerados e reutilização das mesmas trajetórias. Essas contas
não estimam quantas das inversões observadas são falsas e não decidem entre
multiplicidade e mecanismo. Os ICs são pontuais, sem controle familiar.

## Todos os 22 contrastes da região de ordenação histórica

Tuplas explicitam os quatro parâmetros em cada braço. Nada foi filtrado por
magnitude além do critério solicitado de IC95 inteiramente oposto.

'''+table(y[['metrica','perfil_adaptativa','perfil_centralizada','A (tau, limiar, reporte, detecção)','C (tau, limiar, reporte, detecção)','media','ic95_inf','ic95_sup']].round(6))+'''

[Lista integral de ICs opostos em toda a malha](../outputs/diagnosticos/GOV2_CROWDER1_20260919/GOV2_todas_inversoes_IC95.csv),
com os oito valores e a região de cada contraste.
[Sub-região ordenada e assinaturas das diferenças por execução](../outputs/diagnosticos/GOV2_CROWDER1_20260919/GOV2_inversoes_ordenacao_historica.csv).

## Onde se concentram e qual a leitura

- **Atraso (3): concentração clara em um perfil A**, o 71:
  tau=0,80, limiar=0,425, reporte=0,75, detecção=0,12. Os comparadores C
  também começam com assistência aberta e detecção=0,12, mas reporte menor.
  São 3/53 comparações ordenadas envolvendo A=71, contra 0/1.162 no restante.
  Esta região foi identificada após observar os dados, não pré-especificada.
  Não são três ocorrências espalhadas ou três réplicas independentes: as três
  reutilizam o mesmo braço A. Achado descritivo de região candidata; o padrão
  sozinho não confirma mecanismo nem exclui multiplicidade.
- **Omissão (3): dois casos compartilham C=36**, baixa detecção/reporte
  (0,03/0,15), e A com confiança 0,80 versus 0,525. O terceiro mantém
  confiança/limiar/reporte iguais e altera somente detecção 0,03→0,075.
  Há um agrupamento de dois e um caso separado, não uma região única.
- **Falha efetiva (4): dois pares de regiões**. Todos têm confiança A=0,80
  versus C=0,525 e reporte igual entre os braços. Os casos de reporte/detecção
  baixos coincidem com duas inversões de omissão; o outro par usa reporte=0,45,
  detecção A=0,12 versus C=0,075. Mudam limiares A=0,25/0,425. Concentração
  descritiva em maior confiança inicial, não prova causal dos escalares.
- **Dívida latente (1): caso isolado**, tau=0,80 e reporte=0,75 em ambos,
  detecção=0,03; só o limiar muda de C=0,60 para A=0,25. Uma célula não
  estabelece concentração regional: manter como inversão exploratória,
  compatível com flutuação/multiplicidade até confirmação independente.
- **Fração P1 (11): seis são o mesmo vetor de diferenças por execução**,
  com tau=0,25, assistência fechada nos dois braços, detecção=0,12 e
  reporte 0,15→0,45; limiares diferentes não mudam as trajetórias. Os cinco
  restantes são outros contrastes. Há redundância estrutural, não seis
  evidências independentes de uma região. Não atribuir esse agrupamento a Crowder.

**Veredicto:** as inversões de atraso e parte das demais estão concentradas,
e a leitura anterior de “sinal não estável” sem escala regional foi ampla demais.
Predomina o contraste negativo sob ordenação histórica, com exceções locais
exploratórias e dependentes. Não é justificável classificar todas como ruído,
nem elevá-las a regimes científicos confirmados só pela localização. Dívida
permanece um caso isolado; fracão P1 inclui duplicatas exatas. A nova varredura
Crowder caracteriza sensibilidade nominal, mas não reexecuta estes perfis e,
portanto, não poderá provar por si só a causa dessas inversões.
'''
(ROOT/'projeto/70_LOCALIZACAO_DAS_INVERSOES_DE_SINAL.md').write_text(r)
print(s.to_string(index=False))
