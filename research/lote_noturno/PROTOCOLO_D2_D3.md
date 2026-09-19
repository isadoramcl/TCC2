# D2/D3 — cobertura interna repetida, protocolo antes da execução

B=500 réplicas, quatro observáveis históricos e vetor verdadeiro do script 04:
F_ancora=.180, f_retrabalho=.420, tau_sat=.850, k_heuristico=.135, mu_minimo=.620.
Cenário adaptativa, simulador legado (procedimento que gerou o gêmeo original),
mesmas duas instâncias selecionadas por 04. Não testa calibração externa ou
validade do MVP corrigido; testa o procedimento de implausibilidade no verdadeiro.

## Estimando e unidade amostral

z imita média esperada com peso igual das DUAS instâncias FIXAS, sobre
aleatoriedade dos agentes. Instâncias não são sorteadas de população.
Uma unidade amostral é um BLOCO de sementes: média dos observáveis nas duas
instâncias, cada uma com semente própria independente. Observação z_b: média de
10 blocos; previsão do verdadeiro: média de 4 blocos INDEPENDENTES dos de z_b.
V_obs sintético = variância amostral entre 10 médias de bloco /10.
V_sim = variância amostral entre 4 médias de bloco /4. Não usar variância pooled
entre instâncias heterogêneas como se fossem a mesma unidade aleatória.
Sementes novas, disjuntas entre todas as réplicas, fontes e instâncias, enumeradas
antes: 10.000.000 + b*28 + (0..27); primeiros20=observação, últimos8=previsão.

I_j=abs(z_j-f_j)/sqrt(V_obs_j+V_sim_j+V_mod_j), V_mod=0 fixo.
Denominador zero: I=0 se numerador0, infinito caso contrário; não epsilon ajustado.
Registrar quatro I, Imax, Imax>3, contagem de censura. Quatro observáveis históricos:
taxa_omissao (fração), atraso_relativo (razão ao CPM sem recursos),
retrabalho_sobre_plano (esforço/plano), E_total (razão contábil interna com TL unitário).
Essas convenções são FIXAS somente para a verificação interna; não admitem z externo.

Taxa de falsa exclusão: frequência de Imax>3 e IC95 binomial exato Clopper–Pearson.
p95 Imax empírico; se >3, reportar corte conjunto específico deste desenho,
sem alterar o corte aplicado nem V_mod. Se taxa>30% ou houver execução incompleta,
marcar diagnóstico reprovado/pendente de desenho e não usar HM.
Nenhuma onda de HM; nenhuma amostragem do espaço de parâmetros.

Congelar código legado/fuzzy/config em snapshot para permitir D1–A1 independentes
sem alterar este experimento. Resultados brutos e sementes gravados por réplica.
