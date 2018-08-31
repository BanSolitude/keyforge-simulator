from state import State
from cards import Action, Creature, House
from controller import MaxCardsController, MaxReapController

ROUNDS = 10000

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

    wins = [0,0]

    for i in range(ROUNDS):
        gameState = State(deck, deckTwo)
        controllers = [MaxReapController(gameState.players[0]), MaxReapController(gameState.players[1])]

        controllers[0].first_turn()

        activeController = 1
        
        while True:
            controllers[activeController].turn()
            
            if controllers[activeController].player.state.keys >= 3:
                break

            #print ('Active player has %d keys and %d amber' % (controllers[activeController].player.state.keys, controllers[activeController].player.state.amber))

            activeController = (activeController + 1) % 2

        if controllers[activeController].player == gameState.players[0]:
            wins[0] += 1
        else:
            wins[1] += 1

    print('First player won {} and second player won {}'.format(*wins))
