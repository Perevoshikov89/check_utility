import requests
from pathlib import Path


def send_signed_xml(signed_path: Path, url: str) -> bytes:
    """
    Отправляет подписанный XML-файл на сервер и возвращает содержимое ответа (ZIP).

    :param signed_path: Путь к подписанному XML-файлу
    :param url: Адрес сервера
    :return: Байты ZIP-файла
    :raises RuntimeError: при неудачном ответе от сервера
    """
    headers = {
        "Content-Type": "application/xml"  # или "text/xml", в зависимости от API
    }

    with open(signed_path, "rb") as file:
        response = requests.post(url, headers=headers, data=file.read(), timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"Ошибка при отправке запроса: {response.status_code} — {response.text}")

    return response.content
