"""
01_auditar_raw.py — Auditoria dos arquivos brutos NASA MDP
===========================================================

PROBLEMA QUE RESOLVE
--------------------
Antes de aplicar qualquer regra de limpeza, e preciso saber exatamente o
que ha nos arquivos. Shepperd et al. (2013) mostraram que versoes distintas
dos conjuntos NASA circulavam com diferencas nao documentadas. Portanto a
primeira etapa nao limpa nada: ela CARACTERIZA e REGISTRA o estado de
partida, para que qualquer alteracao posterior possa ser atribuida a uma
regra explicita.

ENTRADA
-------
  data/raw/nasa_promise/        (arquivos .arff e .csv, versoes brutas)
  data/raw/nasa_dpp_reference/  (arquivos .arff, versoes D'' de referencia)

Nenhum arquivo de entrada e modificado. O script apenas le.

SAIDA
-----
  outputs/tables/01_auditoria_arquivos.csv   uma linha por arquivo
  outputs/tables/01_auditoria_atributos.csv  uma linha por (arquivo, atributo)
  outputs/tables/01_auditoria_pares.csv      comparacao ARFF x CSV do mesmo conjunto
  outputs/logs/01_auditar_raw.log            registro da execucao

DECISAO METODOLOGICA: SOMENTE BIBLIOTECA PADRAO
-----------------------------------------------
Este script nao usa pandas nem qualquer leitor de ARFF pronto, embora
fosse mais curto assim. O motivo e que uma auditoria precisa observar os
arquivos como eles sao. Leitores de alto nivel convertem tipos, tratam
valores ausentes, descartam linhas malformadas e normalizam nomes -- tudo
silenciosamente. Qualquer uma dessas acoes destruiria justamente a
evidencia que queremos coletar. A partir do script 02 o pandas passa a ser
usado normalmente, porque ai ja saberemos o que estamos manipulando.

O QUE E DA LITERATURA E O QUE E DESTE TRABALHO
-----------------------------------------------
  - Da literatura: a exigencia de documentar proveniencia e pre-processamento
    antes de analisar (Shepperd et al., 2013).
  - Deste trabalho: a escolha das metricas de auditoria abaixo (hash SHA-256,
    fim de linha, duplicatas exatas, celulas ausentes, distribuicao do rotulo)
    e a decisao de usar apenas a biblioteca padrao.
  - Nao ha limpeza, filtro ou julgamento de plausibilidade nesta etapa.

COMO VERIFICAMOS SE O RESULTADO ESTA CORRETO
---------------------------------------------
  1. A soma das linhas por arquivo deve bater com a contagem manual
     (ex.: no Windows, `find /c /v "" arquivo.csv`).
  2. Os pares ARFF/CSV do mesmo conjunto devem ter o mesmo numero de linhas;
     divergencia e achado, nao erro do script.
  3. O hash SHA-256 deve ser identico quando o script rodar no computador 2.
     Se diferir, algum arquivo bruto foi alterado -- o que a configuracao do
     .gitattributes existe justamente para impedir.
"""

import csv
import hashlib
import sys
from datetime import datetime
from pathlib import Path

# Evita erro de codificacao ao imprimir no console do Windows.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------------
# Caminhos
#
# Calculados a partir da localizacao DESTE arquivo, e nao da pasta onde o
# terminal esta. Assim o script funciona sendo chamado de qualquer lugar,
# nos dois computadores, sem nenhum caminho absoluto escrito no codigo.
# ---------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[2]

ENTRADAS = {
    "promise": RAIZ / "data" / "raw" / "nasa_promise",
    "dpp_ref": RAIZ / "data" / "raw" / "nasa_dpp_reference",
}
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"

# Cada script garante a existencia das pastas que usa. Isso evita que a
# execucao quebre num clone novo por causa de uma pasta ausente.
DIR_TABELAS.mkdir(parents=True, exist_ok=True)
DIR_LOGS.mkdir(parents=True, exist_ok=True)

CAMINHO_LOG = DIR_LOGS / "01_auditar_raw.log"
_linhas_log: list[str] = []


