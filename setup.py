import setuptools

with open('README.md', 'r', encoding = 'utf-8') as fh:
  long_description = fh.read()

with open('requirements.txt', 'r') as fr:
  dependencies = fr.read().strip().split('\n')

setuptools.setup(
  name = 'drake',
  version = '0.2.2',
  author = 'Quentin (mefyl) Hocquet',
  author_email = 'mefyl@gruntech.org',
  description = 'The well-formed build system',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/Dimrok/drake',
  package_dir = {'': 'src'},
  packages = setuptools.find_packages('src'),
  classifiers = (
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
  ),
  install_requires = dependencies
)
