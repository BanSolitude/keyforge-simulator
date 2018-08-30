from tests.keyforgeTest import *

class ForgeKeyTests(KeyforgeTest):
    def setUp(self):
        super().setUp()
        self.startAmber = random.randrange(5)
        self.player.add_amber(self.startAmber)

    def test_withLessThanSixAmber_doesntForgeKey(self):
        self.player.forge_key()
        self.assertEqual(self.player.get_keys(), 0)

    def test_withLessThanSixAmber_doesntsubtractamber(self):
        self.player.forge_key()
        self.assertEqual(self.player.get_amber(), self.startAmber)

    def test_withSixAmber_forgesKey(self):
        self.set_active_player_state(amber=6)
        self.player.forge_key()
        self.assertEqual(self.player.get_keys(), 1)

    def test_withMoreThanSixAmber_forgesKey(self):
        self.player.add_amber(6)
        self.player.forge_key()
        self.assertEqual(self.player.get_keys(), 1)

    def test_withMoreThanSixAmber_subtractsCorrectAmountofAmber(self):
        self.player.add_amber(6)
        self.player.forge_key()
        self.assertEqual(self.player.get_amber(), self.startAmber)

    def test_forgeSecondKey_playerHasntWonGame(self):
        self.set_active_player_state(amber=6, keys=1)
        self.player.forge_key()
        self.assertNotEqual(self.state.winner, self.player)

    def test_forgeThirdKey_playerWinsGame(self):
        self.set_active_player_state(amber=6, keys=2)
        self.player.forge_key()
        self.assertEqual(self.state.winner, self.player)

    #TODO different key prices

class SelectHouseTest(KeyforgeTest):
    def test_selectHouse_selectedHouseIsActive(self):
        self.player.choose_house(TEST_HOUSE)
        self.assertEqual(self.player.get_active_house(), TEST_HOUSE)

class ReadyCardsTest(KeyforgeTest):
    def test_NoCardsInPlay_NothingIsModified(self):
        self.player.ready_cards()
        self.assertEqual((self.player.state.battleline, self.player.state.artifacts),
                     (Battleline(),[]))

    def test_ExaustedCardsInPlay_AllReadied(self):
        readyCreature = Creature(TEST_HOUSE)
        readyCreature.ready = True
        exhaustedCreature = Creature(TEST_HOUSE)
        exhaustedCreature.ready = False
        readyArtifact = Artifact(TEST_HOUSE)
        readyArtifact.ready = True
        exhaustedArtifact = Artifact(TEST_HOUSE)
        exhaustedArtifact.ready = False

        self.set_active_player_state(battleline=Battleline([exhaustedCreature, readyCreature]),artifacts=[readyArtifact, exhaustedArtifact])
        self.player.ready_cards()
        for card in self.player.state.battleline.get_all() + self.player.state.artifacts:
            self.assertTrue(card.ready)

    #TODO should "renew armour" test be here?

class RefillHandTest(KeyforgeTest):
    #TODO generate hand function that creates list of n cards?
    def set_five_cards_in_hand(self):
        self.topCard = Action(TEST_HOUSE)
        self.hand = []
        for i in range(5):
            self.hand.append(Action(TEST_HOUSE))

        self.set_active_player_state(hand=self.hand, deck=[self.topCard])

    def test_handHasFewerThanSixCards_DrawUpToSix(self):
        self.deck = []
        for i in range(7):
            self.deck.append(Action(TEST_HOUSE))
        self.set_active_player_state(hand=[Action(TEST_HOUSE)], deck=self.deck)
        self.player.refill_hand()
        self.assertEqual(len(self.player.get_hand()), 6)

    def test_handHasMoreThanSixCards_NoneDrawn(self):
        self.hand = []
        for i in range(7):
            self.hand.append(Action(TEST_HOUSE))

        self.set_active_player_state(hand=self.hand)
        self.player.refill_hand()
        self.assertEqual(self.player.get_hand(), self.hand)

    def test_handHasFiveCards_TopCardIsInHand(self):
        self.set_five_cards_in_hand()
        self.player.refill_hand()
        self.assertIn(self.topCard, self.player.get_hand())

    def test_handHasFiveCards_TopCardIsRemovedFromDeck(self):
        self.set_five_cards_in_hand()
        self.player.refill_hand()
        self.assertNotIn(self.topCard, self.player.state.deck)

    def test_noCardsInDeck_DiscardBecomesDeck(self):
        self.set_five_cards_in_hand()
        self.player.state.discard = [self.player.state.deck.pop()]
        self.player.refill_hand()
        self.assertEqual(self.player.state.discard,[])

    def test_noCardsInDeck_DiscardCardIsInHand(self):
        self.set_five_cards_in_hand()
        self.player.state.discard = [self.player.state.deck.pop()]
        self.player.refill_hand()
        self.assertIn(self.topCard, self.player.get_hand())
