# Reconciliação C3 e retomada B1 — plano anterior às execuções

18/09/2026. Especificação: mensagem integral da autora nesta sessão substitui
parecer 39; parecer 43 excluído. Sem operações Git de publicação neste turno.

## C3

- Implementação operacional BB: n=25, N=94, alpha=.7546, beta=45.4563.
- Células fixas k=0..4: [67.475,18.334,5.639,1.765,.549].
- Resíduos: calculado/publicado; máximo absoluto em %; amplitude em %.
- N1: s=mu*(1-mu)/sigma² sem -1; sigma=1.13*mu, mu=.0163.
- N2 n=24; N3 binomial; N4 troca alpha/beta; N5 sigma=1.13*mu².
- Cada negativo deve exceder 1% e 10 vezes o resíduo candidato; ao menos quatro.
  Executar os cinco. Valores orientativos não são alvos de ajuste.
- Candidato: ausência de tendência estritamente/não estritamente monotônica,
  testada pelas diferenças sucessivas de razões. Não inferir aleatoriedade dos
  resíduos a partir de apenas cinco pontos; publicar os pontos.
- A-16: 73×73=5329 pontos inclusivos na caixa de arredondamento de alpha/beta;
  contagem de mu/CV compatíveis, contagem de E0 que arredonda a 67.475.
  Inversos com um parâmetro fixo são diagnóstico da fonte, nunca parâmetros
  operacionais. Preservar saídas anteriores e inserir registro em 04_FONTES.
- Arquivos: research/lote41/c3.py; research/test_c3_discriminante.py;
  outputs/diagnosticos/lote41_C3_20260918; relatório canônico em projeto/.
- Rodar teste de identidade bit a bit antes de iniciar B1.

## B1/T4

- Runner isolado research/lote41/t4.py. Overrides existentes, sem nova dinâmica.
- Quatro células portão C/A × rede C/A, cada uma em DOIS níveis comuns de
  reporte/detecção (C e A), para reproduzir ambas as comparações T2.
- Portão varia tau inicial E tau_min conforme T2. Rede varia apenas tau inicial.
  Lei Crowder é idêntica; estados separados continuam atualizados pelos mesmos
  eventos do respondente, conforme implementação existente.
- Mesmas 16 instâncias e sementes 0..11 do T2. TL unitário nominal.
- Diagonais devem reproduzir execução sem overrides bit a bit (campos,
  tarefas, agentes, eventos, RNG), antes da interpretação. Confiancas_rede é
  armazenamento auxiliar separado e não se compara ao auxiliar inativo.
- Cinco desfechos T2 e IC95 t sobre médias das sementes por instância.
- Decomposição: portão=AC−CC; rede=CA−CC; interação=AA−AC−CA+CC;
  total=AA−CC. Publicar também efeitos condicionais AA−CA e AA−AC.
  Interação não alocada arbitrariamente como parcela de um canal.
- Conferir diagonais com T2 arquivado (tolerância de serialização 1e-12).
- Instrumentar médias de mu_cog/mu_rede e duração efetiva para leitura do canal,
  sem atribuir causalidade de mediador apenas por correlação.
- Após B1, rodar novamente identidade. Não iniciar outro item enquanto um
  controle obrigatório falhar. Nenhuma nova onda HM, ajuste de V_mod ou ajuste
  a Rieskamp. Permanecem as regras da ordem 37.
