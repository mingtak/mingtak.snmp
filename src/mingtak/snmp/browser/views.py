# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, BigInteger, String, ForeignKey, Boolean, Text, Date, DateTime, JSON
from sqlalchemy import Integer as INTEGER # 名稱衝突，改取別名
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
import re
import os
from pysnmp.hlapi import *

import logging

logger = logging.getLogger("mingtak.snmp")
BASEMODEL = declarative_base()
# 加上charset='utf8'解決phpmyadmin的中文問題
ENGINE = create_engine('mysql+mysqldb://env_monitor:env_monitor@localhost/env_monitor?charset=utf8', echo=True)


class SnmpGet(BrowserView):

    def getDB(self):
        self.metadata = MetaData(ENGINE)
        self.snmp_record = Table(
            'snmp_record', self.metadata,
            Column('id', INTEGER, primary_key=True, autoincrement=True),
            Column('record_time', DateTime), # 紀錄時間
            Column('device_locate', String(200)), # 位置，可以是 ipv4, ipv6 或 domain name
            Column('oid', String(200)), # oid
            Column('record_str', String(500)), # 內容, string
            Column('record_int', INTEGER), # 內容, integer
            mysql_engine='InnoDB',
            mysql_charset='utf8',
            use_unicode=True,
        )
        self.metadata.create_all()


    def snmpGet(self, comm='public', ver=1, ip=None, port=161, oid=None):

        # 預設採 v2c, public, port:161
        errorIndication, errorStatus, errorindex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData(comm, mpModel=ver),
                UdpTransportTarget((ip ,port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
            )
        )

        if errorIndication:
            logger.error('%s' % errorIndication)
        elif errorStatus:
            logger.error('%s at %s' % ( errorStatus.prettyPrint(), errorindex and varBinds[int(errorindex)-1][0] or '?' ))

        return varBinds


    def __call__(self):

        portal = api.portal.get()
        context = self.context
        self.getDB()
        conn = ENGINE.connect() # DB連線

        brain = api.content.find(context=portal, snmp_comm='public', Type='Device')
        for item in brain:
            itemObj = item.getObject()
            device_locate = itemObj.device_locate
            snmp_version = int(itemObj.snmp_version)
            snmp_comm = itemObj.snmp_comm
            port = itemObj.port

            oids = itemObj.monitorOids

            for item in oids:
#                import pdb;pdb.set_trace()
                oid = item.to_object.oid
                snmpData = self.snmpGet(comm=snmp_comm, ver=snmp_version, ip=device_locate, port=port, oid=oid)

                if not snmpData:
                    return

                if 'Integer' in snmpData[0][1].prettyPrintType():
                    record_int = int(snmpData[0][1])
                    record_str = None
                if 'String' in snmpData[0][1].prettyPrintType():
                    record_int = None
                    record_str = str(snmpData[0][1])

                ins = self.snmp_record.insert()
                ins = ins.values(
                    record_time=datetime.now(),
                    device_locate=device_locate,
                    oid=oid,
                    record_str=record_str,
                    record_int=record_int,
                )

                try:
                    conn.execute(ins)
                except:
                    pass

        conn.close()
#            import pdb; pdb.set_trace()
