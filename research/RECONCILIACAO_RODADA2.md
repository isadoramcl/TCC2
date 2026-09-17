# Reconciliação dos documentos preservados — rodada 2

Em 15/09/2026, os três documentos em `research/preservacao_rodada2/` foram
comparados integralmente com as versões vivas após o rebase sobre `dc8721f`.
A preservação havia sido registrada no commit `7fd2e48` antes do rebase.

Resultado da comparação feita imediatamente após o rebase:

- `README.md`: naquele ponto, todo o conteúdo preservado permanecia e a versão
  viva acrescentava a resposta à revisão e atualizações de continuidade.
- `docs/especificacao_modelo.md`: todo o conteúdo preservado permanece; a versão
  viva acrescenta apenas a nota inicial de resposta à revisão.
- `docs/registro_de_decisoes.md`: todo o conteúdo preservado permanece; a versão
  viva acrescenta apenas a nota inicial de resposta à revisão.

Depois dessa conferência, a fase 1 do MVP reescreveu deliberadamente no README
o estado da publicação, a referência ao documento oficial e a ordem de
prioridades. Por isso, o README atual já não deve ser descrito como mera soma de
notas ao texto preservado. A cópia em `research/preservacao_rodada2/README.md`
é o snapshot que garante a preservação integral do conteúdo anterior.

Os dois documentos vivos em `docs/` não foram alterados por esta reconciliação
nem pela fase 1; seus snapshots em `research/preservacao_rodada2/docs/` preservam
integralmente o estado anterior ao rebase.
