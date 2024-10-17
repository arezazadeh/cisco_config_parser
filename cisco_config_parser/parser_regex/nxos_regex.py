import re


RTP_NXOS_REGEX = re.compile(r"^router\s(\S+)", flags=re.MULTILINE)


# NXOS STATIC ROUTE


RTP_NXOS_VRF_CONTEXT_REGEX = re.compile(r"^vrf\scontext\s(\S+)", flags=re.MULTILINE)
RTP_NXOS_VRF_STATIC_ROUTE_REGEX = re.compile(r" ip route .*", flags=re.MULTILINE)
RTP_NXOS_GLOBAL_STATIC_ROUTE_REGEX = re.compile(r"^ip route .*", flags=re.MULTILINE)
RTP_NXOS_STATIC_ROUTE_REGEX = re.compile(r"ip route .*", flags=re.MULTILINE)

# Global
RTP_NXOS_STATIC_REGEX = re.compile(r"ip route (\S+) (\S+)$", flags=re.MULTILINE)
RTP_NXOS_STATIC_AD_REGEX = re.compile(r"ip route (\S+) (\S+) (\d+)", flags=re.MULTILINE)
RTP_NXOS_STATIC_NAME_REGEX = re.compile(r"ip route (\S+) (\S+) name (.*)$", flags=re.MULTILINE)
RTP_NXOS_STATIC_NAME_AD_REGEX = re.compile(r"ip route (\S+) (\S+) name (.*) (\d+)$", flags=re.MULTILINE)




