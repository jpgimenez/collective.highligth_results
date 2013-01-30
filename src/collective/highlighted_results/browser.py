# -*- coding: utf-8 -*-

import re

try:
    from plone.app.search import browser
    BaseSearch = browser.Search
    quote_chars = browser.quote_chars
    EVER = browser.EVER
except:
    from collective.highlighted_results import backward_search
    BaseSearch = backward_search.Search
    quote_chars = backward_search.quote_chars
    EVER = backward_search.EVER

from Products.CMFCore.utils import getToolByName


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
        return [i for i in catalog.queryCatalog(query, show_all=1, show_inactive=1)
                if not i.inactive]