def log(mensagem: str = "") -> None:
    """Imprime na tela e acumula para gravar no arquivo de log."""
    print(mensagem)
    _linhas_log.append(mensagem)


# ---------------------------------------------------------------------
# Leitura de baixo nivel
# ---------------------------------------------------------------------

def sha256_do_arquivo(caminho: Path) -> str:
    """
    Impressao digital criptografica do arquivo, byte a byte.

    Serve como prova de imutabilidade: se um unico byte mudar, o hash muda
    por completo. E assim que se demonstra, sem depender de confianca, que
    os dados analisados sao exatamente os dados baixados.
    """
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def ler_texto(caminho: Path) -> tuple[str, str, str]:
    """
    Le o arquivo como texto e detecta fim de linha e codificacao.

    Retorna (texto, fim_de_linha, codificacao).

    Le em modo binario e decodifica manualmente, em vez de usar o modo texto
    do Python, porque o modo texto converte finais de linha automaticamente
    -- e o fim de linha e uma das coisas que queremos medir.
    """
    bruto = caminho.read_bytes()

    if b"\r\n" in bruto:
        fim_de_linha = "CRLF"
    elif b"\n" in bruto:
        fim_de_linha = "LF"
    else:
        fim_de_linha = "nenhum"

    for codificacao in ("utf-8", "latin-1"):
        try:
            return bruto.decode(codificacao), fim_de_linha, codificacao
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace"), fim_de_linha, "utf-8(com erros)"


# ---------------------------------------------------------------------
# Interpretacao dos formatos
# ---------------------------------------------------------------------

def analisar_arff(texto: str) -> dict:
    """
    Interpreta um arquivo ARFF sem biblioteca externa.

    Estrutura do formato (Weka):
        @relation <nome>
        @attribute <nome> <tipo>      (varias linhas)
        @data
        <linhas de dados separadas por virgula>

    Retorna nome da relacao, lista de (nome, tipo) dos atributos e as
    linhas de dados como texto cru, sem conversao de tipo.
    """
    relacao = ""
    atributos: list[tuple[str, str]] = []
    linhas_dados: list[str] = []
    dentro_dos_dados = False

    for linha in texto.splitlines():
        despida = linha.strip()

        if dentro_dos_dados:
            # Linhas vazias e comentarios (%) nao sao observacoes.
            if despida and not despida.startswith("%"):
                linhas_dados.append(despida)
            continue

        if not despida or despida.startswith("%"):
            continue

        minuscula = despida.lower()
        if minuscula.startswith("@relation"):
            relacao = despida[9:].strip().strip("'\"")
        elif minuscula.startswith("@attribute"):
            # Formato: @attribute <nome> <tipo>. O tipo pode conter espacos,
            # como em "{Y,N}", entao dividimos em no maximo 3 pedacos.
            partes = despida.split(None, 2)
            nome = partes[1].strip("'\"") if len(partes) > 1 else ""
            tipo = partes[2].strip() if len(partes) > 2 else ""
            atributos.append((nome, tipo))
        elif minuscula.startswith("@data"):
            dentro_dos_dados = True

    return {"relacao": relacao, "atributos": atributos, "linhas_dados": linhas_dados}


def analisar_csv(texto: str) -> dict:
    """
    Interpreta um CSV assumindo a primeira linha como cabecalho.

    Nao usa o modulo csv de proposito: queremos as linhas exatamente como
    estao escritas, para poder compara-las byte a byte com as linhas do ARFF
    correspondente.
    """
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    if not linhas:
        return {"relacao": "", "atributos": [], "linhas_dados": []}

    cabecalho = [c.strip().strip("'\"") for c in linhas[0].split(",")]
    # O CSV nao declara tipos; registramos "(nao declarado)" para deixar
    # explicito que a informacao esta ausente, e nao que foi omitida por nos.
    atributos = [(nome, "(nao declarado)") for nome in cabecalho]
    return {"relacao": "", "atributos": atributos, "linhas_dados": linhas[1:]}


# ---------------------------------------------------------------------
# Metricas de auditoria
# ---------------------------------------------------------------------

