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


## Conclusão e verificações — 17/09/2026

768 execuções concluídas; estados físicos/RNG idênticos nos384 pares. Unitário:
diferença -0,050845 IC[-0,059773;-0,041916]. Eq3: +0,051973
IC[0,043253;0,060693]. Conclusão de governança sobre E_total retirada.
40 testes passaram em20,002s. Revisão independente recalculou IC/componentes,
sem impedimento para merge. O piloto identificou dois ajustes no verificador,
sem alterar modelo: soma vazia deve começar float0; a razão TR/esforço também
usa TL no denominador e não é invariante. Após correção, piloto4 execuções
passou antes do lote completo. Manifestos das tentativas ficaram em /private/tmp.

Parecer20 publicado byte a byte em revisao-auditoria (9ef0f47) e incorporado
à resposta (998789d). Resultado completo e resposta ponto a ponto no relatório21.
V_obs/V_mod não iniciado. Merge solicitado em main será feito em checkout
isolado porque o checkout da autora contém índice e arquivos não commitados.
