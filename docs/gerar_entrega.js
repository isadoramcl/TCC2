/*
 * gerar_entrega.js — Gera o documento da Entrega 1 (Metodologia e Resultados
 * Iniciais) a partir das figuras e tabelas produzidas pelo pipeline.
 * ---------------------------------------------------------------------------
 * O documento e um ARTEFATO GERADO, nao um arquivo editado a mao. Isso mantem a
 * mesma regra aplicada aos dados: toda transformacao e feita por codigo e fica
 * registrada. Reeditar o .docx diretamente quebraria essa garantia — as
 * alteracoes devem ser feitas aqui e o documento regerado.
 *
 * Uso:  node docs/gerar_entrega.js
 * Requer: npm i docx   e as figuras em outputs/figures/
 *
 * As figuras sao lidas de FIG; ajuste a constante ao caminho local antes de
 * rodar fora do ambiente em que o documento foi produzido.
 */
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, PageOrientation, LevelFormat, convertMillimetersToTwip,
} = require('docx');

// `[DEC]` Caminhos derivados da posicao do proprio script. Estavam fixos em
// caminhos absolutos de UMA estacao de trabalho, o que impedia a geracao em
// qualquer outra — defeito da mesma familia do numero digitado em texto.
const path = require('path');
const RAIZ = path.resolve(__dirname, '..');
const FIG = path.join(RAIZ, 'outputs', 'figures');
const TAB = path.join(RAIZ, 'outputs', 'tables');
const OUT = path.join(RAIZ, 'docs', 'entrega1_metodologia_resultados_iniciais.docx');
const caminhoTabela = (nome) => path.join(TAB, nome);

const FONTE = 'Times New Roman';
const CORPO = 24;      // 12 pt (meios-pontos)
const PEQUENO = 20;    // 10 pt
const MINI = 18;       // 9 pt
const LARGURA_UTIL = 9070; // DXA (~16 cm) para tabelas

// ---------- helpers ----------

// ============================================================
// REGISTRO DE IDENTIFICADORES
// ------------------------------------------------------------
// `[DEC]` Equacoes, tabelas e figuras sao citadas por NOME, nunca por numero
// digitado. Os numeros sao atribuidos pela ordem declarada abaixo, e as
// funcoes E(), T() e F() os resolvem em qualquer ponto do texto.
//
// A motivacao e um defeito real: ao inserir uma equacao no meio do documento,
// a renumeracao quebrou SETE referencias cruzadas, e uma auditoria automatica
// deu "todas as citacoes resolvem" porque o padrao de busca so casava com
// "Equacao 7" e nao com "equacao (7)". Numero digitado em texto nao sobrevive
// a edicao. Agora nao ha numero para quebrar, e a verificacao do fim deste
// arquivo INTERROMPE a geracao se algo nao fechar.
// ============================================================
const ORDEM_EQ = ['esforco', 'delta_c', 'pr_efetiva', 'tge', 'e_total', 'p_heuristico', 'logistica', 'rc', 'lr', 'vif', 'nc', 'rf', 'rs', 'folga', 'd_norm', 'r_int', 'crit', 'd_index', 'rr', 'f_base', 'implaus_j', 'implaus_max'];
const ORDEM_TAB = ['fuzzy_config', 'cenarios', 'ensaios', 'j60_grade', 'razoes_risco', 'verificacoes', 'tendencia', 'poder_9a', 'experimento', 'fatorial', 'tau_min', 'ablacao', 'porta2', 'rastreabilidade', 'identificabilidade', 'procedencia', 'cronograma'];
const ORDEM_FIG = ['arquitetura', 'controle_tamanho', 'fbase_faixa', 'loo', 'niveis_di', 'gradiente', 'decomposicao', 'trajetorias', 'nroy'];

const emitido = { eq: new Set(), tab: new Set(), fig: new Set() };
const citado = { eq: new Set(), tab: new Set(), fig: new Set() };

function num(ordem, tipo, chave) {
  const i = ordem.indexOf(chave);
  if (i < 0) throw new Error(`[registro] ${tipo} desconhecida: "${chave}"`);
  citado[tipo].add(chave);
  return i + 1;
}
const E = (c) => num(ORDEM_EQ, 'eq', c);          // numero de equacao
const T = (c) => num(ORDEM_TAB, 'tab', c);        // numero de tabela
const F = (c) => num(ORDEM_FIG, 'fig', c);        // numero de figura
// Intervalo inclusivo: E2('logistica','vif') -> "7 a 10"
const E2 = (a, b) => `${E(a)}) a (${E(b)}`;   // rende '(7) a (10)' com os parenteses do texto

function verificarRegistro() {
  const erros = [];
  for (const [tipo, ordem] of [['eq', ORDEM_EQ], ['tab', ORDEM_TAB], ['fig', ORDEM_FIG]]) {
    for (const c of ordem) if (!emitido[tipo].has(c)) erros.push(`${tipo} "${c}" declarada e nunca emitida`);
    for (const c of emitido[tipo]) if (!ordem.includes(c)) erros.push(`${tipo} "${c}" emitida fora da ordem declarada`);
    for (const c of citado[tipo]) if (!emitido[tipo].has(c)) erros.push(`${tipo} "${c}" citada e nunca emitida`);
  }
  return erros;
}

// Le uma tabela CSV simples (sem virgula dentro de campo).
function lerCsv(caminho) {
  const linhas = fs.readFileSync(caminho, 'utf8').trim().split(/\r?\n/);
  const cab = linhas[0].split(',');
  return linhas.slice(1).map(l => {
    const v = l.split(',');
    return Object.fromEntries(cab.map((c, i) => [c, v[i]]));
  });
}
// `[DEC]` Os CSV de `13_exportar_tabelas_entrega.py` usam PONTO E VIRGULA como
// separador, porque os campos ja trazem decimal brasileiro (virgula). O script
// que os gera confere, a cada execucao, que o separador nunca aparece dentro de
// campo — e o proprio teste e verificado contra um arquivo malformado.
function lerCsvPV(caminho) {
  const linhas = fs.readFileSync(caminho, 'utf8').trim().split(/\r?\n/);
  const cab = linhas[0].split(';');
  return linhas.slice(1).map(l => {
    const v = l.split(';');
    if (v.length !== cab.length) throw new Error(`[csv] ${caminho}: linha com ${v.length} campos, esperado ${cab.length}`);
    return Object.fromEntries(cab.map((c, i) => [c, v[i]]));
  });
}
const br = (x, casas = 2) => Number(x).toFixed(casas).replace('.', ',');  // decimal brasileiro

const p = (texto, opts = {}) => new Paragraph({
  alignment: opts.align || AlignmentType.JUSTIFIED,
  spacing: { line: opts.line || 360, after: opts.after === undefined ? 120 : opts.after },
  indent: opts.indent === false ? undefined : { firstLine: convertMillimetersToTwip(12.5) },
  children: [new TextRun({ text: texto, font: FONTE, size: opts.size || CORPO,
                           bold: !!opts.bold, italics: !!opts.italics })],
});

const pRuns = (runs, opts = {}) => new Paragraph({
  alignment: opts.align || AlignmentType.JUSTIFIED,
  spacing: { line: opts.line || 360, after: opts.after === undefined ? 120 : opts.after },
  indent: opts.indent === false ? undefined : { firstLine: convertMillimetersToTwip(12.5) },
  children: runs.map(r => new TextRun({
    text: r.t, font: FONTE, size: r.size || opts.size || CORPO,
    bold: !!r.b, italics: !!r.i, superScript: !!r.sup })),
});

const h1 = (texto) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: texto, font: FONTE, size: 28, bold: true, color: '000000' })],
});

const h2 = (texto) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: texto, font: FONTE, size: CORPO, bold: true, color: '000000' })],
});

const bullet = (texto, negrito) => new Paragraph({
  bullet: { level: 0 },
  alignment: AlignmentType.JUSTIFIED,
  spacing: { line: 300, after: 80 },
  children: negrito
    ? [new TextRun({ text: negrito, font: FONTE, size: CORPO, bold: true }),
       new TextRun({ text: texto, font: FONTE, size: CORPO })]
    : [new TextRun({ text: texto, font: FONTE, size: CORPO })],
});

// `[DEC]` ABNT NBR 14724: a identificacao da ilustracao vem ACIMA dela, com
// travessao, e a fonte ABAIXO. A versao anterior punha tudo abaixo, com
// dois-pontos.
const tituloFigura = (chave, texto) => {
  if (emitido.fig.has(chave)) throw new Error(`[registro] figura "${chave}" emitida duas vezes`);
  emitido.fig.add(chave);
  const n = ORDEM_FIG.indexOf(chave) + 1;
  if (n === 0) throw new Error(`[registro] figura nao declarada: "${chave}"`);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 240, after: 60 },
    children: [new TextRun({ text: `Figura ${n} \u2013 ${texto}`, font: FONTE, size: PEQUENO, bold: true })],
  });
};

const fonte = (texto) => new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 60, after: 240 },
  children: [new TextRun({ text: `Fonte: ${texto}`, font: FONTE, size: PEQUENO })],
});

const legenda = (texto) => new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 80, after: 240 },
  children: [new TextRun({ text: texto, font: FONTE, size: PEQUENO })],
});

const tituloTabela = (chave, texto) => {
  if (emitido.tab.has(chave)) throw new Error(`[registro] tabela "${chave}" emitida duas vezes`);
  emitido.tab.add(chave);
  const n = ORDEM_TAB.indexOf(chave) + 1;
  if (n === 0) throw new Error(`[registro] tabela nao declarada: "${chave}"`);
  return new Paragraph({
  alignment: AlignmentType.LEFT,
  spacing: { before: 240, after: 100 },
  children: [new TextRun({ text: `Tabela ${n} \u2013 ${texto}`, font: FONTE, size: PEQUENO, bold: true })],
});
};

// Equacao centralizada com numero alinhado a direita.
// Nao se usa o suporte a OMML do docx-js: o LibreOffice nao o importa, e sem
// poder verificar a renderizacao no Word o risco de entregar formulas em branco
// nao compensa. Simbolos Unicode renderizam de forma identica em qualquer editor.
const TabStopTipo = { RIGHT: 'right' };
function equacao(texto, chave) {
  if (emitido.eq.has(chave)) throw new Error(`[registro] equacao "${chave}" emitida duas vezes`);
  emitido.eq.add(chave);
  const numero = ORDEM_EQ.indexOf(chave) + 1;
  if (numero === 0) throw new Error(`[registro] equacao nao declarada: "${chave}"`);
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 140, after: 140 },
    indent: { left: convertMillimetersToTwip(12) },
    tabStops: [{ type: TabStopTipo.RIGHT, position: 9070 }],
    children: [
      new TextRun({ text: texto, font: FONTE, size: CORPO, italics: true }),
      new TextRun({ text: '\t(' + numero + ')', font: FONTE, size: CORPO }),
    ],
  });
}

// Linha de definicao de simbolo, recuada e menor.
function simbolo(sim, definicao) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 40 },
    indent: { left: convertMillimetersToTwip(14), hanging: convertMillimetersToTwip(8) },
    children: [
      new TextRun({ text: sim, font: FONTE, size: PEQUENO, italics: true }),
      new TextRun({ text: '  ' + definicao, font: FONTE, size: PEQUENO }),
    ],
  });
}

function figura(arquivo, larguraCm, ratio) {
  const w = Math.round(larguraCm * 37.8);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 40 },
    children: [new ImageRun({
      type: 'png',
      data: fs.readFileSync(`${FIG}/${arquivo}`),
      transformation: { width: w, height: Math.round(w * ratio) },
    })],
  });
}

function celula(texto, { largura, negrito, fundo, tamanho, centro } = {}) {
  return new TableCell({
    width: { size: largura, type: WidthType.DXA },
    shading: fundo ? { type: ShadingType.CLEAR, fill: fundo, color: 'auto' } : undefined,
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children: [new Paragraph({
      alignment: centro ? AlignmentType.CENTER : AlignmentType.LEFT,
      spacing: { line: 240, after: 0 },
      children: [new TextRun({ text: texto, font: FONTE, size: tamanho || MINI, bold: !!negrito })],
    })],
  });
}

function tabela(colunas, cabecalhos, linhas, opcoes = {}) {
  const bordas = {
    top: { style: BorderStyle.SINGLE, size: 4, color: '888888' },
    bottom: { style: BorderStyle.SINGLE, size: 4, color: '888888' },
    left: { style: BorderStyle.SINGLE, size: 4, color: 'BBBBBB' },
    right: { style: BorderStyle.SINGLE, size: 4, color: 'BBBBBB' },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC' },
    insideVertical: { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC' },
  };
  return new Table({
    width: { size: LARGURA_UTIL, type: WidthType.DXA },
    columnWidths: colunas,
    borders: bordas,
    rows: [
      new TableRow({
        tableHeader: true,
        children: cabecalhos.map((c, i) =>
          celula(c, { largura: colunas[i], negrito: true, fundo: 'EFEFEC', centro: true })),
      }),
      ...linhas.map(linha => new TableRow({
        children: linha.map((c, i) => celula(c, {
          largura: colunas[i],
          centro: opcoes.centrar ? opcoes.centrar.includes(i) : false,
        })),
      })),
    ],
  });
}

// ============================================================
// CONTEUDO
// ============================================================
const filhos = [];

// ---- capa curta ----
filhos.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: 'UNIVERSIDADE FEDERAL DE MINAS GERAIS', font: FONTE, size: CORPO, bold: true })],
}));
filhos.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 300 },
  children: [new TextRun({ text: 'Engenharia de Sistemas — Trabalho de Conclusão de Curso II', font: FONTE, size: PEQUENO })],
}));
filhos.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 120 },
  children: [new TextRun({ text: 'Pensamento sistêmico aplicado à gestão de equipes em projetos de engenharia:', font: FONTE, size: CORPO, bold: true })],
}));
filhos.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 300 },
  children: [new TextRun({ text: 'metodologia e resultados iniciais da calibração empírica e da transferência ordinal de risco', font: FONTE, size: CORPO, bold: true })],
}));
filhos.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: 'Isadora Maria Carvalho Lopes', font: FONTE, size: CORPO })],
}));
filhos.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: 'Orientador: Prof. André Batista', font: FONTE, size: PEQUENO })],
}));
filhos.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 400 },
  children: [new TextRun({ text: 'Belo Horizonte, setembro de 2026', font: FONTE, size: PEQUENO })],
}));

// ============================================================
filhos.push(h1('1  METODOLOGIA'));

filhos.push(h2('1.1  Classificação e abordagem da pesquisa'));
filhos.push(p('Esta pesquisa fundamenta-se no método científico-tecnológico, caracterizando-se como pesquisa aplicada e experimental. Quanto à abordagem do problema, o estudo é quantitativo, pois as questões centrais do trabalho — se a complexidade de uma tarefa está associada à ocorrência de falhas, em que magnitude, e se essa associação é estável o bastante para ser transferida ordinalmente a outro domínio — são formuladas como hipóteses estatísticas sobre parâmetros populacionais e respondidas por estimação de efeitos, intervalos de confiança e testes de hipótese sobre bases de dados públicas.'));
filhos.push(p('Cabe uma delimitação metodológica desde já. O trabalho não busca construir o melhor classificador de módulos defeituosos, objetivo usual da literatura de predição de defeitos de software. Busca-se uma relação interpretável e ordinalmente transferível entre um nível de dificuldade técnica e um risco basal de retrabalho, a ser incorporada a um modelo de simulação de equipes de projeto. Essa diferença de objetivo é o que justifica privilegiar interpretabilidade e estabilidade sobre acurácia preditiva, e é o critério declarado que orienta todas as escolhas de modelagem descritas adiante.'));
filhos.push(p('Os procedimentos técnicos adotados baseiam-se na engenharia sistemática e em uma metodologia de desenvolvimento de sistemas organizada em ciclos de concepção, especificação, implementação e validação, aplicados de forma incremental a cada etapa do pipeline de dados.'));

