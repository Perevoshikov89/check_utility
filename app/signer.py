from pathlib import Path
import subprocess
import win32crypt
import win32api


def get_short_path(path: Path) -> str:
    """
    Преобразует путь в короткий (8.3), если файл существует.
    """
    if not path.exists():
        if path.suffix == ".sig":
            path.touch()
        else:
            raise FileNotFoundError(f"Файл не найден: {path}")
    return win32api.GetShortPathName(str(path))


def find_cryptcp_exe() -> Path:
    """
    Поиск cryptcp.exe в стандартных местах.
    """
    candidates = [
        Path(r"C:\Program Files (x86)\Crypto Pro\CSP\cryptcp.exe"),
        Path(r"C:\Program Files\Crypto Pro\CSP\cryptcp.exe")
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("Не найден cryptcp.exe. Убедитесь, что установлен CryptoPro CSP.")


def list_certificates() -> list[tuple[str, str]]:
    """
    Возвращает список (thumbprint, subject) сертификатов с закрытым ключом из CurrentUser\My.
    """
    result = []
    store = win32crypt.CertOpenSystemStore(None, "MY")
    cert_ctx = win32crypt.CertEnumCertificatesInStore(store, None)

    while cert_ctx:
        info = win32crypt.CertGetCertificateContextProperty(cert_ctx, win32crypt.CERT_KEY_PROV_INFO_PROP_ID)
        if info:
            thumb = win32crypt.CertGetCertificateContextProperty(cert_ctx, win32crypt.CERT_HASH_PROP_ID).hex().upper()
            subject = cert_ctx.GetSubject()
            result.append((thumb, subject))
        cert_ctx = win32crypt.CertEnumCertificatesInStore(store, cert_ctx)

    return result


def sign_xml_file(xml_path: Path, output_dir: Path, thumbprint: str) -> Path:
    """
    Подписывает XML-файл через CryptoPro с использованием заданного thumbprint.
    Лог сохраняется в sign_log.txt.
    """
    log_path = output_dir / "sign_log.txt"

    if not xml_path.exists():
        raise FileNotFoundError(f"XML-файл не найден: {xml_path}")
    if not output_dir.exists():
        raise FileNotFoundError(f"Папка не найдена: {output_dir}")

    cryptcp = find_cryptcp_exe()
    output_file = output_dir / (xml_path.stem + ".sig")
    output_file.touch(exist_ok=True)

    command = [
        get_short_path(cryptcp),
        "-sign",
        "-der",
        "-thumbprint", thumbprint,
        "-in", get_short_path(xml_path),
        "-out", get_short_path(output_file)
    ]

    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"Сертификат с отпечатком: {thumbprint}\n")
        log.write("Команда:\n" + " ".join(command) + "\n\n")

        result = subprocess.run(command, capture_output=True, text=True)

        log.write("=== STDOUT ===\n" + result.stdout + "\n")
        log.write("=== STDERR ===\n" + result.stderr + "\n")

        if result.returncode != 0:
            raise RuntimeError("Ошибка подписи, см. sign_log.txt")

    return output_file
