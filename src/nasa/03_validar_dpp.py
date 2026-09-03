"""
03_validar_dpp.py — Validacao dos arquivos D'' contra o algoritmo publicado
===========================================================================

PROBLEMA QUE RESOLVE
--------------------
A decisao metodologica deste trabalho e usar a versao D'' publicada pelos
autores em vez de reproduzir a limpeza a partir dos dados brutos (justificativa
em docs/registro_de_decisoes.md, secao 2). Essa decisao so e defensavel se os
arquivos D'' forem, de fato, o que dizem ser.

Este script faz essa verificacao da unica forma rigorosa possivel com os
arquivos disponiveis: aplica ao conjunto D' os passos do algoritmo publicado que
distinguem D' de D'' -- remocao de casos identicos e de casos inconsistentes --
e compara o resultado com o D'' distribuido.

ENTRADA
-------
  data/raw/nasa_dp_reference/*.arff    versao D'  (somente leitura)
  data/raw/nasa_dpp_reference/*.arff   versao D'' (somente leitura)

SAIDA
-----
  outputs/tables/03_validacao_dpp.csv
  outputs/logs/03_validar_dpp.log

O ALGORITMO, CONFORME PUBLICADO
--------------------------------
`[LITERATURA]` Shepperd, Song, Sun e Mair (2013), procedimento "NASA MDP Data
Preprocessing Approach". Os passos 3 e 4 do pseudocodigo sao os unicos aplicados
condicionalmente ao parametro Flag, e sao portanto exatamente o que separa D' de
D'':

  passo 3 (linhas 12-15) -- remover casos identicos:
      for i = 1 to M-1:  for k = i+1 to M:
          if DS.Value[i][1...N] == DS.Value[k][1...N]:
              DS = DS - DS.Value[k]
  Observe que apenas a ocorrencia POSTERIOR (k) e removida: a primeira e
  preservada.

  passo 4 (linhas 16-20) -- remover casos inconsistentes:
      for i = 1 to M-1:  for k = i+1 to M:
          if DS.Value[i][1...N-1] == DS.Value[k][1...N-1]
             and DS.Value[i][N] != DS.Value[k][N]:
              DS = DS - DS.Value[i]
              DS = DS - DS.Value[k]
  Aqui AMBAS as linhas sao removidas.

`[LITERATURA]` Os autores afirmam explicitamente que a ordem dos passos 3 e 4
nao pode ser trocada: "Note that, the pre-processing order of these two
situations cannot be swapped, otherwise some inconsistent cases may not be
removed."

DUAS INTERPRETACOES TESTADAS
-----------------------------
Como o resultado sob a leitura literal do pseudocodigo nao reproduziu os
arquivos publicados, o script testa tambem uma interpretacao alternativa:

  (A) "remover ambos"  -- leitura literal das linhas 19-20.
  (B) "preservar um"   -- de cada grupo de casos com atributos identicos,
                          preserva-se uma unica linha.

A comparacao entre as duas nao e um ajuste para fazer os numeros baterem: e o
proprio objeto da validacao. Qual delas reproduz os arquivos distribuidos e um
fato verificavel sobre esses arquivos, e a resposta e registrada como achado.

COMO VERIFICAMOS SE O RESULTADO ESTA CORRETO
---------------------------------------------
  1. Comparacao de contagem de linhas por conjunto.
  2. Comparacao do MULTICONJUNTO de vetores de atributos (todas as colunas
     exceto o rotulo). Esta e a comparacao decisiva: se ela bate, o conjunto de
     modulos preservados e exatamente o mesmo.
  3. Comparacao do conteudo completo, incluindo o rotulo. Divergencia aqui, com
     o item 2 batendo, isola o residuo a escolha de qual rotulo foi preservado
     nos grupos inconsistentes.
"""

import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parents[2]
DIR_D1 = RAIZ / "data" / "raw" / "nasa_dp_reference"
DIR_D2 = RAIZ / "data" / "raw" / "nasa_dpp_reference"
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
for d in (DIR_TABELAS, DIR_LOGS):
    d.mkdir(parents=True, exist_ok=True)

_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def ler_arff(caminho: Path) -> list[tuple[str, ...]]:
    """Devolve as linhas de dados como tuplas de campos, sem conversao de tipo."""
    texto = caminho.read_bytes().decode("utf-8", errors="replace")
    linhas, em_dados = [], False
    for linha in texto.splitlines():
        despida = linha.strip()
        if em_dados:
            if despida and not despida.startswith("%"):
                linhas.append(tuple(c.strip() for c in despida.split(",")))
        elif despida.lower().startswith("@data"):
            em_dados = True
    return linhas


def passo3_remover_identicos(linhas):
    """Remove casos identicos em todos os atributos, preservando a primeira
    ocorrencia -- exatamente como o pseudocodigo, que remove DS.Value[k]."""
    vistos, saida = set(), []
    for r in linhas:
        if r not in vistos:
            vistos.add(r)
            saida.append(r)
    return saida


def passo4_interpretacao_A(linhas):
    """Leitura literal: remove TODAS as linhas envolvidas em conflito de rotulo."""
    rotulos = defaultdict(set)
    for r in linhas:
        rotulos[r[:-1]].add(r[-1])
    conflitantes = {atrib for atrib, rs in rotulos.items() if len(rs) > 1}
    return [r for r in linhas if r[:-1] not in conflitantes]


