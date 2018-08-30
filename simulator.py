from state import State
from cards import Action, Creature, House
from copy import deepcopy
from random import shuffle

#TODO Controllers that handle the decision making each turn
#TODO Handle first turn correctly
#TODO Decks that aren't all one House
#TODO Select house in some smart way

if __name__ == '__main__':
    deck = []
    for i in range(18):
        deck.append(Action(House.BROBNAR, 1))
        deck.append(Creature(House.BROBNAR))

    print(deck)

    deckTwo = []
    for i in range(18):
        deckTwo.append(Action(House.BROBNAR, 1))
        deckTwo.append(Creature(House.BROBNAR))

    gameState = State(deck, deckTwo)
    activePlayer = gameState.players[0]
    shuffle(activePlayer.state.deck)
    shuffle(activePlayer.opponent.state.deck)

    while True:
        print ("Battleline length = %d" % len(activePlayer.state.battleline))
        print ("Deck length = %d" % len(activePlayer.state.deck))
        print ("Hand length = %d" % len(activePlayer.state.hand))

        activePlayer.forge_key()
        if activePlayer.state.keys >= 3:
            break
        activePlayer.select_house(House.BROBNAR)

        for creature in activePlayer.state.battleline:
            activePlayer.reap(creature)

        for i in range(len(activePlayer.state.hand)):
            activePlayer.play_card(activePlayer.state.hand[0], leftFlank=True)

        print(len(activePlayer.state.battleline))

        activePlayer.ready_cards()
        activePlayer.refill_hand()

        print ('Active player has %d keys and %d amber' % (activePlayer.state.keys, activePlayer.state.amber))

        activePlayer = activePlayer.opponent

    if activePlayer == gameState.players[0]:
        print('first player won')
    else:
        print('second player won')
