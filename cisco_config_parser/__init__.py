from .cisco_config_parser import ConfigParser, ConfigParserOld


_ALL_ = [
    "ConfigParser"
    "ConfigParserOld",
]

__version__ = "2.3.0"
__author__ = "Ahmad Rezazadeh"
__email__ = "ahmad@klevernet.io"
__url__ = "klevernet.ai"
__license__ = "MIT"
__description__ = "library to parse and automate Cisco configuration files"


__all__ = 'ConfigParser', 'ConfigParserOld'