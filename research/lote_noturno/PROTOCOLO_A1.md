# A1 — protocolo antes de executar

[DEC] Alternativa solicitada: constante (default) versus dependente_estado,
`omega*max(0,2*p_heu-1)>limite`. Não altera seleção P1, RNG ou ação de fuga.
A desigualdade é estrita; fuga continua sendo decisão binária por encontro.
A expectativa de continuidade agregada será testada, não imposta.

Robustez dedicada: quatro instâncias da lista ordenada [::120], sementes 0–3,
ambos os braços; regras constante/dependente_estado × limites 0,10/0,20/0,30/0,40,
mais 0,60 como controle nominal. 320 execuções, horizonte nominal 256×CPM;
nenhum ajuste adaptativo. Esta grade separada inclui limite_aversao_perda sem
multiplicar silenciosamente a grade histórica 20. Protocolo/config YAML dedicado.

Preservar censura e contar n_tarefas, p1_fuga, omissões, P3, pedidos, esforço.
Não calcular atraso terminal das incompletas como resultado final.
Fração de fuga entre seleções P1=p1_fuga/(p1_fuga+p1_omissao), não divisão pelo
número de tarefas (uma tarefa pode sofrer muitas fugas). Sem denominador=NaN.
Também reportar fuga por oportunidade de decisão e histogramas de q em P1.
Parâmetros restantes e sementes pareadas; ordem de consumo de RNG pode divergir
após intervenção (não alegar sorteios alinhados evento a evento).

Para distinguir degrau individual de resposta agregada, usar também os estados
P1 nominais arquivados com q fixo, e avaliar limiares 0..0,60 passo0,01.
Esta análise é local, não nova trajetória; não prova continuidade matemática.
Comparar a variação agregada na grade dinâmica e seus denominadores/censura.
Se houver degeneração ou platôs, publicar; não ajustar fórmula para obter alvo.

Portas: testes negativos/positivos da ação, limite estrito, opção inválida,
identidade bit a bit em padrão e constante explícita, além da suíte existente.
Legado preservado em git 279667f, alternativa nova no MVP apenas.
