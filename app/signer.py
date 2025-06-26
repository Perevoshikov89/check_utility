import subprocess
from pathlib import Path
from app.utils import find_cryptcp_exe


def sign_xml_file(xml_path: Path, output_dir: Path) -> Path:
    """
    Подписывает XML-файл с помощью КриптоПро и сохраняет результат.

    :param xml_path: Путь к исходному XML-файлу
    :param output_dir: Папка, куда сохранить подписанный файл
    :return: Путь к подписанному файлу
    :raises RuntimeError: если подписание не удалось
    """
    cryptcp = find_cryptcp_exe()

    signed_file = output_dir / f"{xml_path.stem}.signed.xml"

    command = [
        str(cryptcp),
        "-signf",
        "-dn", "",  # Если нужна конкретная подпись — здесь укажем
        "-detached",  # Отключаем вложенную подпись, если нужно отдельно
        "-dir", str(output_dir),
        str(xml_path)
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Ошибка при подписании: {result.stderr}")

    if not signed_file.exists():
        raise FileNotFoundError(f"Подписанный файл не найден: {signed_file}")

    return signed_file
