# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from mingtak.snmp.interfaces import IDevice
from mingtak.snmp.testing import MINGTAK_SNMP_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class DeviceIntegrationTest(unittest.TestCase):

    layer = MINGTAK_SNMP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Device')
        schema = fti.lookupSchema()
        self.assertEqual(IDevice, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Device')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Device')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDevice.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Device',
            id='Device',
        )
        self.assertTrue(IDevice.providedBy(obj))
