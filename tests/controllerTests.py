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
        self.assertEqual(self.mockPlayer.called, shouldCall)

    def test_firstTurn_onlyOneCardPlayed(self):
        self.controller.first_turn()
        self.assertEqual(self.mockPlayer.cardsPlayed, 1)

    def test_firstTurn_extraCardDrawn(self):
        self.controller.first_turn()
        self.assertEqual(self.mockPlayer.state.cardsDrawn, 1)

    def test_takeTurn_selectsAppropriateHouse(self):
        self.controller.turn()
        self.assertIn(self.mockPlayer.activeHouse, DECK_HOUSES)

class MockPlayer():
    def __init__(self):
        self.reset()
        self.state = MockState()

    def forge_key(self):
        self.called.add(Steps.FORGE)

    def choose_house(self, house):
        self.called.add(Steps.CHOOSE)
        self.activeHouse = house

    def ready_cards(self):
        self.called.add(Steps.READY)

    def refill_hand(self):
        self.called.add(Steps.DRAW)

    def reset(self):
        self.called = set()
        self.cardsPlayed = 0

    def play_card(self, card):
        self.cardsPlayed += 1

    def play_card(self, card, **kwargs):
        self.cardsPlayed += 1

class MockState():
    def __init__(self):
        self.deck = []
        self.hand = []
        self.cardsDrawn = 0
        for house in DECK_HOUSES:
            self.deck.append(Card(house))
            self.hand.append(Card(house))

    def draw(self, amount):
        self.cardsDrawn += amount
