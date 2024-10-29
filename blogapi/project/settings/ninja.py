from typing import Any

NINJA_JWT = {
    "SIGNING_KEY": "bmxex)1w=o^2**5tzj&uyam9c^y5)b!)@be+=(4yb63r!d$k)x",
}


# Fixes `RemovedInDjango60Warning`. Source: https://github.com/vitalik/django-ninja/issues/1266#issuecomment-2336579784
def monkeypatch_ninja_uuid_converter() -> None:
    import importlib
    import sys

    import django.urls

    module_name = "ninja.signature.utils"
    sys.modules.pop(module_name, None)

    original_register_converter = django.urls.register_converter

    def fake_register_converter(*_: Any, **__: Any) -> None:
        pass

    django.urls.register_converter = fake_register_converter
    importlib.import_module(module_name)

    django.urls.register_converter = original_register_converter


monkeypatch_ninja_uuid_converter()
