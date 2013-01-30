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
        if query is None:
            query = {}
        query = self.filter_query(query)
        if not query:
            return []

        # Turn the query into an OR query
        if 'SearchableText' in query:
            splitter = re.compile("[^\\s\"']+|\"[^\"]*\"|'[^']*'")
            query['SearchableText'] = ' OR '.join(splitter.findall(query['SearchableText']))
        query['portal_type'] = ['rd']
        query['inactive'] = False
        query.pop('show_inactive')
        
        catalog = getToolByName(self.context, 'portal_catalog')
        return [i for i in catalog.queryCatalog(query, show_all=1, show_inactive=1) \
                if not i.inactive]
