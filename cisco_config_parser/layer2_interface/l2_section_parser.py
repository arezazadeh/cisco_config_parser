class _L2AccessSectionParser:

    @classmethod
    def _parse_custom_regex(cls, **kwargs):
        """
        custom_field_regex.groups() returns a tuple of all the groups in the regex
        we filter the tuple to get only the group that is not None
        if the regex is found, split the tuple into a list and get the first element
        which is the custom field
        return: l3_interface_obj
        """
        custom_field_regex = kwargs.get("custom_field_regex")
        l2_access_interface_obj = kwargs.get("l2_access_interface_obj")
        custom_field_name = kwargs.get("custom_field_name")

        if custom_field_regex:
            custom_field = custom_field_regex.groups()
            if not custom_field:
                """
                The custom regex is not in a group
                """
                l2_access_interface_obj._add_custom_field(custom_field_name, custom_field_regex.group().strip())

            else:
                custom_field = [custom_group for custom_group in custom_field if custom_group][0]
                if custom_field:
                    l2_access_interface_obj._add_custom_field(custom_field_name, custom_field.strip())

        return l2_access_interface_obj



class _L2TrunkSectionParser:
    @classmethod
    def _parse_custom_regex(cls, **kwargs):
        """
        custom_field_regex.groups() returns a tuple of all the groups in the regex
        we filter the tuple to get only the group that is not None
        if the regex is found, split the tuple into a list and get the first element
        which is the custom field
        return: l3_interface_obj
        """
        custom_field_regex = kwargs.get("custom_field_regex")
        custom_field_name = kwargs.get("custom_field_name")
        l2_trunk_interface_obj = kwargs.get("l2_trunk_interface_obj")

        if custom_field_regex:
            custom_field = custom_field_regex.groups()
            if not custom_field:
                """
                The custom regex is not in a group
                """
                l2_trunk_interface_obj._add_custom_field(custom_field_name, custom_field_regex.group().strip())

            else:
                custom_field = [custom_group for custom_group in custom_field if custom_group][0]
                if custom_field:
                    l2_trunk_interface_obj._add_custom_field(custom_field_name, custom_field.strip())

        return l2_trunk_interface_obj