# Teste discriminante de TL — antes de V_obs/V_mod

Baseline: 1fd22ff. Parecer20 copiado fielmente para revisao-auditoria (9ef0f47).
A formulação atual permanece `unitario`, inclusive quando a opção é omitida.
Alternativa `crowder_eq3`: sucesso soma 0,5*dC_original; pedido não atendido
soma 0,05; bloqueio pré-pedido soma zero. dC_original usa competências 0–5,
antes do teto da Eq2; não usar incremento normalizado dC/5 como entrada da Eq3.
TL continua uma contagem no denominador, sem mudar ocupação ou relógio.

Desenho fixado: mesmas 16 instâncias e 12 sementes do nominal corrigido,
dois cenários e duas convenções (768 execuções), pares idênticos em tudo mais.
IC95 t sobre 16 diferenças médias por instância; sementes são réplicas internas.
Comparar estado RNG, agentes, tarefas, eventos e todos os resultados exceto
TL/E_total e retrabalho_sobre_esforco_realizado entre convenções (as duas
razões usam TL no denominador; ver _resultado no legado). Comparar unitário ao nominal publicado.
Teste de compatibilidade compara nominal atual (opção omitida e explícita)
ao código fixado 1fd22ff, incluindo bits e estados internos, em 32 casos.

Publicar TW/TL/TU/TR nos dois cenários para cada degrau histórico, sem refazer
as execuções antigas. Declarar que C4_C1_comunicacao combina protocolo,
escala/incremento de competência e teto; não atribuir isoladamente ao protocolo.
Legado continua intacto: +0,162 versus +0,042 para Cp0,8/Cr0,4; teto0,98 versus Dr.

Se o sinal de E_total depender da convenção, retirar o destaque de conclusão
sobre governança. Não escolher uma lei por produzir sinal desejado.
Após resultado, revisão e publicação: merge autorizado em main, preservando
índice e arquivos locais da autora. Nenhuma execução de V_obs/V_mod neste teste.
