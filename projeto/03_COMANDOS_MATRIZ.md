# Comandos matriz

Prompts reutilizáveis. Copiar, preencher o que estiver entre `<>`, colar.

Todos pressupõem que as instruções do projeto (`00`) estão carregadas.

---

## M1 · Abrir sessão de trabalho

> Vou trabalhar no TCC2. Antes de qualquer alteração:
>
> 1. Rode `git --no-optional-locks status --short` e `git log -1` e me diga em
>    que estado o repositório está e se há coisa não commitada.
> 2. Leia `02_ORDEM_DE_SERVICO.md` e me diga quais itens estão abertos, na ordem
>    recomendada.
> 3. Rode o pipeline inteiro num ambiente limpo e me diga o que quebra.
>
> Só depois disso proponha o que fazer. Não comece a editar antes de me mostrar
> o estado.

---

## M2 · Executar um item da ordem de serviço

> Execute o item `<A1>` de `02_ORDEM_DE_SERVICO.md`.
>
> Regras:
> - Branch `revisao-auditoria`. Não commite no `main`.
> - Se a correção mudar qualquer número publicado, traga tabela ANTES/DEPOIS.
> - Se durante a correção você descobrir que o problema é outro, **pare e
>   relate** em vez de corrigir o que você acha que é.
> - Ao terminar, mostre o diff e me diga o que você verificou para afirmar que
>   está correto — e como testou que essa verificação funciona.

---

## M3 · Antes de afirmar que está correto

> Você acabou de dizer que `<afirmação>`.
>
> Antes de eu aceitar:
> 1. Como você verificou isso?
> 2. Você testou o verificador contra um caso que ele **deveria** pegar? Mostre
>    o teste falhando quando deve falhar.
> 3. Se a verificação é por busca textual, ela cobre todas as grafias possíveis?
>    (Já perdemos sete referências cruzadas porque o padrão casava com
>    `Equação 17` e não com `equação (17)`.)
> 4. O que essa verificação **não** cobre?

---

## M4 · Divergência entre texto e código

> Encontrei divergência entre `<texto/especificação>` e `<código>`.
>
> Não faça os dois concordarem. Responda primeiro:
> 1. Qual dos dois está errado, e por quê?
> 2. Se o código está errado: qual o efeito de corrigi-lo nos resultados
>    publicados? Meça antes de mexer.
> 3. Se o texto está errado: o que exatamente a fonte original ou o TCC1 dizem?
>    Cite o trecho.
> 4. Alterar a especificação para descrever o que o código faz é maquiar
>    defeito. Se for esse o caso, diga.

---

## M5 · Item do Bloco C (muda o que o modelo afirma)

> Item `<C1>`. **Não implemente no branch principal.**
>
> 1. Implemente num branch separado.
> 2. Meça o impacto em todos os indicadores publicados: tabela ANTES/DEPOIS.
> 3. Diga o que você recomenda e por quê.
> 4. Diga o que a autora perde se **não** fizer.
> 5. Não faça merge. A decisão é dela.

---

## M6 · Verificar uma fonte antes de citar

> Quero citar `<fonte>` para sustentar `<afirmação>`.
>
> 1. A fonte existe? Link verificável.
> 2. Ela diz exatamente isso, ou diz algo parecido? Cite o trecho.
> 3. A unidade bate? (Já erramos comparando razão de **esforço** contra razão de
>    **custo sobre valor de contrato**.)
> 4. O domínio bate? Se não, a transposição está justificada?
> 5. O verbo está certo? "Valida" é diferente de "propõe e ilustra".
> 6. Atualize `04_FONTES.md` com o que a fonte **não** sustenta.

---

## M7 · Regerar a Entrega 1

> Regere a Entrega 1.
>
> Pré-requisitos, confira antes:
> - Os números pararam de se mexer? Se algum item de B ou C ainda vai rodar,
>   **não regere ainda**.
> - `06_exportar_parametros.py` foi executado depois da última mudança no YAML?
>
> Ao gerar:
> - `node docs/gerar_entrega.js`. A geração **falha** se alguma citação não
>   resolver — se falhar, conserte a causa, não a mensagem.
> - Renderize para PDF e **olhe as páginas**. Colisão de rótulo em figura só
>   aparece olhando.
> - Rode a auditoria de referências cruzadas em **ambas** as grafias.
> - Confira que todo número do documento tem origem em CSV ou YAML.

---

## M8 · Pente-fino antes de mandar ao orientador

> Vou mandar `<documento>` ao Prof. André. Antes:
>
> 1. Existe algum número no documento que não venha de CSV ou do YAML? Liste.
> 2. Existe alguma afirmação de resultado que dependa de um teste que passa por
>    construção? Liste.
> 3. Existe alguma conclusão mais forte do que a evidência permite? Cite a frase
>    e proponha a versão defensável.
> 4. Quais são as três perguntas que a banca faria primeiro e que o documento
>    **não** responde bem?
> 5. Toda limitação conhecida está declarada no documento, ou só no registro
>    interno?

---

## M9 · Fechar sessão

> Antes de encerrar:
> 1. Atualize `02_ORDEM_DE_SERVICO.md` com o status real de cada item tocado.
> 2. Atualize `01_ESTADO_DO_TRABALHO.md` se algo saiu de "quebrado" ou entrou.
> 3. Liste o que você **tentou e não conseguiu** verificar.
> 4. Me dê os comandos de git para eu rodar (não rode você).

---

## M10 · Revisão adversarial (para pedir a outra IA)

> Revisão **adversarial** do TCC2 em anexo. Seu objetivo é encontrar erro, não
> me tranquilizar.
>
> - Para cada problema: o que está errado, por quê, gravidade
>   [FATAL/GRAVE/MENOR], e o que fazer.
> - Separe "isto está errado" de "isto é defensável mas eu faria diferente".
> - Se não puder verificar sem rodar o código, diga — não chute.
> - Ao final: as 3 perguntas que uma banca faria primeiro e que o texto não
>   responde.
>
> Ataque primeiro: a atribuição causal do experimento; a transferência de risco
> entre domínios; os testes que passam por construção; e todo número que não
> tenha origem rastreável.
>
> **Aviso:** se você só tiver o meu documento e não as fontes originais, você vai
> me confirmar, porque estará me lendo citar a mim mesma. Diga explicitamente o
> que você não teve como verificar.
