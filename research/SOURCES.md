> **HISTÓRICO — não usar como catálogo.** Consolidado em
> `projeto/04_FONTES.md` em 20/09/2026. Mantido pelo registro das
> análises de Pukelsheim, McCulloch e Andrianakis, que continuam válidas.

# Fontes verificadas — resposta à revisão, 15/09/2026

Fonte primária e interpretação deste projeto são distinguidas abaixo. Não foram
revalidadas nesta rodada as fontes NASA, PSPLIB, Crowder, segurança psicológica
ou monotonicidade fuzzy; não atribuir a elas sustentação renovada.

## Pukelsheim (1994)

*The Three Sigma Rule*, The American Statistician 48(2), 88–91.
[DOI](https://doi.org/10.1080/00031305.1994.10476030),
[texto primário, repositório bibliográfico](https://d-nb.info/1186632208/34).
Metadados e texto consultados. Relação: **PARTIALLY SUPPORTED**.

A desigualdade é univariada, com densidade unimodal e variância finita; o limite
fora de três desvios é 4/81. Não fornece automaticamente cobertura conjunta ao
máximo de quatro estatísticas com variâncias estimadas. [INFERENCE] Pela união
dos eventos, a garantia marginal não se converte em garantia conjunta de 95%.
Não se verificou unimodalidade dos resíduos do simulador. Não modificar o corte
para obter a cobertura desejada sem novo desenho e validação independente.

## McCulloch et al. (2022)

*Calibrating Agent-Based Models Using Uncertainty Quantification Methods*,
JASSS 25(2):1. [Texto primário](https://www.jasss.org/25/2/1.html),
[DOI](https://doi.org/10.18564/jasss.4791). Texto integral consultado.

**SUPPORTED:** HM, gêmeo sintético e avaliação da estabilidade da variância.
Os tamanhos de ensemble encontrados nos exemplos são 200 (Sugarscape),
30 (aves) e 100 (RISC), escolhidos após diagnóstico; não constituem mínimo
universal para outro simulador. A equação 3 mede variância entre execuções,
não automaticamente a variância da média estimada neste TCC.

**INFERENCE/ressalva:** a equação 1 publicada usa erro quadrático sobre variância,
mas o texto a associa ao corte três e à regra de três desvios. Na forma
padronizada usada pelo TCC, I² ≤ 9 equivale a I ≤ 3; I² ≤ 3 seria outro corte.
Não copiar essa convenção sem conferir escala. A fonte não prova que o limite
do TCC seja exclusivamente número de réplicas, nem justifica pesos escolhidos
para contrair um parâmetro específico.

## Andrianakis et al. (2015)

*Bayesian History Matching of Complex Infectious Disease Models Using Emulation:
A Tutorial and a Case Study on HIV in Uganda*, PLoS Computational Biology 11(1),
e1003968. [Texto primário e DOI](https://doi.org/10.1371/journal.pcbi.1003968).
Seções de implausibilidade unidimensional/multidimensional e ondas consultadas.

**SUPPORTED:** o máximo por observável é procedimento reconhecido de HM;
rejeitar por desacordo em uma saída não é, por si, defeito. A fonte também
discute estatísticas de ordem e medidas multivariadas com cortes próprios.
**Não sustenta:** garantia conjunta automática derivada de um resultado
univariado ou seleção de pesos para forçar identificação de F_ancora.
As taxas de aceitação de ondas com domínios distintos precisam considerar seus
denominadores; taxas condicionais não medem diretamente a mesma região.

## TCC I da autora — fonte conceitual primária

Snapshot fiel em [TCC_I_referencia_2026-09-15.pdf](../docs/snapshots/TCC_I_referencia_2026-09-15.pdf).
SHA-256: `f2017d039b4c5d3561c6213e985a35c58d792d1016dd71178ab20c71374a817a`.
Conferência das páginas 26–33 e 35, especialmente §§4.4.1–4.4.3.

**SUPPORTED:** confiança no vetor de estado; portão estrito de ajuda;
multiplicadores cognitivo e de rede; níveis de confiança distintos na matriz
de cenários. **Não encontrado nessas equações/pseudocódigos:** lei de atualização
de τ. [INFERENCE] τ constante limita a dinâmica conceptual, mas a notação τ(t)
sozinha não determina uma lei correta para substituir a simplificação.
O TCC I não especifica os dois argumentos exatos do sistema fuzzy atual.

## Análise preliminar oficial local — registro, não literatura

Snapshot fiel em [analise_preliminar_oficial_2026-09-15.docx](../docs/snapshots/analise_preliminar_oficial_2026-09-15.docx).
SHA-256: `d5a658f1cdf03d99e6bdc0b5d03cb4aaa9420853ec7ebc2bb3f55e85a728c57d`.
Conteúdo oficial designado explicitamente pela autora na conversa. Essa origem
não é hipótese do revisor. Snapshot resolve preservação no Git; não demonstra
que `gerar_entrega.js` reproduza suas edições locais.
