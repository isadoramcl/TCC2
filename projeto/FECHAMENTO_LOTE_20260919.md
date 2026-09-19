# Fechamento do lote obrigatório — 19/09/2026

**A1, C1, C2, P1 e P2 executados.** C4 e o N da bancada em F continuam
parciais, como autorizado. Fechamento das entregas computacionais não equivale
a validação externa do modelo ou aprovação automática de conclusões da tese.

## 1. A1 — primeiro

Alternativas `constante` (default) e `dependente_estado`, omega*q>limite,
q=max(0,2*p_heu−1), declarada [DEC]. Limites0,10/0,20/0,30/0,40 mais controle0,60
na robustez dedicada `config/robustez_a1.yaml`. 320 execuções,117 completas.
Os testes e a identidade foram reconferidos antes de seguir para C1.

**Não permanece zero, mas continua um interruptor por estado.** No braço
centralizado a fração de fuga/P1 fica entre0,999875 e0,999887 nos quatro limites;
0/16 concluem em cada limite. No adaptativo:8,8,8,9 completas de16. Portanto
não declarar mecanismo contínuo validado. Não houve ajuste para tornar a curva
contínua nem escolha de limiar conveniente. Os dois portões A-13/A-14 foram
identificados independentemente; T-B2.3 e a grade suave identificam duas saídas
do bloqueio conjunto, não um efeito universal de confiança fechada.

Cinco indicadores com IC95, contagens e censura:
[CSV A1](../outputs/diagnosticos/A1_20260919/cinco_indicadores_IC95.csv).
[Relatório A1](A1_FUGA_ESTADO_RESULTADOS.md), com ANTES/DEPOIS e controles.

## 2. C1 — depois de A1

Seis pontos k=1/2/3/4/5/8 reproduzidos, maior resíduo6,94e-18 (<1e-12).
Mapa reverso:0,05→3,90625 e0,10→7,8125. Valores0,15/0,20/0,25 requerem
k=11,71875/15,625/19,53125: **cenários de sensibilidade**, não ancorados.

Dois mapas J60→k sintéticos declarados (curto1/2/3/4; longo1/2/4/8),
nenhum escolhido como verdadeiro. 96/96 execuções completas, identidade
histórica preservada e novamente verificada antes de C2. Na alternativa,
o gradiente por passos substitui NASA, decisão explicitada para não empilhá-los.
[Relatório e números C1](C1_ANCORAGEM_LINEAR_RESULTADOS.md).

## 3. C2 — implementado depois de C1

`heterogeneidade_erro=nenhuma` é default; `beta_cv113` sorteia taxas fixas por
agente/nível com a fórmula prescrita. Validar todos os níveis antes de RNG.
Fluxo auxiliar de sorteios preserva o da dinâmica; nenhuma não consome extras.

**448 células planejadas:352 executadas/completas;96 rejeitadas explicitamente
por domínio**, zero violações. A Beta não degenerada exige mu<0,439193640476086,
com fronteira estrita. Bases históricas0,15/0,20/0,25 têm níveis incompatíveis;
ambos os mapas C1 são admissíveis. Sem reduzir CV ou aparar mu para fazê-los caber.

Controle aproximado, conforme a nova ordem: mu=0,0163/CV=1,13 retornam
alpha=0,754081392435 e beta=45,508580720130. Os desvios frente aos impressos
são publicados; não afirmar igualdade na terceira casa. Os momentos implícitos
nos impressos estão nos intervalos de arredondamento da fonte. Fórmula literal
confirmada independentemente;200.000 agentes por média (20 médias) produziram
maior erro relativo0,3969% na média e0,5946% no CV. Não escolher sementes favoráveis.
A reprovação anterior no critério estrito permanece arquivada e é superada
pela nova exigência aproximada, não apagada ou recodificada retrospectivamente.

[Cinco indicadores, ambas opções, IC95](../outputs/diagnosticos/C2_fechamento_20260919/cinco_indicadores_IC95.csv),
[efeito Beta−nenhuma e ANTES/DEPOIS](../outputs/diagnosticos/C2_fechamento_20260919/efeito_beta_menos_nenhuma.csv),
[relatório C2](C2_HETEROGENEIDADE_FECHAMENTO.md).

## P1 — limitação mantida

[**LIMITACAO**] s_transicao=0,01 permanece na grade como teste de degeneração,
sem elevar o extremo para remover o resultado. No canto centralizado com
competência insuficiente e tau_sat=1/1,4, a rota heurística é praticamente
inacessível: o modelo fica efetivamente no caminho analítico/P2, que pode travar.
Não estender "só Porta3" a toda a grade: tau_sat=0,7 tem execuções completas.

Precisão técnica:3e-29 é representável, **não subfluxo aritmético a zero**.
No exemplo, esse valor é da tarefa mais fácil não escolhida; a escolhida tem
p_heu máximo3,25e-14. É uma degeneração probabilística na escala do horizonte,
não prova de impossibilidade matemática infinita. Essa correção de nomenclatura
não retira a limitação pedida. Ver [diagnóstico](B2_DEADLOCK_TRES_VIAS_E_CENSURA.md).

## P2 — rótulo até a tabela final

As tabelas de B2 publicam `estatuto` e `valor_rotulado`, CSV e Markdown.
−112,291506 e−174,504547 permanecem com CENSURADO; a fração indefinida fica
NA+CENSURADO/INDEFINIDO, jamais0. A1 distingue diagnóstico ao teto de contraste
condicional a pares completos. C2 distingue REJEITADA_DOMINIO de censura.
[Tabela final B2](../outputs/diagnosticos/B2_rotulagem_20260919/contraste_A_menos_C_IC95.md).

## Limites do fechamento

Sem otimização, ajuste de V_mod, novas ondas HM ou calibração contra Rieskamp.
Nominal preservado bit a bit. Inferência dos pilotos usa quatro instâncias,
logo os IC são pouco precisos e não demonstram robustez contínua universal.
Nenhuma alternativa experimental é promovida silenciosamente ao nominal.
C4 e tamanho da base de F permanecem parciais, fora dos obrigatórios deste lote.

## Verificação final e preservação

85 testes de software aprovados. Comparação da opção nenhuma com as96 saídas
C1 anteriores: resíduo máximo0. Controle bit a bit contra efd1248 em16 pares
de execuções cobre resultados, estados e RNG. Hashes de código/dados conferidos.
Logs em `outputs/diagnosticos/fechamento_20260919/` e controles específicos C2.
Os resultados negativos e as tentativas históricas permanecem preservados.
