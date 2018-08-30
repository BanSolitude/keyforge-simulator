import enum

class Steps(enum.Enum):
    FORGE = 0
    CHOOSE = 1
    PLAY_USE = 2
    READY = 3
    DRAW = 4

class Controller():
    def __init__(self, player):
        self.player = player
        self.deckHouses = set()
        for card in self.player.state.deck:
             self.deckHouse.add(card.house)
             if len(self.deckHouse) == 3:
                 break

    def turn(self):
        self.player.forge_key()
        self.player.select_house(self.house_decision())
        self.play_and_use_cards()
        self.player.ready_cards()
        self.player.refill_hand()

    def house_decision(self):
        pass

    def play_and_use_cards(self):
        pass
