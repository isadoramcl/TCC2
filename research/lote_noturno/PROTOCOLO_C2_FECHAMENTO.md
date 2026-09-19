# C2 — fechamento, protocolo antes da execução

A nova ordem explicita controle APROXIMADO. Preservar a reprovação histórica
na terceira casa; não repetir esse critério como se a ordem atual o exigisse.
Critério atual verificável: fórmula literal e reconstrução independente dos
momentos; os parâmetros impressos devem devolver mu e CV dentro dos intervalos
de arredondamento dos momentos publicados. Publicar os desvios alpha/beta,
sem alterar entradas, tolerâncias da fórmula ou parâmetros operacionais C3.

[DEC] Cada agente recebe quatro taxas basais independentes e fixas, uma por
nível ordinal, da Beta cujo mu é F_base(nível) da alternativa C1 escolhida.
Sem redessortear por tarefa; correlação entre níveis não é empiricamente conhecida.
Taxas não alteram F_base médio. p0 usa taxa do agente/nível + R_error*(1-mu_cog).
Sem alteração das demais portas ou do excesso C4.

Fluxo auxiliar de RNG derivado de SeedSequence([semente,20260919,2]), separado
da dinâmica. Nenhuma chama nem sorteio extra com 'nenhuma'. Validar TODOS os
níveis antes de inicializar agentes e sortear taxas; mu estritamente em
(0,1/(1+CV²)), CV=1,13 fixo. Não reduzir CV para células inviáveis.

Grade: quatro instâncias [::120], sementes0–3, dois braços, ambas opções,
sete bases: histórica com F_ancora=0,05/0,10/0,15/0,20/0,25, C1-curto, C1-longo.
448 células planejadas. Célula inválida registrada e não simulada; seu par
'nenhuma' continua registrado. Horizonte256×CPM, fuga constante/limite0,60.
Sem escolher mapa ou âncora por resultado. Cinco indicadores A−C com IC95 t
sobre médias por instância, células/pares incompletos rotulados separadamente.
Diferença beta−nenhuma pareada por instância/semente dentro de cada braço.

Verificar momentos com200.000 agentes sintéticos por média admissível e seed
fixa. Publicar média e CV das taxas dos agentes efetivamente simulados também,
sem esperar precisão igual com apenas24 agentes únicos por configuração/nível.
Critério auxiliar Monte Carlo prévio: erro relativo da média e CV <3% na amostra
grande; não ajustar seed ou repetir até passar. Amostra pequena só descritiva.

Portas: alternativa nenhuma/default exata e identidade ao commit efd1248
anterior a C2 (campos, estados, RNG); teste de p0 usando taxa realmente sorteada;
limites explícitos e rejeição antes de consumir RNG. Arquivar tudo em diretório
novo. Nenhuma alteração V_mod nem calibragem contra Rieskamp.
