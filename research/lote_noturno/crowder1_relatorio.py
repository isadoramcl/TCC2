"""Relatório de sensibilidade sem eleição ou alvo externo."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];o=ROOT/'outputs/diagnosticos/GOV2_CROWDER1_20260919'
x=pd.read_csv(o/'CROWDER1_cinco_IC95.csv');x=x[x.estimando=='observado'];a=pd.read_csv(o/'CROWDER1_atividade.csv');b=pd.read_csv(o/'CROWDER1_por_braco_IC95.csv');delta=pd.read_csv(o/'CROWDER1_antes_depois.csv');v=json.loads((o/'CROWDER1_verificacoes.json').read_text())
def table(df):
 return '| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'+'\n'.join('| '+' | '.join(str(v) for v in row)+' |' for row in df.itertuples(index=False,name=None))
wide=x.copy();wide['contraste [IC95]']=wide.apply(lambda r:f'{r.media:.6f} [{r.ic95_inf:.6f}; {r.ic95_sup:.6f}]',axis=1)
w=wide.pivot(index=['incremento_base','fator_transferencia','estatuto'],columns='metrica',values='contraste [IC95]').reset_index()
debt=x[x.metrica=='divida_latente_sobre_plano'];debtabs=b[b.metrica=='divida_latente_sobre_plano'];debtdelta=delta[(delta.metrica=='divida_latente_sobre_plano')&(delta.cenario=='adaptativa')&(delta.estimando=='observado')]
s='''# T-CROWDER.1 — sensibilidade dos escalares de aprendizagem

## Implementação e porta de identidade

`aprendizado.incremento_base=15` e `aprendizado.fator_transferencia=3`
promovidos ao YAML, condição `tcc1` ([TCC1]), equação (4.2). Os três caminhos
leem as mesmas chaves: Simulacao legado, comunicação Crowder do MVP e
comunicação legada do MVP (inclusive contagem TL alternativa). A aritmética,
as conversões de escala e os tetos anteriores foram mantidos. A confusão de
escala legada não foi corrigida nesta mudança: sustenta o controle histórico.

No Crowder, dC=clip((base+fator*(5*C_p−5*C_r))/100,0,0,30); ganho normalizado
dC/5, limitado pela dificuldade da subtarefa. O teto pode amortecer a grade.
O código anterior está preservado no commit dfc0d78. Identidade por float.hex
com essa versão em (15,3): resultados completos, estados de agentes/tarefas,
eventos, registros, reparos e RNG em 24 comparações pelos três caminhos.
23 testes aprovados antes da execução da grade, incluindo identidade neutra.
O teste local reprovou antes da parametrização e passou depois; logs preservados.

## Desenho

Grade 3x3: base=7,5/15/22,5 e fator=1,5/3/6. **22,5 é 1,5x15**, não o dobro;
a lista explícita solicitada prevalece. Sensibilidade sem alvo externo, sem
recalibração ou escolha de valores. Ambos os braços recebem os mesmos escalares.
16 instâncias e 12 sementes, idênticas às 384 execuções nominais arquivadas,
em cada uma das nove combinações. Horizonte nominal 256xCPM.

IC95 t sobre 16 médias por instância de diferenças pareadas por semente.
Intervalos pontuais exploratórios, sem ajuste para multiplicidade. As 12
sementes por instância não são tratadas como 192 instâncias independentes.
Mesmas sementes iniciais, sem alegar alinhamento de eventos após divergência.

'''+f'**{v["N"]} execuções; {v["completas"]} completas; {v["violacoes"]} violações.**\n'+'''
A censura acompanha todas as tabelas; pares completos são exportados também.
Nenhum valor indefinido é convertido em zero. As nove células não mudam o nominal.

## Cinco indicadores, adaptativa − centralizada

Atraso=makespan/CPM sem recursos (não crescimento externo de prazo); fração P1
conta omissões/(omissões+inícios analíticos). Nenhum desses cinco usa TL no
denominador. Tabela completa de contrastes e IC95:

'''+table(w)+'''

[CSV dos contrastes](../outputs/diagnosticos/GOV2_CROWDER1_20260919/CROWDER1_cinco_IC95.csv),
[valores absolutos por braço](../outputs/diagnosticos/GOV2_CROWDER1_20260919/CROWDER1_por_braco_IC95.csv),
[ANTES/DEPOIS e diferenças pareadas frente a (15,3)](../outputs/diagnosticos/GOV2_CROWDER1_20260919/CROWDER1_antes_depois.csv).

## Dívida latente — leitura prioritária

'''+table(debtabs[['incremento_base','fator_transferencia','cenario','media','ic95_inf','ic95_sup','estatuto']].round(6))+'''

Alteração da dívida na adaptativa frente ao próprio nominal (15,3), com IC95
pareado; a centralizada permanece inalterada:

'''+table(debtdelta[['incremento_base','fator_transferencia','antes','depois','media','ic95_inf','ic95_sup','estatuto']].round(6))+'''

A dívida é pico normalizado pelo plano, estatística de extremo com horizonte
endógeno. Variações de duração e oportunidades de amostragem podem afetá-la;
esta sensibilidade não remove a restrição do contrato observacional externo.

## Assimetria do canal e teto de dC

'''+table(a.round(6))+'''

Em toda a grade centralizada, N_req=0 e TL=0. Seus resultados são idênticos
bit a bit aos da célula (15,3) nos campos comuns. Assim, qualquer mudança do
contraste nesta grade vem do braço adaptativo. A atividade e a fração de
sucessos no teto acima permitem distinguir escalar nominal de ganho realizado.

## Controles e limites da inferência

As 384 execuções em (15,3) reproduzem todos os campos numéricos comuns do
nominal arquivado por float.hex (CSV lido com round_trip). Os hashes da
implementação/configurações permaneceram constantes durante a grade.
Nenhuma alteração de V_mod ou busca de política/valor ótimo foi feita.
Esta grade caracteriza a sensibilidade nominal; não demonstra que os escalares
causaram as exceções localizadas em T-GOV.2, pois aqueles perfis de governança
não foram reexecutados aqui. Ver [localização e multiplicidade](TGOV2_LOCALIZACAO_INVERSOES_20260919.md).
'''
summary=[]
for met,g in x.groupby('metrica'):
 summary.append(dict(metrica=met,N=len(g),medias_negativas=int((g.media<0).sum()),IC_negativos=int((g.ic95_sup<0).sum()),IC_positivos=int((g.ic95_inf>0).sum()),media_min=g.media.min(),media_max=g.media.max()))
r=pd.DataFrame(summary);r.to_csv(o/'CROWDER1_sinais_resumo.csv',index=False)
s+='\n## Síntese dos sinais na grade declarada\n\n'+table(r.round(6))+'\n\nAs faixas são descritivas da família declarada, sem ranking ou seleção.\n'
s+='''
**Leitura:** os cinco indicadores têm média e IC95 inteiramente negativos em
9/9 combinações. Para dívida, o contraste vai de −0,080016 a −0,076383;
a alteração da média adaptativa frente ao nominal vai de −0,002202 a
+0,001432. Apenas (22,5;1,5) exclui zero no IC95 dessa alteração pareada:
−0,002202 [−0,004222;−0,000181], leitura exploratória sem ajuste múltiplo.
Não se elege essa célula. Os escalares afetam magnitude/atividade, mas não
explicam uma inversão nominal de sinal nesta família.

O ganho dC médio por sucesso muda de cerca de 0,081 a 0,252 na escala
original; no canto (22,5;6), 5,98% dos sucessos atingem o teto 0,30. Portanto
a persistência do sinal não decorre de os parâmetros terem ficado inertes
na adaptativa. O nominal (15,3) desta grade usa 16 instâncias; não confundir
seu IC com o nominal de quatro instâncias da grade T-GOV.1.

![Dívida: contraste e alteração pareada](../outputs/diagnosticos/GOV2_CROWDER1_20260919/CROWDER1_divida.png)
'''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
fig,axes=plt.subplots(1,2,figsize=(11,5),sharey=True)
for ax,g,title in [(axes[0],debt,'Dívida: adaptativa − centralizada'),(axes[1],debtdelta,'Dívida adaptativa: alteração frente a (15, 3)')]:
    g=g.sort_values(['incremento_base','fator_transferencia']);pos=np.arange(len(g))
    ax.errorbar(g.media,pos,xerr=np.vstack([g.media-g.ic95_inf,g.ic95_sup-g.media]),fmt='o',capsize=3)
    ax.axvline(0,color='gray',lw=1,ls='--');ax.set_title(title,fontsize=10);ax.set_xlabel('Média e IC95 pareado por instância')
    ax.set_yticks(pos);ax.set_yticklabels([f'{r.incremento_base:g} / {r.fator_transferencia:g}' for r in g.itertuples()]);ax.grid(axis='x',alpha=.2)
axes[0].set_ylabel('incremento_base / fator_transferencia');axes[0].invert_yaxis()
fig.tight_layout();fig.savefig(o/'CROWDER1_divida.png',dpi=160);plt.close(fig)
(ROOT/'projeto/TCROWDER1_SENSIBILIDADE_20260919.md').write_text(s)
print(r.to_string(index=False));print('DIVIDA ALTERACAO',debtdelta[['incremento_base','fator_transferencia','media','ic95_inf','ic95_sup']].to_string(index=False))