filhos.push(h2('1.2  Materiais, ferramentas e recursos de engenharia'));
filhos.push(p('Para o planejamento, a modelagem e a execução das atividades foram utilizados os seguintes recursos técnicos.', { indent: false }));
filhos.push(bullet('Visual Studio Code 1.125 como ambiente de desenvolvimento; Git 2.49 para controle de versão, com repositório remoto privado no GitHub garantindo sincronização entre as duas estações de trabalho utilizadas; ambiente virtual Python isolado por projeto, com dependências declaradas em arquivo de requisitos versionado.', 'Ambientes de desenvolvimento e software: '));
filhos.push(bullet('Python 3.14 como linguagem de implementação. Bibliotecas: pandas 3.0.5 (manipulação tabular), NumPy 2.5.2 (álgebra numérica), SciPy 1.15 (distribuições e testes), statsmodels 0.15 (regressão logística, verossimilhança e inferência) e Matplotlib 3.10 (figuras). A etapa de auditoria dos arquivos brutos foi implementada exclusivamente com a biblioteca padrão, por decisão metodológica justificada na Seção 1.4.', 'Linguagens, frameworks e bibliotecas: '));
filhos.push(bullet('não aplicável. O trabalho é integralmente computacional, baseado em análise secundária de bases públicas e em simulação.', 'Componentes de hardware e instrumentação: '));
filhos.push(bullet('(i) NASA Metrics Data Program (MDP), nas versões limpas D′ e D″ disponibilizadas por Shepperd et al. (2013), utilizadas para a calibração da relação entre complexidade e defeito; (ii) NASA Promise Data Repository, versões brutas dos conjuntos CM1, JM1, KC1, KC2 e PC1, utilizadas como termo de comparação e para a auditoria de proveniência; (iii) PSPLIB, conjunto J60, com 480 instâncias de projeto, utilizado para a estrutura de execução — tarefas, precedências, durações e restrições de recursos; (iv) NASA Software Engineering Handbook, requisito SWE-220, e relatório NASA/TM-20205011566 (NESC), como fonte normativa dos limiares de complexidade ciclomática.', 'Bases de dados e fontes de informação: '));

filhos.push(h2('1.3  Processo de desenvolvimento do software'));
filhos.push(p('O desenvolvimento seguiu um ciclo de engenharia incremental, no qual cada etapa do pipeline é implementada como um script independente, verificada isoladamente e só então integrada à etapa seguinte. A estrutura adotada é a seguinte.', { indent: false }));
filhos.push(bullet('imutabilidade dos dados brutos; rastreabilidade de cada observação até o arquivo e a linha de origem; toda transformação realizada por código e registrada em log; distinção explícita entre o que provém da literatura, o que é decisão metodológica deste trabalho e o que é exploração.', 'Requisitos e restrições: '));
filhos.push(bullet('separação entre camada de dados brutos (somente leitura), camada de processamento (scripts numerados na ordem de execução) e camada de saídas (tabelas, figuras e logs), conforme a Figura ' + F('arquitetura') + '.', 'Projeto e arquitetura: '));
filhos.push(bullet('seis scripts em Python, executáveis de forma independente e em sequência, cada um documentando internamente o problema que resolve, sua entrada, sua saída, sua lógica, a origem de cada decisão e o critério de verificação do próprio resultado.', 'Implementação: '));
filhos.push(bullet('cada script encerra com um bloco de verificações automáticas que compara seu resultado com invariantes conhecidas — totais que devem se conservar, chaves que devem ser únicas, ausências que não podem existir, propriedades matemáticas que devem valer. Uma verificação que falha interrompe a execução com código de erro, de modo que uma etapa defeituosa não alimenta silenciosamente a seguinte.', 'Verificação e ensaios: '));

filhos.push(h2('1.4  Procedimentos experimentais e coleta de dados'));
filhos.push(p('Os dados foram extraídos de forma integralmente automatizada, por meio dos scripts descritos, a partir dos arquivos originais dos repositórios públicos. Nenhum arquivo bruto foi editado em momento algum: todas as transformações produzem arquivos derivados, e a integridade dos originais é verificável por resumo criptográfico SHA-256 calculado a cada execução. O repositório está configurado para preservar os bytes originais dos arquivos de dados, impedindo que o sistema de controle de versão converta terminadores de linha e altere fisicamente os arquivos entre as duas estações de trabalho — precaução sem a qual a verificação por resumo criptográfico deixaria de ser reproduzível.'));
filhos.push(p('A etapa de auditoria foi implementada sem bibliotecas de leitura de alto nível, com uso exclusivo da biblioteca padrão do Python. A justificativa é metodológica: leitores de dados de alto nível convertem tipos, tratam valores ausentes e descartam registros malformados de maneira silenciosa, o que destruiria precisamente a evidência que a auditoria pretende coletar. A partir da etapa de consolidação, com os dados já caracterizados, o uso de bibliotecas de análise passa a ser adequado.'));
filhos.push(p('As condições controladas dos ensaios são as seguintes: a base de análise é fixa (17.377 observações de 12 projetos); a unidade de observação é o módulo de software; o desfecho é binário (módulo defeituoso ou não); o efeito do projeto de origem é sempre incluído nos modelos, de modo que nenhuma associação seja atribuída a uma métrica quando puder ser explicada pela procedência da observação; e todos os testes de robustez — sensibilidade aos pontos de corte e validação por exclusão sucessiva de projetos — são executados sobre a mesma base, sem reamostragem aleatória, o que torna os resultados determinísticos e reproduzíveis bit a bit.'));

filhos.push(h2('1.5  Modelagem do sistema'));
filhos.push(p('O objeto construído é um modelo híbrido que acopla Dinâmica de Sistemas e Modelagem Baseada em Agentes, especificado na fase conceitual deste trabalho. O ecossistema é povoado por duas classes de agentes. O Agente Gestor controla um vetor dinâmico de restrições, composto pela pressão de cronograma P(t), pela restrição orçamentária Ω e pela topologia do fluxo de trabalho W, em que cada nó guarda uma dificuldade técnica Dᵢ. O Agente Engenheiro é caracterizado por um vetor contínuo de atributos que evoluem ao longo da simulação: competência técnica C(t), bateria cognitiva B(t), disponibilidade a(t), taxa de resposta na rede R(t), confiança mútua τ(t) e limiar de saturação da atenção τ_sat.'));

filhos.push(p('A grandeza que engatilha as transições de estado é o esforço cognitivo exigido pela tarefa, que cresce com a dificuldade técnica e com a pressão de cronograma, e é aliviado pela capacidade cognitiva disponível:', { indent: false }));
filhos.push(equacao('E(t) = Dᵢ · P(t) / B(t)', 'esforco'));
filhos.push(simbolo('Dᵢ', '— índice de dificuldade técnica da tarefa i;'));
filhos.push(simbolo('P(t)', '— pressão de cronograma imposta pelo gestor;'));
filhos.push(simbolo('B(t)', '— bateria cognitiva disponível do agente.'));

filhos.push(p('Quando existe hiato de competência e o agente recorre à rede, a transferência lateral de conhecimento produz incremento de competência ao custo de tempo, conforme a formulação de Crowder, Robinson e Hughes (2012):', { indent: false }));
filhos.push(equacao('ΔC = [ 15 + 3 ( C_k − C ) ] / 100', 'delta_c'));
filhos.push(pRuns([
  { t: 'Procedência dos coeficientes. ', b: true },
  { t: 'Os escalares 15 e 3 não são premissas deste trabalho: integram a formulação publicada por Crowder, Robinson e Hughes (2012), na qual o primeiro representa o incremento base de assimilação por interação bem-sucedida e o segundo pondera o ganho adicional pelo hiato técnico entre provedor e receptor. São reproduzidos sem alteração. O que este trabalho decide, e declara como decisão própria, é o contexto em que a equação opera.' },
]));
filhos.push(bullet('a equação e seus dois coeficientes, tal como publicados.', 'Da formulação original: '));
filhos.push(bullet('os autores estabelecem que o incremento é limitado ao intervalo de zero a três décimos, que a competência resultante não ultrapassa a dificuldade da subtarefa, e que, concluída a subtarefa, a competência do agente RETORNA ao valor de partida, por entenderem que parte da competência é específica da subtarefa. A implementação atual não reproduz esse retorno: o ganho obtido com o apoio permanece entre tarefas. Trata-se de adaptação da dinâmica original, e é assim que deve ser lida — não como correção nem como aperfeiçoamento. Nenhum teste foi executado nesta entrega para comparar as duas dinâmicas, e por isso nada se afirma sobre qual delas representa melhor o fenômeno. A avaliação está registrada como pendência para a etapa seguinte.', 'Adaptação declarada nesta implementação: '));
filhos.push(bullet('a exigência adicional de que o agente que presta apoio seja mais competente que o solicitante, discutida na Seção 2.10, e a seleção de um único apoiador por evento, onde a formulação original admite múltiplos respondentes com ganhos acumulados.', 'Decisão de operacionalização deste trabalho: '));

filhos.push(p('A saturação individual e o atrito na rede traduzem-se em multiplicadores adimensionais no intervalo [0,1], obtidos por inferência difusa — fuzzificação dos estados contínuos de fadiga e atrito por funções de pertinência, avaliação por regras e defuzzificação —, procedimento proposto e ilustrado por Liu, Triantis e Sarangi (2011) para representar variáveis qualitativas em Dinâmica de Sistemas. Registre-se que os autores propõem e demonstram o método em aplicação, sem estabelecer validação geral dele; a adoção aqui é, portanto, de um procedimento proposto na literatura, e não de um procedimento validado. A produtividade efetiva resulta da modulação da produtividade nominal por esses multiplicadores:', { indent: false }));
filhos.push(equacao('PR_efetiva = PR_nominal · μ_cognitivo · μ_rede', 'pr_efetiva'));

filhos.push(p('A válvula que alimenta o estoque de retrabalho oculto é regida pela equação de falhas, na qual o risco basal da tarefa soma-se a uma parcela que cresce à medida que a degradação cognitiva avança:', { indent: false }));
filhos.push(equacao('TGE = PR_efetiva · ( F_base + R_error · ( 1 − μ_cognitivo ) )', 'tge'));
filhos.push(simbolo('F_base', '— risco basal de falha associado à dificuldade da tarefa;'));
filhos.push(simbolo('R_error', '— taxa de erro adicional sob degradação cognitiva.'));

filhos.push(p('A métrica terminal agrega os quatro relógios do projeto na fração do esforço contabilizado que corresponde a trabalho produtivo, razão entre o tempo de trabalho efetivo e a soma dos quatro relógios:', { indent: false }));
filhos.push(equacao('E_total = Σ TWᵢ / Σ ( TWᵢ + TLᵢ + TUᵢ + TRᵢ )', 'e_total'));
filhos.push(simbolo('TWᵢ', '— tempo de trabalho efetivo na tarefa i;'));
filhos.push(simbolo('TLᵢ', '— tempo de espera por suporte técnico;'));
filhos.push(simbolo('TUᵢ', '— tempo improdutivo por adiamento ou indisponibilidade da rede;'));
filhos.push(simbolo('TRᵢ', '— esforço de retrabalho contabilizado, decorrente de falhas detectadas. Não ocupa agente nem avança o cronograma na implementação atual (ver Seção 2.8).'));

filhos.push(p('A execução temporal dessas equações é governada por uma árvore de decisão de três portas, avaliada a cada passo. A Porta 1 detecta sobrecarga: quando o esforço exigido supera o limiar de saturação, o agente transita para processamento heurístico e, conforme o nível da restrição orçamentária, ou adia a tarefa ou a conclui com erro, injetando no estoque de retrabalho oculto uma parcela proporcional ao excesso sobre o limiar. A Porta 2 trata o hiato de competência, disparando requisição à rede e aplicando a equação (' + E('delta_c') + ') caso exista agente disponível e com confiança mútua suficiente. A Porta 3 corresponde à execução analítica nominal, acionada quando não há sobrecarga nem hiato de competência.'));


filhos.push(pRuns([
  { t: 'Os três estoques. ', b: true },
  { t: 'A camada de dinâmica de sistemas do modelo é composta por três estoques, cujas taxas de entrada e saída são alimentadas pelas decisões dos agentes. O desgaste cognitivo acumulado (S_DC) acumula a drenagem da bateria cognitiva de todos os agentes e mede o custo cognitivo total incorrido pela equipe. O progresso validado (S_PV) acumula a duração nominal das tarefas concluídas sem defeito, e é a única medida de avanço que o modelo considera legítima: uma tarefa concluída com defeito oculto não incrementa esse estoque, ainda que o cronograma a registre como pronta. A dívida técnica latente (S_UR) acumula o esforço de retrabalho que já foi gerado mas ainda não foi detectado, medido em períodos de trabalho futuro; é o estoque que materializa a diferença entre progresso aparente e progresso real.' },
]));
filhos.push(p('A separação entre S_PV e o simples número de tarefas concluídas é o mecanismo pelo qual o modelo representa a patologia central que o trabalho investiga: sob pressão, a equipe continua a marcar tarefas como concluídas enquanto S_PV estagna e S_UR cresce, de modo que o painel de controle do projeto melhora exatamente enquanto o projeto piora.'));
filhos.push(pRuns([
  { t: 'Portas de decisão. ', b: true },
  { t: 'A cada período, para cada tarefa elegível, o agente designado percorre uma árvore de três portas. A Porta 1 corresponde ao modo heurístico: acionada quando o esforço percebido excede o limiar de saturação, ela executa a tarefa com custo cognitivo elevado e probabilidade de defeito aumentada, e é a porta pela qual o defeito tende a ficar oculto. A Porta 2 corresponde ao adiamento: o agente reconhece que não dispõe de condições para executar a tarefa e a devolve à fila, incorrendo em tempo improdutivo. A Porta 3 corresponde à execução analítica: o agente executa a tarefa em modo deliberado, com custo cognitivo menor e risco de defeito reduzido ao patamar basal da faixa de dificuldade. A probabilidade de transição entre os modos é estocástica e governada pela Equação ' + E('p_heuristico') + '.' },
]));
filhos.push(equacao('p_heurístico = 1 / ( 1 + exp[ − ( E − τ_sat ) / s ] )', 'p_heuristico'));
filhos.push(simbolo('E', 'esforço percebido, conforme Equação ' + E('esforco') + ';'));
filhos.push(simbolo('τ_sat', 'limiar de saturação cognitiva do agente;'));
filhos.push(simbolo('s', 'parâmetro de suavidade da transição.'));
filhos.push(p('A formulação estocástica foi adotada porque o texto do TCC I descreve a transição como estocástica enquanto o pseudocódigo a escreve como limiar determinístico. Com s tendendo a zero a Equação ' + E('p_heuristico') + ' recupera o limiar determinístico, de modo que as duas leituras passam a ser alternativas testáveis por análise de sensibilidade em vez de escolhas arbitrárias.'));

