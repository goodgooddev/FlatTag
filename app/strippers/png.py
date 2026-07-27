import io
from PIL import Image


class PngStripper:
    def inspect(self, data: bytes) -> dict:
        #  Читает файл и проверяет наличие EXIF-данных без их удаления
        with Image.open(io.BytesIO(data)) as img:
            info = img.info
            if not info:
                return {"has_metadata": False, "tags_count": 0}

            return {"has_metadata": True, "tags_count": len(info)}


    def strip(self, data: bytes) -> bytes:
        #  Удаляет метаданные путем полного ре-энкодинга пикселей
        with Image.open(io.BytesIO(data)) as img:
            raw_pixels = list(img.getdata())
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(raw_pixels)
            output = io.BytesIO()
            clean_img.save(output, format="PNG")

            return output.getvalue()