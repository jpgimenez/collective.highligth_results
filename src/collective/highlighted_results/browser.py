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

from zope.component import getMultiAdapter
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.highlighted_results.content import Ird
from plone.app.layout.viewlets.common import TitleViewlet as TitleViewletBase

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


class View(BrowserView):
    """
    """

    def title(self):
        context = self.context
        return context.title and context.title or \
               (context.target and context.target.to_object.Title() or ' ')

    def link(self):
        context = self.context
        return context.link and context.link or \
               (context.target and context.target.to_object.absolute_url() or ' ')


class TitleViewlet(TitleViewletBase):

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        context = self.context
        self.page_title = lambda: context.title and context.title or \
            (context.target and context.target.to_object.Title() or ' ')
        self.portal_title = self.portal_state.portal_title
