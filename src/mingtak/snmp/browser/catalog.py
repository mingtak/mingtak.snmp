# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from zope.interface import Interface
#from Products.CMFPlone.utils import safe_unicode
#import re
#from twNotice.content.interfaces import IOrganization, ICPC, INotice
from mingtak.snmp.interfaces import IDevice, IOid


@indexer(IDevice)
def snmp_comm_indexer(obj):
    return obj.snmp_comm
