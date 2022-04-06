import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.2.15'
PACKAGE_NAME = 'cisco_config_parser'
AUTHOR = 'Ahmad Rezazadeh'
AUTHOR_EMAIL = 'ahmad1785@gmail.com'
URL = 'https://github.com/arezazadeh/cisco_config_parser'

LICENSE = 'MIT License'
DESCRIPTION = 'This Package Will Parse Cisco IOS, IOS-XE, IOS-XR and NXOS Configuration File.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'netmiko',
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )