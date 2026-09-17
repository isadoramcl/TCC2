# Verificação e continuidade — T1/T2/T3

- Protocolo: `PLANO_T1_T2_T3.md`, preservado como entrada do manifesto anterior ao lote.
- Piloto: 92 execuções em `/private/tmp/tcc2-arranjo-piloto`, sem compor inferência.
- Lote principal: 2.176 execuções, zero censuradas e violações. Desfechos em
  `outputs/diagnosticos/arranjo_20260917/`; relatório 24 gerado por script.
- Teste de taxa escrito antes da implementação: falhou por campo inexistente;
  depois passou nos casos sem falha/falha certa e reporte zero/um.
- Testes de isolamento e malha escritos antes do runner: falharam por arquivo
  inexistente; passaram após implementação. Detector confrontado com degrau,
  inclinação e perturbação na igualdade. Não é teste estatístico de continuidade.
- `python3 -m unittest discover -s research -p 'test_*.py' -v`: 44 testes passaram.
- `research/verificar_exports_arranjo.py`: execuções mínimas reais nos runners
  07/09/10/11/20/21/25 e leitura histórica 05 passaram; saídas só em pasta temporária.
- Compilação completa passou com `PYTHONPYCACHEPREFIX=/private/tmp/tcc2-pycache`.
  Primeira tentativa bloqueada ao escrever cache fora do workspace; nenhum erro
  de sintaxe. Nenhum arquivo fonte foi mudado para contornar esse bloqueio.
- Figura T1 inspecionada: cinco indicadores, dois limiares, ambas as células
  comuns de reporte/detecção, IC95 e eixos legíveis.
- Revisão independente recalculou todos os IC95 T2 e controle nominal. Sem
  bloqueio. Ressalvas de salto local, interação, censura e floats incorporadas.
- 72 hashes históricos congelados preservados. Nominal/YAML não foram alterados.
- V_obs/V_mod continua pausado. Próxima questão: discutir a família próxima ao
  limiar e fontes externas dos blocos de premissas, sem nova onda HM.
- Parecer 23 ausente de origin/main após dois fetches, ainda ddc7c94. A autora
  autorizou continuar usando sua instrução textual. Não se alega leitura ou
  integração do documento ausente; incorporar quando for disponibilizado.

Resultados T1/T2 não são avaliação do plano B. Padrões e critério de sucesso
foram registrados no parecer 22 antes de qualquer avaliação deles.
