# Plano registrado antes dos novos pilotos — 15/09/2026

Estado nominal preservado. Baseline: branch publicada `72e6a64`; dados, configuração
e código serão identificados por hash. O checkout local da autora não será editado.

1. Reanálise sem simulação: correlações, R² descritivo (não validação), componentes
   de I, variâncias escaladas separadamente, caixas e denominadores de aceitação.
2. Produto constante: F = 0,12 / 0,18 / 0,24 e f = 0,0756/F; demais parâmetros
   na verdade sintética. Duas instâncias originais e sementes 0..31 pareadas.
   Se a taxa de omissão mudar entre extremos, o produto sozinho não representa
   todas as saídas. Ausência de diferença não provaria equivalência estrutural.
3. Ruído: oito pontos equiespaçados da onda 1, mesmas duas instâncias e sementes
   0..31. Comparar prefixos de quatro e 32 sementes, médias realmente recalculadas.
   É piloto da instrumentação, não estimativa de larguras sobre 400 pontos.
4. Cobertura no vetor verdadeiro: 20 blocos independentes; cada bloco tem quatro
   sementes de simulação e dez de observação, sem sobreposição. Comparar observação
   publicada fixa e observações sintéticas renovadas. Intervalos binomiais serão
   reportados; não recalibrar corte para forçar cobertura.
5. Confiança: quatro combinações entre portão e entrada de rede (0,25 / 0,80),
   mantendo demais parâmetros centralizados; quatro instâncias equiespaçadas,
   sementes 0..11. Subclasse experimental muda somente a leitura da confiança
   pelo multiplicador de rede; confiança de agente continua no portão. As células
   diagonais devem coincidir com o simulador nominal. Não introduzir dinâmica.
6. Horizonte: todos os 32 vértices da caixa de calibração, duas instâncias e duas
   sementes. Medir tarefas terminais, dívida pendente e violações separadamente.

Estimando prioritário: média esperada sobre o conjunto FIXO de duas instâncias.
Sementes iguais são blocos pareados entre instâncias. Estimador alternativo de
variância da média: variância das médias por semente dividida pelo número de
sementes. Diferenças determinísticas entre instâncias não são ruído Monte Carlo
desse estimando. Generalização a outras instâncias exige outro desenho e outra
observação alvo; não acrescentar instâncias silenciosamente.

Nenhum piloto aceita a predição quantitativa do revisor como critério de sucesso.
Todos os resultados, inclusive negativos, serão preservados. Novas ondas completas
ficam adiadas até avaliar estes pilotos e a adequação do denominador.
