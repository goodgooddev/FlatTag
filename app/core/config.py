import os

from dotenv import load_dotenv

load_dotenv()  # подхватывает переменные из .env, если он есть


def _get_int_env(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError:
        raise RuntimeError(
            f"Переменная окружения {name} должна быть целым числом, получено: {raw_value!r}"
        )


MAX_FILE_SIZE_MB = _get_int_env("MAX_FILE_SIZE_MB", default=20)
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024