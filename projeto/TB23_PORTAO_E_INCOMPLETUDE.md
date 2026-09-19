# T-B2.3 — o portão fechado explica as 36 incompletas nesta amostra

## Resultado

Na malha declarada, o primeiro valor sem incompletas é **tau_inicial=0,600001**:
36/36 concluem, assim como em todos os valores superiores testados. Em 0,25,
0,59 e 0,60, 0/36 concluem. O teste é estrito (`confianca > 0,60`).
A transição observada é um degrau de conclusão ao atravessar esse limiar.
Não é estimativa de um limiar contínuo exato, nem escolha de novo nominal.

O controle que altera somente a confiança inicial do portão, preservando a
inicialização da rede em 0,25, também completa 36/36 em cada nível.
Alterar apenas a rede para 0,80 ou 1,00, mantendo o portão fechado, completa
0/36 em ambos. Portanto o desaparecimento das incompletas é atribuível à
abertura inicial do portão e suas consequências, não apenas ao canal difuso.
A lei Crowder continua evoluindo após comunicações; estes controles não congelam
os mediadores posteriores. Não se deduz ausência de efeitos da rede nos outros
indicadores ou em outras populações.

## Números da malha inteira

| modo | tau_varrida | completas | incompletas | hiato_sem_confianca_media | fracao_hiato_sem_confianca | N_req_medio |
|---|---|---|---|---|---|---|
| portao | 0.600001 | 36.000000 | 0.000000 | 3.888889 | 0.011188 | 310.027778 |
| portao | 0.800000 | 36.000000 | 0.000000 | 0.083333 | 0.000237 | 318.111111 |
| portao | 1.000000 | 36.000000 | 0.000000 | 0.083333 | 0.000237 | 318.111111 |
| principal | 0.250000 | 0.000000 | 36.000000 | 106925.777778 | 0.833343 | 0.000000 |
| principal | 0.590000 | 0.000000 | 36.000000 | 106919.333333 | 0.833340 | 0.000000 |
| principal | 0.600000 | 0.000000 | 36.000000 | 106919.333333 | 0.833339 | 0.000000 |
| principal | 0.600001 | 36.000000 | 0.000000 | 14.361111 | 0.037693 | 329.416667 |
| principal | 0.610000 | 36.000000 | 0.000000 | 14.250000 | 0.037402 | 329.416667 |
| principal | 0.650000 | 36.000000 | 0.000000 | 3.583333 | 0.009836 | 325.277778 |
| principal | 0.800000 | 36.000000 | 0.000000 | 0.083333 | 0.000231 | 325.833333 |
| principal | 1.000000 | 36.000000 | 0.000000 | 0.083333 | 0.000223 | 338.583333 |
| rede | 0.800000 | 0.000000 | 36.000000 | 106930.888889 | 0.833343 | 0.000000 |
| rede | 1.000000 | 0.000000 | 36.000000 | 106929.777778 | 0.833342 | 0.000000 |

Contagens são acumuladas até o término ou teto de 256×CPM. A queda do hiato
absoluto combina mecanismo e menor exposição temporal; a fração por oportunidade
está publicada para separar a mudança de escala. N_req conta pedidos enviados,
não bloqueios anteriores ao envio. Trajetórias acima são funções do valor inicial
varrido; não foram exportadas séries temporais desses contadores acumulados.

## Correção da leitura de B2

As 36 incompletas são desfecho do portão degenerado A-13 no desenho histórico,
**não evidência de uma limitação necessária da família ABM+SD**. O horizonte
dobrado continua sendo um controle válido (0/36), mas não estabelece sozinho
uma causa. O precedente Pessoa tem outro mecanismo e não justifica extrapolar
este bloqueio à família. O nominal histórico permanece intacto; os contrastes
condicionais de T-B2.2 continuam descritivos do subconjunto completo daquele
nominal, e não são substituídos por um tau conveniente.

População deste ensaio: somente as 36 chaves historicamente incompletas,
selecionadas explicitamente. 468 execuções, ambos os estados do canal direto,
mesmas sementes/instâncias/parâmetros. Não estimar frequência de incompletude
na população a partir desta amostra selecionada.

## Verificação e reprodução

- `python3 research/tb2/varredura_confianca.py --saida <diretorio-novo>`
- Protocolo anterior: `research/tb2/PROTOCOLO_TB23.md`.
- `controle_baseline.csv`: resíduos menores que 1e-12 nos campos B2 publicados.
- `verificacoes.json`: zero violações e 468 execuções; hashes das fontes
  conferidos no término.
- O controle adicional de override nominal foi executado depois da varredura,
  embora o protocolo previsse antes: igualdade exata confirmada; os quatro
  testes de configuração passaram (`configuracao.log`). Desvio de sequência
  registrado, sem reconstruir um controle anterior que não ocorreu.
- `identidade.log`: três controles bit a bit aprovados (campos, estados e RNG).
- `resumo.csv`, `estratos.csv` e `bruto.csv` preservam toda a malha.
- Figura: `outputs/diagnosticos/TB23_20260918/varredura.png`.

O lote noturno permanece aberto; próximo item: D2 em segundo plano e D1.
