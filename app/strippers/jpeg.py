import io

from PIL import Image, ImageOps


class JpegStripper:
    def inspect(self, data: bytes) -> dict:
        #  Читает файл и проверяет наличие EXIF-данных без их удаления
        with Image.open(io.BytesIO(data)) as img:
            exif = img.getexif()
            if not exif:
                return {"has_metadata": False, "tags_count": 0}

            return {"has_metadata": True, "tags_count": len(exif)}


    def strip(self, data: bytes) -> bytes:
        #  Удаляет метаданные путем полного ре-энкодинга пикселей
        with Image.open(io.BytesIO(data)) as img:
            img = ImageOps.exif_transpose(img)
            clean_img = Image.new(img.mode, img.size)
            clean_img.paste(img)
            output = io.BytesIO()
            clean_img.save(output, format="JPEG", quality=95)

            return output.getvalue()
