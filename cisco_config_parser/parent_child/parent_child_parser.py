import re
from .parent_child_obj import ParentChild
from cisco_config_parser.parser_regex.regex import SPLIT_ON_LINE
from .parent_child_separator import ParentChildSeparator
from dataclasses import dataclass



@dataclass
class ParentChildParser:
    """
    Parent Child Parser class
    :param content: str
    :return: list of ParentChild objects
    """
    content: str = None

    def _fetch_parent_child(self, **kwargs):
        """
        Fetch the parent child from the config file
        return: list of ParentChild objects
        """
        custom_regex = kwargs.get("custom_regex", None)
        if not custom_regex:
            raise ValueError("custom_regex is required")

        custom_regex = re.compile(custom_regex, flags=re.MULTILINE)
        parent_child = ParentChildSeparator(self.content)
        sections = parent_child._get_separated_sections()

        parent_child_obj_list = []

        for section in sections:
            parent_child_obj = ParentChild()
            regex_result = re.match(custom_regex, section.strip())
            if regex_result:
                if section.strip().startswith(regex_result.group()):
                    child_regex = SPLIT_ON_LINE.split(section.strip())
                    parent_child_obj.parent = child_regex[0]
                    child_regex.pop(0)
                    parent_child_obj.children = [line.strip() for line in child_regex if line] if child_regex else ""
                    parent_child_obj_list.append(parent_child_obj)

        return parent_child_obj_list

