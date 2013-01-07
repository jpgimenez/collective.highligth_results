from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class Collectivehighlighted_ResultsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.highlighted_results
        xmlconfig.file('configure.zcml', collective.highlighted_results, context=configurationContext)

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.highlighted_results:default')

COLLECTIVE_HIGHLIGHTED_RESULTS_FIXTURE = Collectivehighlighted_ResultsLayer()
COLLECTIVE_HIGHLIGHTED_RESULTS_INTEGRATION_TESTING = IntegrationTesting(bases=(COLLECTIVE_HIGHLIGHTED_RESULTS_FIXTURE,), name="Collectivehighlighted_ResultsLayer:Integration")
