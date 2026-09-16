# Relatório de instrumentação do MVP — 15/09/2026

## Arquivos

- `README.md`: estado do merge corrigido; prioridades reordenadas; snapshot
  apresentado como ponteiro; comando do verificador vivo documentado.
- `projeto/08_AUDITORIA_AUTONOMA_2026-09-15.md`: registro histórico atualizado
  com a sequência MVP → robustez → calibração/fragilidades e com o merge
  concluído em `dc8721f`.
- `src/modelo/04_gemeo_identico.py`: cabeçalho científico retificado quanto a
  `V_mod = 0`, z fixa, redução de `V_sim`, média exata e 64 réplicas.
- `research/verificar_documento_oficial.py`: CLI somente leitura que exige
  `--vivo`, confere snapshot e documento vivo contra o SHA-256 fixado e retorna
  código diferente de zero com diagnóstico útil em ausência ou divergência.
- `research/test_documento_oficial.py`: testes com fixtures temporárias para os
  casos igual, divergente e ausente, sem alterar o documento oficial.
- `research/RECONCILIACAO_RODADA2.md`: comparação dos três documentos
  preservados com suas versões vivas.

## Testes e verificações

O teste foi criado antes do verificador e falhou inicialmente porque o CLI ainda
não existia. Após a implementação:

```text
python3 -m unittest research/test_documento_oficial.py -v
Ran 3 tests
OK
```

Os hashes atuais de `docs/entrega1_metodologia_resultados_iniciais.docx` e do
snapshot são iguais a
`d5a658f1cdf03d99e6bdc0b5d03cb4aaa9420853ec7ebc2bb3f55e85a728c57d`.
A comparação integral por `diff -u`, feita antes das reescritas deliberadas da
fase 1, mostrou que o conteúdo preservado permanecia nos três documentos vivos.
O README foi depois atualizado quanto ao estado, ao documento oficial e às
prioridades; seu conteúdo anterior permanece integralmente no snapshot de
`research/preservacao_rodada2/`. Os dois documentos em `docs/` continuam apenas
com os acréscimos de notas já reconciliados.

## Ressalvas

- Nenhum DOCX foi editado ou regenerado.
- `docs/especificacao_modelo.md` e `docs/registro_de_decisoes.md` não foram
  modificados nesta tarefa.
- Não houve nova onda, commit ou push.
- O verificador certifica igualdade byte a byte com o snapshot fixado; não
  avalia semanticamente versões futuras nem escolhe qual cópia deve prevalecer.
