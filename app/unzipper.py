import zipfile
import io
from pathlib import Path
from typing import Optional


def extract_zip_response(zip_bytes: bytes, output_dir: Path) -> Optional[Path]:
    """
    Распаковывает ZIP-ответ из байтов и сохраняет содержимое в выходную папку.

    :param zip_bytes: Содержимое архива в байтах
    :param output_dir: Путь к папке для распаковки
    :return: Путь к первому извлечённому XML-файлу (или None)
    :raises RuntimeError: если архив пустой или повреждён
    """
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        if not archive.namelist():
            raise RuntimeError("Пустой архив")

        archive.extractall(output_dir)

        # Ищем первый XML-файл
        for name in archive.namelist():
            if name.lower().endswith(".xml"):
                return output_dir / name

    return None
