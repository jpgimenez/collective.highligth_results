import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from collective.highlighted_results.testing import INTEGRATION_TESTING
from plone.app.testing import login


class TestContent(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_types = getToolByName(self.portal, 'portal_types')

    def test_rd_content_installed(self):
        """
        """
        self.assertTrue('rd' in self.portal_types.objectIds())

    def test_create_rd_content(self):
        """
        """
        login(self.portal, 'manager')
        self.portal.invokeFactory('rd', 'rd1')
        self.assertTrue('rd1' in self.portal.objectIds())

    def test_rd_content_wf(self):
        """
        """
        login(self.portal, 'manager')
        self.portal.invokeFactory('rd', 'rd1')
        workflowTool = getToolByName(self.portal.rd1, "portal_workflow")
        chain = workflowTool.getChainFor(self.portal.rd1)

        # no workflow
        self.failUnless(len(chain) == 1)
        self.failUnless('one_state_workflow' in chain)

    def test_rd_content_fields(self):
        """
        """
        login(self.portal, 'manager')
        self.portal.invokeFactory('rd', 'rd1')
