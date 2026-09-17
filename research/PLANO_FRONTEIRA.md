# Continuação após o piloto inicial — 15/09/2026

Os oito pontos equiespaçados da onda 1 foram rejeitados com ambos os tamanhos
de amostra. Esse piloto verificou a instrumentação, mas não informou sobre a
fronteira do NROY. Preservar esse resultado e não calcular largura de conjunto vazio.

Próximo experimento: quatro pontos equiespaçados entre os NROY legados ordenados
por índice e os quatro pontos rejeitados mais próximos do corte legado. Seleção
baseada somente nos resultados antigos, antes de novas execuções. Manter duas
instâncias, sementes 0..31 e todos os parâmetros originais de cada ponto.

Comparar decisão real com quatro versus 32 sementes, e com a aproximação que
divide apenas V_sim por oito, conservando a média de quatro sementes e V_obs.
Registrar mudanças das médias. Oito pontos escolhidos pela aceitação anterior
NÃO estimam volume ou larguras do espaço original. Não testar a predição de
40% de contração como se fosse critério de aprovação.
