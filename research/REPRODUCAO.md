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
