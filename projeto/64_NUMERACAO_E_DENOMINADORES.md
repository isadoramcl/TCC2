# F — numeração e denominadores

`07_AUTONOMIA.md` foi renomeado para `00_AUTONOMIA.md`; briefing mantém
`07_BRIEFING_ORIENTADOR.md`. Ponteiros atuais README/08 atualizados. Referências
nos pareceres históricos preservam o nome vigente à época, com este mapa.

## Correções de leitura da bancada

- `taxa_reversao_pct = 100*base.reverted.mean()` significa percentagem de commits
  **que foram revertidos**, não percentagem de commits que são reversões.
  Publicação correta requer numerador de alvos revertidos na mesma base e
  `N=len(base)`. N da base **pendente**: arquivos da bancada não localizados no
  clone nem na pasta local de TCC. Não inferir N arredondando 496/1,058%; não usar
  579 reversões como numerador de alvos ou 67.313/45.859 como denominadores sem
  confirmar os filtros. A percentagem 1,058% não foi independentemente verificada.
- Tênis: CSV referido no parecer 31 mede dupla falta por **todos os pontos**,
  0,1035→0,1020 (−0,15 p.p.). Relatório referido mede dupla falta **condicional ao
  segundo saque**, 0,2771→0,2665 (−1,06 p.p.). São denominadores diferentes;
  rotular assim, jamais apresentar como tabelas equivalentes. Arquivos originais
  não localizados, logo não houve edição nem revalidação das tabelas originais.

Fonte de ambas as retificações: parecer 31 local; números acima são os reportados
pelo revisor, não nova medição. F permanece parcial até obter a base e artefatos.
Três controles de identidade aprovados; sem alteração dinâmica.
