from os import path

from setuptools import find_packages, setup


def read(*parts):
    return open(path.join(path.dirname(__file__), *parts)).read()


setup(
    name="django-robots",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    description="Robots exclusion application for Django, complementing Sitemaps.",
    author="Jannis Leidel",
    author_email="jannis@leidel.info",
    python_requires=">=3.7",
    url="https://github.com/jazzband/django-robots/",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    package_data={
        "robots": [
            "locale/*/LC_MESSAGES/*",
            "templates/robots/*.html",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Framework :: Django",
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "Framework :: Django :: 6.1",
    ],
)
