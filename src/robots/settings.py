import sys
import typing as t

from django.conf import settings
from django.test.signals import setting_changed

DEFAULT_ROBOTS_SETTINGS: t.Dict[str, t.Any] = {
    "SITEMAP_URLS": [],
    "USE_SITEMAP": True,
    "USE_HOST": True,
    "CACHE_TIMEOUT": None,
    "SITE_BY_REQUEST": False,
    "USE_SCHEME_IN_HOST": False,
    "SITEMAP_VIEW_NAME": False,
}


def getdefault(setting: str) -> t.Any:
    return getattr(settings, f"ROBOTS_{setting}", DEFAULT_ROBOTS_SETTINGS[setting])


SITEMAP_URLS: t.List[str] = getdefault("SITEMAP_URLS")
USE_SITEMAP: bool = getdefault("USE_SITEMAP")
USE_HOST: bool = getdefault("USE_HOST")
CACHE_TIMEOUT: t.Optional[int] = getdefault("CACHE_TIMEOUT")
SITE_BY_REQUEST: bool = getdefault("SITE_BY_REQUEST")
USE_SCHEME_IN_HOST: bool = getdefault("USE_SCHEME_IN_HOST")
SITEMAP_VIEW_NAME: bool = getdefault("SITEMAP_VIEW_NAME")


def reload_robots_settings(
    setting: str, value: t.Any, enter: bool, **kwargs: object
) -> None:
    if not setting.startswith("ROBOTS_"):  # pragma: no cover
        return

    setting = setting.replace("ROBOTS_", "")
    if enter:  # setting applied
        setattr(sys.modules[__name__], setting, value)
    else:
        setattr(sys.modules[__name__], setting, getdefault(setting))


setting_changed.connect(reload_robots_settings)
