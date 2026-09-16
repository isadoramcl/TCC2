# Reproduzir esta investigação

Executar na raiz de um clone desta branch. O ambiente efetivamente utilizado
está registrado nos manifestos (Python, NumPy, pandas, PyYAML); análises e testes
também usam scipy 1.11.4. Não foi certificada instalação limpa de todas as versões
do `requirements.txt` histórico. Um ambiente compatível com esses pacotes é
necessário; os pilotos não precisam de Word, Node nem acesso à máquina da autora.

## Evidência histórica

`EVIDENCE_INDEX.csv` identifica arquivos pelo SHA-256 e por commit imutável.
Arquivos sem commit de origem são incluídos nesta própria branch. Os demais
podem ser recuperados sem checkout ou merge, em pasta nova:

```sh
git fetch origin revisao-auditoria
python3 research/recuperar_evidencias.py --destino /tmp/tcc2-evidencias
```

O recuperador confere todos os hashes antes de escrever. Não modifica o checkout.
Os commits-fonte são `72e6a64fc53125b6c253bf1acea3eb11ba00b731` e
`113c63894433494a864d77b72e56b7937d8556f9`. A evidência da auditoria anterior
não precisa ser confundida com a árvore do simulador que executa os novos pilotos.

## Novos pilotos

Cada destino deve ainda não existir. Todos preservam dados individuais.

```sh
python3 src/modelo/16_reanalise_revisao.py --saida /tmp/revisao/reanalise
python3 src/modelo/17_pilotos_revisao.py produto --saida /tmp/revisao/produto
python3 src/modelo/17_pilotos_revisao.py ruido --saida /tmp/revisao/ruido
python3 src/modelo/17_pilotos_revisao.py cobertura --saida /tmp/revisao/cobertura
python3 src/modelo/17_pilotos_revisao.py confianca --saida /tmp/revisao/confianca
python3 src/modelo/17_pilotos_revisao.py vertices --saida /tmp/revisao/vertices
python3 src/modelo/18_analisar_pilotos_revisao.py --entrada /tmp/revisao --saida /tmp/revisao/analise
python3 src/modelo/19_piloto_fronteira.py --saida /tmp/revisao/fronteira
python3 research/test_revisao.py
```

Comparar CSVs de saída com `outputs/diagnosticos/revisao_20260915/`.
Tempos de execução e hashes de código podem mudar ao executar a versão que
corrige o texto do relatório HM; os resultados numéricos não devem mudar por
essa alteração. Os manifestos dos primeiros pilotos identificam o HM legado
disponível no commit de origem. Os scripts de simulação e configurações
nominais permanecem preservados.

Versionados: planos, scripts, testes, execuções individuais dos pilotos,
análises, resposta, parecer e snapshots documentais essenciais.
Recuperáveis por commit: tabelas históricas e scripts citados pela auditoria.
Fora do versionamento: ambientes, caches, diretórios temporários e cópias
duplicadas de recuperação. Não executar o relatório histórico sobre os CSVs
publicados para testar: o teste usa diretório temporário e verifica igualdade
numérica da tabela regenerada.

## MVP — execução alternativa e robustez (16/09/2026)

O simulador legado continua em `src/modelo/simulador.py`. Configurações candidatas
em `config/mvp.yaml`, desenho em `research/PLANO_MVP.md`. Não alterar o DOCX oficial.
Use destinos novos: os scripts recusam sobrescrever resultados.

```bash
python3 -m unittest discover -s research -p 'test*py'
python3 research/verificar_documento_oficial.py --vivo /caminho/do/documento/oficial.docx
python3 src/modelo/20_experimento_mvp.py --etapa alternativas --saida outputs/diagnosticos/minha_execucao/alternativas --workers 4
python3 src/modelo/20_experimento_mvp.py --etapa robustez --saida outputs/diagnosticos/minha_execucao/robustez --workers 4
python3 src/modelo/21_canais_mvp.py --modelo legado --saida outputs/diagnosticos/minha_execucao/canais_legado --workers 4
python3 src/modelo/21_canais_mvp.py --modelo mvp --saida outputs/diagnosticos/minha_execucao/canais_mvp --workers 4
python3 src/modelo/22_consolidar_mvp.py --entrada outputs/diagnosticos/minha_execucao --rodar-b9 --workers 4
python3 src/modelo/22_consolidar_mvp.py --entrada outputs/diagnosticos/minha_execucao
```

A saída possui configurações completas, hashes, dados individuais, contrastes
por instância, censura e tabelas ANTES/DEPOIS. São 17.920 execuções novas: 3.072
alternativas + 1.408 robustez + 12.288 canais + 1.152 B9. Intervalos sobre
instâncias são condicionais à família declarada, sem promessa de cobertura
simultânea nem generalização a todo o espaço contínuo. O pós-processamento
confere todas as 384 linhas nominais e as 3.072 diagonais históricas.

A verificação de documento aceita somente o hash fixado. Em um clone sem cópia
viva, fornecer o arquivo designado pela autora. Usar o snapshot como `--vivo`
verifica apenas sua integridade e **não** verifica se a autora editou o documento.

### Ambiente e valores-p

O ambiente efetivo desta execução é Python 3.9.6 e as versões fixadas em
`research/requirements_mvp.txt`. O `requirements.txt` geral declara SciPy 1.15.3;
essa não é a versão efetiva dos experimentos desta branch. `wilcoxon(method='auto')`
pode selecionar procedimentos diferentes diante de empates/zeros. Exemplo
reproduzido: TL, braço `so_tau_inicial`, no legado: auto em 1.11.4 retorna
0,0000305176; `method='approx'` retorna 0,0004358424, o valor publicado.
As funções antigas e novas, rodadas hoje sobre o mesmo CSV histórico, coincidem.
Isso sustenta diferença de cálculo, sem provar qual ambiente gerou cada tabela.

As tabelas detalhadas incluem `ANTES`, `CONTROLE_mesmo_ambiente`, `DEPOIS`,
`delta` e `delta_vs_controle`. Não atribuir mudanças de valores-p já presentes
no controle ao novo modelo. Parcelas muito pequenas também são sensíveis ao
arredondamento no modelo saturado. A padronização definitiva da inferência
entra nas fragilidades após o MVP; nenhum valor-p foi ajustado para obter uma
conclusão. Os contrastes principais são apresentados com magnitudes, sinais
por instância e intervalos t, não pelo ranking de valores-p.
