from cisco_config_parser.separator import Separator


class ParentChildSeparator(Separator):
    def __init__(self, content):
        super().__init__(_content=content)

        self._parent_child_sections: list = []
        self._add_bang_between_section()

    def _get_separated_sections(self):
        return self._sections.split("!")
