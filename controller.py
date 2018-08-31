import enum

class Steps(enum.Enum):
    FORGE = 0
    CHOOSE = 1
    PLAY_USE = 2
    READY = 3
    DRAW = 4

class AbstractController():
    def __init__(self, player):
        self.player = player
        self.deckHouses = set()
        for card in self.player.state.deck:
             self.deckHouses.add(card.house)
             if len(self.deckHouses) == 3:
                 break

    def turn(self):
        self.player.forge_key()
        self.player.choose_house(self.house_decision())
        self.play_and_use_cards()
        self.player.ready_cards()
        self.player.refill_hand()

    def first_turn(self):
        self.player.state.draw(1)
        self.player.choose_house(self.first_turn_house_decision())
        self.first_turn_play()

    def house_decision(self):
        for house in self.deckHouses:
            return house

    def play_and_use_cards(self):
        pass

    def first_turn_play(self):
        for card in self.player.state.hand:
            if card.house == self.player.state.activeHouse:
                self.player.play_card(card, leftFlank= True)
        self.player.ready_cards()

    def first_turn_house_decision(self):
        return self.house_decision()

class MaxCardsController(AbstractController):
    def house_decision(self):
        max_count = 0
        ret_house = None
        
        hand_houses = [card.house for card in self.player.state.hand]
        for house in self.deckHouses:
            count = hand_houses.count(house)
            if count > max_count:
                ret_house = house
                max_count = count
        
        return ret_house
        
    def first_turn_house_decision(self):
        min_count = 8
        ret_house = None
        
        hand_houses = [card.house for card in self.player.state.hand]
        for house in self.deckHouses:
            count = hand_houses.count(house)
            if count < min_count:
                ret_house = house
                min_count = count
        
        return ret_house
    
    def play_and_use_cards(self):
        for creature in [c for c in self.player.state.battleline if c.house == self.player.state.activeHouse]:
            self.player.reap(creature)
        for card in [c for c in self.player.state.hand if c.house == self.player.state.activeHouse]:
            self.player.play_card(card, leftFlank=True)
