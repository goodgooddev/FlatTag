from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import Response
from pydantic import BaseModel
from PIL import UnidentifiedImageError
from PIL.Image import DecompressionBombError

from app.strippers.jpeg import JpegStripper
from app.strippers.png import PngStripper
from app.core.security import validate_file_signature
from app.core.config import MAX_FILE_SIZE


app = FastAPI(title="FlatTag API", description="API для удаления EXIF и других метаданных из изображений", version="1.0.0",)


class InspectResponse(BaseModel):
    filename: str
    has_metadata: bool
    tags_count: int
    file_type: str


def get_stripper(content_type: str):
    #  Для выбора правильного обработчика
    if content_type in ["image/jpg", "image/jpeg"]:
        return JpegStripper()
    elif content_type == "image/png":
        return PngStripper()
    else:
        raise HTTPException(status_code=400, detail="Формат не поддерживается. Только JPEG и PNG.")


async def read_limited(file: UploadFile, max_size: int = MAX_FILE_SIZE) -> bytes:
    #  Читаем файл по частям и обрываемся раньше времени, если он больше лимита, так лимит соблюдается независимо от того, можно ли доверять Content-Length
    chunks = []
    total = 0
    while chunk := await file.read(1024 * 1024):
        total += len(chunk)
        if total > max_size:
            raise HTTPException(status_code=413, detail=f"Файл превышает максимальный размер ({max_size // (1024 * 1024)} МБ).",)
        chunks.append(chunk)
    return b"".join(chunks)


async def run_stripper(func, data: bytes):
    #  Оборачиваем вызов Pillow-логики: битые/аномальные файлы дают понятную 400, а не голый 500
    try:
        return await run_in_threadpool(func, data)
    except DecompressionBombError:
        raise HTTPException(status_code=400, detail="Изображение слишком велико для обработки.")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Файл повреждён или не может быть обработан как изображение.",)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "message": "Сервис работает!"}


@app.post("/inspect", response_model=InspectResponse, tags=["Analysis"])
async def inspect_file(file: UploadFile = File(...)):
    #  Показывает, какие метаданные есть в файле, ничего не удаляя
    file_bytes = await read_limited(file)
    real_content_type = validate_file_signature(file_bytes)
    stripper = get_stripper(real_content_type)

    result = await run_stripper(stripper.inspect, file_bytes)

    return InspectResponse(
        filename=file.filename,
        has_metadata=result["has_metadata"],
        tags_count=result["tags_count"],
        file_type=real_content_type,
    )


@app.post(
    "/clean",
    tags=["Processing"],
    response_class=Response,  # Указываем, что эндпоинт возвращает бинарные данные
    responses={
        200: {
            "content": {
                "image/jpeg": {},
                "image/png": {},
            },
            "description": "Очищенное изображение без метаданных",
        }
    },
)
async def clean_file(file: UploadFile = File(...)):
    #  Принимает файл, определяет формат, удаляет метаданные и возвращает очищенную версию
    file_bytes = await read_limited(file)
    real_content_type = validate_file_signature(file_bytes)
    stripper = get_stripper(real_content_type)
    clean_bytes = await run_stripper(stripper.strip, file_bytes)

    return Response(content=clean_bytes, media_type=real_content_type)