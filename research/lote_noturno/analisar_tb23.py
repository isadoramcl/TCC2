"""Relatório e curvas da malha pré-declarada; nenhuma seleção de política."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'outputs/diagnosticos/TB23_20260918'
d=pd.read_csv(out/'resumo.csv');p=d[d.modo=='principal']
fig,axs=plt.subplots(3,1,figsize=(7,9),sharex=True)
for modo,g in d.groupby('modo'):
    for ax,col,label in zip(axs,['incompletas','fracao_hiato_sem_confianca','N_req_medio'],['Incompletas (de 36)','Hiato sem confiança / hiatos','Pedidos enviados por execução']):
        ax.plot(g.tau_varrida,g[col],'o-',label=modo);ax.set_ylabel(label);ax.axvline(.6,ls=':',color='gray');ax.grid(alpha=.2)
axs[0].legend();axs[-1].set_xlabel('Confiança inicial varrida (malha finita)');fig.tight_layout();fig.savefig(out/'varredura.png',dpi=160)
cols=['modo','tau_varrida','completas','incompletas','hiato_sem_confianca_media','fracao_hiato_sem_confianca','N_req_medio']
table='| '+' | '.join(cols)+' |\n|'+ '|'.join(['---']*len(cols))+'|\n'+'\n'.join('| '+' | '.join(str(x) if isinstance(x,str) else f'{x:.6f}' for x in row)+' |' for row in d[cols].itertuples(index=False,name=None))
s=f'''# T-B2.3 — o portão fechado explica as 36 incompletas nesta amostra

## Resultado

Na malha declarada, o primeiro valor sem incompletas é **tau_inicial=0,600001**:
36/36 concluem, assim como em todos os valores superiores testados. Em 0,25,
0,59 e 0,60, 0/36 concluem. O teste é estrito (`confianca > 0,60`).
A transição observada é um degrau de conclusão ao atravessar esse limiar.
Não é estimativa de um limiar contínuo exato, nem escolha de novo nominal.

O controle que altera somente a confiança inicial do portão, preservando a
inicialização da rede em 0,25, também completa 36/36 em cada nível.
Alterar apenas a rede para 0,80 ou 1,00, mantendo o portão fechado, completa
0/36 em ambos. Portanto o desaparecimento das incompletas é atribuível à
abertura inicial do portão e suas consequências, não apenas ao canal difuso.
A lei Crowder continua evoluindo após comunicações; estes controles não congelam
os mediadores posteriores. Não se deduz ausência de efeitos da rede nos outros
indicadores ou em outras populações.

## Números da malha inteira

{table}

Contagens são acumuladas até o término ou teto de 256×CPM. A queda do hiato
absoluto combina mecanismo e menor exposição temporal; a fração por oportunidade
está publicada para separar a mudança de escala. N_req conta pedidos enviados,
não bloqueios anteriores ao envio. Trajetórias acima são funções do valor inicial
varrido; não foram exportadas séries temporais desses contadores acumulados.

## Correção da leitura de B2

As 36 incompletas são desfecho do portão degenerado A-13 no desenho histórico,
**não evidência de uma limitação necessária da família ABM+SD**. O horizonte
dobrado continua sendo um controle válido (0/36), mas não estabelece sozinho
uma causa. O precedente Pessoa tem outro mecanismo e não justifica extrapolar
este bloqueio à família. O nominal histórico permanece intacto; os contrastes
condicionais de T-B2.2 continuam descritivos do subconjunto completo daquele
nominal, e não são substituídos por um tau conveniente.

População deste ensaio: somente as 36 chaves historicamente incompletas,
selecionadas explicitamente. 468 execuções, ambos os estados do canal direto,
mesmas sementes/instâncias/parâmetros. Não estimar frequência de incompletude
na população a partir desta amostra selecionada.

## Verificação e reprodução

- `python3 research/tb2/varredura_confianca.py --saida <diretorio-novo>`
- Protocolo anterior: `research/tb2/PROTOCOLO_TB23.md`.
- `controle_baseline.csv`: resíduos menores que 1e-12 nos campos B2 publicados.
- `verificacoes.json`: zero violações e 468 execuções; hashes das fontes
  conferidos no término.
- `identidade.log`: três controles bit a bit aprovados (campos, estados e RNG).
- `resumo.csv`, `estratos.csv` e `bruto.csv` preservam toda a malha.
- Figura: `outputs/diagnosticos/TB23_20260918/varredura.png`.

O lote noturno permanece aberto; próximo item: D2 em segundo plano e D1.
'''
(ROOT/'projeto/68_PORTAO_DE_ASSISTENCIA_E_INCOMPLETUDE.md').write_text(s)
