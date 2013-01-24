import urllib2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


def generate_jpeg(width, height):
    url = 'http://lorempixel.com/%d/%d/' % (width, height)
    return urllib2.urlopen(url).read()


class Collectivehighlighted_ResultsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.highlighted_results
        xmlconfig.file('configure.zcml', collective.highlighted_results, context=configurationContext)

    def setUpPloneSite(self, portal):
        self['portal'] = portal
        roles = ('Member', 'Manager')
        portal.portal_membership.addMember('manager', 'secret', roles, [])
        roles = ('Member', 'Contributor')
        portal.portal_membership.addMember('contributor', 'secret', roles, [])
        applyProfile(portal, 'collective.highlighted_results:default')
        applyProfile(portal, 'collective.highlighted_results:testfixture')
        portal['my-image'].setImage(generate_jpeg(100, 100))
        portal['my-file'].setFile(generate_jpeg(100, 100))


COLLECTIVE_HIGHLIGHTED_RESULTS_FIXTURE = Collectivehighlighted_ResultsLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(COLLECTIVE_HIGHLIGHTED_RESULTS_FIXTURE,),
                                         name="collective.highlighted_results:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(COLLECTIVE_HIGHLIGHTED_RESULTS_FIXTURE,
                                              z2.ZSERVER_FIXTURE),
                                       name="collective.highlighted_results:Functional")
