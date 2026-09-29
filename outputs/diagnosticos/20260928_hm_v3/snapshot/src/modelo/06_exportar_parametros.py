"""
06_exportar_parametros.py — Exporta os parâmetros para tabelas consumíveis
============================================================================

`[DEC]` O documento de entrega passou a ler os valores de parâmetro DESTAS
tabelas, e não de números digitados no gerador. A motivação é um defeito real:
a Tabela de matriz de cenários da primeira versão da entrega trazia valores
FABRICADOS — três das quatro linhas divergiam do arquivo de configuração e uma
delas com o sentido invertido entre os braços. Nenhuma revisão de texto poderia
ter detectado isso, porque o documento era internamente coerente.

A regra que passa a valer: nenhum valor de parâmetro é digitado em texto. Todo
valor exibido no documento vem deste arquivo, que por sua vez vem do YAML.

ENTRADA : config/parametros.yaml, config/parametros_derivados.yaml
SAIDA   : outputs/tables/parametros_cenarios.csv
          outputs/tables/parametros_procedencia.csv
          outputs/tables/parametros_orfaos.csv
          outputs/tables/parametros_ambiguos.csv
"""

import sys
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[2]
TAB = RAIZ / "outputs" / "tables"

# Rótulos de exibição e ordem das linhas da matriz de cenários.
ROTULOS = {
    "tau_inicial": ("τ_inicial", "confiança inicial na rede de pares"),
    "tau_min": ("τ_mín", "limiar de confiança para conceder ajuda"),
    "p_reporte": ("p_reporte", "probabilidade de reportar defeito em vez de ocultá-lo"),
    "p_deteccao": ("p_detecção", "probabilidade de a dívida oculta aflorar por período"),
}


def valor(no):
    return no["valor"] if isinstance(no, dict) and "valor" in no else no


def main() -> None:
    par = yaml.safe_load((RAIZ / "config" / "parametros.yaml").read_text(encoding="utf-8"))
    der = yaml.safe_load((RAIZ / "config" / "parametros_derivados.yaml").read_text(encoding="utf-8"))

    # ---- matriz de cenários -------------------------------------------------
    cen = par["cenarios"]
    linhas = []
    for chave, (rot, interp) in ROTULOS.items():
        c, a = valor(cen["centralizada"][chave]), valor(cen["adaptativa"][chave])
        linhas.append({
            "chave": chave, "rotulo": rot,
            "centralizada": c, "adaptativa": a,
            "difere": c != a,
            "interpretacao": interp,
        })
    d = pd.DataFrame(linhas)
    d.to_csv(TAB / "parametros_cenarios.csv", index=False, encoding="utf-8")

    n_dif = int(d["difere"].sum())
    print("MATRIZ DE CENARIOS")
    print(d[["rotulo", "centralizada", "adaptativa", "difere"]].to_string(index=False))
    print(f"\n  parametros que DIFEREM entre os bracos: {n_dif} de {len(d)}")
    if n_dif > 1:
        print(f"  [ATENCAO] o experimento varia {n_dif} parametros ao mesmo tempo.")
        print("  Nenhum efeito pode ser atribuido a um mecanismo isolado sem ablacao.")

    # ---- procedência --------------------------------------------------------
    contagem, orfaos = {}, []

    def anda(no, caminho=""):
        if isinstance(no, dict):
            if "condicao" in no and not isinstance(no.get("condicao"), dict):
                contagem[no["condicao"]] = contagem.get(no["condicao"], 0) + 1
            else:
                for k, v in no.items():
                    anda(v, f"{caminho}.{k}" if caminho else k)

    anda(par)
    for k, v in der.items():
        if isinstance(v, dict) and "valor" in v:
            contagem["derivado"] = contagem.get("derivado", 0) + 1

    pd.DataFrame(sorted(contagem.items()), columns=["condicao", "quantidade"]).to_csv(
        TAB / "parametros_procedencia.csv", index=False, encoding="utf-8")
    print("\nPROCEDENCIA:", dict(sorted(contagem.items())))

    # ---- parâmetros órfãos --------------------------------------------------
    # `[DEC]` Um parâmetro declarado no YAML e nunca lido pelo código é pior que
    # inútil: induz o leitor a acreditar que governa algo. Varre-se o código
    # atrás de cada chave declarada.
    fontes = "\n".join(
        p.read_text(encoding="utf-8", errors="replace")
        for p in (RAIZ / "src").rglob("*.py"))
    caminhos_por_folha: dict[str, set] = {}

    def coleta(no, caminho=""):
        if isinstance(no, dict):
            if "condicao" in no and not isinstance(no.get("condicao"), dict):
                folha = caminho.split(".")[-1]
                caminhos_por_folha.setdefault(folha, set()).add(caminho)
            else:
                for k, v in no.items():
                    coleta(v, f"{caminho}.{k}" if caminho else k)

    coleta(par)
    for k in sorted(caminhos_por_folha):
        if f'"{k}"' not in fontes and f"'{k}'" not in fontes:
            orfaos.append(k)

    # `[DEC]` Nome de folha declarado em MAIS DE UMA seção é armadilha: a busca
    # textual encontra o nome e conclui que o parâmetro é lido, quando quem é
    # lido pode ser o homônimo de outra seção. Foi exatamente o caso de
    # `retrabalho.p_deteccao`, que nunca é lido — o simulador usa o
    # `p_deteccao` do cenário. Estes casos exigem conferência manual.
    ambiguos = {k: v for k, v in caminhos_por_folha.items() if len(v) > 1}
    pd.DataFrame([{"folha": k, "caminhos": " | ".join(sorted(v))}
                  for k, v in sorted(ambiguos.items())]).to_csv(
        TAB / "parametros_ambiguos.csv", index=False, encoding="utf-8")
    if ambiguos:
        print(f"\nNOMES DECLARADOS EM MAIS DE UMA SECAO (conferir manualmente): "
              f"{len(ambiguos)}")
        for k, v in sorted(ambiguos.items()):
            print(f"  - {k}: {', '.join(sorted(v))}")
    pd.DataFrame({"chave": orfaos}).to_csv(
        TAB / "parametros_orfaos.csv", index=False, encoding="utf-8")
    print(f"\nPARAMETROS DECLARADOS E NUNCA LIDOS PELO CODIGO: {len(orfaos)}")
    for k in orfaos:
        print(f"  - {k}")

    print("\n--- Arquivos gerados ---")
    for f in ("parametros_cenarios.csv", "parametros_procedencia.csv",
              "parametros_orfaos.csv", "parametros_ambiguos.csv"):
        print(f"  outputs/tables/{f}")


if __name__ == "__main__":
    main()
