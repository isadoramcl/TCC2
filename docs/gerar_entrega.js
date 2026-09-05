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

const FIG = '/mnt/user-data/uploads/TCC2/outputs/figures';
const OUT = '/tmp/claude-0/-home-claude/af3df90e-2d4b-558d-b3fb-ebef4729e729/scratchpad/TCC2_Metodologia_Resultados_Iniciais_v2.docx';

const FONTE = 'Times New Roman';
const CORPO = 24;      // 12 pt (meios-pontos)
const PEQUENO = 20;    // 10 pt
const MINI = 18;       // 9 pt
const LARGURA_UTIL = 9070; // DXA (~16 cm) para tabelas

// ---------- helpers ----------
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

const legenda = (texto) => new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 80, after: 240 },
  children: [new TextRun({ text: texto, font: FONTE, size: PEQUENO })],
});

const tituloTabela = (texto) => new Paragraph({
  alignment: AlignmentType.LEFT,
  spacing: { before: 240, after: 100 },
  children: [new TextRun({ text: texto, font: FONTE, size: PEQUENO, bold: true })],
});

// Equacao centralizada com numero alinhado a direita.
// Nao se usa o suporte a OMML do docx-js: o LibreOffice nao o importa, e sem
// poder verificar a renderizacao no Word o risco de entregar formulas em branco
// nao compensa. Simbolos Unicode renderizam de forma identica em qualquer editor.
const TabStopTipo = { RIGHT: 'right' };
function equacao(texto, numero) {
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
filhos.push(bullet('separação entre camada de dados brutos (somente leitura), camada de processamento (scripts numerados na ordem de execução) e camada de saídas (tabelas, figuras e logs), conforme a Figura 1.', 'Projeto e arquitetura: '));
filhos.push(bullet('seis scripts em Python, executáveis de forma independente e em sequência, cada um documentando internamente o problema que resolve, sua entrada, sua saída, sua lógica, a origem de cada decisão e o critério de verificação do próprio resultado.', 'Implementação: '));
filhos.push(bullet('cada script encerra com um bloco de verificações automáticas que compara seu resultado com invariantes conhecidas — totais que devem se conservar, chaves que devem ser únicas, ausências que não podem existir, propriedades matemáticas que devem valer. Uma verificação que falha interrompe a execução com código de erro, de modo que uma etapa defeituosa não alimenta silenciosamente a seguinte.', 'Verificação e ensaios: '));

filhos.push(h2('1.4  Procedimentos experimentais e coleta de dados'));
filhos.push(p('Os dados foram extraídos de forma integralmente automatizada, por meio dos scripts descritos, a partir dos arquivos originais dos repositórios públicos. Nenhum arquivo bruto foi editado em momento algum: todas as transformações produzem arquivos derivados, e a integridade dos originais é verificável por resumo criptográfico SHA-256 calculado a cada execução. O repositório está configurado para preservar os bytes originais dos arquivos de dados, impedindo que o sistema de controle de versão converta terminadores de linha e altere fisicamente os arquivos entre as duas estações de trabalho — precaução sem a qual a verificação por resumo criptográfico deixaria de ser reproduzível.'));
filhos.push(p('A etapa de auditoria foi implementada sem bibliotecas de leitura de alto nível, com uso exclusivo da biblioteca padrão do Python. A justificativa é metodológica: leitores de dados de alto nível convertem tipos, tratam valores ausentes e descartam registros malformados de maneira silenciosa, o que destruiria precisamente a evidência que a auditoria pretende coletar. A partir da etapa de consolidação, com os dados já caracterizados, o uso de bibliotecas de análise passa a ser adequado.'));
filhos.push(p('As condições controladas dos ensaios são as seguintes: a base de análise é fixa (17.377 observações de 12 projetos); a unidade de observação é o módulo de software; o desfecho é binário (módulo defeituoso ou não); o efeito do projeto de origem é sempre incluído nos modelos, de modo que nenhuma associação seja atribuída a uma métrica quando puder ser explicada pela procedência da observação; e todos os testes de robustez — sensibilidade aos pontos de corte e validação por exclusão sucessiva de projetos — são executados sobre a mesma base, sem reamostragem aleatória, o que torna os resultados determinísticos e reproduzíveis bit a bit.'));

filhos.push(h2('1.5  Modelagem do sistema'));
filhos.push(p('O objeto construído é um modelo híbrido que acopla Dinâmica de Sistemas e Modelagem Baseada em Agentes, especificado na fase conceitual deste trabalho. O ecossistema é povoado por duas classes de agentes. O Agente Gestor controla um vetor dinâmico de restrições, composto pela pressão de cronograma P(t), pela restrição orçamentária Ω e pela topologia do fluxo de trabalho W, em que cada nó guarda uma dificuldade técnica Dᵢ. O Agente Engenheiro é caracterizado por um vetor contínuo de atributos que evoluem ao longo da simulação: competência técnica C(t), bateria cognitiva B(t), disponibilidade a(t), taxa de resposta na rede R(t), confiança mútua τ(t) e limiar de saturação da atenção τ_sat.'));

filhos.push(p('A grandeza que engatilha as transições de estado é o esforço cognitivo exigido pela tarefa, que cresce com a dificuldade técnica e com a pressão de cronograma, e é aliviado pela capacidade cognitiva disponível:', { indent: false }));
filhos.push(equacao('E(t) = Dᵢ · P(t) / B(t)', 1));
filhos.push(simbolo('Dᵢ', '— índice de dificuldade técnica da tarefa i;'));
filhos.push(simbolo('P(t)', '— pressão de cronograma imposta pelo gestor;'));
filhos.push(simbolo('B(t)', '— bateria cognitiva disponível do agente.'));

filhos.push(p('Quando existe hiato de competência e o agente recorre à rede, a transferência lateral de conhecimento produz incremento de competência ao custo de tempo, conforme a formulação de Crowder, Robinson e Hughes (2012):', { indent: false }));
filhos.push(equacao('ΔC = [ 15 + 3 ( C_k − C ) ] / 100', 2));
filhos.push(p('Os escalares 15 e 3 representam, respectivamente, o incremento base de assimilação por interação bem-sucedida e um fator de eficiência de transferência proporcional ao hiato técnico entre provedor e receptor. São premissas iniciais e serão submetidos a análise de sensibilidade na fase de implementação, e não tratados como constantes absolutas.'));

filhos.push(p('A saturação individual e o atrito na rede traduzem-se em multiplicadores adimensionais no intervalo [0,1], obtidos por inferência difusa — fuzzificação dos estados contínuos de fadiga e atrito por funções de pertinência, avaliação por regras e defuzzificação —, procedimento validado para representar variáveis qualitativas em Dinâmica de Sistemas (Liu, Triantis e Sarangi, 2011). A produtividade efetiva resulta da modulação da produtividade nominal por esses multiplicadores:', { indent: false }));
filhos.push(equacao('PR_efetiva = PR_nominal · μ_cognitivo · μ_rede', 3));

filhos.push(p('A válvula que alimenta o estoque de retrabalho oculto é regida pela equação de falhas, na qual o risco basal da tarefa soma-se a uma parcela que cresce à medida que a degradação cognitiva avança:', { indent: false }));
filhos.push(equacao('TGE = PR_efetiva · ( F_base + R_error · ( 1 − μ_cognitivo ) )', 4));
filhos.push(simbolo('F_base', '— risco basal de falha associado à dificuldade da tarefa;'));
filhos.push(simbolo('R_error', '— taxa de erro adicional sob degradação cognitiva.'));

filhos.push(p('A métrica terminal condensa a ociosidade da rede e a penalidade do satisficing num índice de eficiência total do esforço, razão entre o tempo de trabalho efetivo e o tempo total consumido:', { indent: false }));
filhos.push(equacao('E_total = Σ TWᵢ / Σ ( TWᵢ + TLᵢ + TUᵢ + TRᵢ )', 5));
filhos.push(simbolo('TWᵢ', '— tempo de trabalho efetivo na tarefa i;'));
filhos.push(simbolo('TLᵢ', '— tempo de espera por suporte técnico;'));
filhos.push(simbolo('TUᵢ', '— tempo improdutivo por adiamento ou indisponibilidade da rede;'));
filhos.push(simbolo('TRᵢ', '— tempo de retrabalho decorrente de falhas detectadas.'));

filhos.push(p('A execução temporal dessas equações é governada por uma árvore de decisão de três portas, avaliada a cada passo. A Porta 1 detecta sobrecarga: quando o esforço exigido supera o limiar de saturação, o agente transita para processamento heurístico e, conforme o nível da restrição orçamentária, ou adia a tarefa ou a conclui com erro, injetando no estoque de retrabalho oculto uma parcela proporcional ao excesso sobre o limiar. A Porta 2 trata o hiato de competência, disparando requisição à rede e aplicando a equação (2) caso exista agente disponível e com confiança mútua suficiente. A Porta 3 corresponde à execução analítica nominal, acionada quando não há sobrecarga nem hiato de competência.'));


filhos.push(pRuns([
  { t: 'Os três estoques. ', b: true },
  { t: 'A camada de dinâmica de sistemas do modelo é composta por três estoques, cujas taxas de entrada e saída são alimentadas pelas decisões dos agentes. O desgaste cognitivo acumulado (S_DC) acumula a drenagem da bateria cognitiva de todos os agentes e mede o custo cognitivo total incorrido pela equipe. O progresso validado (S_PV) acumula a duração nominal das tarefas concluídas sem defeito, e é a única medida de avanço que o modelo considera legítima: uma tarefa concluída com defeito oculto não incrementa esse estoque, ainda que o cronograma a registre como pronta. A dívida técnica latente (S_UR) acumula o esforço de retrabalho que já foi gerado mas ainda não foi detectado, medido em períodos de trabalho futuro; é o estoque que materializa a diferença entre progresso aparente e progresso real.' },
]));
filhos.push(p('A separação entre S_PV e o simples número de tarefas concluídas é o mecanismo pelo qual o modelo representa a patologia central que o trabalho investiga: sob pressão, a equipe continua a marcar tarefas como concluídas enquanto S_PV estagna e S_UR cresce, de modo que o painel de controle do projeto melhora exatamente enquanto o projeto piora.'));
filhos.push(pRuns([
  { t: 'Portas de decisão. ', b: true },
  { t: 'A cada período, para cada tarefa elegível, o agente designado percorre uma árvore de três portas. A Porta 1 corresponde ao modo heurístico: acionada quando o esforço percebido excede o limiar de saturação, ela executa a tarefa com custo cognitivo elevado e probabilidade de defeito aumentada, e é a porta pela qual o defeito tende a ficar oculto. A Porta 2 corresponde ao adiamento: o agente reconhece que não dispõe de condições para executar a tarefa e a devolve à fila, incorrendo em tempo improdutivo. A Porta 3 corresponde à execução analítica: o agente executa a tarefa em modo deliberado, com custo cognitivo menor e risco de defeito reduzido ao patamar basal da faixa de dificuldade. A probabilidade de transição entre os modos é estocástica e governada pela Equação 6.' },
]));
filhos.push(equacao('p_heurístico = 1 / ( 1 + exp[ − ( E − τ_sat ) / s ] )', 6));
filhos.push(simbolo('E', 'esforço percebido, conforme Equação 1;'));
filhos.push(simbolo('τ_sat', 'limiar de saturação cognitiva do agente;'));
filhos.push(simbolo('s', 'parâmetro de suavidade da transição.'));
filhos.push(p('A formulação estocástica foi adotada porque o texto do TCC I descreve a transição como estocástica enquanto o pseudocódigo a escreve como limiar determinístico. Com s tendendo a zero a Equação 6 recupera o limiar determinístico, de modo que as duas leituras passam a ser alternativas testáveis por análise de sensibilidade em vez de escolhas arbitrárias.'));

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
  { t: 'Adotou-se a configuração garantida: t-norma produto e partição difusa uniforme na saída. A configuração originalmente especificada foi mantida como valor alternativo do parâmetro declarado t_norma e é executada em varredura, de modo que a diferença entre as duas seja medida e não decretada. A Tabela 1 apresenta a medição sobre malha de 161 por 161 pontos.' },
]));
filhos.push(tituloTabela('Tabela 1 – Maior derivada positiva da superfície difusa por configuração de inferência'));
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
filhos.push(p('As equações anteriores descrevem o modelo; as seguintes descrevem os métodos empregados para estimar, a partir de dados observados, os parâmetros Dᵢ e F_base que nelas aparecem. As equações (6) a (9) constituem o instrumental estatístico; as (10) a (12), os parâmetros de delineamento das instâncias; e as (13) a (19), a construção do índice de dificuldade e a transferência de risco entre domínios.'));

