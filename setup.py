import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '2.2.4'
PACKAGE_NAME = 'cisco_config_parser'
AUTHOR = 'Ahmad Rezazadeh'
AUTHOR_EMAIL = 'ahmad@klevernet.io'

URL = 'https://github.com/arezazadeh/cisco_config_parser'

LICENSE = 'MIT License'
DESCRIPTION = 'This library is used for Network Automation involving Cisco Routers and Switch. It will parse Cisco IOS, IOS-XE, IOS-XR, and NXOS configuration file into objects and/or json format'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"



setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      packages=find_packages()
      )