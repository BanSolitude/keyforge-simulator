from tests.keyforgeTest import *

class AmberTests(KeyforgeTest):
    def setUp(self):
        super().setUp()
        self.randAmount = random.randrange(2,10)

    def test_defaultAddAmber_addsOneAmber(self):
        self.player.add_amber()
        self.assertEqual(self.player.get_amber(), 1)

    def test_addPositiveAmber_addThatAmoutOfAmber(self):
        self.player.add_amber(self.randAmount)
        self.assertEqual(self.player.get_amber(), self.randAmount)

    def test_addNegativeAmber_raisesValueError(self):
        with self.assertRaises(ValueError):
            self.player.add_amber(-1*self.randAmount)

    def test_defaultRemoveAmber_removesOneAmber(self):
        self.set_active_player_state(amber=self.randAmount)
        self.player.remove_amber()
        self.assertEqual(self.player.get_amber(), self.randAmount - 1)

    def test_removePositiveAmber_addThatAmoutOfAmber(self):
        self.set_active_player_state(amber=2*self.randAmount)
        self.player.remove_amber(self.randAmount)
        self.assertEqual(self.player.get_amber(), self.randAmount)

    def test_removeMoreAmberThanPlayerHas_raisesValueError(self):
        with self.assertRaises(ValueError):
            self.player.remove_amber(self.randAmount)

    def test_removeNegativeAmber_raisesValueError(self):
        self.set_active_player_state(amber=self.randAmount)
        with self.assertRaises(ValueError):
            self.player.remove_amber(-1*self.randAmount)

class BattlelineTest(unittest.TestCase):
    def setUp(self):
        self.battleline = Battleline()
        self.testCreature = Creature(TEST_HOUSE)

    def test_addToEmptyBattleLine_creatureIsOnBattleline(self):
        self.battleline.add(self.testCreature, False)
        self.assertIn(self.testCreature, self.battleline)

    def test_addNonCreatureCard_raisesValueError(self):
        with self.assertRaises(ValueError):
            self.battleline.add(Action(TEST_HOUSE), True)

    def test_addToBattleLine_creatureIsOnFlank(self):
        self.battleline = Battleline([Creature(TEST_HOUSE)])
        self.battleline.add(self.testCreature, leftFlank=False)
        self.assertIn(self.testCreature, self.battleline.get_flanks())

    def test_getAll_returnsCreaturesOnBattleline(self):
        battlelineList = [Creature(TEST_HOUSE), Creature(TEST_HOUSE), Creature(TEST_HOUSE)]
        self.battleline = Battleline(battlelineList)
        self.assertEqual(self.battleline.get_all(), battlelineList)

    def test_getFlanks_returnsCreaturesOnFlank(self):
        leftFlank = Creature(TEST_HOUSE)
        rightFlank = Creature(TEST_HOUSE)
        self.battleline = Battleline([leftFlank, Creature(TEST_HOUSE), rightFlank])
        self.assertEqual(self.battleline.get_flanks(), [leftFlank, rightFlank])

    def test_getFlanksOnBattlelineWithOneCreature_returnsOneCreature(self):
        self.battleline = Battleline([Creature(TEST_HOUSE)])
        self.assertEqual(len(self.battleline.get_flanks()), 1)

    def test_remove_battlelineCollapses(self):
        one,two,three,four = Creature(TEST_HOUSE),Creature(TEST_HOUSE),Creature(TEST_HOUSE),Creature(TEST_HOUSE)
        self.battleline = Battleline([one,two,three,four])
        self.battleline.remove(two)
        self.assertEqual(self.battleline, Battleline([one,three,four]))

class opponentTest(KeyforgeTest):
    def test_playCreature_opponenetsBattlelineIsEmpty(self):
        card = Creature(TEST_HOUSE)
        self.set_active_player_state(hand=[card])
        self.player.opponent.state.battleline = Battleline()
        self.player.play_card(card, leftFlank=True)
        self.assertEqual(len(self.player.opponent.state.battleline), 0)

    def test_opponentNotPlayer(self):
        self.assertNotEqual(self.player, self.player.opponent)

    def test_opponentStateNotPlayerState(self):
        self.assertNotEqual(self.player.state, self.player.opponent.state)

    def test_opponentBattlelineNotPlayerBattleline(self):
        self.assertFalse(self.player.state.battleline is self.player.opponent.state.battleline)
