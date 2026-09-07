# Instruções do projeto — TCC2 Isadora

> **Cole este arquivo no campo de instruções personalizadas do projeto.**
> Ele é normativo: vale para toda sessão, sem precisar ser relembrado.

## O trabalho

TCC2 em Engenharia de Sistemas (UFMG), orientação do Prof. André Costa Batista.
Autora: Isadora Maria Carvalho Lopes. Simulação híbrida (Modelagem Baseada em
Agentes + Dinâmica de Sistemas) de equipes de projeto de engenharia: degradação
cognitiva, propagação de retrabalho e arranjos de governança.

O TCC1 foi a fase conceitual. O TCC2 é a implementação: calibração em dados
reais, simulador, experimento e calibração com avaliação de identificabilidade.

Repositório: `C:\Users\Isadora\Dev\TCC2` — `github.com/isadoramcl/TCC2` (privado).

## Regras invioláveis

Estas não são preferências. São o que sustenta a defesa do trabalho na banca.

1. **Dados brutos são imutáveis.** Nenhum arquivo em `data/raw/` é editado.
   Toda transformação é feita por código e registrada em log. A integridade é
   verificável por SHA-256.

2. **Nenhum número é digitado.** Todo valor que aparece em documento, figura ou
   tabela vem de um CSV ou do `config/parametros.yaml`, lido em tempo de
   geração. Isto é requisito, não estilo — ver a seção de lições abaixo.

3. **Toda decisão é rotulada por origem.** `[LIT]` literatura, `[TCC1]` fase
   conceitual, `[DEC]` decisão metodológica deste trabalho, `[CALIB]` derivado
   de dados, `[ABERTO]` não fixado, `[LIMITACAO]` limitação declarada.
   Uma decisão sem rótulo é uma decisão escondida.

4. **Fonte tem que existir e dizer o que se afirma.** Toda referência precisa de
   link verificável. Antes de citar, confira que a fonte sustenta exatamente a
   afirmação — e não uma parecida. Ver `04_FONTES.md`, que registra também o que
   cada fonte **não** sustenta.

5. **Quando texto e código divergirem, decida qual dos dois está errado.**
   Não basta fazê-los concordar. Alterar a especificação para descrever o que o
   código faz é maquiar defeito. Justifique a direção escolhida.

6. **Resultado isolado que contraria todos os outros é suspeita de defeito de
   medida até prova em contrário** — não é achado.

7. **Nada de "corrigi e passou" sem antes testar o teste.** Ver lições.

8. **A autora precisa conseguir explicar cada linha para a banca.** Nada entra
   sem que ela entenda o porquê. Se um trecho não puder ser defendido oralmente,
   ele não serve, por mais correto que seja.

## Lições pagas caro — não repetir

Cada uma destas custou retrabalho real. Estão aqui porque são erros que se
repetem sozinhos.

**Número digitado em texto sempre apodrece.** A matriz de cenários da primeira
Entrega 1 trazia quatro valores de parâmetro escritos à mão. Três estavam
errados e um tinha o sentido invertido entre os braços. O documento era
internamente coerente, então nenhuma revisão de texto detectou. Só apareceu
quando alguém abriu o `parametros.yaml`. Hoje essa tabela é montada a partir do
YAML e o gerador falha se alguém tentar digitar valor.

**Renumerar quebra referência cruzada em silêncio.** Ao inserir uma equação no
meio do documento, sete referências cruzadas quebraram. Hoje o gerador resolve
tudo por identificador simbólico (`E('d_index')`, `T('cenarios')`,
`F('nroy')`) e **interrompe a geração** se algo não fechar.

**Verificador não testado dá falsa confiança.** A auditoria automática dessas
mesmas sete referências devolveu "todas as citações resolvem". O padrão de busca
casava com `Equação 17` mas não com `equação (17)`. Regra: **antes de confiar
num verificador, alimente-o com um caso que ele deveria pegar e confirme que
ele pega.**

**Teste que não pode falhar não é evidência.** Verificações que passam por
construção devem ser declaradas como tal. Uma verificação de retrabalho
"aprovada" foi checada depois e passava para qualquer valor do parâmetro que
ela deveria restringir — não restringia nada.

**Limiar escolhido para o teste passar é fraude estatística.** Quando um teste
falha, a pergunta é se o teste está subdimensionado ou se o modelo está errado —
nunca "qual tolerância faz passar". Um teste de tendência foi refeito com mais
níveis e repetições, e isso ficou registrado como correção de delineamento.

**Config declarada e nunca lida engana o leitor.** Existem parâmetros no YAML
que nenhum script lê. `src/modelo/06_exportar_parametros.py` os detecta e também
sinaliza nomes declarados em mais de uma seção, que é a armadilha pior: a busca
textual encontra o nome e conclui que é lido, mas quem é lido é o homônimo.

## Como trabalhar

- **Branch.** Trabalhe em branch (`revisao-auditoria` ou similar). Não commite
  direto no `main`.
- **Git é da autora.** Não rode `git add/commit/push` por ela — já houve
  travamento por `.git/index.lock`. Comandos de leitura (`git status`) tudo bem.
- **Toda mudança de número publicado vem com tabela ANTES/DEPOIS.** Nenhum
  número muda em silêncio.
- **Entregue diff/patch**, não arquivos soltos.
- **Se discordar, pare e relate.** Não decida sozinho o que muda o que o modelo
  afirma — esses itens estão marcados no `02_ORDEM_DE_SERVICO.md`.

## O que este projeto contém

| arquivo | para quê |
|---|---|
| `00_INSTRUCOES_DO_PROJETO.md` | este arquivo: regras e lições |
| `01_ESTADO_DO_TRABALHO.md` | o que está pronto, verificado e quebrado hoje |
| `02_ORDEM_DE_SERVICO.md` | o backlog consolidado das três revisões |
| `03_COMANDOS_MATRIZ.md` | prompts reutilizáveis para as operações comuns |
| `04_FONTES.md` | referências com link, e o que cada uma NÃO sustenta |
| monografia do TCC1 | **consulta apenas.** Não editar |

**O documento que se edita é a Entrega 1** (`docs/entrega1_*.docx`), e ela é
gerada por `docs/gerar_entrega.js`. Editar o `.docx` no Word quebra a garantia
de reprodutibilidade e a próxima geração apaga a edição. Mudanças vão no script.
