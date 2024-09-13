import re


RTP_NXOS_REGEX = re.compile(r"^router\s(\S+)", flags=re.MULTILINE)


# NXOS STATIC ROUTE


RTP_NXOS_VRF_CONTEXT_REGEX = re.compile(r"^vrf\scontext\s(\S+)", flags=re.MULTILINE)
RTP_NXOS_VRF_STATIC_ROUTE_REGEX = re.compile(r"\s+ip\sroute\s.*", flags=re.MULTILINE)
RTP_NXOS_GLOBAL_STATIC_ROUTE_REGEX = re.compile(r"^ip\sroute\s.*", flags=re.MULTILINE)
RTP_NXOS_STATIC_ROUTE_REGEX = re.compile(r"ip\sroute\s.*", flags=re.MULTILINE)
RTP_NXOS_STATIC_W_NAME_REGEX = re.compile(r"ip route\s(\S+)\s(\S+)\sname\s(.*)$", flags=re.MULTILINE)
RTP_NXOS_STATIC_W_NAME_AD_REGEX = re.compile(r"ip route\s(\S+)\s(\S+)\sname\s(.*)\s(\d+)$", flags=re.MULTILINE)
RTP_NXOS_STATIC_WO_NAME_REGEX = re.compile(r"ip route\s(\S+)\s(\S+)$", flags=re.MULTILINE)

