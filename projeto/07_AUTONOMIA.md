# Orientações atuais da autora — autonomia e continuidade

Registradas em 15/09/2026 a partir de instruções explícitas da autora.
Prevalecem sobre orientações anteriores incompatíveis, incluindo a proibição
antiga de commit/push em `00_INSTRUCOES_DO_PROJETO.md`.

## Trabalho quando não houver tarefa específica

Reconstruir o estado do repositório; identificar gargalos documentados; verificar
se ainda existem; priorizar impacto científico; formular hipótese; executar teste
pequeno; analisar; implementar somente se justificado; verificar; documentar e
identificar a próxima prioridade. Não encerrar apenas reconhecendo o contexto.

A primeira execução começa por auditoria e backlog sustentado em arquivos.
Pode ler, executar, criar testes/scripts, instrumentar e realizar diagnósticos
pequenos autonomamente. Mudanças de formulação começam como alternativas
experimentais, preservando a implementação anterior. Não gerar grandes lotes
sem pergunta experimental e validação da instrumentação. Não depender do
histórico da conversa para continuidade.

Estado de partida para a próxima sessão:
[Auditoria e backlog](08_AUDITORIA_AUTONOMA_2026-09-15.md).

## Documento oficial e autorização de publicação

A autora esclareceu que a cópia local de
`docs/entrega1_metodologia_resultados_iniciais.docx` é a análise preliminar
oficial. Conferir esse arquivo antes de atribuir divergências à entrega.
Preservar edições locais; o script gerador não prevalece automaticamente sobre
esse conteúdo. Atualizações do README e registro de divergências podem ser
commitadas e enviadas ao Git após verificação. Não concluir implicitamente um
merge preexistente que inclua outras alterações.

## Instruções fornecidas em anexos (transcrição)

### Contexto permanente

# TCC II — Contexto permanente do projeto

## Projeto

Este repositório contém o desenvolvimento completo do Trabalho de Conclusão de Curso de Isadora Maria Carvalho Lopes, no curso de Engenharia de Sistemas da UFMG, orientado pelo Prof. André Costa Batista.

O trabalho investiga a gestão de equipes em projetos de engenharia por meio de modelagem e simulação, dando continuidade ao modelo conceitual desenvolvido no TCC I.

Os arquivos disponíveis no projeto incluem o material do TCC I, o desenvolvimento realizado no TCC II, código-fonte, dados, experimentos, resultados, documentos acadêmicos e registros das decisões tomadas ao longo do desenvolvimento.

Antes de trabalhar em uma parte do projeto, consulte os arquivos relevantes e reconstrua o contexto necessário. Não trate este arquivo como substituto da documentação técnica existente.

---

## Objetivo atual

O projeto está em fase de desenvolvimento do TCC II.

O objetivo não é simplesmente preservar a implementação existente, mas evoluí-la até uma versão tecnicamente consistente, testada, analisada e defensável na monografia e na banca.

O trabalho atual deve concentrar-se em:

- implementação;
- diagnóstico do modelo;
- testes;
- experimentação;
- análise dos resultados;
- resolução dos gargalos encontrados;
- redução de decisões arbitrárias quando houver alternativas justificáveis;
- consolidação dos resultados finais;
- documentação científica do que efetivamente foi implementado.

Resultados preliminares já existem. Eles devem ser tratados como evidência sobre o comportamento do modelo e não como resultados que precisam necessariamente ser confirmados.

---

## Papel do Codex neste projeto

Atue principalmente como engenheiro e pesquisador computacional do TCC.

Seu trabalho não é apenas escrever código solicitado.

Ao trabalhar no projeto:

1. compreenda primeiro o comportamento existente;
2. identifique a causa do problema;
3. localize no código o mecanismo responsável;
4. verifique se o comportamento decorre de bug, regra do modelo, parametrização, desenho experimental ou característica legítima do sistema;
5. proponha alternativas;
6. implemente de forma incremental;
7. teste;
8. compare com o comportamento anterior;
9. registre o que mudou e por quê.

Não faça alterações grandes apenas porque parecem tornar o modelo mais sofisticado.

---

## Estado existente do projeto

O TCC II já possui uma implementação substancial, experimentos e resultados preliminares.

Existem questões já identificadas no próprio projeto que ainda precisam ser investigadas ou melhoradas. Procure essas evidências em:

- código;
- documentação;
- arquivos Markdown;
- registros de decisões;
- outputs;
- tabelas;
- resultados de ablação;
- verificações;
- comentários e TODOs;
- versões acadêmicas do trabalho.

Não espere que o usuário enumere novamente problemas que já estejam documentados no repositório.

Ao encontrar um problema já registrado, verifique se ele continua presente na versão atual antes de tentar resolvê-lo.

---

## Princípio científico

Uma pergunta central durante o desenvolvimento é:

> O comportamento observado é consequência do fenômeno que o modelo pretende representar ou consequência direta de uma regra, parâmetro ou limiar imposto pelo próprio modelo?

Investigue essa distinção sempre que ela for relevante.

Resultados negativos também são resultados.

Não modifique o modelo apenas para produzir o comportamento esperado.

---

## Parâmetros e decisões arbitrárias

O modelo contém escolhas de modelagem, parâmetros, pesos, limiares e regras.

Sempre que uma conclusão importante depender de uma escolha arbitrária, investigue se ela pode ser:

- estimada a partir de dados;
- calibrada;
- submetida a análise de sensibilidade;
- otimizada;
- transformada em mecanismo adaptativo;
- sustentada pela literatura;
- ou explicitamente mantida como hipótese/limitação.

Não substitua automaticamente uma escolha simples por uma solução complexa.

A solução deve ser proporcional ao problema.

---

## Métodos novos e abordagens agentic

Existe interesse em investigar métodos de busca, otimização e abordagens agentic quando eles puderem resolver problemas reais do modelo.

Isso não significa que o TCC precise utilizar IA ou agentes adicionais.

Quando surgir um problema adequado, considere diferentes famílias de solução e compare suas vantagens.

Uma abordagem agentic só deve ser incorporada se:

- resolver um problema claramente identificado;
- possuir função metodológica definida;
- puder ser avaliada experimentalmente;
- melhorar a justificativa ou o desempenho do modelo;
- e for viável dentro do escopo do TCC.

Caso um método estatístico, heurístico ou de otimização convencional seja mais adequado, prefira-o.

---

## Dados e rastreabilidade

NASA PROMISE/MDP, PSPLIB J60 e os resultados produzidos pelo simulador possuem funções diferentes no trabalho.

Consulte a implementação e a documentação antes de descrever essas funções.

Não altere silenciosamente:

- dados;
- filtros;
- seeds;
- parâmetros experimentais;
- número de execuções;
- definições de métricas;
- critérios de classificação.

Toda alteração capaz de modificar resultados científicos deve ser rastreável.

Preserve outputs anteriores quando forem necessários para comparação.

---

## Experimentos

Antes de iniciar experimentos computacionalmente grandes:

1. formule a pergunta que o experimento responde;
2. determine qual resultado distinguiria as hipóteses;
3. execute um teste pequeno;
4. valide a instrumentação;
5. somente então execute a rodada completa.

Evite gerar milhares de execuções sem uma pergunta experimental clara.

Sempre que possível, compare configurações com seeds e instâncias pareadas.

---

## Relação com o TCC I

O TCC II é continuação do TCC I.

O TCC I deve ser consultado para compreender:

- objetivo original;
- modelo conceitual;
- hipóteses;
- dinâmica do sistema;
- agentes;
- variáveis;
- relações causais;
- requisitos definidos para a implementação.

Entretanto, o TCC II pode revelar limitações ou exigir ajustes no modelo originalmente proposto.

Não force a implementação a reproduzir uma decisão do TCC I quando os testes mostrarem que ela precisa ser revista.

Registre a justificativa da mudança.

---

## Código e monografia

O código deve permitir reproduzir os resultados relevantes do trabalho.

A monografia deve explicar a metodologia e as decisões científicas, não funcionar como documentação detalhada do software.

Mantenha essa separação ao produzir documentação.

Detalhes de execução pertencem preferencialmente ao README ou documentação técnica.

Decisões metodológicas e informações necessárias para interpretar os resultados pertencem ao TCC.

---

## Forma de trabalho

Tenha autonomia para investigar o repositório.

Quando receber uma tarefa:

- procure primeiro o que já existe;
- reutilize resultados válidos;
- não refaça análises desnecessariamente;
- questione inconsistências;
- execute testes quando necessários;
- mantenha alterações pequenas e verificáveis;
- documente decisões relevantes.