filhos.push(h2('1.6  Sistema de inferência difusa e garantia de monotonicidade'));
filhos.push(p('Os multiplicadores de produtividade μ_cognitivo e μ_rede são produzidos por um sistema de inferência difusa de Mamdani–Assilian com duas entradas, três termos linguísticos triangulares por variável, base completa de nove regras e defuzzificação por centroide, conforme especificado na fase conceitual do trabalho e conforme a prática consolidada de acoplar lógica difusa a modelos de dinâmica de sistemas (LIU; TRIANTIS; SARANGI, 2011).'));
filhos.push(pRuns([
  { t: 'Requisito de monotonicidade. ', b: true },
  { t: 'A saída do sistema é um multiplicador de produtividade. Exige-se, portanto, que ela seja monotonicamente não crescente em ambas as entradas: a produtividade não pode aumentar quando a fadiga ou a pressão aumentam. Trata-se de requisito estrutural do modelo, e não de preferência estética; sua violação tornaria possível que uma equipe mais fatigada produzisse mais.' },
]));
filhos.push(p('A implementação inicial, fiel à especificação conceitual, empregava a t-norma mínimo, isto é, a inferência conhecida como Max-Min. A superfície resultante apresentou regiões de derivada positiva. O refinamento sucessivo da malha de integração mostrou que o efeito não era artefato de discretização: a violação escalava linearmente com o passo da malha, convergindo para uma derivada positiva máxima de aproximadamente 0,26.'));
filhos.push(pRuns([
  { t: 'A causa é um resultado formal. ', b: true },
  { t: 'Van Broekhoven e De Baets (2009) demonstram que a monotonicidade de modelos de Mamdani–Assilian sob defuzzificação por centroide não decorre de a base de regras ser monótona, e enumeram as cinco únicas configurações para as quais a garantia existe. Para modelos de duas entradas há uma única configuração garantida: t-norma produto com base de regras monótona e suave. A combinação de duas entradas com t-norma mínimo não figura entre elas. A não monotonicidade observada não era, portanto, defeito de implementação nem ruído numérico, mas o comportamento previsto pela teoria para a configuração escolhida.' },
]));
filhos.push(p('Duas premissas do teorema foram verificadas por código sobre a base de regras adotada. A primeira, de que a base seja monótona e suave nos termos das Definições 2.1 e 2.2 dos autores, já era satisfeita: as diferenças de índice de consequente entre regras vizinhas são todas nulas ou unitárias. A segunda, de que os termos de saída constituam uma partição difusa, não era satisfeita pelos conjuntos originalmente adotados, cujas pertinências somavam entre zero e um ao longo do domínio.'));
filhos.push(pRuns([
  { t: 'Decisão metodológica. ', b: true },
  { t: 'Adotou-se a configuração garantida: t-norma produto e partição difusa uniforme na saída. A configuração originalmente especificada foi mantida como valor alternativo do parâmetro declarado t_norma e é executada em varredura, de modo que a diferença entre as duas seja medida e não decretada. A Tabela ' + T('fuzzy_config') + ' apresenta a medição sobre malha de 161 por 161 pontos.' },
]));
filhos.push(tituloTabela('fuzzy_config', 'Maior derivada positiva da superfície difusa por configuração de inferência'));
filhos.push(tabela(
  [5230, 1920, 1920],
  ['Configuração', 'Garantida pelo teorema', 'Maior derivada positiva'],
  [
    ['t-norma mínimo com conjuntos originais (especificação conceitual)', 'não', '0,258112'],
    ['t-norma produto com conjuntos originais', 'não', '0,000000'],
    ['t-norma mínimo com partição difusa', 'não', '0,420881'],
    ['t-norma produto com partição difusa (configuração adotada)', 'sim', '0,000000'],
  ],
  { centrar: [1, 2] },
));
filhos.push(legenda('Fonte: Dados da pesquisa (2026). A garantia corresponde à linha 4 da Tabela IX de Van Broekhoven e De Baets (2009).'));
filhos.push(p('A configuração adotada é exatamente monótona dentro da precisão da integração numérica, com derivada positiva máxima da ordem de 10⁻¹⁴. O critério de verificação deixou de ser uma tolerância arbitrada por este trabalho e passou a ser a previsão do teorema. A verificação exige, adicionalmente, que a configuração de t-norma mínimo continue violando a monotonicidade: caso deixasse de violar, o diagnóstico estaria incorreto e a substituição da t-norma perderia justificativa.'));
filhos.push(p('A adoção da partição uniforme teve um efeito colateral favorável ao rigor do modelo: os centros dos termos de saída passaram a ser estruturais, com núcleos em zero, meio e um, e dois parâmetros anteriormente arbitrados deixaram de existir.'));

filhos.push(h2('1.7  Instrumental de calibração empírica'));
filhos.push(p('As equações anteriores descrevem o modelo; as seguintes descrevem os métodos empregados para estimar, a partir de dados observados, os parâmetros Dᵢ e F_base que nelas aparecem. As equações (' + E2('logistica','vif') + ') constituem o instrumental estatístico; as (' + E2('nc','rs') + '), os parâmetros de delineamento das instâncias; e as (' + E2('folga','f_base') + '), a construção do índice de dificuldade e a transferência de risco entre domínios.'));

filhos.push(p('A associação entre métricas e ocorrência de defeito é modelada por regressão logística. Como o desfecho é binário, modela-se o logaritmo da chance, e não a probabilidade — esta é limitada ao intervalo [0,1], que uma função linear extrapolaria:', { indent: false }));
filhos.push(equacao('ln [ p / ( 1 − p ) ] = β₀ + β₁x₁ + β₂x₂ + … + βₚxₚ', 'logistica'));
filhos.push(simbolo('p', '— probabilidade de o módulo ser defeituoso;'));
filhos.push(simbolo('xᵢ', '— variáveis explicativas, incluindo o projeto de origem como fator;'));
filhos.push(simbolo('βᵢ', '— coeficientes estimados por máxima verossimilhança.'));

filhos.push(p('A interpretação dos coeficientes dá-se pela razão de chances, que exprime por quanto a chance de defeito é multiplicada a cada aumento unitário na variável, mantidas as demais constantes:', { indent: false }));
filhos.push(equacao('RC = exp(β)', 'rc'));

filhos.push(p('A comparação entre modelos aninhados emprega o teste da razão de verossimilhança, cuja estatística segue aproximadamente uma distribuição qui-quadrado com graus de liberdade iguais ao número de parâmetros adicionais:', { indent: false }));
filhos.push(equacao('LR = 2 ( ℓ_completo − ℓ_reduzido )  ~  χ² ( gl )', 'lr'));

filhos.push(p('O diagnóstico de multicolinearidade utiliza o fator de inflação da variância, obtido da regressão auxiliar de cada variável contra as demais:', { indent: false }));
filhos.push(equacao('VIFⱼ = 1 / ( 1 − R²ⱼ )', 'vif'));

filhos.push(p('Os três parâmetros de delineamento das instâncias do PSPLIB, conforme Kolisch, Sprecher e Drexl (1995), são a complexidade de rede, o fator de recursos e a força de recursos:', { indent: false }));
filhos.push(equacao('NC = | A | / | V |', 'nc'));
filhos.push(simbolo('| A |', '— número de arcos de precedência;  | V | — número de atividades, incluindo as fictícias.'));
filhos.push(equacao('RF = ( 1/n ) · Σⱼ [ ( 1/K ) · Σₖ 1{ rⱼₖ > 0 } ]', 'rf'));
filhos.push(simbolo('n, K', '— número de atividades reais e de tipos de recurso;'));
filhos.push(simbolo('rⱼₖ', '— demanda da atividade j pelo recurso k;  1{·} — função indicadora.'));
filhos.push(equacao('RSₖ = ( aₖ − rₖᵐⁱⁿ ) / ( rₖᵐᵃˣ − rₖᵐⁱⁿ )', 'rs'));
filhos.push(simbolo('aₖ', '— disponibilidade do recurso k;'));
filhos.push(simbolo('rₖᵐⁱⁿ', '— maior demanda individual, menor disponibilidade que mantém o problema viável;'));
filhos.push(simbolo('rₖᵐᵃˣ', '— pico de demanda no cronograma de inícios mais cedo.'));

filhos.push(p('A criticidade de cada atividade é medida pela folga total, obtida das passagens para frente e para trás do método do caminho crítico:', { indent: false }));
filhos.push(equacao('folgaⱼ = LSⱼ − ESⱼ', 'folga'));
filhos.push(simbolo('ESⱼ, LSⱼ', '— início mais cedo e início mais tarde admissível sem atrasar o projeto.'));

filhos.push(p('O índice de dificuldade técnica compõe três grandezas, normalizadas para [0,1] dentro de cada instância:', { indent: false }));
filhos.push(equacao('dⱼ = ( durⱼ − dur_mín ) / ( dur_máx − dur_mín )', 'd_norm'));
filhos.push(equacao('rⱼ = ( 1/K ) · Σₖ ( rⱼₖ / aₖ )', 'r_int'));
filhos.push(equacao('cⱼ = 1 − folga_normⱼ', 'crit'));
filhos.push(p('sendo o índice a combinação ponderada dos três componentes:', { indent: false }));
filhos.push(equacao('Dⱼ = w₁ dⱼ + w₂ rⱼ + w₃ cⱼ ,   com  w₁ + w₂ + w₃ = 1', 'd_index'));
filhos.push(p('Os pesos são tratados como suposição de partida, fixados em 1/3 cada, e submetidos a análise de sensibilidade conforme reportado na Seção 2.5.'));

filhos.push(p('A transferência de risco entre domínios opera sobre razões, e não sobre níveis absolutos. Para cada nível ordinal ℓ, a razão de risco é estimada na base NASA em relação ao nível de referência ℓ₀:', { indent: false }));
filhos.push(equacao('RR( ℓ ) = F( ℓ ) / F( ℓ₀ )', 'rr'));
filhos.push(p('e o risco basal atribuído a uma tarefa do PSPLIB no nível ℓ resulta do produto dessa razão por uma taxa basal do domínio de engenharia:', { indent: false }));
filhos.push(equacao('F_base( ℓ ) = F_âncora × RR( ℓ )', 'f_base'));
filhos.push(simbolo('F(ℓ)', '— frequência de defeito observada no nível ℓ da base NASA;'));
filhos.push(simbolo('ℓ₀', '— nível de referência, correspondente à dificuldade mais baixa;'));
filhos.push(simbolo('F_âncora', '— taxa basal de retrabalho do domínio de engenharia; parâmetro do modelo, não estimado neste trabalho.'));


filhos.push(h2('1.8  Calibração do modelo e avaliação de identificabilidade'));
filhos.push(p('O modelo contém parâmetros que não são diretamente observáveis. Duas perguntas distintas precisam de resposta: qual o procedimento que os fixa a partir de dados, e qual a evidência de que esse procedimento de fato os identifica. Responder apenas à primeira entregaria um algoritmo em execução, sem demonstração de que ele extrai informação.'));
filhos.push(pRuns([
  { t: 'Procedimento. ', b: true },
  { t: 'Adotou-se o History Matching (ANDRIANAKIS et al., 2015). Em vez de buscar um vetor ótimo de parâmetros, o método descarta do espaço tudo o que é implausível à luz dos dados, e devolve um conjunto — designado NROY, do inglês not ruled out yet — em lugar de uma estimativa pontual. A medida de implausibilidade de cada saída e a regra de descarte são dadas pelas Equações ' + E('implaus_j') + ' e ' + E('implaus_max') + '.' },
]));
filhos.push(equacao('I_j( x ) = | z_j − f̄_j( x ) | / √( V_obs,j + V_sim,j + V_mod,j )', 'implaus_j'));
filhos.push(equacao('I( x ) = máx_j I_j( x ) ,   x ∈ NROY  ⟺  I( x ) ≤ 3', 'implaus_max'));
filhos.push(simbolo('z_j', 'valor observado da saída j;'));
filhos.push(simbolo('f̄_j(x)', 'média do simulador na saída j sob o vetor de parâmetros x;'));
filhos.push(simbolo('V_obs', 'variância da observação;'));
filhos.push(simbolo('V_sim', 'variância da média do simulador, decorrente da estocasticidade;'));
filhos.push(simbolo('V_mod', 'variância de discrepância entre modelo e realidade.'));
filhos.push(p('O corte em três desvios não é escolha deste trabalho. Pela desigualdade de Vysochanskii–Petunin, para distribuições unimodais dotadas de densidade e com variância finita, ao menos noventa e cinco por cento da massa de probabilidade situa-se a menos de três desvios da média (PUKELSHEIM, 1994), de modo que descartar valores com implausibilidade superior a três raramente descarta o vetor verdadeiro. As condições do resultado são registradas porque o corte se apoia nelas: a desigualdade não vale para uma distribuição unimodal qualquer.'));
filhos.push(pRuns([
  { t: 'Dispensa do emulador. ', b: true },
  { t: 'A literatura de History Matching recorre a emuladores estatísticos porque o simulador que se deseja calibrar costuma ser caro. O simulador aqui construído custa cerca de um décimo de segundo por execução, e o delineamento completo, com três mil e duzentas execuções, conclui em minutos. Avalia-se o simulador diretamente. A decisão elimina o termo de erro de emulação da Equação ' + E('implaus_j') + ', isto é, remove uma aproximação em vez de acrescentá-la. Caso o modelo venha a encarecer, o emulador pode ser introduzido sem alteração do restante do procedimento.' },
]));
filhos.push(pRuns([
  { t: 'Teste do gêmeo idêntico. ', b: true },
  { t: 'Para verificar se o procedimento identifica parâmetros, empregou-se o teste do gêmeo idêntico (McCULLOCH et al., 2022): geram-se observações sintéticas a partir de um vetor de parâmetros conhecido, executa-se a calibração sem informar esse vetor, e verifica-se se o conjunto NROY resultante o contém. Duas precauções de desenho foram adotadas. O vetor verdadeiro foi posicionado deliberadamente fora do centro das faixas, pois um alvo situado no meio do espaço não testa as bordas do procedimento. E as sementes aleatórias que geram as observações sintéticas são disjuntas das utilizadas pelo simulador durante a calibração; sem essa separação, o teste compararia ruído idêntico consigo mesmo e seria aprovado trivialmente.' },
]));
filhos.push(pRuns([
  { t: 'Limitação a declarar. ', b: true },
  { t: 'No teste do gêmeo idêntico o modelo é, por construção, a própria verdade, de modo que a variância de discrepância V_mod é nula. O teste é, portanto, otimista: mede se o procedimento identifica parâmetros no cenário mais favorável concebível. A reprovação nele condenaria o procedimento, mas a aprovação não garante desempenho equivalente diante de dados reais, situação em que V_mod é positiva e precisa ser especificada. Essa assimetria é mantida explícita na leitura dos resultados.' },
]));

