import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / "research" / "verificar_documento_oficial.py"
SNAPSHOT = RAIZ / "docs" / "snapshots" / "analise_preliminar_oficial_2026-09-15.docx"


class VerificadorDocumentoOficialTest(unittest.TestCase):
    def executar(self, caminho: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--vivo", str(caminho)],
            cwd=RAIZ,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_aceita_copia_viva_identica_ao_snapshot_fixado(self):
        with tempfile.TemporaryDirectory() as pasta:
            vivo = Path(pasta) / "documento_vivo.docx"
            vivo.write_bytes(SNAPSHOT.read_bytes())

            resultado = self.executar(vivo)

            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertIn(hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest(), resultado.stdout)
            self.assertIn("snapshot e documento vivo conferem", resultado.stdout.lower())

    def test_rejeita_documento_vivo_divergente(self):
        with tempfile.TemporaryDirectory() as pasta:
            vivo = Path(pasta) / "documento_vivo.docx"
            vivo.write_bytes(SNAPSHOT.read_bytes() + b"divergencia-controlada")

            resultado = self.executar(vivo)

            self.assertNotEqual(resultado.returncode, 0)
            self.assertIn("documento vivo diverge", resultado.stderr.lower())
            self.assertIn(str(vivo), resultado.stderr)

    def test_rejeita_caminho_vivo_ausente(self):
        with tempfile.TemporaryDirectory() as pasta:
            vivo = Path(pasta) / "ausente.docx"

            resultado = self.executar(vivo)

            self.assertNotEqual(resultado.returncode, 0)
            self.assertIn("documento vivo ausente", resultado.stderr.lower())
            self.assertIn(str(vivo), resultado.stderr)


if __name__ == "__main__":
    unittest.main()