filhos.push(p('A associação entre métricas e ocorrência de defeito é modelada por regressão logística. Como o desfecho é binário, modela-se o logaritmo da chance, e não a probabilidade — esta é limitada ao intervalo [0,1], que uma função linear extrapolaria:', { indent: false }));
filhos.push(equacao('ln [ p / ( 1 − p ) ] = β₀ + β₁x₁ + β₂x₂ + … + βₚxₚ', 7));
filhos.push(simbolo('p', '— probabilidade de o módulo ser defeituoso;'));
filhos.push(simbolo('xᵢ', '— variáveis explicativas, incluindo o projeto de origem como fator;'));
filhos.push(simbolo('βᵢ', '— coeficientes estimados por máxima verossimilhança.'));

filhos.push(p('A interpretação dos coeficientes dá-se pela razão de chances, que exprime por quanto a chance de defeito é multiplicada a cada aumento unitário na variável, mantidas as demais constantes:', { indent: false }));
filhos.push(equacao('RC = exp(β)', 8));

filhos.push(p('A comparação entre modelos aninhados emprega o teste da razão de verossimilhança, cuja estatística segue aproximadamente uma distribuição qui-quadrado com graus de liberdade iguais ao número de parâmetros adicionais:', { indent: false }));
filhos.push(equacao('LR = 2 ( ℓ_completo − ℓ_reduzido )  ~  χ² ( gl )', 9));

