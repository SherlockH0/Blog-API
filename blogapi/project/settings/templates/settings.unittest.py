DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",  # pyright: ignore
    }
}

NINJA_JWT = {
    "SIGNING_KEY": "bmxex)1w=o^2**5tzj&uyam9c^y5)b!)@be+=(4yb63r!d$k)x",
}