def passo4_interpretacao_B(linhas):
    """Alternativa: preserva uma unica linha por vetor de atributos."""
    vistos, saida = set(), []
    for r in linhas:
        if r[:-1] not in vistos:
            vistos.add(r[:-1])
            saida.append(r)
    return saida


def main() -> None:
    log("=" * 78)
    log("VALIDACAO DOS ARQUIVOS D'' CONTRA O ALGORITMO PUBLICADO")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    if not DIR_D1.exists() or not any(DIR_D1.glob("*.arff")):
        log(f"\n[ABORTADO] Versao D' nao encontrada em {DIR_D1}")
        log("Sem os arquivos D' esta validacao nao pode ser feita.")
        (DIR_LOGS / "03_validar_dpp.log").write_text("\n".join(_log) + "\n", encoding="utf-8")
        sys.exit(1)

    conjuntos = sorted(p.stem.upper() for p in DIR_D2.glob("*.arff"))
    registros = []

    log(f"\n  {'base':<6} {'D1':>7} {'D2':>7} | {'A:ambos':>8} {'B:um so':>8} | "
        f"{'atributos':>10} {'conteudo':>9} {'rot.dif':>8}")
    log("  " + "-" * 76)

    total_dif_rotulo = 0
    for nome in conjuntos:
        c1, c2 = DIR_D1 / f"{nome}.arff", DIR_D2 / f"{nome}.arff"
        if not c1.exists():
            log(f"  {nome:<6} [sem contraparte D']")
            continue

        d1, d2 = ler_arff(c1), ler_arff(c2)
        if not d1 and not d2:
            log(f"  {nome:<6} {0:>7} {0:>7} | {'-':>8} {'-':>8} | (arquivo vazio nas duas versoes)")
            registros.append({"conjunto": nome, "n_D1": 0, "n_D2": 0, "observacao": "vazio"})
            continue

        base3 = passo3_remover_identicos(d1)
        a = passo4_interpretacao_A(base3)
        b = passo4_interpretacao_B(base3)

        # Comparacao decisiva: multiconjunto de vetores de atributos, sem rotulo
        atributos_iguais = Counter(r[:-1] for r in b) == Counter(r[:-1] for r in d2)
        conteudo_igual_A = sorted(a) == sorted(d2)
        conteudo_igual_B = sorted(b) == sorted(d2)

        # Residuo: entre as linhas com os mesmos atributos, quantas divergem no rotulo
        rotulo_b = {r[:-1]: r[-1] for r in b}
        difs = sum(1 for r in d2 if r[:-1] in rotulo_b and rotulo_b[r[:-1]] != r[-1])
        total_dif_rotulo += difs

        log(f"  {nome:<6} {len(d1):>7} {len(d2):>7} | {len(a):>8} {len(b):>8} | "
            f"{str(atributos_iguais):>10} {str(conteudo_igual_B):>9} {difs:>8}")

        registros.append({
            "conjunto": nome,
            "n_D1": len(d1), "n_D2_publicado": len(d2),
            "n_apos_passo3": len(base3),
            "n_interpretacao_A_remover_ambos": len(a),
            "n_interpretacao_B_preservar_um": len(b),
            "contagem_bate_A": len(a) == len(d2),
            "contagem_bate_B": len(b) == len(d2),
            "multiconjunto_de_atributos_identico_B": atributos_iguais,
            "conteudo_completo_identico_A": conteudo_igual_A,
            "conteudo_completo_identico_B": conteudo_igual_B,
            "n_linhas_com_rotulo_divergente": difs,
        })

    df = pd.DataFrame(registros)
    validos = df[df.get("observacao", pd.Series(dtype=object)).isna()] if "observacao" in df else df

    log("\n" + "=" * 78)
    log("SINTESE")
    log("=" * 78)
    n = len(validos)
    log(f"  Conjuntos avaliados                                      : {n}")
    log(f"  Contagem reproduzida pela interpretacao A (remover ambos): "
        f"{int(validos['contagem_bate_A'].sum())}/{n}")
    log(f"  Contagem reproduzida pela interpretacao B (preservar um) : "
        f"{int(validos['contagem_bate_B'].sum())}/{n}")
    log(f"  Multiconjunto de atributos reproduzido (interpretacao B) : "
        f"{int(validos['multiconjunto_de_atributos_identico_B'].sum())}/{n}")
    log(f"  Conteudo completo reproduzido (interpretacao B)          : "
        f"{int(validos['conteudo_completo_identico_B'].sum())}/{n}")
    total_d2 = int(validos["n_D2_publicado"].sum())
    log(f"\n  Linhas com rotulo divergente: {total_dif_rotulo} de {total_d2} "
        f"({total_dif_rotulo / total_d2:.4%})")

    log("\n  LEITURA DO RESULTADO")
    log("  Se o multiconjunto de atributos e reproduzido em todos os conjuntos,")
    log("  entao os MODULOS preservados no D'' publicado sao exatamente os que o")
    log("  algoritmo seleciona, e o unico residuo esta em qual rotulo foi mantido")
    log("  nos grupos que tinham rotulos conflitantes -- ponto em que o")
    log("  pseudocodigo publicado e a distribuicao efetiva divergem.")

    df.to_csv(DIR_TABELAS / "03_validacao_dpp.csv", index=False, encoding="utf-8")
    log(f"\n  -> outputs/tables/03_validacao_dpp.csv")
    (DIR_LOGS / "03_validar_dpp.log").write_text("\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
