

## Retomada autorizada — exceção de plataforma registrada antes dos cantos mistos

A autora informou ter verificado em Linux x86, Python 3.10 e NumPy 2.2.6, as oito combinações de instância/arranjo da semente 3: `competencia_minima_inicial` reproduziu `0x1.f251dbea89292p-3`, idêntico ao arquivo. A causa foi identificada pela autora como arredondamento de plataforma no `rng.normal` inicial. **Proveniência:** verificação externa comunicada pela autora nesta sessão; não executamos Linux nem recebemos seu log bruto. A conferência local independente demonstra que o parser não explica a diferença e que não há diferença nos campos dinâmicos arquivados das 960 execuções controladas. Isso não prova identidade de todos os estados internos ou de outras configurações.

**Ambiente desta execução:** Python 3.12.14 (Clang 22.1.3), NumPy 2.5.2, macOS ARM64. Valor local: `0x1.f251dbea89293p-3`; diferença positiva de 1 ULP.

**Novo critério, autorizado pela autora:** todos os campos devem continuar idênticos por `float.hex()` (textos/bools por igualdade), com exceção exclusiva de `competencia_minima_inicial`, que admite distância de até 1 ULP. Qualquer outra diferença interrompe a análise. Não aplicamos tolerância global nem alteramos referências, sorteios ou parâmetros.

Revalidação integral concluída antes de executar os cantos mistos: **960/960 controles aprovados pelo critério atualizado**, 49.440 comparações de campos, 240 exceções de exatamente 1 ULP apenas na competência mínima inicial, zero diferenças não permitidas. Evidência: `fatorial_completo/controle_criterio_atualizado.json`. O critério original e as duas interrupções permanecem preservados como histórico; o estado atual é retomado sob a autorização acima. A amostra, a semente e os testes de H1–H3 permanecem os do pré-registro.
