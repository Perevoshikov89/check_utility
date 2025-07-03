from pathlib import Path
import zipfile


def extract_zip_response(zip_bytes: bytes, output_dir: Path) -> Path:
    zip_path = output_dir / "response.zip"
    zip_path.write_bytes(zip_bytes)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)
        for name in z.namelist():
            if name.endswith(".xml"):
                return output_dir / name
    return None
