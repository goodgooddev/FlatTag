from typing import Protocol


class MetadataStripper(Protocol):
    def inspect(self, data: bytes) -> dict:
        #  Анализирует файл и возвращает информацию о метаданных
        ...

    def strip(self, data: bytes) -> bytes:
        #  Возвращает очищенные байты файла
        ...
