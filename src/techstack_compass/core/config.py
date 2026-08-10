from __future__ import annotations

import os
from typing import Final

import dotenv


def get_adzuna_credentials() -> tuple[str, str]:
    """Load Adzuna credentials from the environment or a discovered .env file."""
    dotenv_path = dotenv.find_dotenv(usecwd=True)
    if dotenv_path:
        dotenv.load_dotenv(dotenv_path)
    else:
        dotenv.load_dotenv()

    app_id = os.getenv("APP_ID")
    app_key = os.getenv("APP_KEY")
    if not app_id or not app_key:
        raise RuntimeError("Missing APP_ID or APP_KEY in .env")

    return app_id, app_key


ADZUNA_BASE_URL: Final[str] = "https://api.adzuna.com/v1/api"