filhos.push(p('O diagnóstico de multicolinearidade utiliza o fator de inflação da variância, obtido da regressão auxiliar de cada variável contra as demais:', { indent: false }));
filhos.push(equacao('VIFⱼ = 1 / ( 1 − R²ⱼ )', 10));

filhos.push(p('Os três parâmetros de delineamento das instâncias do PSPLIB, conforme Kolisch, Sprecher e Drexl (1995), são a complexidade de rede, o fator de recursos e a força de recursos:', { indent: false }));
filhos.push(equacao('NC = | A | / | V |', 11));
filhos.push(simbolo('| A |', '— número de arcos de precedência;  | V | — número de atividades, incluindo as fictícias.'));
filhos.push(equacao('RF = ( 1/n ) · Σⱼ [ ( 1/K ) · Σₖ 1{ rⱼₖ > 0 } ]', 12));
filhos.push(simbolo('n, K', '— número de atividades reais e de tipos de recurso;'));
filhos.push(simbolo('rⱼₖ', '— demanda da atividade j pelo recurso k;  1{·} — função indicadora.'));
filhos.push(equacao('RSₖ = ( aₖ − rₖᵐⁱⁿ ) / ( rₖᵐᵃˣ − rₖᵐⁱⁿ )', 13));
filhos.push(simbolo('aₖ', '— disponibilidade do recurso k;'));
filhos.push(simbolo('rₖᵐⁱⁿ', '— maior demanda individual, menor disponibilidade que mantém o problema viável;'));
filhos.push(simbolo('rₖᵐᵃˣ', '— pico de demanda no cronograma de inícios mais cedo.'));

filhos.push(p('A criticidade de cada atividade é medida pela folga total, obtida das passagens para frente e para trás do método do caminho crítico:', { indent: false }));
filhos.push(equacao('folgaⱼ = LSⱼ − ESⱼ', 14));
filhos.push(simbolo('ESⱼ, LSⱼ', '— início mais cedo e início mais tarde admissível sem atrasar o projeto.'));

filhos.push(p('O índice de dificuldade técnica compõe três grandezas, normalizadas para [0,1] dentro de cada instância:', { indent: false }));
filhos.push(equacao('dⱼ = ( durⱼ − dur_mín ) / ( dur_máx − dur_mín )', 15));
filhos.push(equacao('rⱼ = ( 1/K ) · Σₖ ( rⱼₖ / aₖ )', 16));
filhos.push(equacao('cⱼ = 1 − folga_normⱼ', 17));
filhos.push(p('sendo o índice a combinação ponderada dos três componentes:', { indent: false }));
filhos.push(equacao('Dⱼ = w₁ dⱼ + w₂ rⱼ + w₃ cⱼ ,   com  w₁ + w₂ + w₃ = 1', 18));
filhos.push(p('Os pesos são tratados como suposição de partida, fixados em 1/3 cada, e submetidos a análise de sensibilidade conforme reportado na Seção 2.5.'));

filhos.push(p('A transferência de risco entre domínios opera sobre razões, e não sobre níveis absolutos. Para cada nível ordinal ℓ, a razão de risco é estimada na base NASA em relação ao nível de referência ℓ₀:', { indent: false }));
filhos.push(equacao('RR( ℓ ) = F( ℓ ) / F( ℓ₀ )', 19));
filhos.push(p('e o risco basal atribuído a uma tarefa do PSPLIB no nível ℓ resulta do produto dessa razão por uma taxa basal do domínio de engenharia:', { indent: false }));
filhos.push(equacao('F_base( ℓ ) = F_âncora × RR( ℓ )', 20));
filhos.push(simbolo('F(ℓ)', '— frequência de defeito observada no nível ℓ da base NASA;'));
filhos.push(simbolo('ℓ₀', '— nível de referência, correspondente à dificuldade mais baixa;'));
filhos.push(simbolo('F_âncora', '— taxa basal de retrabalho do domínio de engenharia; parâmetro do modelo, não estimado neste trabalho.'));


