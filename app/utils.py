from pathlib import Path
import shutil


def find_cryptcp_exe() -> Path:
    """
    Поиск исполняемого файла cryptcp.exe в типичных путях или в системной переменной PATH.
    
    :return: Полный путь к cryptcp.exe
    :raises FileNotFoundError: если файл не найден
    """
    # Возможные стандартные пути установки
    possible_paths = [
        Path("C:/Program Files/Crypto Pro/CSP/cryptcp.exe"),
        Path("C:/Program Files (x86)/Crypto Pro/CSP/cryptcp.exe")
    ]

    for path in possible_paths:
        if path.exists():
            return path

    # Проверка в переменной PATH
    cryptcp_in_path = shutil.which("cryptcp")
    if cryptcp_in_path:
        return Path(cryptcp_in_path)

    raise FileNotFoundError("Файл cryptcp.exe не найден. Проверьте установку КриптоПро CSP.")
