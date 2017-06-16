# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from mingtak.snmp.testing import MINGTAK_SNMP_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that mingtak.snmp is properly installed."""

    layer = MINGTAK_SNMP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if mingtak.snmp is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'mingtak.snmp'))

    def test_browserlayer(self):
        """Test that IMingtakSnmpLayer is registered."""
        from mingtak.snmp.interfaces import (
            IMingtakSnmpLayer)
        from plone.browserlayer import utils
        self.assertIn(IMingtakSnmpLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MINGTAK_SNMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['mingtak.snmp'])

    def test_product_uninstalled(self):
        """Test if mingtak.snmp is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'mingtak.snmp'))

    def test_browserlayer_removed(self):
        """Test that IMingtakSnmpLayer is removed."""
        from mingtak.snmp.interfaces import \
            IMingtakSnmpLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMingtakSnmpLayer, utils.registered_layers())
