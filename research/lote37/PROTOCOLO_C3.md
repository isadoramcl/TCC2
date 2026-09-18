# Ordem 37 — C3 antes de qualquer integração

[DEC] Protocolo do controle publicado. Nenhuma distribuição entra no simulador
antes de reproduzir a Tabela 2. Ordem 32 ignorada. Nominal e fontes anteriores
preservados. Demais itens da ordem 37 aguardam este controle.

Fonte: Stewart (1992), PDF da autora em Downloads, páginas 174–175, inspecionadas
visualmente e por extração de texto. DOI 10.1016/0951-8320(92)90097-5.

- Implementar a binomial pela fórmula de massa; beta-binomial por log-gamma;
  p-dependente por recorrência de estados (Eq7/8): tendo k erros, a probabilidade
  do próximo é phi*p_av*(k+1), e não phi*p_av*k.
- Parâmetros literais da ordem37: n=25, N=94, p=.0163, CV=1.13, phi=.845.
- Comparar frequências e Pearson agrupando 3 ou mais erros, como explica p.175.
- Aceitação: igualdade na terceira casa decimal, sem ajustar parâmetros ou alvo.
- Diagnóstico separado, sem substituição: usar também alpha=.7546/beta=45.4563
  impressos na p.174 e os momentos impressos xbar=.4083/s²=.6057.
- Verificar independentemente contra SciPy para binomial/beta-binomial; para
  p-dependente, enumeração de todas sequências em n pequeno e caso p constante
  que deve reduzir à binomial. Conferir P(X=0)=(1-phi*p_av)^n diretamente.
- Registrar saídas antes de lançar erro se falhar. Não inserir aprovação falsa
  em unittest: separar teste de algoritmo do portão científico publicado.
- Depois do item, executar identidade bit a bit existente com opções neutras.

Limite: parâmetros publicados arredondados podem não reconstruir uma tabela
à precisão exigida. Esse resultado bloqueia o lote; não autoriza afrouxar a
aceitação nem ajustar parâmetros para aproximar a tabela.
