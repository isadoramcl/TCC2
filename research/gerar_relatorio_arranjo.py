"""Relatório 24: todos os números calculados a partir do lote T1/T2."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
R=Path(__file__).resolve().parents[1]
O=R/'outputs/diagnosticos/arranjo_20260917'
d=pd.read_csv(O/'bruto.csv');t1=d[d.etapa=='T1'];t2=d[d.etapa=='T2']
c=pd.read_csv(O/'T2_contrastes_IC95.csv')
metrics=['atraso_relativo','taxa_omissao','divida_latente_sobre_plano','taxa_falha_efetiva','fracao_porta1']

def intervalo(x):
    a=x.groupby('arquivo').mean();m=a.mean();h=t.ppf(.975,len(a)-1)*a.std(ddof=1)/np.sqrt(len(a))
    return dict(media=m,ic95_inferior=m-h,ic95_superior=m+h,n_instancias=len(a))

def tabela(rows,cols):
    s='| '+' | '.join(cols)+' |\n|'+ '|'.join(['---']*len(cols))+'|\n'
    for row in rows:s+='| '+' | '.join(str(x) for x in row)+' |\n'
    return s

jumps=[]
for (tm,pr,pd_),g in t1.groupby(['tau_min','p_reporte','p_deteccao']):
    for met in metrics+['N_req']:
        p=g.pivot(index=['arquivo','semente'],columns='tau_inicial',values=met)
        jumps.append(dict(tau_min=tm,p_reporte=pr,p_deteccao=pd_,metrica=met,
                          **intervalo(p[round(tm+1e-6,6)]-p[tm])))
pd.DataFrame(jumps).to_csv(O/'T1_saltos_pareados_IC95.csv',index=False)
cond=[]
for met in metrics:
    p=t2.pivot(index=['arquivo','semente'],columns='configuracao',values=met)
    cond.append(dict(metrica=met,contraste='ambos menos reporte',**intervalo(p.ambos-p.reporte)))
pd.DataFrame(cond).to_csv(O/'T2_confianca_apos_reporte_IC95.csv',index=False)
ref=t2[t2.configuracao=='referencia'];amb=t2[t2.configuracao=='ambos']
local=pd.read_csv(O/'T1_canal_fuzzy_estado_fixo.csv')
texto=f'''# T1/T2/T3 — arranjo, portão e premissas de reporte

**V_obs/V_mod continua pausado. Nominal histórico preservado.**

## Desenho e verificações

[DEC] Protocolo registrado em `research/PLANO_T1_T2_T3.md` antes de executar.
{len(d)} execuções: {len(t1)} em T1, {len(t2)} em T2; todas completas, sem violações.
T1: {t1.configuracao.nunique()} células, {t1.arquivo.nunique()} instâncias e
{t1.semente.nunique()} sementes por célula. T2: {t2.arquivo.nunique()} instâncias,
{t2.semente.nunique()} sementes; referência compartilhada e três intervenções.
IC95 t sobre médias por instância, sementes internas pareadas; intervalos pontuais.
O piloto foi executado em pasta separada e não compõe esses números.
Os pares comuns (p_reporte, p_deteccao), lidos do desenho, são
{sorted(set(zip(t1.p_reporte, t1.p_deteccao)))}.

T2 altera blocos: **confiança significa tau_inicial E tau_min**. Não é efeito
isolado de tau_inicial. Na referência ambos estão no nível centralizado; a célula
confiança troca os dois, a célula reporte troca p_reporte e p_deteccao, e ambos
reproduz o nominal adaptativo. Os demais parâmetros são idênticos.

Mesmas instâncias/sementes e mesma sequência pseudoaleatória inicial em todos
os contrastes. O consumo sequencial pode desalinhá-la entre eventos após as
trajetórias divergirem. Não se alega identidade de sorteio por tarefa/evento.
O estimando é o contraste entre regimes simulados, não um contrafactual local de
uma mesma tarefa. Nenhum resultado abaixo constitui calibração externa.

## T1 — portão binário, resposta global não reduzida a degrau puro

Na igualdade tau=tau_min e abaixo dela, pedidos ficam bloqueados. Logo acima,
a comunicação se ativa. Essa é a descontinuidade do predicado estrito. Porém os
cinco desfechos variam também dentro de cada lado, inclusive quando N_req é zero.
**A hipótese de um degrau puro não descreve a resposta observada.** A arquitetura
combina um portão binário e um canal fuzzy variável; não se pode concluir que o
aparato difuso não contribui ao contraste.

Em estado local fixo (bateria e pressão fixadas no arquivo), mu_rede varia de
{local.mu_rede.min():.6f} a {local.mu_rede.max():.6f} com tau, sem alterar mu_cog.
O CSV local separa a resposta fuzzy de seleção, disponibilidade e aprendizado.
A trajetória completa é discreta, com ceil, sorteios, filas e confiança dinâmica;
malha finita não prova continuidade matemática. O indicador `degrau_puro=False`
é descritivo, não teste de significância (usa igualdade numérica exata).

Curvas dos cinco indicadores com IC95: [figura](../outputs/diagnosticos/arranjo_20260917/T1_curvas.png).
Dados completos: `T1_curvas_IC95.csv`, `T1_forma.csv` e
`T1_canal_fuzzy_estado_fixo.csv`. Não se impõe monotonicidade aos resultados.

### Contraste local tau_min+epsilon menos igualdade

'''
rows=[]
for x in jumps:
 rows.append([x['tau_min'],x['p_reporte'],x['metrica'],f"{x['media']:.6f}",f"[{x['ic95_inferior']:.6f}; {x['ic95_superior']:.6f}]"])
texto+=tabela(rows,['tau_min','p_reporte','Indicador','Diferença local','IC95'])
texto+='''
[LIMITACAO] Epsilon = 10⁻⁶ é o menor passo declarado na malha. O salto de pedidos não
implica salto detectável em todos os desfechos: IC95 de omissão, dívida e falha
efetiva incluem zero nas células locais. No limiar alto com reporte baixo, abrir
o portão **aumenta** atraso neste desenho. Não escolher limiar pelo sinal favorável.
A incerteza com poucas instâncias e as interações impedem extrapolação universal.

### Alternativa de reposicionamento proposta, sem eleger cenário

[DEC] Para investigar comunicação ativa nos dois braços, usar limiar comum e
confianças iniciais a pequenas distâncias positivas dele: uma família com margens
+0,01 e +0,05, repetida separadamente para cada limiar nominal. Repetir cada par
nos dois níveis comuns de reporte/detecção. Ambos os braços começam com pedidos
elegíveis; Crowder poderá alterar essa condição ao longo da execução. Os rótulos
passam a significar confiança próxima ao limiar, não os arranjos históricos.
Não aplicar a mudança ao YAML nominal. Esta é proposta experimental a priori,
não a seleção do ponto de melhor desempenho; não foi executada nesta entrega.

## T2 — bloqueio de premissas

Diferença = intervenção − referência centralizada. Razões são médias das razões
por execução. A fração P1 usa tarefas executadas, não oportunidades ou esforço.

'''
rows=[]
for x in c[c.celula!='interacao'].itertuples():
 rows.append([x.celula,x.metrica,f'{x.referencia:.6f}',f'{x.intervencao:.6f}',f'{x.media:.6f}',f'[{x.ic95_inferior:.6f}; {x.ic95_superior:.6f}]'])
texto+=tabela(rows,['Bloco alterado','Indicador','Referência','Intervenção','Diferença','IC95'])
texto+='''
O bloco reporte/detecção altera fortemente a fração de falhas não reportadas e
seu estoque oculto. Isso não demonstra redução equivalente de defeitos gerados:
seu IC95 de taxa de falha efetiva inclui zero. “Inclui zero” significa inconclusivo,
não ausência de efeito. A confiança isolada reduz a taxa efetiva neste desenho.
A redução do nominal combina mecanismos e premissas; não é evidência de um efeito
único de governança independente das escolhas de reporte e limiar.

### Interação e efeito condicionado

Não somar contribuições como percentuais causais. A interação é
(ambos − referência) − (confiança − referência) − (reporte − referência).
Interação positiva nos desfechos reduzidos expressa subaditividade das reduções,
não um prejuízo provocado pela confiança.

'''
texto+=tabela([[x.metrica,f'{x.media:.6f}',f'[{x.ic95_inferior:.6f}; {x.ic95_superior:.6f}]'] for x in c[c.celula=='interacao'].itertuples()],['Indicador','Interação','IC95'])
texto+='\nConfiança adicional depois de igualar o bloco reporte ao adaptativo:\n\n'
texto+=tabela([[x['metrica'],f"{x['media']:.6f}",f"[{x['ic95_inferior']:.6f}; {x['ic95_superior']:.6f}]"] for x in cond],['Indicador','Ambos − reporte','IC95'])
texto+=f'''
## Conferência do braço sem comunicação

No nominal centralizado: hiato_encontrado médio={ref.hiato_encontrado.mean():.6f};
hiato_colega_capaz_sem_confianca={ref.hiato_colega_capaz_sem_confianca.mean():.6f};
N_req={ref.N_req.mean():.6f}, p2_ajuda={ref.p2_ajuda.mean():.6f}, TL={ref.TL.mean():.6f}.
A porta não se abre e Crowder não recebe eventos nesse braço. Isso explica por
que os degraus de comunicação/lei/reset anteriores só alteraram o adaptativo.
Não significa que todos os mecanismos fuzzy estejam inertes no centralizado.

A razão das probabilidades de não reporte é
{(1-ref.p_reporte.iloc[0])/(1-amb.p_reporte.iloc[0]):.6f}; a razão observada de omissão é
{ref.taxa_omissao.mean()/amb.taxa_omissao.mean():.6f}. A comparação logarítmica da
premissa com o contraste é descritiva; não identifica uma parcela causal porque
reporte/detecção também afetam filas, duração, pressão e futuros sorteios.
T2 mede esses regimes explicitamente, incluindo suas interações.

## T3 — taxa de falha efetiva de primeira classe

`Resultado.taxa_falha_efetiva = (n_com_erro+n_reportadas)/n_tarefas`.
O campo é derivado sem alterar RNG, decisões ou estados. Foi propagado aos
runners que exportam execuções, inclusive por asdict, e aos resumos de desfechos.
Os artefatos anteriores não foram sobrescritos. Consumidores de CSV histórico
podem derivá-lo em memória quando os dois contadores e o denominador existem;
onde faltam contadores, não inventar uma baseline.

Neste lote completo a soma confere com todas as falhas instrumentadas por tarefa.
Nos runs censurados, ocultos entram no contador após conclusão e reportados entram
durante a execução: a fórmula não deve ser interpretada como taxa final de todas
as tentativas. Publicar sempre concluiu/censura. Reparos não reincidem no modelo;
essa taxa conta falhas da execução original, não tentativas de reparo.

Controles exatos existentes preservam campos anteriores, estados e RNG. A tabela
`controle_nominal.csv` registra ANTES/DEPOIS sem mudança substantiva; o maior
resíduo de leitura CSV foi {pd.read_csv(O/'controle_nominal.csv').diferenca_maxima.max():.3g}.

## Correções documentais e continuidade

Parecer 22: retrabalho_sobre_esforco_realizado excluído do vetor z pela dependência
de TL; pico de dívida exige controlar número de amostras e horizonte endógeno.
Plano B orientado a padrões registrado antes de avaliá-los, com padrões candidatos,
critério de sucesso conjunto e exigência de fonte externa. Não converter controles
internos tautológicos em validação externa. Nenhuma retomada de V_obs/V_mod ou HM.

Próxima questão: discutir a alternativa próxima ao limiar e obter evidência externa
para premissas de reporte/detecção. Resultados desta entrega não substituem o
nominal histórico. O parecer 23 citado não estava disponível no remoto consultado;
a instrução textual da autora foi integralmente usada como referência operacional.

Reprodução: `python3 src/modelo/26_testes_arranjo.py --saida /tmp/arranjo-novo --workers 4`,
seguida da geração deste relatório por `research/gerar_relatorio_arranjo.py`
(a geração lê o lote publicado). O diretório do experimento deve ser novo.
'''
(R/'projeto/24_TESTES_ARRANJO_T1_T2_T3.md').write_text(texto)
print('Relatório 24 e tabelas suplementares gerados')