def resumir_rotulo(linhas_dados: list[str]) -> str:
    """
    Conta os valores distintos da ULTIMA coluna, que nos conjuntos NASA e
    sempre o rotulo de defeito. Formato do retorno: "false=449; true=49".
    """
    contagens: dict[str, int] = {}
    for linha in linhas_dados:
        campos = linha.split(",")
        if campos:
            valor = campos[-1].strip()
            contagens[valor] = contagens.get(valor, 0) + 1
    return "; ".join(f"{k}={v}" for k, v in sorted(contagens.items()))


def contar_ausentes(linhas_dados: list[str]) -> int:
    """
    Conta celulas com '?', a marca de valor ausente no padrao ARFF.
    Apenas conta -- nao remove, nao imputa.
    """
    total = 0
    for linha in linhas_dados:
        total += sum(1 for campo in linha.split(",") if campo.strip() == "?")
    return total


def contar_duplicatas_exatas(linhas_dados: list[str]) -> int:
    """
    Numero de linhas que sao copia textual de outra ja vista.

    Relevante porque a remocao de observacoes identicas e um dos criterios
    do procedimento de limpeza da literatura. Aqui apenas medimos o quanto
    existe; a decisao de remover pertence ao script 02.
    """
    vistas: set[str] = set()
    duplicatas = 0
    for linha in linhas_dados:
        if linha in vistas:
            duplicatas += 1
        else:
            vistas.add(linha)
    return duplicatas


def comparar_semanticamente(linhas_a: list[str], linhas_b: list[str]) -> tuple[bool, str]:
    """
    Compara duas listas de linhas campo a campo, tratando numeros como
    numeros e nao como texto.

    POR QUE ISTO EXISTE
    -------------------
    Comparacao textual e rigorosa demais para julgar equivalencia de dados.
    O valor 59 pode aparecer escrito como "59" num arquivo e "59.0" noutro:
    as cadeias de caracteres diferem, o valor nao. Sem esta distincao, uma
    diferenca puramente de formatacao seria reportada como divergencia de
    conteudo e geraria investigacao desnecessaria.

    Regra aplicada a cada campo:
      - se AMBOS os campos convertem para numero, compara os numeros;
      - caso contrario, compara o texto sem espacos nas pontas.

    Retorna (sao_equivalentes, descricao_da_primeira_diferenca).

    Limitacao assumida: a conversao para float pode, em tese, igualar valores
    que diferem em casas decimais alem da precisao de ponto flutuante. Para as
    magnitudes presentes nestes conjuntos isso nao ocorre, mas a limitacao
    fica registrada.
    """
    if len(linhas_a) != len(linhas_b):
        return False, f"numero de linhas difere ({len(linhas_a)} vs {len(linhas_b)})"

    for indice, (la, lb) in enumerate(zip(linhas_a, linhas_b), start=1):
        campos_a = [c.strip() for c in la.split(",")]
        campos_b = [c.strip() for c in lb.split(",")]

        if len(campos_a) != len(campos_b):
            return False, f"linha {indice}: numero de campos difere"

        for coluna, (ca, cb) in enumerate(zip(campos_a, campos_b), start=1):
            if ca == cb:
                continue
            try:
                if float(ca) == float(cb):
                    continue  # mesmo numero, grafia diferente
            except ValueError:
                pass
            return False, f"linha {indice}, coluna {coluna}: '{ca}' vs '{cb}'"

    return True, ""


# ---------------------------------------------------------------------
# Execucao
# ---------------------------------------------------------------------

