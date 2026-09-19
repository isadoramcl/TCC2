# B2 — protocolo anterior à implementação e execução

Alternativa `canal_erro_direto`: ativo (default, sem mudança nos bits) ou desligado
(R_error=0 no cálculo p0). Não mudar seleção p_heu, risco de omissão, reporte ou
qualquer outro parâmetro. Teste: desligado equivale bit a bit ao modelo ativo
com R_error configurado em zero; mesma sequência RNG e todos os campos.

Nominal: 16 instâncias × 12 sementes × 2 cenários × 2 canais, mesmas de T2.
Sensibilidade: produto cartesiano tau_sat=[.7,1.,1.4] e
s_transicao=[.01,.25,.6], exatamente as varreduras YAML preexistentes;
4 instâncias igualmente espaçadas entre as 16, 4 sementes, dois cenários e
ambos os canais. Grade pequena declarada; sem otimização ou ranking.

Reportar cinco indicadores T4, médias/IC por célula e contraste A−C pareado
com IC95 t sobre médias por instância; seeds internas. IC pontuais, n=4 na grade.
Comparar nominal ativo com T2 histórico. Responder quais contrastes sobrevivem
com R_error=0, sem escolher uma configuração favorável.

Ausência de evidência de campo para erro direto não demonstra efeito nulo;
alternativa é diagnóstico da dependência estrutural do resultado. PROIBIDOS
mantidos. Só avançar após identidade neutra passar novamente.


## Adendo após erro do runner, antes da reexecução

Primeira execução falhou ao dividir p1/(p1+p3) com denominador zero na grade;
nenhum bruto foi salvo pelo runner original. Preservado seu manifesto.
Correção observacional: fração indefinida vira NaN; registrar n_executadas,
N_req/N_blocked, motivo de término e contagem de censura. Salvar cada linha ao
terminar para evitar perda de resultados se ocorrer outra exceção.
Células censuradas não sustentam contraste de resultados finais; as médias
exportadas são observações até o horizonte, com flag explícita, não estimativas
de prazo final. NaN não vira zero. Desabilitar armazenamento de registros por
tarefa neste runner (não utilizados por seus desfechos) para limitar memória;
nenhuma decisão, sorteio, tempo ou estado físico muda.
