# 77 — Revisão da auditoria 76

**Data:** 22/09/2026 · **Revisor:** Claude

## Veredito

A auditoria 76 se sustenta nos itens 1, 3, 4, 5, 6, 7 e 8. Dois pontos precisam
de correção no registro.

## Item 2 — CONFIRMADO só na primeira metade

A reexecução das 384 células da v1 com identidade bit a bit está feita e é válida.
A segunda metade — rodar três scripts históricos e confirmar que reproduzem a
evidência deles — **não foi executada**, embora o veredito diga "conferidos":

- `a1_exec.log` termina em `KeyboardInterrupt`;
- `sat_gov_exec.log` e `crowder1_exec.log` têm uma linha: `command not found:
  timeout` (o comando não existe no macOS).

O veredito se apoiou em artefatos de controle **antigos**, que não testam a troca
para `config/mvp_v1.yaml`.

**O que fecha o item sem rodar os scripts** (verificado nesta revisão): o conteúdo
de `config/mvp_v1.yaml`, lido como YAML, é **idêntico** ao de `config/mvp.yaml` no
commit 09710d7 — só os comentários mudaram. E o diff dos três scripts contra
09710d7 troca apenas o caminho `mvp.yaml` → `mvp_v1.yaml`, em uma ou duas linhas
cada. Mesma configuração lida, mesmo código de simulação com as opções novas
desligadas (item 1) → mesma saída. Item 2 passa a **CONFIRMADO por equivalência
de entrada**, não por reexecução.

## Item 9 — já tratado

A divergência veio do enunciado da ordem de auditoria, que não dizia "em média".
Causa verificada e registrada em `projeto/75`, seção Auditoria: pedidos de ajuda
frustrados reduzem a confiança pela Eq. (4) de Crowder. Não é defeito.

## Pendência que a auditoria abriu

O teste discriminante proposto no item 7 — fatorial `portao_assistencia` ∈
{limiar, logístico} nas células em que a falha efetiva favorece o centralizado —
não foi executado. Fica como trabalho aberto; a monografia declara que a vantagem
em falha efetiva vale no ponto nominal, não no espaço de governança.
