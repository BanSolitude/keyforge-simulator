from tests.keyforgeTest import *

class PlayCardsTest(KeyforgeTest):
    def test_playCardWithAmberBonus_gainAmber(self):
        card = Action(TEST_HOUSE, 1)
        self.set_active_player_state(hand=[card], activeHouse = TEST_HOUSE)
        self.player.play_card(card)
        self.assertEqual(self.player.get_amber(), 1)

    def test_playCardOfInactiveHouse_raisesError(self):
        card = Action(OTHER_HOUSE)
        with self.assertRaises(ValueError):
            self.player.play_card(card)

    def test_playAction_cardGoesToDiscard(self):
        card = Action(TEST_HOUSE)
        self.set_active_player_state(hand=[card], activeHouse = TEST_HOUSE)
        self.player.play_card(card)
        self.assertIn(card, self.player.get_discard())

    def test_playArtifact_isInPlay(self):
        card = Artifact(TEST_HOUSE)
        self.set_active_player_state(hand=[card], activeHouse = TEST_HOUSE)
        self.player.play_card(card)
        self.assertIn(card, self.player.state.artifacts)

    def test_playCreature_isOnBattleline(self):
        card = Creature(TEST_HOUSE)
        self.set_active_player_state(hand=[card], activeHouse = TEST_HOUSE)
        self.player.play_card(card, leftFlank=True)
        self.assertIn(card, self.player.state.battleline.get_all())

    @unittest.skip("Haven't decided how to implement upgrades.")
    def test_playUpgrade_isAttachedToCreature(self):
        pass

class DamageTest(KeyforgeTest):
    def setUp(self):
        super().setUp()
        self.player.state.battleline.add(self.creature, leftFlank=True)
        
    def test_damageCreatureEqualToPower_creatureIsRemovedFromBattleline(self):
        self.player.damage(self.creature, self.creature.power)
        self.assertNotIn(self.creature, self.player.state.battleline)

    def test_damageCreatureEqualToPower_creatureIsMovedToDiscard(self):
        self.player.damage(self.creature, self.creature.power)
        self.assertIn(self.creature, self.player.state.discard)

    def test_damamageCreatureNotOnBattleline_raisesExcepiton(self):
        #TODO right exception?
        with self.assertRaises(ValueError):
            self.player.damage(Creature(TEST_HOUSE), 1)
