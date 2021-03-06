# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from gaiatest import GaiaTestCase
from gaiatest.apps.system.regions.cards_view import CardsView


class TestCardsView(GaiaTestCase):

    _app_under_test = "Clock"
    _clock_frame_locator = (By.CSS_SELECTOR, "iframe[mozapp^='app://clock'][mozapp$='manifest.webapp']")

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.cards_view = CardsView(self.marionette)

        # Launch the Clock app as a basic, reliable
        # app to test against in Cards View
        self.app = self.apps.launch(self._app_under_test)

    def test_cards_view(self):
        # https://moztrap.mozilla.org/manage/case/1909/
        # Switch to top level frame before dispatching the event
        self.marionette.switch_to_frame()

        # Check that cards view is not displayed
        self.assertFalse(self.cards_view.is_cards_view_displayed, "Cards view not expected to be visible")

        # Pull up the cards view
        self.cards_view.open_cards_view()

        self.assertTrue(self.cards_view.is_app_displayed(self._app_under_test),
            "%s app expected to be visible in cards view" % self._app_under_test)

        self.cards_view.exit_cards_view()

    def test_that_app_can_be_launched_from_cards_view(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/98
        # Switch to top level frame before dispatching the event
        self.marionette.switch_to_frame()

        # Find the cards frame html element
        clock_frame = self.marionette.find_element(*self._clock_frame_locator)

        # Pull up the cards view
        self.cards_view.open_cards_view()

        self.assertFalse(clock_frame.is_displayed(), "Clock frame not expected to be displayed")

        # Launch the app from the cards view
        self.cards_view.tap_app(self._app_under_test)

        self.cards_view.wait_for_cards_view_not_displayed()
        self.assertTrue(clock_frame.is_displayed(), "Clock frame expected to be displayed")

    def test_kill_app_from_cards_view(self):
        # https://moztrap.mozilla.org/manage/case/1917/
        # Switch to top level frame before dispatching the event
        self.marionette.switch_to_frame()

        # Pull up the cards view
        self.cards_view.open_cards_view()

        # Close the current app from cards view
        self.cards_view.close_app(self._app_under_test)

        self.marionette.switch_to_frame()

        # Pull up the cards view again
        self.cards_view.open_cards_view()

        # If successfully killed, the app should no longer appear in the cards view.
        self.assertFalse(self.cards_view.is_app_present(self._app_under_test),
            "Killed app not expected to appear in cards view")
