import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from collective.highlighted_results.testing import INTEGRATION_TESTING


class TestContent(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_types = getToolByName(self.portal, 'portal_types')

    def test_search_with(self):
        """
        """
        pass

    def test_search_without(self):
        """
        """
        pass