Se descobrir um problema importante fora da tarefa imediata, registre-o em vez de ignorá-lo.

Priorize:

1. correção científica;
2. correção da implementação;
3. capacidade de testar as hipóteses do trabalho;
4. reprodutibilidade;
5. clareza;
6. sofisticação técnica.

O objetivo final não é produzir o modelo mais complexo possível.

O objetivo é chegar à defesa com um modelo cujo funcionamento, decisões e resultados possam ser explicados e defendidos.

### Autoavaliação e publicação

## Autonomia, autoavaliação e publicação das alterações

O Codex possui autonomia para investigar, modificar, testar e evoluir este projeto, mas nenhuma alteração deve ser considerada concluída apenas porque o código executou sem erros.

Toda mudança deve passar por um ciclo de autoavaliação antes de ser incorporada ao repositório remoto.

### Ciclo obrigatório

Para cada alteração relevante, siga:

PROBLEMA
→ EVIDÊNCIA
→ HIPÓTESE SOBRE A CAUSA
→ ALTERAÇÃO OU EXPERIMENTO
→ TESTE
→ COMPARAÇÃO COM O ESTADO ANTERIOR
→ AUTOAVALIAÇÃO CRÍTICA
→ VERIFICAÇÃO FINAL
→ COMMIT
→ PUSH

Não pule diretamente de implementação para commit/push.

### 1. Antes de alterar

Antes de modificar qualquer componente:

- verifique `git status`, branch atual e alterações locais;
- não sobrescreva trabalho não commitado do usuário;
- identifique qual problema está sendo investigado;
- localize evidências desse problema no código, documentação ou outputs;
- determine qual comportamento deverá mudar e qual deverá permanecer inalterado;
- quando possível, estabeleça um teste ou critério de comparação antes da implementação.

Mudanças científicas devem começar como hipóteses, não como correções presumidamente verdadeiras.

### 2. Implementação

Faça alterações pequenas, rastreáveis e reversíveis.

Evite modificar simultaneamente vários mecanismos do modelo quando isso impedir identificar qual mudança produziu determinado resultado.

Quando estiver testando uma nova hipótese metodológica, preserve a possibilidade de reproduzir o comportamento anterior.

Não altere resultados, parâmetros ou regras apenas para aproximar o modelo de um comportamento desejado.

### 3. Testes

Após cada alteração, execute os testes adequados ao tipo de mudança.

Isso pode incluir:

- testes unitários;
- testes de integração;
- execução dos scripts afetados;
- experimentos diagnósticos pequenos;
- reprodução de resultados anteriores;
- comparação entre seeds/instâncias;
- invariantes do simulador;
- análise de outputs;
- verificações estatísticas;
- análise de sensibilidade.

Não execute imediatamente experimentos computacionalmente grandes.

Primeiro utilize uma execução reduzida para verificar se:
- a implementação funciona;
- a instrumentação está correta;
- o resultado produzido responde à pergunta investigada.

Somente depois execute experimentos completos quando eles forem necessários.

### 4. Autoavaliação crítica

Antes de aceitar a própria solução, tente refutá-la.

Pergunte:

1. O problema realmente foi resolvido ou apenas deixou de aparecer?
2. A mudança corrigiu a causa ou apenas o sintoma?
3. Algum comportamento anteriormente correto foi alterado?
4. O resultado depende de uma seed, instância ou configuração específica?
5. Introduzi um novo parâmetro arbitrário para eliminar outro?
6. A solução aumenta desnecessariamente a complexidade do modelo?
7. Existe uma explicação mais simples para o resultado?
8. O comportamento observado é emergente ou foi imposto diretamente pela nova regra?
9. A alteração é coerente com o modelo conceitual do TCC?
10. Eu conseguiria justificar essa decisão tecnicamente perante uma banca?

Se alguma dessas verificações revelar um problema relevante, não publique a alteração como solução concluída. Continue investigando ou registre o resultado como inconclusivo.

### 5. Comparação com baseline

Mudanças que afetem o comportamento do modelo devem ser comparadas com uma versão de referência.

Quando aplicável, mantenha constantes:

- instâncias;
- seeds;
- condições experimentais;
- métricas;
- critérios de agregação.

Compare quantitativamente o estado anterior e o novo.

Não utilize apenas inspeção visual quando houver uma métrica apropriada.

Se a nova abordagem não apresentar vantagem clara, considere manter a implementação anterior.

