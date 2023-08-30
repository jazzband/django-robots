try:
    from importlib.metadata import version

    __version__ = version("django-robots")
except ImportError:
    from pkg_resources import get_distribution

    __version__ = get_distribution("django-robots").version

# needed for Django<3.2
default_app_config = "robots.apps.RobotsConfig"