filhos.push(h2('1.8  Calibração do modelo e avaliação de identificabilidade'));
filhos.push(p('O modelo contém parâmetros que não são diretamente observáveis. Duas perguntas distintas precisam de resposta: qual o procedimento que os fixa a partir de dados, e qual a evidência de que esse procedimento de fato os identifica. Responder apenas à primeira entregaria um algoritmo em execução, sem demonstração de que ele extrai informação.'));
filhos.push(pRuns([
  { t: 'Procedimento. ', b: true },
  { t: 'Adotou-se o History Matching (ANDRIANAKIS et al., 2015). Em vez de buscar um vetor ótimo de parâmetros, o método descarta do espaço tudo o que é implausível à luz dos dados, e devolve um conjunto — designado NROY, do inglês not ruled out yet — em lugar de uma estimativa pontual. A medida de implausibilidade de cada saída e a regra de descarte são dadas pelas Equações 21 e 22.' },
]));
filhos.push(equacao('I_j( x ) = | z_j − f̄_j( x ) | / √( V_obs,j + V_sim,j + V_mod,j )', 21));
filhos.push(equacao('I( x ) = máx_j I_j( x ) ,   x ∈ NROY  ⟺  I( x ) ≤ 3', 22));
filhos.push(simbolo('z_j', 'valor observado da saída j;'));
filhos.push(simbolo('f̄_j(x)', 'média do simulador na saída j sob o vetor de parâmetros x;'));
filhos.push(simbolo('V_obs', 'variância da observação;'));
filhos.push(simbolo('V_sim', 'variância da média do simulador, decorrente da estocasticidade;'));
filhos.push(simbolo('V_mod', 'variância de discrepância entre modelo e realidade.'));
filhos.push(p('O corte em três desvios não é escolha deste trabalho. Pela desigualdade de Vysochanskii–Petunin, para qualquer distribuição unimodal ao menos noventa e cinco por cento da massa de probabilidade situa-se a menos de três desvios da média, de modo que descartar valores com implausibilidade superior a três raramente descarta o vetor verdadeiro (PUKELSHEIM, 1994).'));
filhos.push(pRuns([
  { t: 'Dispensa do emulador. ', b: true },
  { t: 'A literatura de History Matching recorre a emuladores estatísticos porque o simulador que se deseja calibrar costuma ser caro. O simulador aqui construído custa cerca de um décimo de segundo por execução, e o delineamento completo, com três mil e duzentas execuções, conclui em minutos. Avalia-se o simulador diretamente. A decisão elimina o termo de erro de emulação da Equação 21, isto é, remove uma aproximação em vez de acrescentá-la. Caso o modelo venha a encarecer, o emulador pode ser introduzido sem alteração do restante do procedimento.' },
]));
filhos.push(pRuns([
  { t: 'Validação por gêmeo idêntico. ', b: true },
  { t: 'Para verificar se o procedimento identifica parâmetros, empregou-se o teste do gêmeo idêntico (McCULLOCH et al., 2022): geram-se observações sintéticas a partir de um vetor de parâmetros conhecido, executa-se a calibração sem informar esse vetor, e verifica-se se o conjunto NROY resultante o contém. Duas precauções de desenho foram adotadas. O vetor verdadeiro foi posicionado deliberadamente fora do centro das faixas, pois um alvo situado no meio do espaço não testa as bordas do procedimento. E as sementes aleatórias que geram as observações sintéticas são disjuntas das utilizadas pelo simulador durante a calibração; sem essa separação, o teste compararia ruído idêntico consigo mesmo e seria aprovado trivialmente.' },
]));
filhos.push(pRuns([
  { t: 'Limitação a declarar. ', b: true },
  { t: 'No teste do gêmeo idêntico o modelo é, por construção, a própria verdade, de modo que a variância de discrepância V_mod é nula. O teste é, portanto, otimista: mede se o procedimento identifica parâmetros no cenário mais favorável concebível. A reprovação nele condenaria o procedimento, mas a aprovação não garante desempenho equivalente diante de dados reais, situação em que V_mod é positiva e precisa ser especificada. Essa assimetria é mantida explícita na leitura dos resultados.' },
]));

filhos.push(h2('1.9  Matriz de cenários e desenho experimental'));
filhos.push(p('O experimento central do trabalho contrasta dois arranjos de governança submetidos a condições externas idênticas. A Tabela 2 apresenta os parâmetros organizacionais que os distinguem. Todos os demais elementos — instâncias de projeto, índice de dificuldade das tarefas, disponibilidade de recursos e função de pressão — são idênticos entre os braços, e constituem o controle experimental.'));
filhos.push(tituloTabela('Tabela 2 – Matriz de cenários: parâmetros organizacionais que distinguem os arranjos'));
filhos.push(tabela(
  [3350, 1860, 1860, 2000],
  ['Parâmetro', 'Centralizada', 'Adaptativa', 'Interpretação organizacional'],
  [
    ['τ_inicial', '0,30', '0,70', 'confiança inicial na rede de pares'],
    ['τ_mín', '0,20', '0,50', 'piso de segurança psicológica'],
    ['p_reporte', '0,15', '0,75', 'probabilidade de reportar defeito detectado'],
    ['p_detecção', '0,05', '0,05', 'idêntica: não é variável de governança'],
  ],
  { centrar: [1, 2] },
));
filhos.push(legenda('Fonte: Elaborado pela autora (2026), a partir da Tabela 1.1 do TCC I.'));
filhos.push(pRuns([
  { t: 'Segurança psicológica como mecanismo. ', b: true },
  { t: 'O parâmetro que distingue substantivamente os dois arranjos é a probabilidade de reporte de defeito. Ela operacionaliza a noção de segurança psicológica: em um arranjo centralizado, o agente que detecta um defeito próprio antecipa custo pessoal ao reportá-lo e tende a ocultá-lo, alimentando o estoque de dívida técnica latente; em um arranjo adaptativo, o mesmo agente reporta, e o retrabalho é pago imediatamente e de forma visível. O modelo não presume qual arranjo é superior: a diferença de desempenho, se existir, emerge da interação entre ocultação, acúmulo de dívida e pressão de prazo.' },
]));
filhos.push(pRuns([
  { t: 'Delineamento pareado. ', b: true },
  { t: 'Cada par de execuções emprega a mesma instância e a mesma semente aleatória nos dois braços. A variação atribuível à instância e ao sorteio é, portanto, comum aos dois e cancela-se na diferença, o que eleva substancialmente a potência estatística em relação a um delineamento independente de mesmo tamanho. A inferência emprega o teste de Wilcoxon para amostras pareadas, e não o teste t, porque as saídas do modelo são assimétricas e limitadas inferiormente por zero. O tamanho de efeito é reportado pelo d de Cohen pareado e pela proporção de pares favoráveis, uma vez que, com centenas de pares, o valor-p isoladamente não distingue diferença relevante de diferença meramente detectável.' },
]));

