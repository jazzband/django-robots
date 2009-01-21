from distutils.core import setup

setup(
    name='django-robots',
    version=__import__('robots').__version__,
    description='Robots exclusion application for Django, complementing Sitemaps.',
    long_description=open('docs/overview.txt').read(),
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    url='http://code.google.com/p/django-robots/',
    download_url='http://github.com/jezdez/django-dbtemplates/zipball/0.5.4',
    packages=['robots'],
    package_dir={'dbtemplates': 'dbtemplates'},
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