filhos.push(h2('1.9  Matriz de cenários e desenho experimental'));
filhos.push(p('O experimento central do trabalho contrasta dois arranjos de governança submetidos a condições externas idênticas. A Tabela ' + T('cenarios') + ' apresenta os parâmetros organizacionais que os distinguem. Todos os demais elementos — instâncias de projeto, índice de dificuldade das tarefas, disponibilidade de recursos e função de pressão — são idênticos entre os braços, e constituem o controle experimental.'));
filhos.push(tituloTabela('cenarios', 'Matriz de cenários: parâmetros organizacionais que distinguem os arranjos'));
// `[DEC]` Esta tabela e MONTADA A PARTIR de outputs/tables/parametros_cenarios.csv,
// que por sua vez vem de config/parametros.yaml. A versao anterior trazia valores
// DIGITADOS e FABRICADOS: tres das quatro linhas divergiam do arquivo de
// configuracao e uma delas tinha o sentido invertido entre os bracos. O documento
// era internamente coerente, de modo que nenhuma revisao de texto poderia
// detecta-lo. Valor de parametro nao se digita.
const cenarios = lerCsv(`${TAB}/parametros_cenarios.csv`);
const nDiferem = cenarios.filter(r => r.difere === 'True' || r.difere === 'true').length;
filhos.push(tabela(
  [2100, 1500, 1500, 3970],
  ['Parâmetro', 'Centralizada', 'Adaptativa', 'Interpretação organizacional'],
  cenarios.map(r => [r.rotulo, br(r.centralizada), br(r.adaptativa), r.interpretacao]),
  { centrar: [1, 2] },
));
filhos.push(legenda('Fonte: Elaborado pela autora (2026), a partir de config/parametros.yaml.'));
filhos.push(pRuns([
  { t: 'Quatro parâmetros variam simultaneamente. ', b: true },
  { t: 'Os dois arranjos diferem em todos os quatro parâmetros organizacionais, e não apenas na probabilidade de reporte. Essa é uma limitação de delineamento que precisa ser declarada: um contraste que move quatro variáveis ao mesmo tempo não permite atribuir o efeito observado a nenhum mecanismo isolado. O experimento compara dois PACOTES de governança, e é assim que deve ser lido. A decomposição do efeito exige ablação, executada e apresentada na Seção 2.9 — cujo resultado obriga a qualificar parte da leitura mecanística deste experimento.' },
]));
filhos.push(pRuns([
  { t: 'Sobre a probabilidade de detecção. ', b: true },
  { t: 'A probabilidade de a dívida oculta aflorar por período é quatro vezes maior no arranjo adaptativo. Ela não é, portanto, uma constante do ambiente: é parte do pacote de governança, e responde pela diferença no tempo que o projeto passa aguardando o afloramento de defeitos já cometidos. Uma versão anterior deste documento afirmava que esse parâmetro era idêntico entre os braços e que não constituía variável de governança; a afirmação era falsa e foi corrigida.' },
]));

filhos.push(pRuns([
  { t: 'Segurança psicológica como mecanismo. ', b: true },
  { t: 'A probabilidade de reporte de defeito operacionaliza a noção de segurança psicológica: em um arranjo centralizado, o agente que detecta um defeito próprio antecipa custo pessoal ao reportá-lo e tende a ocultá-lo, alimentando o estoque de dívida técnica latente; em um arranjo adaptativo, o mesmo agente reporta, e o retrabalho é pago imediatamente e de forma visível. A relação entre segurança psicológica e disposição a reportar erros é sustentada na fase conceitual deste trabalho, que a apoia em literatura própria de comportamento organizacional. Esta entrega, porém, NÃO auditou essas fontes primárias, e elas não constam das referências aqui listadas. Em consequência, a relação é apresentada como PREMISSA DE MODELAGEM herdada da fase conceitual, e não como resultado estabelecido da literatura, e a verificação das fontes correspondentes fica registrada como pendência bibliográfica para a etapa seguinte. O que esta entrega afirma é apenas o que mediu: dado o parâmetro, como o modelo se comporta. O modelo não presume qual arranjo é superior; a diferença de desempenho emerge da interação entre ocultação, acúmulo de dívida e pressão de prazo.' },
]));
filhos.push(pRuns([
  { t: 'Delineamento pareado. ', b: true },
  { t: 'Cada par de execuções emprega a mesma instância e a mesma semente aleatória nos dois braços. A variação atribuível à instância e ao sorteio é, portanto, comum aos dois e cancela-se na diferença, o que eleva substancialmente a potência estatística em relação a um delineamento independente de mesmo tamanho. A inferência emprega o teste de Wilcoxon para amostras pareadas, e não o teste t, porque as saídas do modelo são assimétricas e limitadas inferiormente por zero. O tamanho de efeito é reportado pelo d de Cohen pareado e pela proporção de pares favoráveis, uma vez que, com centenas de pares, o valor-p isoladamente não distingue diferença relevante de diferença meramente detectável.' },
]));

filhos.push(h2('1.10  Pontos de acoplamento entre a calibração e o modelo'));
filhos.push(p('As duas formulações anteriores encontram-se em dois pontos precisos, e é esse encontro que define o escopo da presente entrega.'));
filhos.push(pRuns([
  { t: 'Primeiro acoplamento. ', b: true },
  { t: 'O índice Dᵢ, construído pela equação (' + E('d_index') + ') sobre as 28.800 tarefas do PSPLIB J60, é exatamente a grandeza que aparece no numerador da equação (' + E('esforco') + '). Antes desta etapa, a dificuldade técnica das tarefas seria um parâmetro arbitrado; ela passa a ser derivada de grandezas medidas nas próprias instâncias.' },
]));
filhos.push(pRuns([
  { t: 'Segundo acoplamento. ', b: true },
  { t: 'O risco basal F_base, obtido pela equação (' + E('f_base') + ') a partir da calibração sobre a base NASA, é o termo que aparece na equação de falhas (4), governando a válvula que alimenta o estoque de retrabalho oculto. Antes desta etapa, esse risco seria uma suposição; ele passa a ser um gradiente estimado empiricamente, com incerteza quantificada, ainda que ancorado a uma taxa basal a definir.' },
]));
filhos.push(p('Os resultados apresentados no capítulo seguinte referem-se integralmente a esses dois acoplamentos. Os demais componentes do modelo — a inferência difusa que produz μ_cognitivo e μ_rede, a árvore de decisão de três portas, os estoques e a integração temporal — encontram-se implementados e verificados, e são eles que produzem os resultados das Seções 2.7 a 2.11; a Seção 2.7 relaciona as verificações executadas sobre cada um.'));

// ============================================================
filhos.push(h1('2  RESULTADOS INICIAIS E DISCUSSÃO'));

filhos.push(h2('2.1  Arquitetura e implementação da solução inicial'));
filhos.push(p('A primeira versão funcional do pipeline de dados foi concluída e verificada. Os requisitos essenciais de rastreabilidade, imutabilidade e verificação automática foram atendidos. A Figura ' + F('arquitetura') + ' apresenta a arquitetura implementada, organizada em três camadas: dados brutos imutáveis, scripts de processamento e saídas auditáveis.'));
filhos.push(tituloFigura('arquitetura', 'Arquitetura do pipeline de dados implementado'));
filhos.push(figura('fig1_arquitetura_pipeline.png', 15.5, 0.633));
filhos.push(fonte('Dados da pesquisa (2026).'));
filhos.push(p('Como verificação independente de reprodutibilidade, o pipeline foi executado em dois ambientes computacionais distintos — sistemas operacionais e versões de biblioteca diferentes — produzindo resultados numericamente idênticos em todas as etapas.'));

filhos.push(h2('2.2  Métricas de desempenho e resultados dos ensaios'));
filhos.push(p('Os ensaios iniciais avaliaram três dimensões: a integridade dos dados de entrada, a fidelidade da base de análise em relação ao procedimento publicado que a gerou, e a magnitude e a estabilidade das associações estatísticas de interesse. A Tabela ' + T('ensaios') + ' consolida os indicadores obtidos.'));
filhos.push(tituloTabela('ensaios', 'Indicadores de desempenho obtidos nos ensaios iniciais'));
filhos.push(tabela(
  [1750, 2550, 3170, 1600],
  ['Módulo', 'Parâmetro analisado', 'Valor / métrica medida', 'Situação'],
  [
    ['01 – Auditoria', 'Cobertura e integridade dos arquivos brutos', '23 arquivos, 49.942 observações; resumo SHA-256 por arquivo', 'Atende'],
    ['01 – Auditoria', 'Correspondência entre pares ARFF e CSV', '4 de 5 pares equivalentes; JM1 divergente (10.885 vs. 13.204 registros)', 'Anomalia identificada'],
    ['03 – Validação', 'Reprodução de D′ para D″ pelo algoritmo publicado', '12 de 12 conjuntos reproduzidos no conjunto de módulos preservados', 'Atende'],
    ['03 – Validação', 'Resíduo não explicado pelo pseudocódigo', '46 de 17.377 registros (0,26%), restritos à escolha do rótulo', 'Documentado'],
    ['02 – Consolidação', 'Base única com rastreabilidade', '17.377 observações, 12 projetos, 20 métricas, 0 valores ausentes', 'Atende'],
    ['04 – Modelagem', 'Ganho explicativo da complexidade sobre o efeito de projeto', 'LR = 639,8; gl = 1; p ≈ 3,6 × 10⁻¹⁴¹', 'Atende'],
    ['04 – Modelagem', 'Efeito da complexidade ciclomática controlando o tamanho', 'RC = 0,944; IC 95% [0,870; 1,024]; p = 0,17', 'Não atende'],
    ['04 – Modelagem', 'Multicolinearidade entre métricas (VIF)', 'HALSTEAD_EFFORT = 23,1; HALSTEAD_DIFFICULTY = 15,2', 'Métricas excluídas'],
    ['05 – F_base', 'Ordenação do risco por faixa de complexidade', '0,147 / 0,285 / 0,348 / 0,439; tendência z = 25,6; p ≈ 1,8 × 10⁻¹⁴⁴', 'Atende'],
    ['05 – F_base', 'Sensibilidade aos pontos de corte', 'Ordenação monotônica preservada em 5 de 5 esquemas testados', 'Atende'],
    ['05 – F_base', 'Validação por exclusão sucessiva de projetos', 'Monotonicidade em 12 de 12 reamostragens; amplitude máxima 0,087', 'Atende'],
    ['J60 – Auditoria', 'Integridade estrutural das instâncias', '480 arquivos; 62 nós e 4 recursos renováveis em todos; 480/480 grafos acíclicos', 'Atende'],
    ['J60 – Auditoria', 'Reconstrução do delineamento experimental', 'Fatorial 3 × 4 × 4 = 48 células completo e balanceado, 10 instâncias por célula', 'Atende'],
    ['J60 – Índice Di', 'Ortogonalidade entre os componentes do índice', 'Spearman entre duração, intensidade e criticidade: −0,004; 0,003; 0,193', 'Atende'],
    ['J60 – Índice Di', 'Adequação da medida de criticidade prevista', 'Contagem de sucessores × folga total: Spearman 0,116', 'Substituída'],
    ['J60 – Índice Di', 'Sensibilidade da ordenação aos pesos', 'Menor correlação de ordenação entre 6 esquemas: 0,847', 'Atende'],
    ['Transferência', 'Gradiente de risco NASA → J60', 'RR = 1,00 / 1,94 / 2,37 / 2,99; IC 95% por bootstrap de projetos', 'Atende'],
    ['Transferência', 'Viés da correspondência direta de rótulos', 'Inflação de 1,74× no risco médio, por artefato do tamanho dos estratos', 'Método descartado'],
    ['Pipeline', 'Reprodutibilidade entre ambientes distintos', 'Resultados numericamente idênticos em duas execuções independentes', 'Atende'],
  ],
  { centrar: [3] },
));
filhos.push(legenda('Fonte: Dados da pesquisa (2026). RC = razão de chances; LR = estatística do teste da razão de verossimilhança; VIF = fator de inflação da variância.'));

filhos.push(h2('2.3  Discussão científica preliminar'));

filhos.push(p('A solução comporta-se de maneira estável sob as condições de ensaio. Três resultados merecem discussão.', { indent: false }));

filhos.push(pRuns([
  { t: 'Qualidade e proveniência dos dados. ', b: true },
  { t: 'A auditoria confirmou empiricamente as advertências de Shepperd et al. (2013) quanto à circulação de versões divergentes dos conjuntos NASA. Os cinco pares de arquivos do repositório Promise reproduzem exatamente as contagens tabuladas pelos autores, exceto o JM1: o arquivo em formato ARFF contém 10.885 registros, coincidindo com o catalogado, enquanto o arquivo CSV homônimo contém 13.204. Os dois arquivos compartilham praticamente o mesmo conjunto de observações distintas, diferindo na multiplicidade das repetições, o que indica que um deles já passou por remoção parcial de duplicatas antes de ser distribuído como bruto. A versão CSV foi, por isso, descartada.' },
]));

filhos.push(pRuns([
  { t: 'Fidelidade da base de análise. ', b: true },
  { t: 'Optou-se por utilizar a versão D″ publicada, e não por reproduzir a limpeza a partir dos dados brutos, porque o algoritmo dos autores pressupõe atributos (MODULE_ID, ERROR_DENSITY e ERROR_COUNT) ausentes das versões do repositório Promise disponíveis: aplicá-lo a essas versões constituiria adaptação, não replicação. Essa decisão exigia, contudo, verificar que os arquivos D″ são o que declaram ser. Dispondo também da versão D′, aplicaram-se a ela os dois passos do algoritmo que distinguem uma versão da outra — remoção de casos idênticos e de casos inconsistentes. O conjunto de módulos preservados foi reproduzido exatamente nos 12 conjuntos. Registrou-se, entretanto, uma discrepância: sob a leitura literal do pseudocódigo, que determina remover ambos os membros de um par inconsistente, apenas 4 dos 12 conjuntos são reproduzidos; sob a interpretação de que se preserva um representante por vetor de atributos, os 12 são reproduzidos em contagem. O resíduo restante — 46 registros, ou 0,26% da base — restringe-se a qual rótulo foi mantido nos grupos conflitantes. Conclui-se que os arquivos distribuídos são consistentes com o procedimento publicado quanto aos módulos selecionados, mas não seguem literalmente o pseudocódigo quanto ao tratamento do rótulo. O achado é registrado como limitação conhecida e quantificada da base, e é ele próprio um exemplo do problema de documentação de pré-processamento que os autores denunciam.' },
]));

filhos.push(pRuns([
  { t: 'Complexidade, tamanho e risco. ', b: true },
  { t: 'O resultado de maior consequência para o trabalho é negativo e foi obtido pelo teste que a metodologia previa. Isoladamente, a complexidade ciclomática apresenta associação forte com a ocorrência de defeito, mesmo controlando o projeto de origem (razão de chances 1,90 por unidade logarítmica; LR = 639,8). Contudo, ao se acrescentar o tamanho do módulo ao modelo, o efeito da complexidade desaparece: a razão de chances ajustada cai para 0,944, com intervalo de confiança de 95% entre 0,870 e 1,024 — contendo, portanto, o valor nulo — e p = 0,17. A relação inversa não se verifica: o tamanho sobrevive folgadamente ao controle pela complexidade (LR = 431,2; p ≈ 9 × 10⁻⁹⁶). A Figura ' + F('controle_tamanho') + ' apresenta o mesmo teste aplicado a todas as seis métricas candidatas. Uma delas — a complexidade de projeto — exibe efeito positivo com intervalo de confiança acima da unidade (razão de chances 1,098; IC 95% [1,010; 1,194]; p = 0,028); as demais que permanecem distinguíveis do nulo o fazem com sinal negativo, padrão característico de colinearidade e não de mecanismo causal. O efeito positivo isolado, porém, não sobrevive à correção para comparações múltiplas: as seis métricas foram testadas na mesma base, e sob o procedimento de Holm–Bonferroni o valor-p corrigido dessa métrica sobe a 0,084. NENHUMA das seis sobrevive à correção. A distinção é registrada porque a figura mostra o intervalo não corrigido: lida isoladamente, ela sugere um sobrevivente que a correção elimina.' },
]));

