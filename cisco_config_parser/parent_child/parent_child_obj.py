from dataclasses import dataclass


@dataclass
class ParentChild:
    """
    Parent Child class
    """
    parent: str = None
    children: list = None

    def _add_custom_field(self, field_name, field_value):
        """
        Add custom field to the object
        :param field_name: name of the field
        :param field_value: value of the field
        """
        setattr(self, field_name, field_value)

    def __getattr__(self, item):
        """
        Get the attribute of the object
        :param item: attribute name
        :return: None
        """
        return None

    def _add_child(self, child):
        """
        Add child to the object
        :param child: child object
        """
        self.children.append(child)