filhos.push(h2('1.10  Pontos de acoplamento entre a calibração e o modelo'));
filhos.push(p('As duas formulações anteriores encontram-se em dois pontos precisos, e é esse encontro que define o escopo da presente entrega.'));
filhos.push(pRuns([
  { t: 'Primeiro acoplamento. ', b: true },
  { t: 'O índice Dᵢ, construído pela equação (17) sobre as 28.800 tarefas do PSPLIB J60, é exatamente a grandeza que aparece no numerador da equação (1). Antes desta etapa, a dificuldade técnica das tarefas seria um parâmetro arbitrado; ela passa a ser derivada de grandezas medidas nas próprias instâncias.' },
]));
filhos.push(pRuns([
  { t: 'Segundo acoplamento. ', b: true },
  { t: 'O risco basal F_base, obtido pela equação (19) a partir da calibração sobre a base NASA, é o termo que aparece na equação de falhas (4), governando a válvula que alimenta o estoque de retrabalho oculto. Antes desta etapa, esse risco seria uma suposição; ele passa a ser um gradiente estimado empiricamente, com incerteza quantificada, ainda que ancorado a uma taxa basal a definir.' },
]));
filhos.push(p('Os resultados apresentados no capítulo seguinte referem-se integralmente a esses dois acoplamentos. Os demais componentes do modelo — a inferência difusa que produz μ_cognitivo e μ_rede, a árvore de decisão de três portas, os estoques e a integração temporal — permanecem na especificação formal estabelecida na fase conceitual e serão implementados na etapa subsequente, conforme o cronograma da Seção 2.7.'));

// ============================================================
filhos.push(h1('2  RESULTADOS INICIAIS E DISCUSSÃO'));

filhos.push(h2('2.1  Arquitetura e implementação da solução inicial'));
filhos.push(p('A primeira versão funcional do pipeline de dados foi concluída e validada. Os requisitos essenciais de rastreabilidade, imutabilidade e verificação automática foram atendidos. A Figura 1 apresenta a arquitetura implementada, organizada em três camadas: dados brutos imutáveis, scripts de processamento e saídas auditáveis.'));
filhos.push(figura('fig1_arquitetura_pipeline.png', 15.5, 0.633));
filhos.push(legenda('Figura 1: Arquitetura do pipeline de dados implementado. Fonte: Dados da pesquisa (2026).'));
filhos.push(p('Como verificação independente de reprodutibilidade, o pipeline foi executado em dois ambientes computacionais distintos — sistemas operacionais e versões de biblioteca diferentes — produzindo resultados numericamente idênticos em todas as etapas.'));

filhos.push(h2('2.2  Métricas de desempenho e resultados dos ensaios'));
filhos.push(p('Os ensaios iniciais avaliaram três dimensões: a integridade dos dados de entrada, a fidelidade da base de análise em relação ao procedimento publicado que a gerou, e a magnitude e a estabilidade das associações estatísticas de interesse. A Tabela 3 consolida os indicadores obtidos.'));
filhos.push(tituloTabela('Tabela 3 – Indicadores de desempenho obtidos nos ensaios iniciais'));
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
  { t: 'O resultado de maior consequência para o trabalho é negativo e foi obtido pelo teste que a metodologia previa. Isoladamente, a complexidade ciclomática apresenta associação forte com a ocorrência de defeito, mesmo controlando o projeto de origem (razão de chances 1,90 por unidade logarítmica; LR = 639,8). Contudo, ao se acrescentar o tamanho do módulo ao modelo, o efeito da complexidade desaparece: a razão de chances ajustada cai para 0,944, com intervalo de confiança de 95% entre 0,870 e 1,024 — contendo, portanto, o valor nulo — e p = 0,17. A relação inversa não se verifica: o tamanho sobrevive folgadamente ao controle pela complexidade (LR = 431,2; p ≈ 9 × 10⁻⁹⁶). A Figura 2 apresenta o mesmo teste aplicado a todas as métricas candidatas; nenhuma delas exibe efeito positivo independente do tamanho, e as que permanecem estatisticamente distinguíveis do nulo o fazem com sinal negativo, padrão característico de colinearidade e não de mecanismo causal.' },
]));

filhos.push(figura('fig3_controle_por_tamanho.png', 15.5, 0.538));
filhos.push(legenda('Figura 2: Razões de chances das métricas candidatas antes e depois do controle pelo tamanho do módulo. Fonte: Dados da pesquisa (2026).'));

filhos.push(p('Esse resultado não invalida o uso da complexidade como eixo ordinal, mas altera o que se pode afirmar a partir dele. A ordenação do risco pelas faixas de complexidade é forte e robusta, como mostram a Figura 3 e a Tabela 3: o risco cresce monotonicamente de 0,147 a 0,439 entre a faixa mais baixa e a mais alta, a tendência é altamente significativa, e a monotonicidade se preserva sob todos os cinco esquemas alternativos de corte testados e sob todas as doze reamostragens por exclusão de projeto. O que os dados não sustentam é a atribuição causal: a complexidade ciclomática opera, nesta base, como marcador ordinal de risco correlacionado ao tamanho, e não como fator de risco independente dele. Para o propósito deste trabalho — transferência ordinal de risco entre domínios — um marcador estável é suficiente; a afirmação de efeito independente, que não seria sustentável, é explicitamente abandonada.'));

filhos.push(figura('fig2_fbase_por_faixa.png', 14.5, 0.587));
filhos.push(legenda('Figura 3: Risco basal por faixa de complexidade ciclomática, em frequência bruta e em probabilidade ajustada pelo efeito do projeto de origem. Fonte: Dados da pesquisa (2026).'));

filhos.push(p('As faixas adotadas — v(G) ≤ 10, de 11 a 15, de 16 a 20 e acima de 20 — constituem adaptação metodológica deste trabalho a partir das faixas interpretativas do NASA Software Engineering Handbook, cujo requisito SWE-220 estabelece o limiar de 15 para software crítico de segurança e exige revisão formal e justificativa documentada para qualquer excedente. As faixas da fonte original são cinco e sobrepõem-se nos extremos; a adaptação a quatro níveis não sobrepostos, alinhada ao limiar normativo, é registrada como decisão deste trabalho e não como classificação oficial.'));