filhos.push(tituloFigura('controle_tamanho', 'Razões de chances das métricas candidatas antes e depois do controle pelo tamanho do módulo'));
filhos.push(figura('fig3_controle_por_tamanho.png', 15.5, 0.538));
filhos.push(fonte('Dados da pesquisa (2026).'));

filhos.push(p('Esse resultado não invalida o uso da complexidade como eixo ordinal, mas altera o que se pode afirmar a partir dele. A ordenação do risco pelas faixas de complexidade é forte e robusta, como mostram a Figura ' + F('fbase_faixa') + ' e a Tabela ' + T('ensaios') + ': o risco cresce monotonicamente de 0,147 a 0,439 entre a faixa mais baixa e a mais alta, e a monotonicidade se preserva sob todos os cinco esquemas alternativos de corte testados e sob todas as doze reamostragens por exclusão de projeto. O que os dados não sustentam é a atribuição causal: a complexidade ciclomática opera, nesta base, como marcador ordinal de risco correlacionado ao tamanho, e não como fator de risco independente dele. Para o propósito deste trabalho — transferência ordinal de risco entre domínios — um marcador estável é suficiente; a afirmação de efeito independente, que não seria sustentável, é explicitamente abandonada.'));

filhos.push(pRuns([
  { t: 'A força dos valores-p desta camada, e por que ela não deve ser lida ao pé da letra. ', b: true },
  { t: 'Os valores-p reportados na Tabela ' + T('ensaios') + ' para os modelos logísticos e para o teste de tendência são calculados sobre dezessete mil trezentos e setenta e sete módulos, tratados como observações independentes. Eles não são: os módulos estão agrupados em doze projetos, e módulos do mesmo projeto compartilham equipe, processo e período. Os modelos incluem o projeto de origem como efeito fixo, o que impede que uma associação seja atribuída a uma métrica quando puder ser explicada pela procedência da observação, mas isso trata o confundimento ENTRE projetos e não a dependência DENTRO de cada um. Em consequência, os erros-padrão estão subestimados e valores-p da ordem de dez elevado a menos cento e quarenta expressam o tamanho da base, não a força da evidência. O que sustenta a conclusão desta seção não são esses valores-p, e sim duas verificações que operam na unidade correta: a monotonicidade se preserva nas doze reamostragens por exclusão sucessiva de projeto, e os intervalos das razões de risco por faixa são obtidos por reamostragem de PROJETOS, não de módulos. A inferência com erros-padrão robustos a agrupamento fica registrada como pendência; ela não altera as estimativas pontuais, apenas a precisão declarada.' },
]));
filhos.push(tituloFigura('fbase_faixa', 'Risco basal por faixa de complexidade ciclomática, em frequência bruta e em probabilidade ajustada pelo efeito do projeto de origem'));
filhos.push(figura('fig2_fbase_por_faixa.png', 14.5, 0.587));
filhos.push(fonte('Dados da pesquisa (2026).'));

filhos.push(p('As faixas adotadas — v(G) ≤ 10, de 11 a 15, de 16 a 20 e acima de 20 — constituem adaptação metodológica deste trabalho a partir das faixas interpretativas do NASA Software Engineering Handbook, cujo requisito SWE-220 estabelece o limiar de 15 para software crítico de segurança e exige revisão formal e justificativa documentada para qualquer excedente. As faixas da fonte original são cinco e sobrepõem-se nos extremos; a adaptação a quatro níveis não sobrepostos, alinhada ao limiar normativo, é registrada como decisão deste trabalho e não como classificação oficial.'));

filhos.push(tituloFigura('loo', 'Estabilidade da ordenação sob exclusão sucessiva de cada projeto'));
filhos.push(figura('fig4_estabilidade_loo.png', 14.5, 0.576));
filhos.push(fonte('Dados da pesquisa (2026).'));

filhos.push(pRuns([
  { t: 'Limitações. ', b: true },
  { t: 'Três limitações condicionam a leitura destes resultados. Primeira, e mais importante, os dados NASA descrevem módulos de software, ao passo que o objeto do trabalho são tarefas de projetos de engenharia; não se afirma equivalência métrica entre os domínios, e a transferência prevista é ordinal, não cardinal — a ser explicitamente qualificada na monografia. Segunda, a proveniência dos arquivos utilizados é de segunda mão: os arquivos do repositório Promise foram obtidos por meio de um espelho público que declara sua origem, e os arquivos D′ e D″ têm data anterior ao artigo que os descreve, o que recomenda confirmação junto à coleção oficial dos autores antes da redação final. Terceira, a métrica HALSTEAD_ERROR_EST foi deliberadamente excluída da seleção por circularidade: sendo definida como estimativa do número de erros derivada do volume do programa, seu uso para explicar a ocorrência de defeito equivaleria a prever defeito a partir de uma previsão de defeito; sua correlação de Spearman de 0,979 com HALSTEAD_EFFORT confirma que ela não carrega informação estrutural independente.' },
]));

filhos.push(pRuns([
  { t: 'Consequência para a próxima etapa. ', b: true },
  { t: 'O achado sobre complexidade e tamanho tem implicação direta sobre a construção do índice de dificuldade técnica no PSPLIB J60. O componente do índice análogo à magnitude da tarefa — duração normalizada e intensidade de recursos — encontra respaldo empírico na base NASA, ao passo que o componente análogo à complexidade estrutural, a criticidade na rede de precedências, não encontra respaldo independente. Recomenda-se, portanto, ponderar conservadoramente o componente estrutural e submetê-lo a análise de sensibilidade específica, em vez de tratá-lo como equivalente ao componente de magnitude. A decisão final sobre a ponderação será tomada após a caracterização do J60 e registrada no guia metodológico.' },
]));

filhos.push(h2('2.4  Caracterização da base PSPLIB J60'));
filhos.push(p('A segunda base do trabalho, que fornece a estrutura de execução de projeto — tarefas, precedências, durações e restrições de recursos —, foi auditada com o mesmo protocolo. As 480 instâncias do conjunto J60 foram lidas diretamente do formato original, sem intermediários, e verificadas quanto à integridade estrutural: todas declaram 62 atividades, sendo 60 reais e duas fictícias, e 4 recursos renováveis; os 480 grafos de precedência são acíclicos.'));
filhos.push(p('A verificação central, contudo, não é estrutural e sim de delineamento. As instâncias do PSPLIB são geradas por um projeto experimental fatorial sobre três parâmetros definidos por Kolisch, Sprecher e Drexl (1995): a complexidade de rede, dada pela razão entre arcos de precedência e atividades; o fator de recursos, que mede a fração média de tipos de recurso requisitados por atividade; e a força de recursos, que posiciona a disponibilidade entre o mínimo de viabilidade e o pico de demanda do cronograma de inícios mais cedo. Os três parâmetros foram recalculados a partir dos arquivos e seus níveis foram reconstruídos por agrupamento dos valores obtidos, sem que nenhum valor de referência fosse suposto. A Tabela ' + T('j60_grade') + ' apresenta o resultado.'));
filhos.push(tituloTabela('j60_grade', 'Níveis dos parâmetros de delineamento reconstruídos a partir das instâncias'));
filhos.push(tabela(
  [2400, 3670, 3000],
  ['Parâmetro', 'Níveis reconstruídos dos arquivos', 'Níveis nominais do delineamento'],
  [
    ['Complexidade de rede (NC)', '1,5000 / 1,8065 / 2,1129', '1,5 / 1,8 / 2,1'],
    ['Fator de recursos (RF)', '0,2500 / 0,5042 / 0,7542 / 1,0000', '0,25 / 0,50 / 0,75 / 1,00'],
    ['Força de recursos (RS)', '0,1975 / 0,5106 / 0,7038 / 1,0000', '0,20 / 0,50 / 0,70 / 1,00'],
  ],
  { centrar: [1, 2] },
));
filhos.push(legenda('Fonte: Dados da pesquisa (2026).'));
filhos.push(p('A reconstrução recupera um delineamento fatorial completo e balanceado de 3 × 4 × 4 = 48 células, com exatamente uma combinação por célula e dez instâncias por combinação. Como os níveis foram derivados dos próprios arquivos, o resultado valida simultaneamente a rotina de leitura e as três formulações implementadas.'));
filhos.push(p('Registrou-se ainda uma característica relevante do conjunto: a complexidade de rede e o fator de recursos são exatamente constantes dentro de cada combinação, ao passo que a força de recursos não é, variando em até 0,12 dentro de uma mesma célula. A causa é estrutural e não constitui defeito: a disponibilidade de cada recurso é um número inteiro, de modo que o gerador não realiza exatamente o valor pretendido e arredonda. A consequência metodológica é que o nível nominal e o valor realizado são variáveis distintas — o primeiro é um fator do delineamento, o segundo uma medida contínua — e tratá-los como equivalentes converteria ruído de arredondamento em variação experimental. Nos modelos subsequentes, o nível nominal será utilizado como fator e o valor realizado, quando pertinente, como covariável.'));

filhos.push(h2('2.5  Índice de dificuldade técnica das tarefas'));
filhos.push(p('Com as instâncias caracterizadas, construiu-se o índice de dificuldade técnica que atribui a cada tarefa um nível ordinal. O índice, definido pelas equações (' + E2('d_norm','d_index') + '), combina três grandezas medidas nas próprias instâncias: a duração normalizada, a intensidade de uso de recursos — definida como a fração média da disponibilidade de cada recurso que a tarefa consome, adaptação por atividade do fator de recursos de Kolisch, Sprecher e Drexl (1995) — e a criticidade na rede de precedências. As normalizações são feitas dentro de cada instância, uma vez que o modelo compara tarefas de um mesmo projeto e não tarefas de projetos distintos.'));
filhos.push(pRuns([
  { t: 'Correção de uma atribuição de fonte. ', b: true },
  { t: 'A formulação preliminar deste trabalho atribuía a construção do índice a De Reyck e Herroelen (1996). A verificação da fonte mostrou que a atribuição era imprópria: o índice de complexidade ali discutido deriva de Bein, Kamburowski e Stallmann (1992) e mede a distância da rede inteira à série-paralelidade, sendo uma propriedade do grafo e não da atividade. A referência foi mantida no trabalho, porém realocada para sustentar a caracterização da rede por instância, e o índice por tarefa passou a ser declarado como construção deste trabalho, com cada componente apoiado em fonte própria.' },
]));
filhos.push(pRuns([
  { t: 'Substituição da medida de criticidade. ', b: true },
  { t: 'A formulação preliminar previa a contagem de sucessores como medida de criticidade. Comparada à folga total obtida do método do caminho crítico, sobre as mesmas 28.800 tarefas, a correlação de Spearman entre as duas é de apenas 0,116, e 3.488 tarefas apresentam folga acima da mediana e três ou mais sucessores — isto é, muitos sucessores e nenhuma urgência. A criticidade passou a ser medida pela folga total, que é a medida canônica no nível da atividade. A contagem de sucessores permanece calculada e gravada na base, disponível como variável alternativa para análise de sensibilidade.' },
]));
filhos.push(p('Os três componentes mostram-se quase ortogonais entre si, com correlações de Spearman de −0,004 entre duração e intensidade de recursos, 0,003 entre intensidade e criticidade, e 0,193 entre duração e criticidade. Cada um carrega, portanto, informação distinta, e o índice composto não é uma única grandeza sob três nomes — situação oposta à observada na base NASA, onde complexidade e tamanho apresentavam correlação de 0,752 e o composto colapsava sobre um único eixo. A Figura ' + F('niveis_di') + ' apresenta o comportamento dos níveis resultantes.'));
filhos.push(tituloFigura('niveis_di', 'Duração média e folga total média por nível de dificuldade'));
filhos.push(figura('fig6_niveis_di.png', 15.5, 0.478));
filhos.push(fonte('Dados da pesquisa (2026).'));
filhos.push(p('A duração média cresce e a folga média decresce monotonicamente ao longo dos quatro níveis, comportamento coerente com a interpretação do índice. Os pontos de corte são os quartis da distribuição, decisão declarada deste trabalho: ao contrário do domínio de software, que dispõe do limiar normativo do requisito SWE-220, não há para tarefas de projeto um limiar externo equivalente. A ordenação mostrou-se razoavelmente robusta à ponderação: entre seis esquemas alternativos de pesos, a menor correlação de ordenação observada foi de 0,847.'));

filhos.push(h2('2.6  Transferência ordinal de risco'));
filhos.push(p('A etapa que liga as duas bases consiste em atribuir às tarefas do PSPLIB o risco calibrado sobre os módulos da NASA. A forma dessa atribuição não é indiferente, e a decisão adotada apoia-se em evidência numérica.'));
filhos.push(p('Os quatro níveis não têm o mesmo tamanho relativo nos dois domínios: na base NASA, 86,24% dos módulos situam-se no nível mais baixo, contra 25,00% das tarefas do J60, por construção dos quartis. Atribuir a cada nível do J60 o risco absoluto do nível homônimo da NASA produziria risco médio de 0,3046 nas tarefas, contra taxa observada de 0,1749 na NASA — uma inflação de 1,74 vezes gerada exclusivamente pela diferença de tamanho dos estratos, e não por qualquer propriedade das tarefas. Seria um artefato de construção apresentado como resultado.'));
filhos.push(p('Adotou-se, portanto, a transferência por razão de risco relativo, conforme as equações (' + E('rr') + ') e (' + E('f_base') + '). O que os dados NASA sustentam não é o nível absoluto de risco de um módulo de software, que não tem razão para valer em tarefas de engenharia, e sim a forma do gradiente: quantas vezes mais arriscada é uma tarefa difícil em relação a uma fácil. Essa razão é adimensional e independe da taxa basal do domínio. A Tabela ' + T('razoes_risco') + ' e a Figura ' + F('gradiente') + ' apresentam as razões estimadas.'));
filhos.push(tituloTabela('razoes_risco', 'Razões de risco transferidas, com intervalos por reamostragem de projetos'));
filhos.push(tabela(
  [2500, 2200, 2000, 2370],
  ['Nível de dificuldade', 'Risco basal NASA', 'Razão de risco', 'IC 95% (bootstrap)'],
  [
    ['baixa (referência)', '0,1470', '1,000', '—'],
    ['média', '0,2845', '1,935', '[1,758; 2,599]'],
    ['alta', '0,3479', '2,367', '[1,720; 3,229]'],
    ['muito alta', '0,4388', '2,985', '[1,878; 4,156]'],
  ],
  { centrar: [1, 2, 3] },
));
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Bootstrap com 4.000 réplicas, reamostrando projetos.'));
filhos.push(tituloFigura('gradiente', 'Gradiente de risco transferido, com intervalo de confiança'));
filhos.push(figura('fig5_gradiente_risco.png', 14.0, 0.609));
filhos.push(fonte('Dados da pesquisa (2026).'));
filhos.push(pRuns([
  { t: 'Unidade de reamostragem. ', b: true },
  { t: 'Os intervalos foram obtidos reamostrando projetos, e não observações individuais. As observações de um mesmo projeto não são independentes, pois compartilham equipe, processo, domínio de aplicação e critério de registro de defeito; reamostrar módulos trataria 17.377 observações como 17.377 evidências independentes e produziria intervalos artificialmente estreitos. A unidade de agrupamento correta é o projeto — o mesmo raciocínio que fundamenta a validação por exclusão sucessiva de projetos apresentada na Seção 2.3.' },
]));
filhos.push(p('Os intervalos resultantes são largos, sobretudo no nível mais alto, cujo limite superior alcança 4,156. Isso constitui informação e não deficiência: com doze projetos, a incerteza sobre o gradiente é substancial, e reportá-la é preferível a apresentar a estimativa pontual como se fosse precisa.'));
filhos.push(pRuns([
  { t: 'A âncora do modelo. ', b: true },
  { t: 'A razão de risco fixa a forma da relação, não o seu nível. O risco atribuído a uma tarefa é o produto da razão por uma taxa basal de retrabalho do domínio de engenharia, que este trabalho não estima e trata explicitamente como parâmetro do modelo, a ser fixado por dado do domínio ou tratado como incerteza na simulação. Por essa razão, a base de tarefas resultante grava o multiplicador de risco e seu intervalo, e não uma probabilidade absoluta: gravar a probabilidade embutiria um valor arbitrário na base como se fosse dado observado.' },
]));
filhos.push(pRuns([
  { t: 'Limitação a declarar. ', b: true },
  { t: 'A construção assume que o gradiente ordinal de risco por dificuldade é transferível entre domínios, ainda que o nível absoluto não seja. Trata-se de suposição e não de resultado. É uma suposição mais fraca do que a de equivalência métrica direta, que os dados não sustentam, mas não é vazia, e será mantida explícita na redação final.' },
]));


