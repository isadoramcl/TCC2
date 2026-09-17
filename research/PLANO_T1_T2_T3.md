# T1/T2/T3 — plano registrado antes da execução

[DEC] Solicitação da autora de 17/09/2026. V_obs/V_mod pausado. Nominal histórico
intacto: parâmetros, equações, RNG e artefatos anteriores não são substituídos.
Parecer 23 não estava no origin/main após fetch (ddc7c94); instrução integral da
autora é o contrato desta execução. Incorporar o documento quando disponível.

## Desenho

- T1: ambos os limiares nominais, separadamente; em cada um, dois pares comuns
  de reporte/detecção (níveis centralizado e adaptativo). Todos os demais campos
  de cenário são idênticos. tau_inicial varia em malha declarada no runner,
  de zero a um, com ±0.1, ±0.05, ±0.02, ±0.01, ±0.001 e ±0.000001 do limiar,
  incluindo igualdade. Crowder permanece dinâmico. Quatro instâncias igualmente
  espaçadas do nominal e quatro sementes: diagnóstico de forma, sem otimização.
- T1 local: mesma competência/carga/bateria e varredura contínua da entrada fuzzy;
  separar predicado estrito tau>tau_min da saída mu_rede. Saídas discretas do
  simulador (ceil e decisões) não provam ausência de um canal fuzzy contínuo.
  Degrau puro exige constância dos cinco desfechos dentro de cada lado; variação
  fora da fronteira refuta essa hipótese. Não provar continuidade matemática por
  uma malha finita. Registrar resposta mista caso coexistam salto e variação.
- T2: referência centralizada comum e três contrastes: bloco confiança
  (tau_inicial E tau_min) apenas; bloco reporte/detecção apenas; ambos (nominal).
  Nomear os dois parâmetros de confiança para não atribuir efeito só a tau_inicial.
  Dezesseis instâncias nominais e doze sementes; mesmas sementes/instâncias por
  contraste, mesma sequência RNG inicial, sem garantir alinhamento por evento
  após divergência endógena. Publicar também a diferença de interação
  ambos − confiança − reporte, sem percentuais causais de escala log.
- Desfechos: atraso_relativo, taxa_omissao, divida_latente_sobre_plano,
  taxa_falha_efetiva=(n_com_erro+n_reportadas)/n_tarefas e
  fracao_porta1=p1_omissao/(p1_omissao+p3_analitica), por tarefas executadas.
  Não usar oportunidades ou tempo heurístico como denominador da fração P1.
- IC95 t sobre médias por instância, sementes como réplicas internas pareadas.
  Publicar censura, violações e amostra. IC pontuais, não simultâneos.
- TL unitário preservado; E_total e razão TR/esforço não são desfechos de T1/T2.
  Nenhuma nova afirmação de governança antes de concluir os dois testes.

## Implementação e verificação

- [ ] Teste de taxa efetiva com falha certa, reporte zero/um e ausência de falha;
  resultado deve ser invariante à simples classificação reportado/oculto.
- [ ] Adicionar campo derivado em Resultado e aos runners que exportam linhas;
  manter vetor OBSERVAVEIS histórico HM intacto (coluna extra é diagnóstico).
- [ ] Testar isolamento das células, fronteira estrita e curvas-controle do
  detector de degrau (degrau sintético versus inclinação); rodar piloto real.
- [ ] Congelar manifesto antes do lote; comparar nominal T2 com arquivo anterior;
  produzir tabelas, IC95 e curvas T1 com as cinco métricas.
- [ ] Corrigir admissibilidade e registrar plano B com critérios anteriores
  à avaliação; padrões propostos não são fatos empíricos validados.
- [ ] Rodar controles exatos existentes, rever diff e preservar hashes históricos.
