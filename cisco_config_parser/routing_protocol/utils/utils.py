import ipaddress


def get_subnet(network=None, mask=None):
    """
    Get the subnet from the network and mask
    :param network: str
    :param mask: str
    :return: str
    """
    return str(ipaddress.ip_network((network, mask), strict=False)) if mask else str(ipaddress.ip_network(network))


def get_mask_from_cidr(subnet):
    """
    Get the mask from the CIDR
    Args:
        subnet: str
    Returns:
        str
    """
    return str(ipaddress.IPv4Network(subnet).netmask)


def convert_wildcard_to_mask(wildcard_mask):
    """
    Convert the wildcard mask to a subnet mask
    :param wildcard_mask: str
    :return: str
    """
    wildcard_mask = wildcard_mask.split(".")
    wildcard_mask = [str(255 - int(i)) for i in wildcard_mask]
    return ".".join(wildcard_mask)