filhos.push(h2('2.7  Verificação do simulador'));
filhos.push(pRuns([
  { t: 'O que cada verificação sustenta. ', b: true },
  { t: 'A seção intitulava-se “verificação e validação”. O termo validação foi retirado: não há neste trabalho critério confrontado com dado externo capaz de reprovar o modelo, e chamar de validação um teste que não pode reprovar nada seria atribuir ao resultado uma força que ele não tem. As verificações passam a ser declaradas por classe, e a classe determina o que se pode afirmar a partir delas.' },
]));
filhos.push(bullet('passam qualquer que seja o modelo, porque decorrem da forma como a grandeza é construída. São registradas para que não sejam confundidas com evidência. Exemplo: com risco basal e pressão nulos, a dívida técnica é nula porque o termo que a gera foi zerado.', 'Verdadeiras por construção: '));
filhos.push(bullet('conservação de tarefas, precedências, disponibilidade de recursos e consistência dos relógios. Um simulador correto não pode falhá-las, e falhá-las indica defeito de código.', 'Invariantes estruturais: '));
filhos.push(bullet('testam se o código realiza a direção que a formulação prevê. Não constituem evidência sobre equipes reais e não restringem magnitude.', 'Verificações de implementação: '));
filhos.push(bullet('confrontam a saída com a literatura de campo numa faixa larga. Rejeitam desalinhamento grosseiro e nada mais; não calibram parâmetro algum.', 'Verificações de ordem de grandeza: '));
filhos.push(p('A Tabela ' + T('verificacoes') + ' apresenta o conjunto executado, com a classe de cada verificação e o valor medido. Uma propriedade esperada que não se confirma é registrada como tal, e não convertida em aprovação nem suprimida.', { indent: false }));
filhos.push(tituloTabela('verificacoes', 'Verificações do simulador, por classe, e seus resultados'));
{
  const v = lerCsvPV(caminhoTabela('entrega_verificacoes.csv'));
  filhos.push(tabela(
    [620, 3250, 1550, 1500, 2150],
    ['Id', 'Verificação', 'Classe', 'Situação', 'Medido'],
    v.map(r => [r.id, r.verificacao, r.classe, r.situacao, r.medido]),
    { centrar: [0, 2, 3] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026).'));

filhos.push(pRuns([
  { t: 'Correção do teste de tendência sob pressão. ', b: true },
  { t: 'A verificação de que a dívida técnica cresce com a pressão calculava a correlação de Spearman sobre cinco médias, uma por nível de pressão, e reportava o valor-p assintótico devolvido pela biblioteca. Esse valor-p não é utilizável com cinco observações: o menor valor-p bilateral exato possível nesse caso é a razão entre duas e cento e vinte permutações, ou seja, aproximadamente dezessete milésimos. Um valor-p de ordem de grandeza muito inferior a esse não é atingível e não podia ter sido apresentado como evidência. O teste também rodava em apenas um braço e uma instância, e a agregação em cinco médias descartava as quarenta repetições de cada nível.' },
]));
filhos.push(p('O teste foi refeito sobre os pontos individuais, nos dois braços e em duas instâncias, com delineamento em duas etapas. Na primeira, um piloto de duzentas execuções por célula estima o tamanho de efeito. Na segunda, o número de repetições é fixado por cálculo de potência antes da execução, e o teste confirmatório roda com sementes disjuntas das do piloto, de modo que a escolha do tamanho amostral não contamine o resultado. O critério permaneceu inalterado — correlação positiva e valor-p abaixo de cinco centésimos —; apenas o número de repetições mudou. A Tabela ' + T('tendencia') + ' apresenta o resultado.'));
filhos.push(tituloTabela('tendencia', 'Tendência sob pressão: piloto e teste confirmatório, por braço'));
{
  const b1 = lerCsvPV(caminhoTabela('entrega_b1_tendencia.csv'));
  filhos.push(tabela(
    [2900, 1750, 1750, 1750, 1750, 1170],
    ['Grandeza', 'Braço', 'ρ piloto (n = 200)', 'ρ confirmatório (n = 500)', 'IC 95% confirmatório', 'Confirma'],
    b1.map(r => [r.grandeza, r.cenario, r.rho_piloto_n200, r.rho_confirmatorio_n500, r.ic95_confirmatorio, r.confirma]),
    { centrar: [1, 2, 3, 4, 5] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Piloto com sementes 0 a 39; confirmatório com sementes 1000 a 1099, disjuntas.'));
filhos.push(pRuns([
  { t: 'O que a correção mudou. ', b: true },
  { t: 'No braço adaptativo, a dívida oculta de pico não apresentava tendência detectável com duzentas execuções e passa a apresentá-la com quinhentas, exatamente como o cálculo de potência previa: tratava-se de teste subdimensionado, não de propriedade ausente. Já a contagem de defeitos gerados continua sem se confirmar nesse braço mesmo com potência adequada, e a razão foi medida, não suposta. São duas causas somadas. A primeira é que a pressão é endógena ao atraso: o braço adaptativo conclui mais perto do caminho crítico, atrasa menos e por isso recebe apenas cinquenta e sete por cento da amplitude de pressão que o braço centralizado recebe para o mesmo teto nominal. A segunda é que o canal de defeito é pouco sensível à pressão nesta parametrização — a pressão acrescenta no máximo quarenta e sete milésimos à probabilidade de falha, sobre uma base que varia de um décimo a três décimos conforme a faixa de dificuldade, de modo que a dificuldade domina a pressão por um fator entre três e vinte. Nenhuma das duas é defeito de código; ambas são propriedades declaradas do modelo calibrado. O resultado é registrado como não confirmado, e não confirmado não significa refutado: o intervalo de confiança contém tanto o zero quanto efeitos positivos pequenos.' },
]));

filhos.push(pRuns([
  { t: 'Verificação de ordem de grandeza e seu poder de rejeição. ', b: true },
  { t: 'A fração de esforço dedicada a retrabalho foi confrontada com a literatura de campo. A referência medida na mesma unidade da saída do modelo é a de Boehm e Basili (2001), segundo a qual projetos de software despendem entre quarenta e cinquenta por cento do esforço em retrabalho evitável. As cifras de Love et al. (2026) e de Love e Li (2000), da construção civil, são retidas apenas como piso de ordem de grandeza, com a ressalva explícita de que sua base é o valor de contrato e não o esforço, o que as torna grandezas de unidades distintas. Esta verificação era anteriormente apresentada como validação externa. Não é. Um critério de validação precisa poder reprovar, e este aprova em toda a faixa declarada do parâmetro de risco basal, como mostra a Tabela ' + T('poder_9a') + '. Seu poder de rejeição sobre esse parâmetro é nulo, e ele é portanto rebaixado a verificação de ordem de grandeza: rejeita desalinhamento grosseiro e nada mais, não confirma o modelo e não substitui calibração.' },
]));
filhos.push(tituloTabela('poder_9a', 'Poder de rejeição do critério de plausibilidade sobre o risco basal'));
{
  const b3 = lerCsvPV(caminhoTabela('entrega_b3_poder.csv'));
  filhos.push(tabela(
    [3000, 3000, 3070],
    ['F_âncora', 'Mediana do retrabalho sobre o plano', 'Critério'],
    b3.map(r => [r.f_ancora, r.mediana, r.criterio_9a]),
    { centrar: [0, 1, 2] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026). A faixa varrida é a faixa aberta declarada para o parâmetro.'));

filhos.push(h2('2.8  Experimento central: governança centralizada e adaptativa'));
filhos.push(p('O experimento comparou os dois arranjos da Tabela ' + T('cenarios') + ' sobre dezesseis instâncias do J60 com doze sementes cada, totalizando trezentas e oitenta e quatro execuções pareadas. Nenhuma execução deixou de concluir dentro do horizonte estabelecido. A Tabela ' + T('experimento') + ' apresenta os resultados.'));
filhos.push(tituloTabela('experimento', 'Comparação pareada entre os arranjos de governança, por instância'));
{
  const ex = lerCsvPV(caminhoTabela('entrega_experimento.csv'));
  filhos.push(tabela(
    [2620, 1180, 1180, 1080, 1080, 1160, 770],
    ['Indicador', 'Centraliz.', 'Adaptat.', 'Variação', 'd de Cohen', 'Instâncias favor.', 'p'],
    ex.map(r => [r.indicador, r.centralizada, r.adaptativa, r.variacao, r.d_cohen, r.instancias_favoraveis, r.p]),
    { centrar: [1, 2, 3, 4, 5, 6] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Dezesseis instâncias, cada uma com a média das suas doze sementes. “= piso” indica que o valor-p atingiu 3,05 × 10⁻⁵, o menor possível com dezesseis pares. A última linha é métrica de diagnóstico, discutida adiante.'));
filhos.push(pRuns([
  { t: 'O atraso depende da definição de conclusão. ', b: true },
  { t: 'O laço de simulação só encerra quando, além de todas as tarefas concluídas, a dívida oculta pendente foi integralmente detectada. O makespan aqui reportado inclui, portanto, uma cauda posterior à conclusão da última tarefa, durante a qual nenhuma tarefa está ativa e o projeto apenas aguarda que a dívida aflore. Essa cauda é maior no arranjo centralizado, que acumula mais dívida oculta e a detecta com probabilidade menor. Em consequência, a magnitude do contraste de atraso é condicionada à definição operacional de conclusão adotada, e não é independente dela: medido até a conclusão da última tarefa, e não até a quitação da dívida, o contraste seria menor. As duas definições são legítimas e medem coisas diferentes — prazo até entregar e prazo até estabilizar —, e apenas a segunda está implementada. Quantificar a alternativa exige alterar a condição de parada, o que não foi feito nesta entrega; a comparação entre as duas medidas está registrada como pendência. O sinal do efeito não está em questão: o arranjo adaptativo conclui antes sob a definição adotada, e a cauda que a definição acrescenta é maior justamente no arranjo que já era o mais lento.' },
]));
// `[AUDITORIA]` A figura de tamanhos de efeito (fig7) foi REMOVIDA desta
// entrega. Ela foi construída sobre 192 pares de instância e semente, unidade
// superada pela correção de pseudorreplicação, e seus intervalos vêm de
// reamostragem sobre esses pares. Manter uma visualização que exige, na própria
// legenda, o aviso de que não deve ser usada para inferência acrescenta risco de
// leitura sem acrescentar evidência: a Tabela do experimento já traz a análise
// válida, por instância, com tamanho de efeito e proporção de casos favoráveis.
// A figura permanece no repositório e será regerada na unidade correta.
filhos.push(p('O arranjo adaptativo supera o centralizado em todos os indicadores substantivos, em dezesseis de dezesseis instâncias, com tamanhos de efeito grandes. A leitura mecanística — a de que o arranjo adaptativo, ao converter defeito oculto em retrabalho visível e imediato, impede o acúmulo de dívida técnica que no arranjo centralizado retorna adiante sob pressão de prazo — é compatível com estes números, mas não decorre deles: os dois arranjos diferem em quatro parâmetros ao mesmo tempo, e enquanto variarem juntos a comparação mede o pacote e não um mecanismo. A Seção 2.9 executa a ablação que separa as parcelas, e o resultado obriga a qualificar parte desta leitura.'));
filhos.push(pRuns([
  { t: 'A unidade de inferência é a instância, e não a semente. ', b: true },
  { t: 'Uma versão anterior desta tabela pareava por combinação de instância e semente, totalizando cento e noventa e dois pares. As doze sementes de uma mesma instância não são projetos independentes: tratá-las como observações separadas é pseudorreplicação, que infla os graus de liberdade e produz valores-p sem correspondência com a informação disponível — com cento e noventa e dois pares, o menor valor-p atingível no teste de Wilcoxon é da ordem de três vezes dez elevado a menos cinquenta e oito, e nenhum valor nessa escala é interpretável. A inferência foi refeita tomando a instância como unidade, cada uma entrando com a média das suas doze sementes. As médias por braço não se alteram; alteram-se o tamanho de efeito e a proporção de casos favoráveis, que passam a ser calculados sobre a unidade correta. A correção FORTALECE o resultado: os tamanhos de efeito crescem, e a proporção de casos favoráveis ao arranjo adaptativo vai a dezesseis de dezesseis em todos os indicadores substantivos. Em contrapartida, os valores-p deixam de ser astronômicos e vários passam a coincidir com o piso de três vírgula zero cinco vezes dez elevado a menos cinco, o menor atingível com dezesseis pares; o piso informa que todos os pares apontam no mesmo sentido, e não a magnitude do efeito, que deve ser lida no tamanho de efeito e na proporção.' },
]));
filhos.push(pRuns([
  { t: 'Evidência duplicada na tabela. ', b: true },
  { t: 'As duas primeiras linhas são a mesma grandeza dividida por sessenta. Os tamanhos de efeito e as proporções coincidem exatamente, e os valores-p diferem apenas pelo tratamento de empates no teste sobre valores inteiros. Mantê-las juntas faz a mesma evidência aparecer duas vezes; a supressão de uma delas está registrada como pendência de apresentação.' },
]));
filhos.push(pRuns([
  { t: 'Uma métrica que media visibilidade, não dano. ', b: true },
  { t: 'A última linha da Tabela ' + T('experimento') + ' move-se em sentido contrário a todas as demais. A investigação dessa discrepância revelou defeito na formulação original da métrica, e não achado substantivo. A razão entre retrabalho e esforço realizado tem por denominador o esforço efetivamente despendido, que inclui o tempo ocioso e bloqueado. O braço centralizado acumula tempo ocioso muito superior — cento e vinte e seis contra seis períodos em média — e, ao inflar o próprio denominador, dilui o retrabalho e aparenta desempenho melhor, ainda que seu retrabalho absoluto seja vinte e três vírgula oito por cento maior. A métrica premiava a ineficiência que se pretendia medir.' },
]));
filhos.push(tituloFigura('decomposicao', 'Composição do esforço realizado e o mesmo retrabalho medido sob duas bases distintas'));
filhos.push(figura('fig8_decomposicao_esforco.png', 15.5, 0.5521));
filhos.push(fonte('Dados da pesquisa (2026).'));
filhos.push(pRuns([
  { t: 'Correção adotada. ', b: true },
  { t: 'A base da razão passou a ser o esforço planejado do projeto, dado pela soma das durações nominais das tarefas. Trata-se de propriedade da instância, idêntica nos dois braços, de modo que a razão só pode variar pelo numerador. A métrica agregada original foi ainda decomposta em duas: o retrabalho efetivamente pago e a dívida latente de pico. A decomposição é necessária, e não cosmética, porque os arranjos diferem justamente na probabilidade de reporte: o adaptativo converte dívida oculta em retrabalho visível, e um agregado que soma as duas parcelas não distingue conversão de redução. Com a correção, o indicador passa a favorecer o arranjo adaptativo em vinte e três vírgula nove por cento, em concordância com os demais.' },
]));
filhos.push(p('Registra-se ainda que o valor final do estoque de dívida latente é nulo em todas as trezentas e oitenta e quatro execuções, por construção do laço de simulação, que só encerra após a quitação da dívida pendente. Por essa razão, a estatística informativa é o valor de pico do estoque, e não o seu valor terminal.'));
filhos.push(pRuns([
  { t: 'O que TR mede, e o que não mede. ', b: true },
  { t: 'A grandeza designada TR é ESFORÇO DE RETRABALHO CONTABILIZADO, e não tempo consumido no cronograma. Quando um defeito é reportado ou aflora, a implementação atual acresce a parcela correspondente ao relógio de retrabalho, mas essa parcela não ocupa um agente nem avança o calendário do projeto do mesmo modo que a execução de uma tarefa. A denominação foi corrigida ao longo do texto para não induzir a leitura de tempo efetivamente despendido. A limitação tem duas consequências que ficam declaradas. A primeira é que o custo de cronograma do retrabalho está subestimado: no modelo atual, refazer não disputa capacidade com executar. A segunda incide sobre a métrica de ocupação, cujo denominador soma os quatro relógios e portanto inclui TR: uma parcela que não consome capacidade entra no denominador como se consumisse, de modo que a métrica não deve ser lida como medida de produtividade. Fazer o retrabalho ocupar agente e recurso é alteração estrutural do modelo, não implementada nesta entrega, e está registrada como pendência.' },
]));
filhos.push(tituloFigura('trajetorias', 'Trajetórias médias dos estoques nos dois arranjos, com faixa interquartil'));
filhos.push(figura('fig9_trajetorias.png', 15.0, 0.7463));
filhos.push(fonte('Dados da pesquisa (2026).'));
filhos.push(p('A Figura ' + F('trajetorias') + ' torna visível o mecanismo. No arranjo centralizado, a dívida técnica latente cresce ao longo de todo o período nominal do projeto, atinge o máximo em torno de uma vez e meia o prazo do caminho crítico e só então é drenada, o que prolonga a execução muito além do previsto. No arranjo adaptativo, o mesmo estoque permanece próximo de zero, e o progresso validado acumula-se de forma sustentada. A bateria cognitiva média recupera-se mais cedo, o que é consequência, e não causa, do menor volume de retrabalho tardio.'));

filhos.push(pRuns([
  { t: 'Comportamento no limite de pressão nula. ', b: true },
  { t: 'Registra-se um comportamento de fronteira, fora do domínio de operação. Com pressão nula o esforço cognitivo exigido zera, e a probabilidade de transição para o modo heurístico cai ao seu piso, de aproximadamente um vírgula oito por cento por período de agente. Como no arranjo centralizado a confiança constante impede toda concessão de ajuda, uma tarefa cuja dificuldade excede a competência de todos os agentes passa a depender exclusivamente desse piso para ser iniciada, o que corresponde a uma espera média da ordem de cinquenta e seis períodos por tarefa. O efeito é de lentidão severa, e não de travamento: a transição é estocástica e sua probabilidade nunca chega a zero, de modo que a execução sempre termina. O caso está fora do domínio nominal, porque a pressão é limitada inferiormente a três décimos e nunca atinge zero em nenhuma execução apresentada; e as trezentas e oitenta e quatro execuções do experimento e as duas mil oitocentas e oitenta da ablação concluíram todas dentro do horizonte. Nenhuma conclusão desta entrega depende de ignorar esse comportamento. Ele é consequência lógica da formulação atual — transição estocástica combinada com confiança constante — e desaparece assim que qualquer das duas hipóteses estruturais em avaliação for alterada.' },
]));
filhos.push(h2('2.9  Ablação: a que o contraste entre os arranjos se deve'));
filhos.push(pRuns([
  { t: 'Por que a ablação é obrigatória. ', b: true },
  { t: 'Os dois arranjos da Tabela ' + T('cenarios') + ' diferem em quatro parâmetros simultaneamente. Enquanto variarem juntos, a comparação mede o pacote, e nenhum efeito observado pode ser atribuído a mecanismo algum. A ablação separa as parcelas, e a primeira conclusão que ela produz é sobre o próprio método de atribuição.' },
]));
filhos.push(pRuns([
  { t: 'Substituição isolada não é decomposição. ', b: true },
  { t: 'A leitura natural — trocar um parâmetro por vez e reportar a fração do contraste que cada troca reproduz — não decompõe coisa alguma, porque as frações resultantes não somam o contraste. Afirmar que “determinado parâmetro explica tal percentual do efeito” seria atribuição causal indevida sempre que houver interação, e há. A decomposição legítima exige o fatorial completo dos quatro parâmetros, com dezesseis células, e o ajuste do modelo saturado correspondente: dezesseis termos para dezesseis células produzem ajuste exato, sem resíduo e sem escolha de modelo, e vale a identidade que decompõe o contraste na soma dos efeitos principais e de todas as interações. A Tabela ' + T('fatorial') + ' apresenta essa decomposição.' },
]));
filhos.push(tituloTabela('fatorial', 'Decomposição exata do contraste em efeitos principais e interações'));
{
  const fa = lerCsvPV(caminhoTabela('entrega_fatorial.csv'));
  filhos.push(tabela(
    [3400, 1900, 1900, 1870],
    ['Indicador', 'Efeitos principais', 'Interações', 'Maior interação'],
    fa.map(r => [r.metrica, r.efeitos_principais, r.interacoes, r.maior_interacao]),
    { centrar: [1, 2, 3] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026). A = confiança inicial; B = limiar de confiança; C = probabilidade de reporte; D = probabilidade de detecção. Percentuais relativos ao contraste nominal entre os arranjos.'));
filhos.push(p('A leitura da tabela é direta. Para os indicadores de tempo e ocupação, as interações são pequenas e a decomposição é quase aditiva. Para a família da dívida oculta, ao contrário, as interações carregam mais de três quintos do contraste, e a maior delas é antagônica entre a probabilidade de reporte e a de detecção: os dois parâmetros fazem em larga medida o mesmo trabalho — converter dívida oculta em retrabalho visível — e juntos entregam muito menos que a soma dos efeitos isolados. Nessa família, nenhuma atribuição a um parâmetro isolado é defensável.'));
filhos.push(pRuns([
  { t: 'Um parâmetro inerte. ', b: true },
  { t: 'O fatorial revelou que o limiar de confiança não produz efeito algum em nenhuma das dezesseis células: as oito comparações que trocam apenas esse parâmetro são idênticas execução a execução, e todo termo do modelo saturado que o contém é exatamente zero. A causa não está no parâmetro e sim no fato de a confiança ser constante e igual para todos os agentes: o portão da Porta 2 compara sempre a confiança inicial com o limiar, de modo que os dois níveis testados do limiar caem do mesmo lado dos dois níveis testados da confiança inicial. A Tabela ' + T('tau_min') + ' mostra a resposta local do modelo a esse limiar.' },
]));
filhos.push(tituloTabela('tau_min', 'Resposta do arranjo centralizado ao limiar de confiança, com os demais parâmetros fixos'));
{
  const tm = lerCsvPV(caminhoTabela('entrega_tau_min.csv'));
  filhos.push(tabela(
    [1250, 1150, 1350, 1450, 1150, 1150, 1150, 1420],
    ['τ_mín', 'Ajudas', 'Bloqueios', 'Atraso relativo', 'TU', 'TL', 'TR', 'Ocupação'],
    tm.map(r => [r.tau_min, r.ajudas, r.bloqueios, r.atraso_relativo, r.tu, r.tl, r.tr, r.e_total]),
    { centrar: [0, 1, 2, 3, 4, 5, 6, 7] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Dezesseis instâncias com doze sementes por ponto. A confiança inicial do arranjo centralizado vale 0,25.'));
filhos.push(p('A resposta é um degrau, não um gradiente. Onze pontos da grade produzem apenas dois comportamentos, idênticos até a sexta casa decimal dentro de cada um, e o salto único ocorre num intervalo de largura de um décimo de milésimo que contém exatamente o valor da confiança inicial. Uma variação quatrocentas e noventa vezes maior, entre os dois extremos inferiores da grade, não produz efeito algum. A descontinuidade não decorre de má escolha de valor: enquanto a confiança for constante e idêntica entre agentes, o portão é uma única comparação global e o parâmetro não pode assumir outra forma. Registra-se, adicionalmente, que a confiança inicial do arranjo centralizado e o limiar do arranjo adaptativo foram fixados no mesmo valor, ambos declarados como premissa e sem justificativa numérica registrada, e que esse valor é precisamente o ponto de fronteira em que o resultado depende de a desigualdade do portão ser estrita. A desigualdade estrita é herdada da formulação conceitual; a coincidência dos dois valores é escolha de parametrização deste trabalho, e fica registrada como questão a rever.'));

filhos.push(p('A segunda ablação neutraliza o mecanismo de assistência nos dois braços, em duas direções opostas: suprimindo integralmente a concessão de ajuda, e tornando-a disponível independentemente da confiança. A Tabela ' + T('ablacao') + ' apresenta o contraste entre os arranjos sob cada condição.'));
filhos.push(tituloTabela('ablacao', 'Contraste entre os arranjos, nominal e sob ablação do mecanismo de assistência'));
{
  const ab = lerCsvPV(caminhoTabela('entrega_ablacao_mecanismo.csv'));
  filhos.push(tabela(
    [2550, 1180, 1300, 1350, 900, 900, 1890],
    ['Indicador', 'Nominal', 'Sem assist.', 'Assist. univ.', 'Resta (sem)', 'Resta (univ.)', 'Veredito'],
    ab.map(r => [r.metrica, r.nominal, r.sem_assistencia, r.assistencia_universal, r.resta_sem, r.resta_univ, r.veredito]),
    { centrar: [1, 2, 3, 4, 5, 6] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Contraste = média do arranjo adaptativo menos média do centralizado, por instância. As duas colunas “Resta” dão a fração do contraste nominal que sobrevive a cada ablação.'));
filhos.push(pRuns([
  { t: 'O que sobrevive e o que não sobrevive. ', b: true },
  { t: 'A ablação separa dois conjuntos de resultados que estavam somados numa conclusão única. A redução da dívida técnica oculta sobrevive às duas ablações com mais de quatro quintos do contraste nominal, e é portanto robusta ao mecanismo de assistência. Já a vantagem em tempo e ocupação depende desse mecanismo: o tempo de ajuda desaparece por construção, a ociosidade e a ocupação invertem de sinal, o retrabalho pago conserva entre um quarto e dois quintos do contraste, e o atraso relativo conserva cerca de três quartos. Esses resultados ficam declarados como condicionados a uma hipótese estrutural ainda em avaliação — a de confiança constante — e não como estabelecidos.' },
]));

filhos.push(h2('2.10  Divergência declarada na Porta 2'));
filhos.push(p('A conferência do código contra o pseudocódigo da fase conceitual encontrou uma divergência não declarada na Porta 2. A regra conceitual condiciona a concessão de ajuda a duas condições, disponibilidade e confiança, e nada estabelece sobre competência. A implementação acrescenta uma terceira condição, a de que o agente que presta apoio seja mais competente que o que solicita. A Tabela ' + T('porta2') + ' mede a diferença entre as duas operacionalizações sobre as mesmas instâncias, sementes e demais parâmetros.'));
filhos.push(tituloTabela('porta2', 'Porta 2: operacionalização implementada e regra conceitual literal'));
{
  const p2 = lerCsvPV(caminhoTabela('entrega_porta2.csv'));
  filhos.push(tabela(
    [1900, 2400, 1500, 1500, 1250, 520],
    ['Arranjo', 'Indicador', 'Implementada', 'Conceitual', 'Diferença', 'p'],
    p2.map(r => [r.cenario, r.metrica, r.a_nominal, r.b_tcc1, r.dif_relativa, r.p]),
    { centrar: [2, 3, 4, 5] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Dezesseis instâncias com doze sementes, pareadas; unidade inferencial: instância.'));
filhos.push(pRuns([
  { t: 'Magnitude. ', b: true },
  { t: 'No arranjo centralizado a diferença é exatamente nula, porque o filtro de competência nunca chega a ser avaliado: a confiança já impede toda concessão de ajuda. No arranjo adaptativo, todos os indicadores publicados variam menos de três por cento, com exceção da ociosidade, cuja variação relativa é maior mas incide sobre valores absolutos pequenos e não é estatisticamente distinguível. O critério de materialidade foi declarado antes da medição: a divergência seria material se alterasse algum indicador publicado em mais de cinco por cento com significância, ou se invertesse algum sinal. Nenhuma das duas condições se verifica.' },
]));
filhos.push(pRuns([
  { t: 'Avaliação conceitual da restrição. ', b: true },
  { t: 'A restrição não é arbitrária, e sua justificativa não depende do desempenho que produz. A equação de transferência de conhecimento permanece positiva mesmo quando o agente que presta apoio é menos competente que o que solicita, porque o termo proporcional à diferença de competências jamais chega a anular o incremento de base. Sem a restrição, portanto, a formulação permitiria que um agente elevasse sua competência ao receber apoio de um colega que sabe menos, o que é incompatível com o significado da variável: a própria lista de símbolos da fase conceitual define o limiar como limiar de transferência de conhecimento, e não se transfere o que não se possui. O protocolo de Crowder et al. (2012), origem da equação, é coerente com essa leitura ao fazer o agente difundir o pedido precisamente porque sua competência é inferior à dificuldade da subtarefa. A restrição é, assim, apresentada como decisão de operacionalização na passagem do modelo conceitual ao computacional, e não como correção nem como erro. Fica registrado que ela não constava da especificação e que deverá ser formalizada nela, com a justificativa acima, antes da versão final. A escolha definitiva entre as duas formulações não é feita nesta entrega e não será feita com base em desempenho.' },
]));

filhos.push(h2('2.11  Rastreabilidade das verificações'));
filhos.push(p('A Tabela ' + T('rastreabilidade') + ' registra, para cada procedimento, as instâncias e sementes utilizadas, o número de execuções e o arquivo de saída correspondente, de modo que qualquer número apresentado possa ser reencontrado. As tabelas das Seções 2.7 a 2.11, bem como a matriz de cenários e a tabela do experimento, são montadas em tempo de geração a partir desses arquivos, sem valor digitado. Registre-se, para não induzir generalização indevida, que as demais tabelas e os valores citados no corpo do texto das Seções 2.2 a 2.6 — a camada de dados — ainda são transcritos manualmente a partir das saídas dos scripts correspondentes. Foram conferidos contra os arquivos de origem, mas a garantia que vale para as seções derivadas de CSV não vale para eles; a extensão desse mecanismo às seções de dados está registrada como pendência.'));
filhos.push(tituloTabela('rastreabilidade', 'Procedimentos de verificação, condições de execução e arquivos de saída'));
{
  const ra = lerCsvPV(caminhoTabela('entrega_rastreabilidade.csv'));
  filhos.push(tabela(
    [2450, 2050, 1250, 1050, 2270],
    ['Procedimento', 'Instâncias', 'Sementes', 'Execuções', 'Arquivo'],
    ra.map(r => [r.procedimento, r.instancias, r.sementes, r.execucoes, r.arquivo]),
    { centrar: [2, 3] },
  ));
}
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Os arquivos residem em outputs/tables no repositório do trabalho.'));

filhos.push(h2('2.12  Calibração e identificabilidade dos parâmetros'));
filhos.push(p('O procedimento descrito na Seção 1.8 foi executado em duas ondas de quatrocentos pontos amostrados por hipercubo latino, calibrando cinco parâmetros contra quatro observáveis. O teste do gêmeo idêntico foi aprovado nos três critérios: o conjunto NROY não é vazio, com cento e quinze pontos; contém o vetor verdadeiro nos cinco parâmetros; e o volume da caixa envolvente foi reduzido a quatorze vírgula oito por cento do volume a priori.'));
filhos.push(p('A aprovação do teste, contudo, não implica que os cinco parâmetros tenham sido determinados. A Tabela ' + T('identificabilidade') + ' reporta, para cada um, a redução da largura marginal do conjunto NROY relativamente à faixa inicial.'));
filhos.push(tituloTabela('identificabilidade', 'Identificabilidade dos parâmetros calibrados'));
filhos.push(tabela(
  [3470, 1600, 1800, 2200],
  ['Parâmetro', 'Valor verdadeiro', 'Redução da largura', 'Veredito'],
  [
    ['μ_mín (piso do multiplicador de produtividade)', '0,6200', '70,3%', 'identificado'],
    ['F_âncora (frequência basal de defeito)', '0,1800', '36,8%', 'parcialmente identificado'],
    ['τ_sat (limiar de saturação cognitiva)', '0,8500', '10,9%', 'não identificado'],
    ['f_retrabalho (severidade do retrabalho)', '0,4200', '6,0%', 'não identificado'],
    ['k_heurístico (drenagem em modo heurístico)', '0,1350', '5,8%', 'não identificado'],
    ['F_âncora × f_retrabalho (produto)', '0,0756', '74,7%', 'identificado'],
  ],
  { centrar: [1, 2] },
));
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Adotou-se o limiar de vinte e cinco por cento de redução como fronteira da não identificabilidade.'));
filhos.push(pRuns([
  { t: 'Equifinalidade de causa estrutural. ', b: true },
  { t: 'A correlação de postos entre F_âncora e f_retrabalho, calculada dentro do conjunto NROY, é de menos zero vírgula oitocentos e quarenta, o que caracteriza uma crista. A crista não é acidente amostral: decorre da estrutura do modelo. O esforço de retrabalho gerado por tarefa é, em esperança, o produto entre a probabilidade de falha e a severidade do retrabalho, e a probabilidade de falha é proporcional a F_âncora. Os observáveis agregados enxergam apenas esse produto, de modo que aumentos em um fator podem ser compensados por reduções no outro sem alteração das saídas.' },
]));
filhos.push(tituloFigura('nroy', 'Conjunto NROY projetado sobre a crista de equifinalidade e redução marginal por parâmetro'));
filhos.push(figura('fig10_nroy_identificabilidade.png', 15.5, 0.5428));
filhos.push(fonte('Dados da pesquisa (2026).'));
filhos.push(p('A hipótese foi testada e confirmada: o produto dos dois fatores apresenta redução de setenta e quatro vírgula sete por cento, contra trinta e seis vírgula oito e seis vírgula zero por cento dos fatores isolados. Decorre daí uma recomendação de reparametrização: em calibração com dados reais, deve-se estimar o produto — interpretável como esforço esperado de retrabalho por tarefa — e declarar a divisão entre frequência e severidade como não identificada, em vez de reportar dois números que os dados não sustentam. A separação dos fatores exigiria observar a taxa de defeito e o custo unitário de correção de forma independente, dado que o delineamento atual não contempla.'));
filhos.push(pRuns([
  { t: 'Estabilidade entre ondas: achado preliminar. ', b: true },
  { t: 'As larguras marginais praticamente não se alteraram entre a primeira e a segunda onda. Essa estabilidade é compatível com um limite de identificabilidade estrutural, e não de tamanho de amostra, mas a hipótese ainda não está demonstrada: a segunda onda foi amostrada a partir do mesmo gerador da primeira, e um desenho amostral independente é necessário para distinguir estabilidade real de estabilidade herdada do delineamento. Até que essa verificação seja executada, o achado é registrado como preliminar, e não se afirma que uma terceira onda não reduziria o espaço.' },
]));

filhos.push(h2('2.13  Procedência dos parâmetros e limitações declaradas'));
filhos.push(p('A Tabela ' + T('procedencia') + ' resume a procedência dos parâmetros do modelo, segundo a classificação mantida no arquivo único de configuração. A distinção é mantida explícita porque a credibilidade de um modelo de simulação depende menos do número de parâmetros do que da clareza sobre a origem de cada um.'));
filhos.push(tituloTabela('procedencia', 'Procedência dos parâmetros do modelo'));
// Quantidades lidas de outputs/tables/parametros_procedencia.csv.
const SIGNIF = {"calibrado": "estimado dos dados por procedimento documentado: o gradiente de risco RR por faixa, obtido da base NASA", "literatura": "exigido por resultado publicado: a t-norma produto e a existência de partição difusa na saída (Van Broekhoven e De Baets, 2009)", "tcc1": "herdado da fase conceitual sem alteração", "premissa": "arbitrado de forma declarada, com justificativa registrada e sujeito a varredura", "aberto": "ainda não fixado; cinco deles submetidos à calibração da Seção 2.9", "derivado": "calculado do escalonamento de referência das próprias instâncias"};
const proc = lerCsv(`${TAB}/parametros_procedencia.csv`);
filhos.push(tabela(
  [1700, 1300, 6070],
  ['Condição', 'Quantidade', 'Significado'],
  proc.map(r => [r.condicao, r.quantidade, SIGNIF[r.condicao] || '—']),
  { centrar: [1] },
));
filhos.push(legenda('Fonte: Elaborado pela autora (2026), a partir do arquivo de configuração do modelo.'));
filhos.push(pRuns([
  { t: 'Limitações. ', b: true },
  { t: 'Quatro limitações são declaradas. Primeira, a transferência ordinal de risco entre domínios pressupõe que o gradiente de risco por dificuldade seja transferível, ainda que o nível absoluto não seja; trata-se de suposição, e não de resultado. Segunda, e mais importante para a leitura desta entrega, NÃO foi realizada validação externa do simulador: não há aqui nenhum critério confrontado com observação de campo que pudesse reprová-lo. A comparação da fração de retrabalho com a literatura funciona apenas como verificação de ordem de grandeza, e a Seção 2.7 demonstra que ela aprova em toda a faixa declarada do parâmetro de risco basal, isto é, que seu poder de rejeição é nulo. Terceira, o teste do gêmeo idêntico é otimista por construção, uma vez que anula a discrepância entre modelo e realidade. Quarta, três dos cinco parâmetros submetidos à calibração não são identificáveis com os observáveis do delineamento atual, e assim são reportados.' },
]));

filhos.push(h2('2.14  Cronograma de atividades e próximas etapas'));
filhos.push(p('A Tabela ' + T('cronograma') + ' distribui cronologicamente as atividades previstas para a conclusão do trabalho.'));
filhos.push(tituloTabela('cronograma', 'Cronograma de finalização do trabalho (TCC II)'));
filhos.push(tabela(
  [4270, 960, 960, 960, 960, 960],
  ['Atividade / etapa de engenharia', 'Set.', 'Out.', 'Nov.', 'Dez.', 'Jan.'],
  [
    ['1. Confirmação da proveniência dos dados junto à coleção oficial e fechamento da calibração NASA', 'X', '', '', '', ''],
    ['2. Auditoria do PSPLIB J60 e validação dos parâmetros NC, RF e RS (concluída)', 'X', '', '', '', ''],
    ['3. Construção do índice de dificuldade e da transferência ordinal NASA → J60 (concluída)', 'X', '', '', '', ''],
    ['4. Implementação do sistema de inferência difusa e do simulador de equipes (concluída)', 'X', '', '', '', ''],
    ['5. Verificação do simulador e experimento de governança (concluídos)', 'X', '', '', '', ''],
    ['6. Calibração por History Matching e teste do gêmeo idêntico (concluídos)', 'X', '', '', '', ''],
    ['7. Fixação da âncora de risco por dado do domínio de engenharia', '', 'X', '', '', ''],
    ['8. Análise de sensibilidade sobre os parâmetros em varredura', '', 'X', 'X', '', ''],
    ['9. Ensaios finais e validação do modelo integrado', '', '', 'X', 'X', ''],
    ['10. Redação final da monografia conforme normas ABNT e preparação da defesa', '', '', '', 'X', 'X'],
  ],
  { centrar: [1, 2, 3, 4, 5] },
));
filhos.push(legenda('Fonte: Elaborado pela autora (2026).'));

// ============================================================
filhos.push(h1('REFERÊNCIAS'));
const ref = (texto) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { line: 240, after: 200 },
  children: [new TextRun({ text: texto, font: FONTE, size: CORPO })],
});
filhos.push(ref('ANDRIANAKIS, I.; VERNON, I. R.; McCREESH, N. et al. Bayesian history matching of complex infectious disease models using emulation: a tutorial and a case study on HIV in Uganda. PLoS Computational Biology, v. 11, n. 1, e1003968, 2015. DOI 10.1371/journal.pcbi.1003968.'));
filhos.push(ref('BEIN, W. W.; KAMBUROWSKI, J.; STALLMANN, M. F. M. Optimal reduction of two-terminal directed acyclic graphs. SIAM Journal on Computing, v. 21, n. 6, p. 1112-1129, 1992.'));
filhos.push(ref('BOEHM, B.; BASILI, V. R. Software defect reduction top 10 list. Computer, v. 34, n. 1, p. 135-137, jan. 2001. DOI 10.1109/2.962984.'));
filhos.push(ref('CROWDER, R. M.; ROBINSON, M. A.; HUGHES, H. P. N. et al. The development of an agent-based modeling framework for simulating engineering team work. IEEE Transactions on Systems, Man, and Cybernetics – Part A: Systems and Humans, v. 42, n. 6, p. 1425-1439, 2012.'));
filhos.push(ref('DE REYCK, B.; HERROELEN, W. On the use of the complexity index as a measure of complexity in activity networks. European Journal of Operational Research, v. 91, n. 2, p. 347-366, 1996.'));
filhos.push(ref('KOLISCH, R. Serial and parallel resource-constrained project scheduling methods revisited: theory and computation. European Journal of Operational Research, v. 90, n. 2, p. 320-333, 1996.'));
filhos.push(ref('KOLISCH, R.; SPRECHER, A. PSPLIB – a project scheduling problem library. European Journal of Operational Research, v. 96, n. 1, p. 205-216, 1997.'));
filhos.push(ref('KOLISCH, R.; SPRECHER, A.; DREXL, A. Characterization and generation of a general class of resource-constrained project scheduling problems. Management Science, v. 41, n. 10, p. 1693-1703, 1995.'));
filhos.push(ref('LIU, S.; TRIANTIS, K. P.; SARANGI, S. Representing qualitative variables and their interactions with fuzzy logic in system dynamics modeling. Systems Research and Behavioral Science, v. 28, p. 245-263, 2011.'));
filhos.push(ref('LOVE, P. E. D.; LI, H. Quantifying the causes and costs of rework in construction. Construction Management and Economics, v. 18, n. 4, p. 479-490, 2000.'));
filhos.push(ref('LOVE, P. E. D.; MATTHEWS, J.; FANG, W. et al. Quantifying the costs of field rework in construction. Journal of Construction Engineering and Management, v. 152, n. 1, 2026. DOI 10.1061/JCEMD4.COENG-17026.'));
filhos.push(ref('MACAL, C. M.; NORTH, M. J. Tutorial on agent-based modelling and simulation. Journal of Simulation, v. 4, n. 3, p. 151-162, 2010.'));
filhos.push(ref('McCABE, T. J. A complexity measure. IEEE Transactions on Software Engineering, v. SE-2, n. 4, p. 308-320, 1976.'));
filhos.push(ref('McCULLOCH, J.; GE, J.; WARD, J. A.; HEPPENSTALL, A.; POLHILL, J. G.; MALLESON, N. Calibrating agent-based models using uncertainty quantification methods. Journal of Artificial Societies and Social Simulation, v. 25, n. 2, artigo 1, 2022. DOI 10.18564/jasss.4791.'));
filhos.push(ref('NATIONAL AERONAUTICS AND SPACE ADMINISTRATION. Cyclomatic complexity assessment. NASA/TM-20205011566, NESC-RP-20-01515. Washington: NASA, 2020.'));
filhos.push(ref('NATIONAL AERONAUTICS AND SPACE ADMINISTRATION. SWE-220 – Cyclomatic complexity for safety-critical software. NASA Software Engineering Handbook, versão D. Disponível em: https://swehb.nasa.gov. Acesso em: 3 set. 2026.'));
filhos.push(ref('PUKELSHEIM, F. The three sigma rule. The American Statistician, v. 48, n. 2, p. 88-91, 1994. DOI 10.1080/00031305.1994.10476030.'));
filhos.push(ref('RODRIGUES, A. G. The application of system dynamics to project management: an integrated methodology (SYDPIM). Tese (Doctor of Philosophy) — University of Strathclyde, Glasgow, 2000.'));
filhos.push(ref('SHEPPERD, M. The cleaned NASA MDP data sets. Thoughts on Empirical Software Engineering, 1 abr. 2018. Disponível em: https://empiricalsoftwareengineering.wordpress.com. Acesso em: 3 set. 2026.'));
filhos.push(ref('SHEPPERD, M.; SONG, Q.; SUN, Z.; MAIR, C. Data quality: some comments on the NASA software defect datasets. IEEE Transactions on Software Engineering, v. 39, n. 9, p. 1208-1215, 2013.'));
filhos.push(ref('STERMAN, J. D. Business dynamics: systems thinking and modeling for a complex world. Boston: Irwin/McGraw-Hill, 2000.'));
filhos.push(ref('VAN BROEKHOVEN, E.; DE BAETS, B. Only smooth rule bases can generate monotone Mamdani-Assilian models under center-of-gravity defuzzification. IEEE Transactions on Fuzzy Systems, v. 17, n. 5, p. 1157-1174, out. 2009. DOI 10.1109/TFUZZ.2009.2023328.'));

// ============================================================
const doc = new Document({
  creator: 'Isadora Maria Carvalho Lopes',
  title: 'TCC II — Metodologia e Resultados Iniciais',
  styles: {
    default: {
      document: { run: { font: FONTE, size: CORPO } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838, orientation: PageOrientation.PORTRAIT },
        margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 },
      },
    },
    children: filhos,
  }],
});

const errosRegistro = verificarRegistro();
if (errosRegistro.length) {
  console.error('GERACAO INTERROMPIDA — registro inconsistente:');
  for (const e of errosRegistro) console.error('  - ' + e);
  process.exit(1);
}
console.log(`registro OK: ${ORDEM_EQ.length} equacoes, ${ORDEM_TAB.length} tabelas, ${ORDEM_FIG.length} figuras`);

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log('gerado:', OUT, buf.length, 'bytes');
});