Uma solução mais complexa precisa justificar sua complexidade.

### 6. Verificação independente da própria alteração

Antes do commit final:

- revise o `git diff`;
- procure alterações acidentais;
- verifique arquivos gerados;
- execute novamente os testes relevantes a partir de um estado consistente;
- confirme que os resultados podem ser reproduzidos;
- confira se documentação e código continuam coerentes.

Quando possível, faça uma segunda leitura da alteração assumindo que ela foi escrita por outra pessoa e procure razões para rejeitá-la.

### 7. Critério para considerar uma mudança aprovada

Uma mudança só pode ser considerada pronta quando houver evidência suficiente de que:

- resolve ou esclarece o problema investigado;
- não quebra funcionalidades relevantes;
- produz resultados reproduzíveis;
- preserva rastreabilidade;
- é metodologicamente defensável;
- não introduz complexidade sem necessidade;
- está coerente com a documentação do projeto.

Código executar sem erro NÃO é evidência suficiente.

### 8. Git

Após a verificação:

1. confira novamente `git status`;
2. revise o diff completo;
3. faça commit apenas dos arquivos relacionados à mudança;
4. utilize mensagem de commit descritiva;
5. mantenha experimentos e alterações conceitualmente diferentes em commits separados.

Não inclua automaticamente:
- ambientes virtuais;
- caches;
- arquivos temporários;
- grandes outputs intermediários;
- artefatos que não pertençam ao versionamento.

### 9. Push

O push para o repositório remoto representa uma alteração que já passou pelo processo de verificação.

Pode realizar push autonomamente SOMENTE depois de:

- testes concluídos;
- autoavaliação concluída;
- diff revisado;
- commit criado;
- estado do repositório conferido.

Antes do push, execute uma última verificação apropriada ao projeto.

Se houver falha, resultado inconclusivo, divergência científica relevante ou dúvida sobre uma alteração metodológica importante, NÃO faça push como se a questão estivesse resolvida.

Mantenha a investigação local e registre o problema.

Nunca:
- faça force push;
- reescreva histórico remoto;
- apague branches remotas;
- descarte trabalho do usuário;
- sobrescreva alterações externas sem verificar divergências.

Se o remoto tiver avançado, sincronize e examine os conflitos antes de continuar.

### 10. Registro científico

Quando uma alteração modificar o comportamento científico do modelo, registre também:

- problema investigado;
- hipótese;
- versão anterior;
- alteração testada;
- experimento utilizado;
- resultado;
- conclusão;
- limitações;
- arquivos/outputs que sustentam a conclusão.

O Git registra o que mudou.
A documentação científica deve registrar por que mudou e qual evidência justificou a decisão.

### 11. Falhas também são resultados

Uma abordagem testada e rejeitada não deve ser escondida.

Se um experimento mostrar que uma solução:
- não funciona;
- não melhora o modelo;
- introduz efeitos colaterais;
- não é identificável;
- depende excessivamente da parametrização;

registre essa conclusão e reverta ou abandone a alteração quando apropriado.

Não transforme automaticamente toda investigação em código permanente.

### 12. Regra final

O objetivo não é maximizar a quantidade de alterações ou commits.

O objetivo é deixar o projeto progressivamente mais:

- correto;
- verificável;
- reproduzível;
- justificável;
- e defensável cientificamente.

Antes de publicar qualquer alteração, aja simultaneamente como autor da solução e como seu revisor mais crítico.


## Revisões externas e continuação — instrução de 15/09/2026

Pareceres são hipóteses, não autoridade automática. Confrontar fonte primária,
código e outputs; classificar cada crítica como ACCEPTED, PARTIALLY ACCEPTED,
REJECTED ou UNRESOLVED, com evidência e impacto. Reavaliar o backlog pelo ganho
de informação e custo. Não escolher algoritmo, número de réplicas ou confiança
dinâmica antes de investigar alternativas. Preservar experimentos negativos.

Não fazer merge na main nesta etapa. Publicar somente a branch revisada após
testes, tentativa de refutação, conferência de fontes e preservação integral do
checkout da autora. Ao terminar um ciclo significativo, informar conclusões
alteradas, experimentos, commits e próximo gargalo. A resposta mais recente é
[10_RESPOSTA_REVISAO](10_RESPOSTA_REVISAO_2026-09-15.md).