filhos.push(figura('fig4_estabilidade_loo.png', 14.5, 0.576));
filhos.push(legenda('Figura 4: Estabilidade da ordenação sob exclusão sucessiva de cada projeto. Fonte: Dados da pesquisa (2026).'));

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
filhos.push(p('A verificação central, contudo, não é estrutural e sim de delineamento. As instâncias do PSPLIB são geradas por um projeto experimental fatorial sobre três parâmetros definidos por Kolisch, Sprecher e Drexl (1995): a complexidade de rede, dada pela razão entre arcos de precedência e atividades; o fator de recursos, que mede a fração média de tipos de recurso requisitados por atividade; e a força de recursos, que posiciona a disponibilidade entre o mínimo de viabilidade e o pico de demanda do cronograma de inícios mais cedo. Os três parâmetros foram recalculados a partir dos arquivos e seus níveis foram reconstruídos por agrupamento dos valores obtidos, sem que nenhum valor de referência fosse suposto. A Tabela 4 apresenta o resultado.'));
filhos.push(tituloTabela('Tabela 4 – Níveis dos parâmetros de delineamento reconstruídos a partir das instâncias'));
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
filhos.push(p('Com as instâncias caracterizadas, construiu-se o índice de dificuldade técnica que atribui a cada tarefa um nível ordinal. O índice, definido pelas equações (14) a (17), combina três grandezas medidas nas próprias instâncias: a duração normalizada, a intensidade de uso de recursos — definida como a fração média da disponibilidade de cada recurso que a tarefa consome, adaptação por atividade do fator de recursos de Kolisch, Sprecher e Drexl (1995) — e a criticidade na rede de precedências. As normalizações são feitas dentro de cada instância, uma vez que o modelo compara tarefas de um mesmo projeto e não tarefas de projetos distintos.'));
filhos.push(pRuns([
  { t: 'Correção de uma atribuição de fonte. ', b: true },
  { t: 'A formulação preliminar deste trabalho atribuía a construção do índice a De Reyck e Herroelen (1996). A verificação da fonte mostrou que a atribuição era imprópria: o índice de complexidade ali discutido deriva de Bein, Kamburowski e Stallmann (1992) e mede a distância da rede inteira à série-paralelidade, sendo uma propriedade do grafo e não da atividade. A referência foi mantida no trabalho, porém realocada para sustentar a caracterização da rede por instância, e o índice por tarefa passou a ser declarado como construção deste trabalho, com cada componente apoiado em fonte própria.' },
]));
filhos.push(pRuns([
  { t: 'Substituição da medida de criticidade. ', b: true },
  { t: 'A formulação preliminar previa a contagem de sucessores como medida de criticidade. Comparada à folga total obtida do método do caminho crítico, sobre as mesmas 28.800 tarefas, a correlação de Spearman entre as duas é de apenas 0,116, e 3.488 tarefas apresentam folga acima da mediana e três ou mais sucessores — isto é, muitos sucessores e nenhuma urgência. A criticidade passou a ser medida pela folga total, que é a medida canônica no nível da atividade. A contagem de sucessores permanece calculada e gravada na base, disponível como variável alternativa para análise de sensibilidade.' },
]));
filhos.push(p('Os três componentes mostram-se quase ortogonais entre si, com correlações de Spearman de −0,004 entre duração e intensidade de recursos, 0,003 entre intensidade e criticidade, e 0,193 entre duração e criticidade. Cada um carrega, portanto, informação distinta, e o índice composto não é uma única grandeza sob três nomes — situação oposta à observada na base NASA, onde complexidade e tamanho apresentavam correlação de 0,752 e o composto colapsava sobre um único eixo. A Figura 5 apresenta o comportamento dos níveis resultantes.'));
filhos.push(figura('fig6_niveis_di.png', 15.5, 0.478));
filhos.push(legenda('Figura 5: Duração média e folga total média por nível de dificuldade. Fonte: Dados da pesquisa (2026).'));
filhos.push(p('A duração média cresce e a folga média decresce monotonicamente ao longo dos quatro níveis, comportamento coerente com a interpretação do índice. Os pontos de corte são os quartis da distribuição, decisão declarada deste trabalho: ao contrário do domínio de software, que dispõe do limiar normativo do requisito SWE-220, não há para tarefas de projeto um limiar externo equivalente. A ordenação mostrou-se razoavelmente robusta à ponderação: entre seis esquemas alternativos de pesos, a menor correlação de ordenação observada foi de 0,847.'));

filhos.push(h2('2.6  Transferência ordinal de risco'));
filhos.push(p('A etapa que liga as duas bases consiste em atribuir às tarefas do PSPLIB o risco calibrado sobre os módulos da NASA. A forma dessa atribuição não é indiferente, e a decisão adotada apoia-se em evidência numérica.'));
filhos.push(p('Os quatro níveis não têm o mesmo tamanho relativo nos dois domínios: na base NASA, 86,24% dos módulos situam-se no nível mais baixo, contra 25,00% das tarefas do J60, por construção dos quartis. Atribuir a cada nível do J60 o risco absoluto do nível homônimo da NASA produziria risco médio de 0,3046 nas tarefas, contra taxa observada de 0,1749 na NASA — uma inflação de 1,74 vezes gerada exclusivamente pela diferença de tamanho dos estratos, e não por qualquer propriedade das tarefas. Seria um artefato de construção apresentado como resultado.'));
filhos.push(p('Adotou-se, portanto, a transferência por razão de risco relativo, conforme as equações (18) e (19). O que os dados NASA sustentam não é o nível absoluto de risco de um módulo de software, que não tem razão para valer em tarefas de engenharia, e sim a forma do gradiente: quantas vezes mais arriscada é uma tarefa difícil em relação a uma fácil. Essa razão é adimensional e independe da taxa basal do domínio. A Tabela 5 e a Figura 6 apresentam as razões estimadas.'));
filhos.push(tituloTabela('Tabela 5 – Razões de risco transferidas, com intervalos por reamostragem de projetos'));
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
filhos.push(figura('fig5_gradiente_risco.png', 14.0, 0.609));
filhos.push(legenda('Figura 6: Gradiente de risco transferido, com intervalo de confiança. Fonte: Dados da pesquisa (2026).'));
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


