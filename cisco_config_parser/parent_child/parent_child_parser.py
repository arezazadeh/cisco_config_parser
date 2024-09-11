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

    def _fetch_parent_child_old(self, **kwargs):
        """
        Fetch the parent child from the config file
        return: list of ParentChild objects
        """
        custom_regex = kwargs.get("custom_regex", None)
        return_json = kwargs.get("return_json", False)
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

        if return_json:
            return [obj.__dict__ for obj in parent_child_obj_list]

        return parent_child_obj_list


    def _fetch_parent_child(self, **kwargs):
        """
        Fetch the parent child from the config file
        :param parent_regex: str Default is None (required)
        :param child_regex: str Default is None (optional)
        :param return_json: bool Default is False (optional)
        return: list of ParentChild objects
        """
        parent_regex = kwargs.get("parent_regex", None)
        child_regex = kwargs.get("child_regex", None)
        return_json = kwargs.get("return_json", False)

        if not parent_regex:
            raise ValueError("parent_regex is required")

        PARENT_REGEX = re.compile(parent_regex, flags=re.MULTILINE)
        parent_child = ParentChildSeparator(self.content)
        sections = parent_child._get_separated_sections()

        parent_child_obj_list = []

        for section in sections:
            parent_child_obj = ParentChild()
            parent_regex_result = PARENT_REGEX.search(section.strip())
            if parent_regex_result:
                if section.strip().startswith(parent_regex_result.group()):
                    if child_regex:
                        CHILD_REGEX = re.compile(child_regex, flags=re.MULTILINE)
                        child_regex_result = CHILD_REGEX.search(section.strip())
                        if child_regex_result:
                            parent_child_obj.parent = parent_regex_result.group()
                            parent_child_obj.children = child_regex_result.group()
                            parent_child_obj_list.append(parent_child_obj)
                    else:
                        children_regex = SPLIT_ON_LINE.split(section.strip())
                        children_regex.pop(0)
                        parent_child_obj.parent = parent_regex_result.group()
                        parent_child_obj.children = [line.strip() for line in children_regex if line] if children_regex else ""
                        parent_child_obj_list.append(parent_child_obj)

        if return_json:
            return [obj.__dict__ for obj in parent_child_obj_list]

        return parent_child_obj_list
