# Parecer 28 — Cronograma até 29/11, com congelamento da simulação

**Data:** 17/09/2026 · **Revisor:** Claude

| Marco | Data | Dias a partir de 17/09 |
|---|---|---:|
| Documento modelo / ponto de controle | 27/09 | 10 |
| Entrega da marcação da defesa | 25/10 | 38 |
| Texto inicial da monografia | 08/11 | 52 |
| Entrega final | 29/11 | 73 |

---

## 1. A decisão estruturante

**Congelar a simulação em 27/09.** Depois dessa data, nenhum experimento novo, nenhum
parâmetro novo, nenhuma métrica nova. Só escrita, verificação de fontes e revisão.

Motivo: a simulação está madura. O que falta para a monografia não é resultado — é
texto. E todo experimento rodado depois de 27/09 obriga a reescrever o que já estava
escrito, que é o modo clássico de perder novembro.

O único item técnico que ainda vale rodar é o **T4** (separar portão de canal difuso),
porque ele fecha a leitura do mecanismo principal. Se não couber até 27/09, entra como
trabalho futuro e a redação usa a leitura atual, que já é defensável.

## 2. Fase 1 — até 27/09 (10 dias)

| Item | Quem | Por que agora |
|---|---|---|
| **T4**: quatro células `tau_portao` × `tau_rede`, reporte igualado | Codex | Fecha se o efeito sobre falha real passa pela assistência ou pelo canal difuso. Maquinaria pronta. |
| **Ler o precedente ABM+SD e escrever o delta (D-13)** | Isadora | **Maior risco isolado do trabalho.** Não depende de nada. Meia página. |
| **Consolidar fontes novas em `04_FONTES.md`** | Isadora | Toda fonte do Word 18 que não está lá, no formato dele, com a linha do que **não** sustenta |
| **Verificar Edmondson (1999)** na fonte primária | Isadora | Está marcada NÃO VERIFICADA e é central para o argumento de segurança psicológica |
| Montar o documento de ponto de controle | Isadora | Material já existe; é montagem, não produção |

Do lado técnico, o ponto de controle já tem tudo: modelo implementado e verificado,
identidade bit a bit, 44 testes, invariantes, resultados com IC, contrato observacional,
e um histórico de auditoria com oito retratações registradas. Isso é mais rigor do que
a maioria dos TCCs de simulação apresenta.

## 3. Fase 2 — 27/09 a 25/10 (4 semanas): escrever os capítulos difíceis

Ordem sugerida, do mais arriscado para o menos:

**Semana 1 — Introdução e posicionamento.** É o capítulo que hoje não existe e é onde
a banca ataca. Precisa responder: o que já foi feito (precedente ABM+SD com ciclos de
retrabalho, Crowder et al., a revisão sistemática de SoS que está nos arquivos do
Projeto), e o que **este** trabalho acrescenta — degradação cognitiva por porta de
decisão, arranjos de governança contrastados e decompostos, e ancoragem externa
tentada e documentada.

**Semana 2 — Resultados de governança.** Na forma da seção 4 do parecer 27. O que pode
e o que não pode ser afirmado, com a tabela de decomposição. Inclui o achado não óbvio:
em limiar alto com reporte baixo, abrir o portão **aumenta** o atraso.

**Semana 3 — Verificação e validação.** É o ponto alto do trabalho e deve ser escrito
como tal: controle de identidade bit a bit, controles negativos no verificador,
protocolo registrado antes de executar, e as retratações. Um capítulo que mostra
afirmações retiradas porque não sobreviveram ao teste vale mais que um que só mostra
acertos.

**Semana 4 — Limitações e o contrato observacional.** Transformar a ausência de
calibração em contribuição declarada, usando o parecer 22 como artefato. Mais a rota
alternativa: modelagem orientada a padrões (Grimm et al. 2005).

## 4. Fase 3 — 25/10 a 08/11 (2 semanas): fechar o texto inicial

Método, modelo conceitual, implementação, resumo/abstract, conclusão. São os capítulos
mais mecânicos e podem ser escritos rápido porque a documentação existe: `docs/
especificacao_modelo.md`, `docs/registro_de_decisoes.md` e os pareceres 09 a 27.

## 5. Fase 4 — 08/11 a 29/11 (3 semanas): revisão

- **Auditoria de citações.** Cada afirmação da monografia contra `04_FONTES.md`.
  Nenhuma pode se apoiar em fonte marcada NÃO VERIFICADA ou METADADOS CONFERIDOS.
  Esta é a semana que protege você juridicamente e não pode ser comprimida.
- Coerência numérica: todo número do texto conferido contra o CSV que o gerou.
- Formatação, normas, revisão de língua.
- Folga para imprevisto — e vai haver.

## 6. O que fica de fora, declarado como limitação

Não tentar fechar. Cada um exige dado externo que não existe em forma compatível, e
tentar consome o prazo sem fechar:

- **G-01** — comparador de retrabalho em esforço fora do domínio de software;
- **G-02** — ponte de agregação do HEART (passo elementar × pacote de trabalho);
- **G-03** — validação externa de P(heurístico | pressão, dificuldade);
- **Calibração e novas ondas de History Matching** — o vetor z não está habilitado;
- **Reposicionamento dos cenários próximo ao limiar** — interessante, não é
  pré-requisito;
- **Recálculo do gradiente sobre linhas de código (D-06)** — se couber na Fase 1, ótimo;
  senão, declarar que o gradiente está em eixo confundido por tamanho.

Essas seis viram uma seção de trabalhos futuros que é, ela própria, contribuição:
cada uma vem com o critério preciso que uma fonte teria de satisfazer.

## 7. Regras que protegem o prazo

1. **Nenhum experimento novo depois de 27/09.** Se aparecer uma ideia boa, ela vira
   trabalho futuro, não uma rodada.
2. **Escrever antes de aperfeiçoar.** Capítulo fraco escrito vale mais que capítulo
   perfeito planejado.
3. **A auditoria de citações da Fase 4 não é comprimível.** Se algo tiver de ceder,
   que ceda no polimento, nunca aí.
4. **Se um resultado novo contradisser texto já escrito**, a pergunta é "isso muda a
   conclusão?". Se não muda, vira nota de rodapé. Só se mudar é que se reescreve.