filhos.push(h2('2.7  Verificação e validação do simulador'));
filhos.push(p('Antes de qualquer resultado substantivo, o simulador foi submetido a quinze verificações automatizadas, executadas a cada alteração do código. Sete são verificações de consistência estrutural, que um simulador correto não pode falhar: encerramento de todas as tarefas em estado terminal, respeito às relações de precedência, não excedência da disponibilidade de recursos, não negatividade dos relógios, permanência das variáveis normalizadas no intervalo unitário, reprodutibilidade sob mesma semente e variabilidade sob sementes distintas. As demais são verificações de comportamento, que testam se o modelo se comporta como a teoria que o fundamenta prevê.'));
filhos.push(tituloTabela('Tabela 6 – Verificações de comportamento do simulador e seus resultados'));
filhos.push(tabela(
  [4470, 2600, 2000],
  ['Verificação de comportamento', 'Resultado medido', 'Situação'],
  [
    ['Sem risco nem pressão, nenhuma tarefa falha', 'erros = 0; reportadas = 0', 'aprovada'],
    ['Sem risco nem pressão, a eficiência tende à unidade', 'E_total = 0,9671', 'aprovada'],
    ['Sem risco nem pressão, a dívida técnica é nula', 'S_UR máximo = 0,0000', 'aprovada'],
    ['A dívida técnica cresce com a pressão (teste de tendência)', 'ρ = +1,000; p < 0,001', 'aprovada'],
    ['O tempo em modo heurístico cresce com a pressão', 'ρ = +1,000; p < 0,001', 'aprovada'],
    ['Mediana do retrabalho na faixa de plausibilidade externa', 'mediana = 0,1913', 'aprovada'],
    ['Cauda fora da faixa inferior a dez por cento das execuções', '0 de 24 execuções', 'aprovada'],
    ['Dívida latente estritamente positiva (estoque não inerte)', 'mediana = 0,0423', 'aprovada'],
  ],
  { centrar: [1, 2] },
));
filhos.push(legenda('Fonte: Dados da pesquisa (2026). As sete verificações estruturais, todas aprovadas, foram omitidas da tabela por brevidade.'));
filhos.push(pRuns([
  { t: 'Sobre o teste de tendência. ', b: true },
  { t: 'A verificação de que a dívida técnica cresce com a pressão foi inicialmente construída com doze repetições e três níveis de pressão, e falhou. A análise do erro-padrão mostrou que o teste era subdimensionado por construção: o ruído amostral excedia a diferença que se pretendia detectar. O teste foi refeito com cinco níveis e quarenta repetições, e a decisão foi registrada como correção de delineamento, e não como ajuste de tolerância até que o resultado passasse.' },
]));
filhos.push(pRuns([
  { t: 'Validação externa e seus limites. ', b: true },
  { t: 'A fração de esforço dedicada a retrabalho foi confrontada com a literatura de campo. A referência medida na mesma unidade da saída do modelo é a de Boehm e Basili (2001), segundo a qual projetos de software despendem entre quarenta e cinquenta por cento do esforço em retrabalho evitável. As cifras de Love et al. (2026) e de Love e Li (2000), da construção civil, são retidas apenas como piso de ordem de grandeza, com a ressalva explícita de que sua base é o valor de contrato e não o esforço, o que as torna grandezas de unidades distintas. A faixa de plausibilidade adotada, de um a cinquenta por cento do esforço planejado, é deliberadamente larga, e o teste correspondente é fraco: ele rejeita desalinhamento grosseiro e nada mais, não constituindo confirmação empírica do modelo nem substituto de calibração.' },
]));

filhos.push(h2('2.8  Experimento central: governança centralizada e adaptativa'));
filhos.push(p('O experimento comparou os dois arranjos da Tabela 2 sobre dezesseis instâncias do J60 com doze sementes cada, totalizando trezentas e oitenta e quatro execuções pareadas. Nenhuma execução deixou de concluir dentro do horizonte estabelecido. A Tabela 7 apresenta os resultados.'));
filhos.push(tituloTabela('Tabela 7 – Comparação pareada entre os arranjos de governança (192 pares)'));
filhos.push(tabela(
  [2700, 1220, 1220, 1120, 1330, 1480],
  ['Indicador', 'Centraliz.', 'Adaptat.', 'Variação', 'd de Cohen', 'Pares favoráveis'],
  [
    ['Tarefas concluídas com defeito', '13,02', '3,82', '−70,6%', '−2,400', '97,9%'],
    ['Taxa de omissão', '0,2170', '0,0637', '−70,6%', '−2,400', '97,9%'],
    ['Dívida latente de pico sobre o plano', '0,0741', '0,0201', '−72,8%', '−2,046', '98,4%'],
    ['Atraso relativo (makespan sobre CPM)', '3,1345', '1,9991', '−36,2%', '−1,988', '100,0%'],
    ['Eficiência alocativa E_total', '0,7839', '0,8885', '+13,3%', '+1,901', '97,4%'],
    ['Retrabalho pago sobre o plano', '0,2031', '0,1545', '−23,9%', '−0,729', '77,1%'],
    ['Retrabalho sobre esforço realizado (diagnóstico)', '0,0770', '0,0846', '+9,9%', '+0,288', '39,6%'],
  ],
  { centrar: [1, 2, 3, 4, 5] },
));
filhos.push(legenda('Fonte: Dados da pesquisa (2026). Todos os valores-p do teste de Wilcoxon pareado são inferiores a 0,003. A última linha é métrica de diagnóstico, discutida adiante.'));
filhos.push(figura('fig7_efeitos_pareados.png', 14.5, 0.640));
filhos.push(legenda('Figura 7: Tamanhos de efeito pareados com intervalos de confiança por reamostragem sobre os pares. Fonte: Dados da pesquisa (2026).'));
filhos.push(p('O arranjo adaptativo supera o centralizado em todos os indicadores substantivos, com tamanhos de efeito grandes e intervalos de confiança que não cruzam a origem. O resultado é coerente com o mecanismo postulado: ao converter defeito oculto em retrabalho visível e imediato, o arranjo adaptativo impede o acúmulo de dívida técnica que, no arranjo centralizado, retorna adiante sob pressão de prazo e amplia o atraso.'));
filhos.push(pRuns([
  { t: 'Uma métrica que media visibilidade, não dano. ', b: true },
  { t: 'A última linha da Tabela 7 move-se em sentido contrário a todas as demais. A investigação dessa discrepância revelou defeito na formulação original da métrica, e não achado substantivo. A razão entre retrabalho e esforço realizado tem por denominador o esforço efetivamente despendido, que inclui o tempo ocioso e bloqueado. O braço centralizado acumula tempo ocioso muito superior — cento e vinte e seis contra seis períodos em média — e, ao inflar o próprio denominador, dilui o retrabalho e aparenta desempenho melhor, ainda que seu retrabalho absoluto seja vinte e três vírgula oito por cento maior. A métrica premiava a ineficiência que se pretendia medir.' },
]));
filhos.push(figura('fig8_decomposicao_esforco.png', 15.5, 0.5521));
filhos.push(legenda('Figura 8: Composição do esforço realizado e o mesmo retrabalho medido sob duas bases distintas. Fonte: Dados da pesquisa (2026).'));
filhos.push(pRuns([
  { t: 'Correção adotada. ', b: true },
  { t: 'A base da razão passou a ser o esforço planejado do projeto, dado pela soma das durações nominais das tarefas. Trata-se de propriedade da instância, idêntica nos dois braços, de modo que a razão só pode variar pelo numerador. A métrica agregada original foi ainda decomposta em duas: o retrabalho efetivamente pago e a dívida latente de pico. A decomposição é necessária, e não cosmética, porque os arranjos diferem justamente na probabilidade de reporte: o adaptativo converte dívida oculta em retrabalho visível, e um agregado que soma as duas parcelas não distingue conversão de redução. Com a correção, o indicador passa a favorecer o arranjo adaptativo em vinte e três vírgula nove por cento, em concordância com os demais.' },
]));
filhos.push(p('Registra-se ainda que o valor final do estoque de dívida latente é nulo em todas as trezentas e oitenta e quatro execuções, por construção do laço de simulação, que só encerra após a quitação da dívida pendente. Por essa razão, a estatística informativa é o valor de pico do estoque, e não o seu valor terminal.'));
filhos.push(figura('fig9_trajetorias.png', 15.0, 0.7463));
filhos.push(legenda('Figura 9: Trajetórias médias dos estoques nos dois arranjos, com faixa interquartil. Fonte: Dados da pesquisa (2026).'));
filhos.push(p('A Figura 9 torna visível o mecanismo. No arranjo centralizado, a dívida técnica latente cresce ao longo de todo o período nominal do projeto, atinge o máximo em torno de uma vez e meia o prazo do caminho crítico e só então é drenada, o que prolonga a execução muito além do previsto. No arranjo adaptativo, o mesmo estoque permanece próximo de zero, e o progresso validado acumula-se de forma sustentada. A bateria cognitiva média recupera-se mais cedo, o que é consequência, e não causa, do menor volume de retrabalho tardio.'));

