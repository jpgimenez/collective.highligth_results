import unittest

import robotsuite

from plone.testing import layered

from collective.highlighted_results.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("test_highlighted_results.txt"),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
