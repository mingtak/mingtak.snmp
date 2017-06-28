# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode
import json
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, BigInteger, String, ForeignKey, Boolean, Text, Date, DateTime, JSON
from sqlalchemy import Integer as INTEGER # 名稱衝突，改取別名
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
import re
import os
import logging


logger = logging.getLogger("mingtak.snmp.browser.report")
BASEMODEL = declarative_base()
# 加上charset='utf8'解決phpmyadmin的中文問題
ENGINE = create_engine('mysql+mysqldb://env_monitor:env_monitor@localhost/env_monitor?charset=utf8', echo=True)


class ReportView(BrowserView):
    """ Report View
    """
    index = ViewPageTemplateFile("template/report_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        self.getDB()
        catalog = context.portal_catalog
        portal = api.portal.get()

        upperLimit = context.upperLimit
        lowerLimit = context.lowerLimit
        timesNumber = context.relOid.to_object.timesNumber
        start = int(request.form.get('start', 1))
        startDate = date.today() - timedelta(start)

        Session = sessionmaker()
        session = Session()
        queryCond = select([self.snmp_record])\
            .where(self.snmp_record.c.device_locate == context.relDevice.to_object.device_locate)\
            .where(self.snmp_record.c.oid == context.relOid.to_object.oid)\
            .where(self.snmp_record.c.record_time > startDate)\
            .order_by(self.snmp_record.c.record_time)
        conn = ENGINE.connect()
#        import pdb; pdb.set_trace()
        result = conn.execute(queryCond)

        self.timeStr = ''
        self.floatStr = ''
        self.upperFloatStr = ''
        self.lowerFloatStr = ''
        for item in result:
            self.timeStr += "'%s', " % item['record_time']
            self.floatStr += "%s, " % round(int(item['record_int'])*timesNumber,1)
            self.upperFloatStr += "%s, " % upperLimit
            self.lowerFloatStr += "%s, " % lowerLimit

        self.timeStr = self.timeStr[:-2]
        self.floatStr = self.floatStr[:-2]
        self.upperFloatStr = self.upperFloatStr[:-2]
        self.lowerFloatStr = self.lowerFloatStr[:-2]

        conn.close()
        return self.index()


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
