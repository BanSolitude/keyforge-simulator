import enum

MAX_CARDS_IN_GAME = 72

class Steps(enum.Enum):
    FORGE = 0
    CHOOSE = 1
    PLAY_USE = 2
    READY = 3
    DRAW = 4

def reap_and_play_all(p):
    for creature in [c for c in p.state.battleline if c.house == p.state.activeHouse]:
        p.reap(creature)
    for card in [c for c in p.state.hand if c.house == p.state.activeHouse]:
        p.play_card(card, leftFlank=True)

def house_decision_cards_used_or_played(p, deckHouses,  wPlay, wUse):
    #Deal with negative weights
    maxScore = min(0, (MAX_CARDS_IN_GAME + 1)*wPlay) + min(0, (MAX_CARDS_IN_GAME + 1)*wUse)
    retHouse = None
    
    handHouses = [card.house for card in p.state.hand]
    inPlayHouses = [card.house for card in p.state.get_cards_in_play()]
    for house in deckHouses:
        score = handHouses.count(house)*wPlay + inPlayHouses.count(house)*wUse
        if score > maxScore:
            retHouse = house
            maxScore = score
    
    return retHouse

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
        return house_decision_cards_used_or_played(self.player, self.deckHouses, 1, 0)
        
    def first_turn_house_decision(self):
        return house_decision_cards_used_or_played(self.player, self.deckHouses, -1, 0)
    
    def play_and_use_cards(self):
        reap_and_play_all(self.player)
    
class MaxReapController(AbstractController):
    def house_decision(self):
        return house_decision_cards_used_or_played(self.player, self.deckHouses, 1, 10)

    def first_turn_house_decision(self):
        return house_decision_cards_used_or_played(self.player, self.deckHouses, -1, -10)
    
    def play_and_use_cards(self):
        reap_and_play_all(self.player)
