# 85 — Sensibilidade ao eixo de F_base e aos pesos de Di

## Pré-registro

2026-09-29T13:42:41.162852+00:00

Nominal v3 final preservado. Primeiro: 384 execuções por eixo no nominal, comparar média e limites de IC95 às referências fornecidas e eixo complexidade à etapa3 oficial, tolerância 0,0005; parar se exceder. Tamanho usa exatamente as razões declaradas 1/1,9018/2,8368/5,3670, derivadas arredondadas da frequência bruta LOC_TOTAL. Complexidade usa o YAML nominal, não arredondamento alternativo.

A: após controle, dois eixos nos conjuntos fora48 e aleatorio24, com as chaves (arquivo,semente) da etapa3. B: três alternativas de pesos do YAML no nominal16 e fora48. Referência pesos iguais é o Di arquivado que alimenta o nominal, sem recalculá-lo artificialmente pelos pesos arredondados do YAML. Alternativas usam a função recalcular_di existente no runner20, no universo completo das tarefas; recálculo de Di, quartis globais e nível antes da instanciação do simulador. Não altera dados originais.

IC95: contraste pareado adaptativa−centralizada por (arquivo,semente), médias das sementes por instância, t sobre instâncias. Sem descarte de variantes. Todas as execuções devem concluir e ter zero violações. Nenhum parâmetro será ajustado por resultado.

## Critério da autora (transcrição)

Vale para os dois itens.

1. Zero violações em todas as execuções; todas concluem.
2. INSENSIBILIDADE, a afirmação que se quer testar: os cinco contrastes mantêm
   SINAL NEGATIVO com IC 95% EXCLUINDO ZERO em todas as variantes e em todos os
   conjuntos. Se isso valer, a conclusão do trabalho não depende da escolha e
   ambos os itens fecham como decisão de escopo declarada.
3. Se algum contraste MUDAR DE SINAL ou passar a incluir zero em alguma
   variante, isso é resultado e entra como tal — identificando exatamente qual
   indicador, qual variante e qual conjunto. Não é motivo para descartar a
   variante nem para procurar outra ponderação que recupere o resultado.
4. A taxa de falha efetiva já está declarada como não robusta à varredura de
   governança. Se ela for a única a falhar aqui, isso é consistente com o que já
   se sabe e deve ser dito assim, sem virar achado novo.
5. Reportar tudo em tabela única, variante por variante, conjunto por conjunto.

## Estado

Pré-registro escrito antes de executar. Resultados pendentes. Código de produção e nominal não serão modificados; orquestração temporária será copiada como texto na saída para rastreabilidade.
