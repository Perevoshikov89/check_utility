import subprocess
from pathlib import Path
from app.utils import find_cryptcp_exe


def remove_signature(xml_path: Path, output_dir: Path) -> Path:
    """
    Снимает ЭЦП с XML-файла с помощью КриптоПро и сохраняет чистый результат.

    :param xml_path: Путь к XML-файлу с ЭЦП
    :param output_dir: Папка, куда сохранить результат
    :return: Путь к новому XML-файлу без ЭЦП
    :raises RuntimeError: если верификация не прошла
    """
    cryptcp = find_cryptcp_exe()

    clean_path = output_dir / f"{xml_path.stem}.clean.xml"

    command = [
        str(cryptcp),
        "-verify",
        "-dir", str(output_dir),
        str(xml_path)
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Ошибка при снятии подписи: {result.stderr}")

    if not clean_path.exists():
        raise FileNotFoundError(f"Файл без подписи не найден: {clean_path}")

    return clean_path
