# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode
import json
import logging

logger = logging.getLogger("mingtak.snmp.browser.report")


class ReportView(BrowserView):
    """ Report View
    """
    index = ViewPageTemplateFile("template/report_view.pt")

    def __call__(self):
        context = self.context
        request = self.request
        catalog = context.portal_catalog
        portal = api.portal.get()

        return self.index()