filhos.push(h2('2.9  Calibração e identificabilidade dos parâmetros'));
filhos.push(p('O procedimento descrito na Seção 1.8 foi executado em duas ondas de quatrocentos pontos amostrados por hipercubo latino, calibrando cinco parâmetros contra quatro observáveis. O teste do gêmeo idêntico foi aprovado nos três critérios: o conjunto NROY não é vazio, com cento e quinze pontos; contém o vetor verdadeiro nos cinco parâmetros; e o volume da caixa envolvente foi reduzido a quatorze vírgula oito por cento do volume a priori.'));
filhos.push(p('A aprovação do teste, contudo, não implica que os cinco parâmetros tenham sido determinados. A Tabela 8 reporta, para cada um, a redução da largura marginal do conjunto NROY relativamente à faixa inicial.'));
filhos.push(tituloTabela('Tabela 8 – Identificabilidade dos parâmetros calibrados'));
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
filhos.push(figura('fig10_nroy_identificabilidade.png', 15.5, 0.5428));
filhos.push(legenda('Figura 10: Conjunto NROY projetado sobre a crista de equifinalidade e redução marginal por parâmetro. Fonte: Dados da pesquisa (2026).'));
filhos.push(p('A hipótese foi testada e confirmada: o produto dos dois fatores apresenta redução de setenta e quatro vírgula sete por cento, contra trinta e seis vírgula oito e seis vírgula zero por cento dos fatores isolados. Decorre daí uma recomendação de reparametrização: em calibração com dados reais, deve-se estimar o produto — interpretável como esforço esperado de retrabalho por tarefa — e declarar a divisão entre frequência e severidade como não identificada, em vez de reportar dois números que os dados não sustentam. A separação dos fatores exigiria observar a taxa de defeito e o custo unitário de correção de forma independente, dado que o delineamento atual não contempla.'));
filhos.push(p('Registra-se, por fim, que as larguras marginais praticamente não se alteraram entre a primeira e a segunda onda. As ondas convergiram, e uma terceira não reduziria o espaço, porque o limite encontrado é de identificabilidade estrutural e não de tamanho de amostra.'));

filhos.push(h2('2.10  Procedência dos parâmetros e limitações declaradas'));
filhos.push(p('A Tabela 9 resume a procedência dos parâmetros do modelo, segundo a classificação mantida no arquivo único de configuração. A distinção é mantida explícita porque a credibilidade de um modelo de simulação depende menos do número de parâmetros do que da clareza sobre a origem de cada um.'));
filhos.push(tituloTabela('Tabela 9 – Procedência dos parâmetros do modelo'));
filhos.push(tabela(
  [2100, 1100, 5870],
  ['Condição', 'Quantidade', 'Significado e exemplo'],
  [
    ['calibrado', '1', 'derivado dos dados por procedimento documentado: F_base por faixa de dificuldade, obtido da base NASA'],
    ['literatura', '2', 'fixado por resultado publicado: t-norma e partição difusa, por Van Broekhoven e De Baets (2009)'],
    ['tcc1', '1', 'herdado da fase conceitual sem alteração'],
    ['premissa', '21', 'arbitrado de forma declarada, com justificativa registrada e sujeito a varredura'],
    ['aberto', '13', 'ainda não fixado; cinco deles submetidos à calibração da Seção 2.9'],
  ],
  { centrar: [1] },
));
filhos.push(legenda('Fonte: Elaborado pela autora (2026), a partir do arquivo de configuração do modelo.'));
filhos.push(pRuns([
  { t: 'Limitações. ', b: true },
  { t: 'Quatro limitações são declaradas. Primeira, a transferência ordinal de risco entre domínios pressupõe que o gradiente de risco por dificuldade seja transferível, ainda que o nível absoluto não seja; trata-se de suposição, e não de resultado. Segunda, a validação externa do retrabalho é um teste fraco, pelas razões expostas na Seção 2.7. Terceira, o teste do gêmeo idêntico é otimista por construção, uma vez que anula a discrepância entre modelo e realidade. Quarta, três dos cinco parâmetros submetidos à calibração não são identificáveis com os observáveis do delineamento atual, e assim são reportados.' },
]));

filhos.push(h2('2.11  Cronograma de atividades e próximas etapas'));
filhos.push(p('A Tabela 10 distribui cronologicamente as atividades previstas para a conclusão do trabalho.'));
filhos.push(tituloTabela('Tabela 10 – Cronograma de finalização do trabalho (TCC II)'));
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

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log('gerado:', OUT, buf.length, 'bytes');
});
