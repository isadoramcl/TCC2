"""
02_consolidar_dpp.py — Consolidacao da base D'' em tabela unica
================================================================

PROBLEMA QUE RESOLVE
--------------------
Os arquivos D'' publicados vem separados por projeto e com conjuntos de
metricas diferentes entre si. Para investigar a relacao entre complexidade e
defeito controlando o efeito do projeto de origem, e preciso uma unica tabela
contendo todos os projetos, com um conjunto de metricas comparavel, sem perder
a capacidade de retornar cada linha ao arquivo de onde veio.

ENTRADA
-------
  data/raw/nasa_dpp_reference/*.arff   (13 arquivos, somente leitura)

SAIDA
-----
  data/processed/nasa/base_dpp_consolidada.csv
  outputs/tables/02_consolidacao_resumo.csv
  outputs/tables/02_metricas_descartadas.csv
  outputs/logs/02_consolidar_dpp.log

DECISOES METODOLOGICAS DESTA ETAPA
-----------------------------------
1. Base de partida: a versao D'' publicada pelos autores, nao uma limpeza
   reproduzida por nos. Justificativa registrada em docs/registro_de_decisoes.md
   secao 2: os arquivos brutos disponiveis (repositorio PROMISE) nao sao a
   entrada que o algoritmo de Shepperd et al. (2013) pressupoe, de modo que
   aplicar as regras a eles seria adaptacao e nao replicacao.

2. KC4 e excluido. O arquivo contem apenas cabecalho, sem nenhuma observacao.
   O artigo registra em nota de rodape que o KC4 nao esta presente no
   repositorio PROMISE. A exclusao e registrada no log, nao silenciosa.

3. Conjunto de metricas: usamos a INTERSECAO das metricas presentes em todos os
   arquivos aproveitados. A alternativa (uniao, preenchendo com ausentes) foi
   descartada porque introduziria ausencia sistematica correlacionada com o
   projeto -- exatamente a variavel cujo efeito queremos controlar -- o que
   confundiria a interpretacao dos modelos.
   Verificacao: todas as metricas candidatas do trabalho (CYCLOMATIC_COMPLEXITY,
   DESIGN_COMPLEXITY, ESSENTIAL_COMPLEXITY, LOC_TOTAL, HALSTEAD_DIFFICULTY,
   HALSTEAD_EFFORT) sobrevivem a intersecao, de modo que a decisao nao custa
   nenhuma variavel de interesse.

4. Rotulo: normalizado para inteiro 0/1. O atributo chama-se "Defective" em 11
   arquivos e "label" no JM1; ambos assumem os valores {Y, N}. A diferenca de
   nome e registrada, nao corrigida no arquivo de origem.

5. Rastreabilidade: cada linha carrega project, source_file e source_row, onde
   source_row e a posicao da observacao dentro da secao @data do arquivo
   original, comecando em 1. Qualquer linha da base consolidada pode assim ser
   reconduzida ao arquivo e a linha de origem.

COMO VERIFICAMOS SE O RESULTADO ESTA CORRETO
---------------------------------------------
  1. O total de linhas da base consolidada deve ser igual a soma das linhas dos
     arquivos aproveitados, conforme medido independentemente pelo script 01.
  2. A contagem de defeitos por projeto deve reproduzir a distribuicao do rotulo
     registrada pelo script 01.
  3. A base final nao pode conter nenhum valor ausente, ja que o passo 5 do
     algoritmo de limpeza dos autores remove casos com valores ausentes.
  4. source_file + source_row deve ser unico para toda a base.
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parents[2]
DIR_ENTRADA = RAIZ / "data" / "raw" / "nasa_dpp_reference"
DIR_PROCESSADO = RAIZ / "data" / "processed" / "nasa"
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"

for d in (DIR_PROCESSADO, DIR_TABELAS, DIR_LOGS):
    d.mkdir(parents=True, exist_ok=True)

ARQUIVO_SAIDA = DIR_PROCESSADO / "base_dpp_consolidada.csv"
CAMINHO_LOG = DIR_LOGS / "02_consolidar_dpp.log"
_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def ler_arff(caminho: Path) -> tuple[list[str], list[list[str]]]:
    """
    Le um ARFF e devolve (nomes_dos_atributos, linhas_de_dados_em_campos).

    Reaproveita a mesma logica de leitura do script 01, deliberadamente simples,
    para que a base consolidada seja construida a partir da mesma interpretacao
    dos arquivos que foi auditada.
    """
    texto = caminho.read_bytes().decode("utf-8", errors="replace")
    atributos: list[str] = []
    dados: list[list[str]] = []
    em_dados = False

    for linha in texto.splitlines():
        despida = linha.strip()
        if em_dados:
            if despida and not despida.startswith("%"):
                dados.append([c.strip() for c in despida.split(",")])
            continue
        if not despida or despida.startswith("%"):
            continue
        minuscula = despida.lower()
        if minuscula.startswith("@attribute"):
            partes = despida.split(None, 2)
            if len(partes) > 1:
                atributos.append(partes[1].strip("'\""))
        elif minuscula.startswith("@data"):
            em_dados = True

    return atributos, dados


def main() -> None:
    log("=" * 78)
    log("CONSOLIDACAO DA BASE D''")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    arquivos = sorted(DIR_ENTRADA.glob("*.arff"))
    if not arquivos:
        raise SystemExit(f"Nenhum arquivo .arff encontrado em {DIR_ENTRADA}")

    # ---------------------------------------------------------------
    # Passo 1 — leitura e triagem
    # ---------------------------------------------------------------
    lidos: dict[str, tuple[list[str], list[list[str]]]] = {}
    excluidos: list[tuple[str, str]] = []

    log("\n--- Leitura dos arquivos ---")
    for caminho in arquivos:
        projeto = caminho.stem.upper()
        atributos, dados = ler_arff(caminho)

        if not dados:
            excluidos.append((projeto, "arquivo sem observacoes (somente cabecalho)"))
            log(f"  {projeto:<6} EXCLUIDO -- arquivo sem observacoes")
            continue

        lidos[projeto] = (atributos, dados)
        log(f"  {projeto:<6} {len(dados):>6} observacoes, {len(atributos):>3} atributos "
            f"(rotulo: {atributos[-1]})")

    if excluidos:
        log("\n  Arquivos excluidos desta consolidacao:")
        for projeto, motivo in excluidos:
            log(f"    {projeto}: {motivo}")

    # ---------------------------------------------------------------
    # Passo 2 — intersecao das metricas
    #
    # O ultimo atributo de cada arquivo e o rotulo e nao entra na intersecao,
    # porque seu nome varia entre arquivos ("Defective" e "label").
    # ---------------------------------------------------------------
    conjuntos = {p: set(a[:-1]) for p, (a, _) in lidos.items()}
    metricas_comuns = sorted(set.intersection(*conjuntos.values()))
    metricas_todas = sorted(set().union(*conjuntos.values()))

    log("\n--- Selecao de metricas ---")
    log(f"  Metricas presentes em ao menos um arquivo : {len(metricas_todas)}")
    log(f"  Metricas comuns a TODOS os arquivos       : {len(metricas_comuns)}")

    descartadas = []
    for metrica in sorted(set(metricas_todas) - set(metricas_comuns)):
        ausente_em = sorted(p for p in lidos if metrica not in conjuntos[p])
        descartadas.append({
            "metrica": metrica,
            "n_projetos_com": len(lidos) - len(ausente_em),
            "ausente_em": "; ".join(ausente_em),
        })
        log(f"    descartada: {metrica:<34} ausente em {', '.join(ausente_em)}")

    METRICAS_DE_INTERESSE = [
        "CYCLOMATIC_COMPLEXITY", "DESIGN_COMPLEXITY", "ESSENTIAL_COMPLEXITY",
        "LOC_TOTAL", "HALSTEAD_DIFFICULTY", "HALSTEAD_EFFORT", "HALSTEAD_ERROR_EST",
    ]
    log("\n  Verificacao das metricas de interesse do trabalho:")
    for metrica in METRICAS_DE_INTERESSE:
        situacao = "PRESERVADA" if metrica in metricas_comuns else "PERDIDA NA INTERSECAO"
        log(f"    {metrica:<24} {situacao}")

    perdidas = [m for m in METRICAS_DE_INTERESSE if m not in metricas_comuns]
    if perdidas:
        log(f"\n  [ATENCAO] Metricas de interesse perdidas: {perdidas}")

    # ---------------------------------------------------------------
    # Passo 3 — montagem da tabela unica
    # ---------------------------------------------------------------
    log("\n--- Montagem da base consolidada ---")
    registros: list[dict] = []
    nomes_rotulo: dict[str, str] = {}

    for projeto, (atributos, dados) in sorted(lidos.items()):
        indice = {nome: i for i, nome in enumerate(atributos)}
        nome_rotulo = atributos[-1]
        nomes_rotulo[projeto] = nome_rotulo
        posicao_rotulo = len(atributos) - 1

        for numero_da_linha, campos in enumerate(dados, start=1):
            if len(campos) != len(atributos):
                # Nao deve ocorrer nos arquivos D''; se ocorrer, e achado.
                log(f"  [ATENCAO] {projeto} linha {numero_da_linha}: "
                    f"{len(campos)} campos para {len(atributos)} atributos -- linha ignorada")
                continue

            registro = {
                "project": projeto,
                "source_file": f"{projeto}.arff",
                "source_row": numero_da_linha,
            }
            for metrica in metricas_comuns:
                registro[metrica] = campos[indice[metrica]]

            valor_rotulo = campos[posicao_rotulo].strip().upper()
            registro["defective"] = 1 if valor_rotulo == "Y" else 0
            registro["rotulo_original"] = campos[posicao_rotulo].strip()
            registros.append(registro)

    base = pd.DataFrame(registros)

    # Conversao numerica explicita. Qualquer valor que nao converta vira ausente
    # e sera detectado na verificacao seguinte, em vez de passar despercebido.
    for metrica in metricas_comuns:
        base[metrica] = pd.to_numeric(base[metrica], errors="coerce")

    log(f"  Base construida: {len(base)} linhas x {len(base.columns)} colunas")

    # ---------------------------------------------------------------
    # Passo 4 — verificacoes
    # ---------------------------------------------------------------
    log("\n--- Verificacoes ---")
    falhas: list[str] = []

    esperado = sum(len(d) for _, d in lidos.values())
    if len(base) == esperado:
        log(f"  [OK]    Total de linhas confere: {len(base)} = soma dos arquivos")
    else:
        falhas.append(f"total de linhas {len(base)} != esperado {esperado}")
        log(f"  [FALHA] Total {len(base)} != esperado {esperado}")

    ausentes = int(base[metricas_comuns].isna().sum().sum())
    if ausentes == 0:
        log("  [OK]    Nenhum valor ausente nas metricas")
    else:
        falhas.append(f"{ausentes} valores ausentes")
        log(f"  [FALHA] {ausentes} valores ausentes encontrados")
        for metrica in metricas_comuns:
            n = int(base[metrica].isna().sum())
            if n:
                log(f"            {metrica}: {n}")

    duplicadas = int(base.duplicated(subset=["source_file", "source_row"]).sum())
    if duplicadas == 0:
        log("  [OK]    Chave (source_file, source_row) e unica")
    else:
        falhas.append(f"{duplicadas} chaves duplicadas")
        log(f"  [FALHA] {duplicadas} chaves duplicadas")

    valores_rotulo = set(base["rotulo_original"].str.upper().unique())
    if valores_rotulo <= {"Y", "N"}:
        log(f"  [OK]    Rotulo assume apenas {sorted(valores_rotulo)}")
    else:
        falhas.append(f"rotulo com valores inesperados: {valores_rotulo}")
        log(f"  [FALHA] Rotulo com valores inesperados: {sorted(valores_rotulo)}")

    # ---------------------------------------------------------------
    # Passo 5 — resumo por projeto
    # ---------------------------------------------------------------
    log("\n--- Distribuicao por projeto ---")
    log(f"  {'projeto':<8} {'n':>7} {'defeituosos':>12} {'taxa':>8}  rotulo no arquivo")
    resumo: list[dict] = []
    for projeto, grupo in base.groupby("project", sort=True):
        n = len(grupo)
        d = int(grupo["defective"].sum())
        taxa = d / n
        resumo.append({
            "projeto": projeto,
            "n_observacoes": n,
            "n_defeituosos": d,
            "n_nao_defeituosos": n - d,
            "taxa_defeito": round(taxa, 4),
            "nome_rotulo_no_arquivo": nomes_rotulo[projeto],
        })
        log(f"  {projeto:<8} {n:>7} {d:>12} {taxa:>8.2%}  {nomes_rotulo[projeto]}")

    n_total = len(base)
    d_total = int(base["defective"].sum())
    log(f"  {'TOTAL':<8} {n_total:>7} {d_total:>12} {d_total / n_total:>8.2%}")

    # ---------------------------------------------------------------
    # Passo 6 — gravacao
    # ---------------------------------------------------------------
    colunas = ["project", "source_file", "source_row"] + metricas_comuns + ["defective", "rotulo_original"]
    base[colunas].to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8")
    pd.DataFrame(resumo).to_csv(DIR_TABELAS / "02_consolidacao_resumo.csv", index=False, encoding="utf-8")
    pd.DataFrame(descartadas or [{"metrica": "(nenhuma)", "n_projetos_com": "", "ausente_em": ""}]).to_csv(
        DIR_TABELAS / "02_metricas_descartadas.csv", index=False, encoding="utf-8")

    log("\n--- Arquivos gerados ---")
    for caminho in (ARQUIVO_SAIDA,
                    DIR_TABELAS / "02_consolidacao_resumo.csv",
                    DIR_TABELAS / "02_metricas_descartadas.csv"):
        log(f"  {caminho.relative_to(RAIZ)}")

    log("\n" + "=" * 78)
    if falhas:
        log("RESULTADO: CONSOLIDACAO CONCLUIDA COM FALHAS DE VERIFICACAO")
        for f in falhas:
            log(f"  - {f}")
    else:
        log("RESULTADO: CONSOLIDACAO CONCLUIDA, TODAS AS VERIFICACOES PASSARAM")
    log("=" * 78)

    CAMINHO_LOG.write_text("\n".join(_log) + "\n", encoding="utf-8")
    print(f"\nLog gravado em: {CAMINHO_LOG.relative_to(RAIZ)}")

    if falhas:
        sys.exit(1)


if __name__ == "__main__":
    main()
