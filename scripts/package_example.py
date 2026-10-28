"""Empacota somente fontes e instruções do laboratório executável."""
from pathlib import Path
import zipfile
root = Path(__file__).resolve().parent.parent
source = root / "examples" / "mvc-python"
with zipfile.ZipFile(root / "examples" / "mvc-python.zip", "w", zipfile.ZIP_DEFLATED) as bundle:
    for file in sorted(source.rglob("*")):
        if file.is_file() and "__pycache__" not in file.parts and file.suffix in (".py", ".md"):
            bundle.write(file, "mvc-python/" + file.relative_to(source).as_posix())
