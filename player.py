from cards import Action, Artifact, Battleline, Creature, Upgrade
from random import shuffle

class Player():
    def __init__(self, deck, endGame):
        self.state = PlayerState(deck)
        #TODO should always be initialized through State so this isn't really needed
        self.opponent = None
        self.playFuncs = {Action: self.play_action,
                        Artifact: self.play_artifact,
                        Creature: self.play_creature,
                        Upgrade: self.play_upgrade}
        self.endGame = endGame

    def get_amber(self):
        return self.state.amber

    def add_amber(self, amount = 1):
        if amount < 0:
            raise ValueError("Amount for add_amber must always be positive")

        self.state.amber += amount

    def remove_amber(self, amount = 1):
        self.state.remove_amber(amount)

    def get_keys(self):
        return self.state.keys

    def forge_key(self):
        self.state.forge_key()
        if self.state.keys >= 3:
            self.endGame(self)

    def get_active_house(self):
        return self.state.activeHouse

    def choose_house(self, house):
        self.state.choose_house(house)

    def get_hand(self):
        return self.state.hand

    #TODO how to handle playing different types (with diff reqs) does kwargs make sense
    def play_card(self, card, **kwargs):
        #check that card is of activeHouse
        self.add_amber(card.amberBonus)
        self.perform_ability(card.playAbility)
        self.state.get_hand().remove(card)
        self.playFuncs[type(card)](card, **kwargs)

    #TODO abilities probably will need more arguments
    def perform_ability(self, ability):
        ability(self)

    def play_action(self, card, **kwargs):
        self.state.discard.append(card)

    def play_creature(self, card, **kwargs):
        self.state.battleline.add(card, kwargs['leftFlank'])
        card.ready = False

    def play_artifact(self, card, **kwargs):
        self.state.artifacts.append(card)
        card.ready = False

    def play_upgrade(self, card, **kwargs):
        pass

    def ready_cards(self):
        for card in self.state.get_cards_in_play():
            card.ready = True

    def refill_hand(self):
        curHandSize = len(self.state.get_hand())
        #TODO max hand size can be modified by chains and/or cards in play
        if curHandSize < 6:
            self.state.draw(6-curHandSize)

    def get_discard(self):
        return self.state.discard

    def reap(self, creature):
        self.activate_creature_verification(creature)

        creature.ready = False
        self.add_amber(1)
        #perfom on reap ability

    def activate_creature_verification(self, creature):
        if not creature in self.state.battleline:
            raise ValueError("Creature must be on battleline to use")
        if not creature.ready:
            raise ValueError("Creature must be ready to use")
        if not creature.house == self.state.activeHouse:
            raise ValueError("Creature must be of active house to use")

    def damage(self, creature, amount):
        if not creature in self.state.battleline:
            raise ValueError("Must control creature to damage it.")

        creature.take_damage(amount)
        if creature.damage >= creature.power:
            self.state.battleline.remove(creature)
            self.state.discard.insert(0,creature)

class PlayerState():
    def __init__(self, deck):
        self.keys = 0
        self.amber = 0
        self.keyPrice = 6
        self.battleline = Battleline()
        self.artifacts = []
        self.deck = deck
        self.hand = []
        self.discard = []
        self.activeHouse = None
        
        shuffle(self.deck)
        self.draw(6)

    def remove_amber(self, amount):
        if amount < 0:
            raise ValueError("Amount for remove_amber must always be positive")

        if self.amber < amount:
            raise ValueError("Tried to remove %d amber but only had %d."
                                % (amount, self.amber) )

        self.amber -= amount

    def choose_house(self, house):
        #check if house is valid
        self.activeHouse = house

    def get_keys(self):
        return self.keys

    #TODO does it make sense for this to be here?
    def forge_key(self):
        try:
            self.remove_amber(self.keyPrice)
            self.keys += 1

        except ValueError:
            pass #don't have enough amber, eat exception

    def get_hand(self):
        return self.hand

    def get_discard(self):
        return self.discard

    def draw(self, numCards):
        #TODO deal with deck running out
        if numCards > len(self.deck):
            shuffle(self.discard)
            self.deck += self.discard
            self.discard = []
        drawn = self.deck[0:numCards]
        self.deck = self.deck[numCards:]
        self.hand += drawn

    def get_cards_in_play(self):
        return self.battleline.get_all() + self.artifacts
