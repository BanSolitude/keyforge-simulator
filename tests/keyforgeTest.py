import unittest
import random
from player import *
from cards import *
from state import *

TEST_HOUSE = House.BROBNAR
OTHER_HOUSE = House.DIS

#TODO probably don't need all this setup now that I have "set_active_player_state"
class KeyforgeTest(unittest.TestCase):
    def setUp(self):
        self.action = Action(TEST_HOUSE)
        self.artifact = Artifact(TEST_HOUSE)
        self.creature = Creature(TEST_HOUSE)
        self.upgrade = Upgrade(TEST_HOUSE)
        self.state = State([],[])
        '''
                [self.action,
                self.artifact,
                self.creature,
                self.upgrade,
                Action(TEST_HOUSE),
                Action(TEST_HOUSE)]),
            []
        )'''
        self.player = self.state.players[0]
        self.player.state.activeHouse = TEST_HOUSE

    def set_active_player_state(self, **kwargs):
        for arg in kwargs:
            setattr(self.player.state, arg, kwargs[arg])
