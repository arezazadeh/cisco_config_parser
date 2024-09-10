from .help import *


class IOSStaticRouteConfig:
    def __repr__(self):
        return RTP_IOS_STATIC_HELP

class IOSOSPFConfig:
    def __repr__(self):
        return RTP_IOS_OSPF_HELP


class IOSEIGRPConfig:
    def __repr__(self):
        return RTP_IOS_EIGRP_HELP

class IOSBGPConfig:
    def __repr__(self):
        return RTP_IOS_BGP_HELP


class ParentChild:
    def __repr__(self):
        return PARENT_CHILD_HELP


class L3Interface:
    def __repr__(self):
        return LAYER3_INTERFACE_HELP


class L2Interface:
    def __repr__(self):
        return LAYER2_INTERFACE_HELP




