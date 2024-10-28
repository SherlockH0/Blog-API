import os.path
from pathlib import Path

from split_settings.tools import include, optional

from blogapi.core.utils.pytest import is_pytest_running

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

ENVVAR_SETTINGS_PREFIX = "BLOGAPI_SETTINGS_"

LOCAL_SETTINGS_PATH = os.getenv(f"{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = (
        f"local/settings.{'unittests' if is_pytest_running() else 'dev'}.py"
    )

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    "base.py",
    "custom.py",
    "ninja.py",
    optional(LOCAL_SETTINGS_PATH),
    "envvars.py",
)

if not is_pytest_running():
    assert SECRET_KEY is not NotImplemented  # pyright: ignore
