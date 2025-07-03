import requests
from pathlib import Path


def send_signed_xml(sig_path: Path, url: str, output_dir: Path) -> bytes:
    log_path = output_dir / "request_log.txt"
    with open(sig_path, "rb") as f:
        data = f.read()

    headers = {
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(url, data=data, headers=headers)

    with open(log_path, "w", encoding="utf-8") as log:
        log.write(f"URL: {url}\nStatus: {response.status_code}\n\n")
        log.write(response.text)

    if response.status_code != 200:
        raise RuntimeError("Ошибка HTTP-запроса, см. request_log.txt")

    return response.content
