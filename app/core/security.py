from fastapi import HTTPException


MAGIC_BYTES = {
    b"\xFF\xD8\xFF": "image/jpeg",
    b"\x89PNG\r\n\x1a\n": "image/png",
}


def validate_file_signature(file_bytes: bytes) -> str:
    """
    Проверяет реальный формат файла по его содержимому, игнорируя расширение.
    Возвращает настоящий MIME-тип или выбрасывает ошибку.
    """
    for signature, mime_type in MAGIC_BYTES.items():
        if file_bytes.startswith(signature):
            return mime_type

    raise HTTPException(
        status_code=400,
        detail="Недопустимый тип файла. Файл не является подлинным изображением JPEG или PNG."
    )