def main() -> None:
    log("=" * 78)
    log("AUDITORIA DOS ARQUIVOS BRUTOS NASA MDP")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log(f"Raiz do projeto: {RAIZ}")
    log("=" * 78)

    registros_arquivos: list[dict] = []
    registros_atributos: list[dict] = []
    analises: dict[tuple[str, str, str], dict] = {}

    for grupo, pasta in ENTRADAS.items():
        if not pasta.exists():
            log(f"\n[AVISO] Pasta nao encontrada: {pasta}")
            continue

        arquivos = sorted(
            p for p in pasta.iterdir()
            if p.suffix.lower() in (".arff", ".csv")
        )

        log(f"\n--- Grupo '{grupo}' -- {len(arquivos)} arquivo(s) em {pasta.name}/")

        for caminho in arquivos:
            texto, fim_de_linha, codificacao = ler_texto(caminho)
            formato = caminho.suffix.lower().lstrip(".")

            analise = analisar_arff(texto) if formato == "arff" else analisar_csv(texto)
            linhas_dados = analise["linhas_dados"]
            conjunto = caminho.stem.lower()
            analises[(grupo, conjunto, formato)] = analise

            registros_arquivos.append({
                "grupo": grupo,
                "conjunto": conjunto,
                "arquivo": caminho.name,
                "formato": formato,
                "bytes": caminho.stat().st_size,
                "sha256": sha256_do_arquivo(caminho),
                "fim_de_linha": fim_de_linha,
                "codificacao": codificacao,
                "relacao_declarada": analise["relacao"],
                "n_atributos": len(analise["atributos"]),
                "nome_ultimo_atributo": analise["atributos"][-1][0] if analise["atributos"] else "",
                "n_linhas_dados": len(linhas_dados),
                "n_duplicatas_exatas": contar_duplicatas_exatas(linhas_dados),
                "n_celulas_ausentes": contar_ausentes(linhas_dados),
                "distribuicao_rotulo": resumir_rotulo(linhas_dados),
            })

            for posicao, (nome, tipo) in enumerate(analise["atributos"], start=1):
                registros_atributos.append({
                    "grupo": grupo,
                    "conjunto": conjunto,
                    "arquivo": caminho.name,
                    "posicao": posicao,
                    "atributo": nome,
                    "tipo_declarado": tipo,
                })

            log(f"  {caminho.name:<28} {len(linhas_dados):>6} linhas  "
                f"{len(analise['atributos']):>3} atributos  {fim_de_linha}")

    # -----------------------------------------------------------------
    # Comparacao ARFF x CSV do mesmo conjunto
    #
    # Responde diretamente a pergunta: os dois formatos representam a mesma
    # versao dos dados? Comparamos nomes de atributos, numero de linhas e o
    # conteudo textual das linhas de dados.
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("COMPARACAO ARFF x CSV (mesmo conjunto, mesmo grupo)")
    log("=" * 78)

    registros_pares: list[dict] = []
    conjuntos_com_par = sorted({
        (g, c) for (g, c, f) in analises
        if (g, c, "arff") in analises and (g, c, "csv") in analises
    })

    if not conjuntos_com_par:
        log("Nenhum conjunto possui os dois formatos.")

    for grupo, conjunto in conjuntos_com_par:
        a = analises[(grupo, conjunto, "arff")]
        c = analises[(grupo, conjunto, "csv")]

        nomes_arff = [n.lower() for n, _ in a["atributos"]]
        nomes_csv = [n.lower() for n, _ in c["atributos"]]
        linhas_iguais = len(a["linhas_dados"]) == len(c["linhas_dados"])
        conteudo_identico = a["linhas_dados"] == c["linhas_dados"]

        # Comparacao por CONJUNTO de linhas distintas, alem da comparacao
        # posicional acima.
        #
        # Por que isso importa: dois arquivos podem conter exatamente as
        # mesmas observacoes distintas e ainda assim ter tamanhos diferentes,
        # se um deles repetir linhas mais vezes que o outro. Nesse caso a
        # diferenca nao e de conteudo, e de multiplicidade -- indicio de que
        # um dos arquivos ja passou por remocao (parcial ou total) de
        # duplicatas antes de ser publicado. Distinguir os dois casos e
        # essencial: "arquivos diferentes" e um problema; "mesmo conteudo com
        # deduplicacao diferente" e uma pista sobre o pre-processamento.
        conjunto_arff = set(a["linhas_dados"])
        conjunto_csv = set(c["linhas_dados"])
        exclusivas_arff = len(conjunto_arff - conjunto_csv)
        exclusivas_csv = len(conjunto_csv - conjunto_arff)

        equivalentes, detalhe_diferenca = comparar_semanticamente(
            a["linhas_dados"], c["linhas_dados"]
        )

        # Se o conteudo difere, localizamos a primeira divergencia. Um
        # numero de linha concreto e muito mais util para investigar do que
        # um "sao diferentes".
        primeira_divergencia = ""
        if not conteudo_identico:
            for i, (la, lc) in enumerate(zip(a["linhas_dados"], c["linhas_dados"]), start=1):
                if la != lc:
                    primeira_divergencia = str(i)
                    break
            else:
                primeira_divergencia = f"apos linha {min(len(a['linhas_dados']), len(c['linhas_dados']))}"

        registros_pares.append({
            "grupo": grupo,
            "conjunto": conjunto,
            "n_linhas_arff": len(a["linhas_dados"]),
            "n_linhas_csv": len(c["linhas_dados"]),
            "atributos_iguais": nomes_arff == nomes_csv,
            "n_linhas_iguais": linhas_iguais,
            "conteudo_identico": conteudo_identico,
            "primeira_linha_divergente": primeira_divergencia,
            "n_linhas_distintas_arff": len(conjunto_arff),
            "n_linhas_distintas_csv": len(conjunto_csv),
            "n_exclusivas_arff": exclusivas_arff,
            "n_exclusivas_csv": exclusivas_csv,
            "mesmo_conjunto_de_observacoes": exclusivas_arff == 0 and exclusivas_csv == 0,
            "equivalentes_numericamente": equivalentes,
            "primeira_diferenca_semantica": detalhe_diferenca,
        })

        if conteudo_identico:
            veredito = "IDENTICOS (texto)"
        elif equivalentes:
            veredito = "EQUIVALENTES (mesmos valores, grafia numerica diferente)"
        elif exclusivas_arff == 0 and exclusivas_csv == 0:
            veredito = "MESMO CONJUNTO DE OBSERVACOES, MULTIPLICIDADE DIFERENTE"
        else:
            veredito = "DIVERGENTES (conteudo diferente)"

        log(f"  {conjunto:<8} arff={len(a['linhas_dados']):>6}  csv={len(c['linhas_dados']):>6}  "
            f"distintas: arff={len(conjunto_arff):>6} csv={len(conjunto_csv):>6}  "
            f"exclusivas: arff={exclusivas_arff:>4} csv={exclusivas_csv:>4}")
        log(f"           -> {veredito}")
        if not equivalentes and detalhe_diferenca:
            log(f"              1a diferenca real: {detalhe_diferenca}")

    # -----------------------------------------------------------------
    # Gravacao das tabelas
    # -----------------------------------------------------------------
    def gravar(nome_arquivo: str, registros: list[dict]) -> None:
        caminho = DIR_TABELAS / nome_arquivo
        if not registros:
            log(f"\n[AVISO] Nada a gravar em {nome_arquivo}")
            return
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=list(registros[0].keys()))
            escritor.writeheader()
            escritor.writerows(registros)
        log(f"  {caminho.relative_to(RAIZ)}  ({len(registros)} linhas)")

    log("\n" + "=" * 78)
    log("TABELAS GERADAS")
    log("=" * 78)
    gravar("01_auditoria_arquivos.csv", registros_arquivos)
    gravar("01_auditoria_atributos.csv", registros_atributos)
    gravar("01_auditoria_pares.csv", registros_pares)

    log("\n" + "=" * 78)
    log("RESUMO")
    log("=" * 78)
    log(f"Arquivos auditados : {len(registros_arquivos)}")
    log(f"Observacoes lidas  : {sum(r['n_linhas_dados'] for r in registros_arquivos)}")
    log(f"Duplicatas exatas  : {sum(r['n_duplicatas_exatas'] for r in registros_arquivos)}")
    log(f"Celulas ausentes   : {sum(r['n_celulas_ausentes'] for r in registros_arquivos)}")
    log("\nNenhum arquivo de entrada foi modificado.")

    CAMINHO_LOG.write_text("\n".join(_linhas_log) + "\n", encoding="utf-8")
    print(f"\nLog gravado em: {CAMINHO_LOG.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
