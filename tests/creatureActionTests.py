from tests.keyforgeTest import *

class ReapTests(KeyforgeTest):
    def setUp(self):
        super().setUp()
        self.creature = Creature(TEST_HOUSE)
        self.player.play_creature(self.creature, leftFlank=True)
        self.creature.ready = True

    def test_reapActiveCreature_gainOneAmber(self):
        self.player.reap(self.creature)
        self.assertEqual(self.player.get_amber(), 1)

    def test_reapActiveCreature_creatureIsExhausted(self):
        self.player.reap(self.creature)
        self.assertFalse(self.creature.ready)

    def test_reapInactiveCreature_raisesError(self):
        with self.assertRaises(ValueError):
            self.creature.ready = False
            self.player.reap(self.creature)

    def test_reapCreatureOfInactiveHouse_raisesError(self):
        self.creature.house = OTHER_HOUSE
        with self.assertRaises(ValueError):
            self.player.reap(self.creature)

    def test_reapCreatureNotOnBattleline_raisesError(self):
        self.creature = Creature(TEST_HOUSE)
        #TODO should this be a different error
        with self.assertRaises(ValueError):
            self.player.reap(self.creature)

class TakeDamageTest(KeyforgeTest):
    def test_damageCreatureOnBattleline_dealsDamage(self):
        self.creature.take_damage(1)
        self.assertEqual(self.creature.damage, 1)

    def test_damageCreatureWithArmour_takesNoDamage(self):
        self.creature.armour = 1
        self.creature.take_damage(1)
        self.assertEqual(self.creature.damage, 0)

    def test_damageCreatureWithArmourTwice_takesDamage(self):
        self.creature.armour = 1
        self.creature.take_damage(1)
        self.creature.take_damage(1)
        self.assertEqual(self.creature.damage, 1)

    def test_damageCreatureWithArmourTwice_takesNoDamage(self):
        self.creature.armour = 2
        self.creature.take_damage(1)
        self.creature.take_damage(1)
        self.assertEqual(self.creature.damage, 0)

    def test_damageCreatureWithArmourMoreThanArmour_takesDamage(self):
        self.creature.armour = 2
        self.creature.take_damage(3)
        self.assertEqual(self.creature.damage, 1)
