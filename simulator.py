from state import State
from cards import Action, Creature, House
from controller import MaxCardsController

if __name__ == '__main__':
    deck = []
    for i in range(6):
        deck.append(Action(House.BROBNAR, 1))
        deck.append(Action(House.DIS, 1))
        deck.append(Action(House.LOGOS, 1))
        deck.append(Creature(House.BROBNAR))
        deck.append(Creature(House.DIS))
        deck.append(Creature(House.LOGOS))

    deckTwo = []
    for i in range(6):
        deckTwo.append(Action(House.BROBNAR, 1))
        deckTwo.append(Action(House.DIS, 1))
        deckTwo.append(Action(House.LOGOS, 1))
        deckTwo.append(Creature(House.BROBNAR))
        deckTwo.append(Creature(House.DIS))
        deckTwo.append(Creature(House.LOGOS))

    gameState = State(deck, deckTwo)
    controllers = [MaxCardsController(gameState.players[0]), MaxCardsController(gameState.players[1])]

    controllers[0].first_turn()

    activeController = 1
    
    while True:
        print ("Battleline length = %d" % len(controllers[activeController].player.state.battleline))
        print ("Deck length = %d" % len(controllers[activeController].player.state.deck))
        print ("Hand length = %d" % len(controllers[activeController].player.state.hand))

        controllers[activeController].turn()
        
        if controllers[activeController].player.state.keys >= 3:
            break

        print(len(controllers[activeController].player.state.battleline))

        print ('Active player has %d keys and %d amber' % (controllers[activeController].player.state.keys, controllers[activeController].player.state.amber))

        activeController = (activeController + 1) % 2

    if controllers[activeController].player == gameState.players[0]:
        print('first player won')
    else:
        print('second player won')
