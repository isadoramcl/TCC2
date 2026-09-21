"""ICs com rótulos, antes/depois e análise da forma; nunca oculta censura."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[2];out=ROOT/'outputs/diagnosticos/A1_20260919'
d=pd.read_csv(out/'bruto.csv');d['fracao_porta1']=d.p1_omissao/(d.p1_omissao+d.p3_analitica)
metrics=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1'];rows=[];before=[]
def interval(x):
    x=x.dropna();n=len(x);m=x.mean();h=t.ppf(.975,n-1)*x.std(ddof=1)/np.sqrt(n) if n>1 else np.nan
    return dict(media=m,ic95_inf=m-h,ic95_sup=m+h,N_instancias=n)
for (regra,lim),g in d.groupby(['regra','limite']):
    ok=g.pivot(index=['arquivo','semente'],columns='cenario',values='concluiu').all(axis=1)
    for met in metrics:
        p=g.pivot(index=['arquivo','semente'],columns='cenario',values=met);diff=p.adaptativa-p.centralizada
        for estimando,delta in [('observado_ate_termino_ou_teto',diff),('condicional_pares_completos',diff[ok])]:
            c=int((~g.concluiu).sum());status=('CENSURADO: nao terminal' if c else 'COMPLETO') if estimando.startswith('observado') else ('CONDICIONAL: perda de pares' if not ok.all() else 'COMPLETO')
            rows.append(dict(regra=regra,limite=lim,metrica=met,estimando=estimando,estatuto=status,censuradas=c,pares_previstos=len(diff),pares_retidos=len(delta),pares_indefinidos=int(delta.isna().sum()),**interval(delta.groupby('arquivo').mean())))
    for cen,h in g.groupby('cenario'):
        a=d[(d.regra=='constante')&(d.limite==.6)&(d.cenario==cen)].set_index(['arquivo','semente']);b=h.set_index(['arquivo','semente'])
        for met in metrics+['p1_fuga','fracao_fuga_p1','N_req','TW','TL','TU','TR','retrabalho_sobre_esforco_total']:
            before.append(dict(regra=regra,limite=lim,cenario=cen,metrica=met,antes=a[met].mean(),depois=b[met].mean(),delta=(b[met]-a[met]).mean(),N=len(b),incompletas=int((~b.concluiu).sum()),estatuto='CENSURADO: media ao teto, nao terminal' if not b.concluiu.all() else 'COMPLETO'))
pd.DataFrame(rows).to_csv(out/'cinco_indicadores_IC95.csv',index=False);pd.DataFrame(before).to_csv(out/'antes_depois.csv',index=False)
r=pd.read_csv(out/'resumo.csv');lines=['| Regra | Limite | Braço | Completas/N | Fuga média | Fração de fuga em P1 (média por execução) | Estatuto |','|---|---:|---|---:|---:|---:|---|']
for x in r.itertuples():
    lines.append(f'| {x.regra} | {x.limite:.2f} | {x.cenario} | {x.completas}/{x.N} | {x.p1_fuga_medio:.4f} | {x.fracao_fuga_p1_media:.6f} | '+('CENSURADO; acumulado até teto' if x.incompletas else 'COMPLETO')+' |')
local=pd.read_csv(out/'sensibilidade_local.csv');summary=local.groupby('cenario').fracao_fuga_estado.nunique().to_dict()
ver=json.loads((out/'verificacoes.json').read_text())
s='''# A1 — rota de fuga dependente de estado, alternativa preservada

[DEC] `regra_fuga=constante` permanece default; alternativa
`dependente_estado` aplica omega*q>limite, q=max(0,2*p_heu−1).
Seleção P1, ação de fuga, RNG e nominal não foram substituídos.
Robustez dedicada: `config/robustez_a1.yaml`, quatro instâncias ×quatro sementes
×dois braços ×duas regras ×cinco limites (0,60 é controle). Horizonte256×CPM.
O limite está efetivamente varrido aqui; não foi acrescentado silenciosamente
à antiga família do runner20. Células/indefinições não são descartadas.

## Grade inteira

'''+ '\n'.join(lines)+f'''

Total: {ver['N']} execuções; {ver['completas']} completas; zero violações.
Fuga positiva na alternativa: {ver['fuga_positiva']}. As taxas dividem por
seleções P1, não por tarefas; uma tarefa pode sofrer muitas fugas. Publicados
numeradores, denominadores, histogramas de q, médias por execução e pooled.

## Forma da resposta e estatuto científico

O comparador individual continua um **interruptor por estado**, com degrau em
q=limite/omega. A alternativa retira a degeneração de comparar duas constantes,
mas NÃO introduz probabilidade contínua de fuga. Uma mistura agregada de
limiares entre estados pode variar; não prova continuidade do comparador.
A análise local nos mesmos estados nominais, sem realimentação, produz
{summary} valores distintos na malha 0..0,60 passo0,01; arquivo separado.
Os quatro limites dinâmicos não demonstram continuidade matemática. Platôs,
saltos e censura da grade devem ser lidos como tais. Não chamar a alternativa
de mecanismo empiricamente validado nem ajustar limite para obter uma curva
esperada. Ela permanece hipótese [DEC], sem eleger limite conveniente.

## Conexão com A-13 / T-B2.3

A-13 e A-14 foram identificados independentemente: ambos continham comparação
de constantes na inicialização/histórico capaz de desligar uma rota.
T-B2.3 mostrou a assistência como uma saída do bloqueio conjunto de três vias;
B2 suave confirmou a saída heurística. A1 modifica a segunda comparação, a fuga.
Isso não garante conclusão: fuga recorrente pode gerar outro bloqueio prático.
Não converter os indicadores ao teto em benefícios finais de governança.

## Verificação e limites

- Cinco testes A1: positivo, negativos, limiar estrito, opção inválida,
  constante explícita/default e contrafactual no mesmo estado/sorteios.
- Identidade neutra e nominal histórico bit a bit: três testes aprovados.
- Baseline constante/0,60 contra nominal arquivado: diferenças <1e-12.
- Primeira configuração de teste tinha rho ativo, misturando retrabalho C4;
  corrigida apenas a fixture com rho=0; falha preservada, experimento sem ajuste.
- `cinco_indicadores_IC95.csv`: IC t sobre médias por instância (n≤4), tanto
  diagnóstico ao término/teto quanto contraste condicional a pares completos.
  Nulo/NaN quando não há pares ou denominador. Condicionais não corrigem seleção.
- `antes_depois.csv`: nominal preservado e todos os indicadores publicados,
  componentes e contagens; rótulo de censura em cada linha afetada.
- Resultados em `outputs/diagnosticos/A1_20260919`; manifesto e hashes conferidos.

Lote não fechado. A regra solicitada está implementada/testada; a expectativa
de continuidade não é um controle aprovado por construção. Próximos: C1 e C2,
com os controles publicados antes de resultados dinâmicos.
'''
(ROOT/'projeto/50_FUGA_DEPENDENTE_DE_ESTADO.md').write_text(s)

# Figura científica; todos os pontos e contagens de censura ficam visíveis.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(1,2,figsize=(11,4))
for (rule,cen),g in r.groupby(['regra','cenario']):
    g=g.sort_values('limite');label=rule+' / '+cen
    axes[0].plot(g.limite,g.fracao_fuga_p1_media,'o-',label=label)
    axes[1].plot(g.limite,g.incompletas,'o-',label=label)
axes[0].set_ylabel('Fração fuga/P1; inclui execuções censuradas')
axes[1].set_ylabel('Incompletas (de 16 por ponto)')
for ax in axes:ax.set_xlabel('Limite de aversão à perda');ax.grid(alpha=.2)
axes[0].legend(fontsize=7);fig.tight_layout();fig.savefig(out/'fuga_e_censura.png',dpi=150)
