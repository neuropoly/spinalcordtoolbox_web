import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'waitress',
    'alembic',
    'pyramid_jinja2',
    'pyramid_mako',
    'passlib',
    'colander',
    'pyramid_marrowmailer',
    'html2text',
    'pyramid_tm',
    'sqlalchemy_utils',
    'cryptacular',
    'wtforms',
    'deform',
    'zope.sqlalchemy',
    'simplejson',
    'psutil',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'deform_bootstrap',
    'pyramid_chameleon',
    'cornice'
    ]

setup(name='server',
      version='0.1',
      description='server',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Willis Pinaud & Pierre Olivier Quirion',
      author_email='',
      url='spinalcordtoolbox.org',
      keywords='Spinal cord toolbox web mri',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="server",
      entry_points="""\
      [paste.app_factory]
      main = server:main
      """,
      )
