from tests.keyforgeTest import *
from controller import *

DECK_HOUSES = [House.BROBNAR, House.DIS, House.LOGOS]

class ControllerTests(KeyforgeTest):
    def setUp(self):
        super().setUp() #maybe?
        self.mockPlayer = MockPlayer()
        self.controller = Controller(self.mockPlayer)

    def test_takeTurn_appropriateFunctionsCalled(self):
        shouldCall = set([Steps.FORGE, Steps.CHOOSE, Steps.READY, Steps.DRAW])
        self.controller.turn()
        selfAssertEqual(self.mockPlayer.called, shouldCall)

    def test_firstTurn_onlyOneCardPlayed(self):
        self.controller.first_turn()
        #TODO test that one card is played

    def test_firstTurn_extraCardDrawn(self):
        self.controller.first_turn()
        #TODO how do I actually test this?

    def test_takeTurn_selectsAppropriateHouse(self):
        self.controller.turn()
        self.assertIn(self.mockPlayer.selectedHouse, DECK_HOUSES)

class MockPlayer():
    def __init__(self):
        self.reset()
        self.state = MockState()

    def forge_key(self):
        self.called.add(Steps.FORGE)

    def choose_house(self):
        self.called.add(Steps.CHOOSE)

    def ready_cards(self):
        self.called.add(Steps.READY)

    def refill_hand(self):
        self.called.add(Steps.DRAW)

    def reset(self):
        self.called = set()
        self.cardsPlayed = 0

class MockState():
    def __init__(self):
        self.deck = []
        for house in DECK_HOUSES:
            self.deck.append(Card(house))