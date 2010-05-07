from setuptools import setup, find_packages

setup(
    name='django-robots',
    version=__import__('robots').__version__,
    description='Robots exclusion application for Django, complementing Sitemaps.',
    long_description=open('docs/overview.txt').read(),
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    url='http://bitbucket.org/jezdez/django-robots/',
    packages=find_packages(),
    zip_safe=False,
    package_data = {
        'robots': [
            'locale/*/LC_MESSAGES/*',
            'templates/robots/*.html',
        ],
    },
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Framework :: Django',
    ]
)
