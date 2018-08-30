from player import Player

class State:
    #Deck is (id, cards) pair
    def __init__(self, deckOne, deckTwo):
        self.players = [Player(deckOne, self.end_game), Player(deckTwo, self.end_game)]
        self.players[0].opponent = self.players[1]
        self.players[1].opponent = self.players[0]
        self.winner = None

    def end_game(self, player):
        self.winner = player
        #print ("game over")
