# T-B2.1 e T-B2.2 — protocolo anterior à execução

Solicitação direta da autora, 18/09/2026. Antes de continuar o bloco C.

## T-B2.1

Selecionar exatamente as 36 execuções incompletas da grade B2 arquivada,
sem alterar instância, semente, cenário, canal ou tau_sat/s_transicao.
Dobrar limite_horizonte_fator de 256 para 512 (horizonte automático já ativo).
Reexecutar desde o início; não reutilizar um estado truncado. Registrar contagem
que completa, contadores, tarefas executadas e estado terminal. Comparar o prefixo
observável do resultado anterior: makespan anterior=256*CPM e entradas idênticas.
Não alterar código do simulador. Persistência no dobro é evidência de bloqueio
estrutural no desenho testado, não prova de impossibilidade em horizonte infinito.

## T-B2.2

N da grade=576 (nominal separado, N=768). Tabular completude por cenário, canal,
tau_sat, s_transicao, e cruzamento de todos. Preservar linhas incompletas.
Recalcular cinco contrastes A−C dentro de cada combinação canal/tau/s usando
somente pares instância/semente em que AMBOS concluíram. Informar N pares previsto,
retido, excluído, n instâncias retidas, sementes por instância. IC95 t sobre médias
por instância retida; se n<2, IC indefinido. Estimando condicional à conclusão,
não efeito incondicional da governança nem hipótese de ausência ao acaso.
Publicar também médias marginais completas por braço, com N, como descritivas.
Nominal sem censura não depende dessa exclusão; conferir separadamente.
Recalcular também após substituir somente as 36 linhas pela execução dobrada.

## Controles

Teste de filtro pareado rejeita combinação de braços de sementes diferentes;
controle sintético com uma instância não produz IC. Verificar 36 chaves únicas,
N=576 e N=768, nenhuma substituição de linha completa e nenhum parâmetro alterado
além do limite. Rodar identidade bit a bit; não iniciar bloco C neste diagnóstico.
Não inferir equivalência causal a Pessoa et al. apenas pela assinatura de não
conclusão: conferir fonte primária e distinguir mecanismos.
