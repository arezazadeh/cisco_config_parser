from cisco_config_parser.parser_regex.regex import *
import ipaddress



class _L3SectionParser:



    @classmethod
    def _parse_ip_address_line(cls, **kwargs):
        """
        ip_address_line_regex.groups() returns a tuple of all the groups in the regex
        we filter the tuple to get only the group that is not None
        if the regex is found, split the tuple into a list and get the first element
        which is the ip address and the second element which is the mask
        we then create a subnet from the ip address and the
        mask using the ipaddress module
        return: l3_interface_obj
        """

        def process_ip_address_with_cidr(ip_address_with_cidr, obj):
            """
            Process the ip address with cidr
            :param ip_address_with_cidr: str
            :param obj: L3Interface object
            :return:
            """
            ip_address_config = ip_address_with_cidr.split("/")
            ip_addr = ip_address_config[0].strip()
            cidr = ip_address_config[1].strip()
            subnet_ = ipaddress.IPv4Network(f"{ip_addr}/{cidr}", strict=False)
            obj.ip_address = ip_addr.strip()
            obj.mask = str(subnet_.netmask)
            obj.subnet = str(subnet_).strip()
            return obj

        ip_address_line_regex = kwargs.get("ip_address_line_regex")
        l3_interface_obj = kwargs.get("l3_interface_obj")
        primary = kwargs.get("primary", True)

        ip_address_regex = [ip_group for ip_group in ip_address_line_regex.groups() if ip_group]

        # Check if the ip address has a CIDR - 10.1.1.1/24
        if "/" in ip_address_regex[0]:
            l3_interface_obj = process_ip_address_with_cidr(ip_address_regex[0], l3_interface_obj)
            return l3_interface_obj

        ip_address_section = ip_address_regex[0].split()
        ip_address = ip_address_section[0].strip()
        mask = ip_address_section[1].strip()
        subnet = str(ipaddress.IPv4Network(f"{ip_address}/{mask}", strict=False))
        if primary:
            l3_interface_obj.ip_address = ip_address.strip()
            l3_interface_obj.mask = mask.strip()
            l3_interface_obj.subnet = subnet.strip()
        else:
            l3_interface_obj.sec_ip_address = ip_address.strip()
            l3_interface_obj.sec_mask = mask.strip()
            l3_interface_obj.sec_subnet = subnet.strip()

        return l3_interface_obj

    @classmethod
    def _parse_vrf_line(cls, **kwargs):
        """
        vrf_line_regex.groups() returns a tuple of all the groups in the regex
        we filter the tuple to get only the group that is not None
        if the regex is found, split the tuple into a list and get the first element
        which is the vrf
        return: l3_interface_obj
        """
        vrf_line_regex = kwargs.get("vrf_line_regex")
        l3_interface_obj = kwargs.get("l3_interface_obj")
        vrf = vrf_line_regex.groups()
        vrf = [vrf_group for vrf_group in vrf if vrf_group][0]
        l3_interface_obj.vrf = vrf.strip()
        return l3_interface_obj

    @classmethod
    def _parse_helper_address_line(cls, **kwargs):
        """
        helper_address_list is an empty list
        split the section into lines
        for each line in the lines, search for the helper address regex
        if the regex is found, append the helper address to the helper_address_list
        return: l3_interface_obj
        """
        l3_interface_obj = kwargs.get("l3_interface_obj")
        section = kwargs.get("section")

        helper_address_list = []
        lines = SPLIT_ON_LINE.split(section)
        for line in lines:
            helper_address = HELPER_ADDRESS_REGEX.search(line)
            if helper_address:
                helper_address_list.append(helper_address.group(1).strip())
        l3_interface_obj.helpers = helper_address_list
        return l3_interface_obj


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
        l3_interface_obj = kwargs.get("l3_interface_obj")
        custom_field_name = kwargs.get("custom_field_name")

        if custom_field_regex:
            custom_field = custom_field_regex.groups()
            if not custom_field:
                """
                The custom regex is not in a group
                """
                l3_interface_obj._add_custom_field(custom_field_name, custom_field_regex.group().strip())

            else:
                custom_field = [custom_group for custom_group in custom_field if custom_group][0]
                if custom_field:
                    l3_interface_obj._add_custom_field(custom_field_name, custom_field.strip())

        return l3_interface_obj

