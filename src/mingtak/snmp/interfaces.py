# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from mingtak.snmp import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.app.vocabularies.catalog import CatalogSource


SNMP_VERSION = SimpleVocabulary(
    [SimpleTerm(value=u'0', title=_(u'v1')),
     SimpleTerm(value=u'1', title=_(u'v2c'))]
)

OID_TYPE = SimpleVocabulary(
    [SimpleTerm(value=u'Integer', title=_(u'Integer')),
     SimpleTerm(value=u'String', title=_(u'String'))]
)


class IMingtakSnmpLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IDevice(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    device_locate = schema.TextLine(
        title=_(u'Device Locate'),
        description=_(u'Support ipv4, ipv6 and domain name.'),
        default=u'localhost',
        required=True,
    )

    port = schema.Int(
        title=_(u'Port'),
        default=161,
        required=True,
    )

    snmp_version = schema.Choice(
        title=_(u'SNMP Version'),
        default=u'1',
        vocabulary=SNMP_VERSION,
        required=True,
    )

    snmp_comm = schema.TextLine(
        title=_(u'Community'),
        default=u'public',
        required=True,
    )

    monitorOids = RelationList(
        title=_(u"Monitor Oids"),
        value_type=RelationChoice(title=_(u"Related"),
                                  source=CatalogSource(Type='Oid'),),
        required=False,
    )


class IOid(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    oid = schema.TextLine(
        title=_(u'OID'),
        required=True,
    )

    oidType = schema.Choice(
        title=_(u'OID Type'),
        vocabulary=OID_TYPE,
        required=True,
    )

    timesNumber = schema.Float(
        title=_(u'Times of Number'),
        description=_(u'Must be a float number, as 1.0, 100.0, 0.1 or ext..., if OID Type is String, this number will ignore.'),
        default=0.1,
        required=False,
    )


class IReport(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    relDevice = RelationChoice(
        title=_(u"Related Device"),
        source=CatalogSource(Type='Device'),  
        required=True,
    )

    relOid = RelationChoice(
        title=_(u"Related Oid"),
        source=CatalogSource(Type='Oid'),
        required=True,
    )

    upperLimit = schema.Float(
        title=_(u"Upper Limit"),
        required=False,
    )

    lowerLimit = schema.Float(
        title=_(u"Lower Limit"),
        required=False,
    )
