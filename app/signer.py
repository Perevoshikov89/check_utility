from pathlib import Path
import subprocess
import win32api


def get_short_path(path: Path) -> str:
    """Преобразует путь в короткий (8.3), если файл существует."""
    if not path.exists():
        # Создаём файл-пустышку, если его ещё нет (только для .sig)
        if path.suffix == ".sig":
            path.touch()
        else:
            raise FileNotFoundError(f"Файл не найден: {path}")
    return win32api.GetShortPathName(str(path))


def sign_xml_file(xml_path: Path, output_dir: Path) -> Path:
    cryptcp_path = Path(r"C:\Program Files (x86)\Crypto Pro\CSP\cryptcp.exe")
    thumbprint = "A7C66ED56957C6912A5D54349D206E4F946524F1"

    if not xml_path.exists():
        raise FileNotFoundError(f"XML-файл не найден: {xml_path}")
    if not output_dir.exists():
        raise FileNotFoundError(f"Папка не найдена: {output_dir}")
    if not cryptcp_path.exists():
        raise FileNotFoundError("Не найден cryptcp.exe. Убедитесь, что установлен CryptoPro.")

    output_file = output_dir / (xml_path.stem + ".sig")
    output_file.touch(exist_ok=True)  # Создаём заранее, чтобы получить short path

    command = [
        get_short_path(cryptcp_path),
        "-sign",
        "-der",
        "-thumbprint", thumbprint,
        "-in", get_short_path(xml_path),
        "-out", get_short_path(output_file)
    ]

    print("🧪 Команда для выполнения:")
    print(" ".join(f'"{x}"' for x in command))

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("=== STDOUT ===")
        print(result.stdout)
        print("=== STDERR ===")
        print(result.stderr)
        raise RuntimeError(f"Ошибка подписи файла (код {result.returncode})")

    return output_file
