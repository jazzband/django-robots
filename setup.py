from distutils.core import setup

setup(name='robots',
      version='0.1',
      description='Robots exclusion application for Django, complementing Sitemaps.',
      author='Jannis Leidel',
      author_email='jannis@leidel.info',
      url='http://code.google.com/p/django-robots/',
      packages=['robots'],
      package_dir={'robots': 'robots'},
      package_data={'robots': ['templates/robots/*.html']},
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
