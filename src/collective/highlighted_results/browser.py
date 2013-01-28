# -*- coding: utf-8 -*-

import re
from DateTime import DateTime
from Acquisition import aq_parent

try:
    from plone.app.search import browser
    BaseSearch = browser.Search
    quote_chars = browser.quote_chars
    EVER = browser.EVER
except:
    from collective.highlighted_results.backward_search import Search as BaseSearch
    from collective.highlighted_results.backward_search import quote_chars
    from collective.highlighted_results.backward_search import EVER

from plone.z3cform import layout
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.CMFPlone.PloneBatch import Batch
from Products.ZCTextIndex.ParseTree import ParseError


class Search(BaseSearch):
    """
    """

    def getHighlights(self, query=None):
        import ipdb;ipdb.set_trace()
        if query is None:
            query = {}
        query = self.filter_query(query)

        # Turn the query into an OR query
        if 'SearchableText' in query:
            splitter = re.compile("[^\\s\"']+|\"[^\"]*\"|'[^']*'")
            query['SearchableText'] = ' OR '.join(splitter.findall(query['SearchableText']))
        query['portal_type'] = ['rd']
        query['show_inactive'] = True

        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(query)
