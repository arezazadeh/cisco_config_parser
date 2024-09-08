from cisco_config_parser.parser_regex.regex import *
from dataclasses import dataclass

"""
1. section the config file with "!" between each section
2. 
"""

@dataclass
class Separator:
    _content: str = None
    _sections: str = ""

    def _add_bang_between_section(self):
        split_on_line = SPLIT_ON_LINE.split(self._content)
        for i in split_on_line:
            parent_regex = PARENT_LINE_REGEX.search(i)
            children_regex = CHILDREN_LINE_REGEX.search(i)
            if parent_regex:
                self._sections += "!" + "\n"
                self._sections += parent_regex.group() + '\n'
            if children_regex:
                self._sections += children_regex.group() + '\n'












