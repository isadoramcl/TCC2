#!/usr/bin/env python3
"""Confere, sem editar, o snapshot fixado e uma cópia viva do DOCX oficial."""

import argparse
import hashlib
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
SNAPSHOT = RAIZ / "docs" / "snapshots" / "analise_preliminar_oficial_2026-09-15.docx"
HASH_FIXADO = "d5a658f1cdf03d99e6bdc0b5d03cb4aaa9420853ec7ebc2bb3f55e85a728c57d"


def sha256(caminho: Path) -> str:
    digest = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def erro(mensagem: str) -> int:
    print(f"ERRO: {mensagem}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Confere o snapshot versionado e um documento oficial vivo contra o hash fixado."
    )
    parser.add_argument("--vivo", required=True, type=Path, help="caminho da cópia viva do DOCX oficial")
    args = parser.parse_args()

    if not SNAPSHOT.is_file():
        return erro(f"snapshot ausente: {SNAPSHOT}")
    hash_snapshot = sha256(SNAPSHOT)
    if hash_snapshot != HASH_FIXADO:
        return erro(
            f"snapshot diverge do hash fixado: {SNAPSHOT}\n"
            f"esperado: {HASH_FIXADO}\nobtido:   {hash_snapshot}"
        )

    vivo = args.vivo.expanduser().resolve()
    if not vivo.is_file():
        return erro(f"documento vivo ausente: {vivo}")
    hash_vivo = sha256(vivo)
    if hash_vivo != HASH_FIXADO:
        return erro(
            f"documento vivo diverge do snapshot fixado: {vivo}\n"
            f"esperado: {HASH_FIXADO}\nobtido:   {hash_vivo}"
        )

    print(f"OK: snapshot e documento vivo conferem ({HASH_FIXADO})")
    print(f"snapshot: {SNAPSHOT}")
    print(f"vivo:     {vivo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
