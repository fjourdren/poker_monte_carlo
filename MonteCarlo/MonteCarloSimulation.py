import copy

from .Player import Player
from .Table import Table
from .Card import stringToCard

class MonteCarloSimulation: 
    nbSimulation = 1000
    winNumber = 0
    table = None
    player = None
    nbPlayer = 2
    staticPlayercard1 = None
    staticPlayercard2 = None
    staticBoard = []



    
    def __init__(self, nbSimulation, nbPlayer, playerCard1, playerCard2, boardFlop1, boardFlop2, boardFlop3, boardRiver, boardTurn):
        self.nbSimulation = nbSimulation
        self.winNumber = 0
        self.table = Table()
        self.player = Player()
        self.nbPlayer = nbPlayer
        self.staticPlayercard1 = None
        self.staticPlayercard2 = None
        self.staticBoard = []

        self.table.addPlayer(self.player)

        # setup player's static cards
        if(playerCard1 != None and playerCard2 != None):
            playercard1 = self.table.getCard(stringToCard(playerCard1))
            self.staticPlayercard1 = playercard1

            playercard2 = self.table.getCard(stringToCard(playerCard2))
            self.staticPlayercard2 = playercard2

        # setup static board
        if(boardFlop1 != None):
            cardFlop1 = self.table.getCard(stringToCard(boardFlop1))
            self.staticBoard.append(cardFlop1)
        if(boardFlop2 != None):
            cardFlop2 = self.table.getCard(stringToCard(boardFlop2))
            self.staticBoard.append(cardFlop2)
        if(boardFlop3 != None):
            cardFlop3 = self.table.getCard(stringToCard(boardFlop3))
            self.staticBoard.append(cardFlop3)
        if(boardRiver != None):
            cardRiver = self.table.getCard(stringToCard(boardRiver))
            self.staticBoard.append(cardRiver)
        if(boardTurn != None):
            cardTurn = self.table.getCard(stringToCard(boardTurn))       
            self.staticBoard.append(cardTurn)

        # fill table with players
        self.table.fillPlayers(self.nbPlayer)

    def run(self):
        for i in range(self.nbSimulation):
            # setup player cards configured by the user
            if(self.staticPlayercard1 != None and self.staticPlayercard2 != None):
                self.table.players[0].card1 = self.staticPlayercard1
                self.table.removeAvailableCard(self.staticPlayercard1)

                self.table.players[0].card2 = self.staticPlayercard2
                self.table.removeAvailableCard(self.staticPlayercard2)

            # setup board's cards configured by the user
            if(len(self.staticBoard) != 0):
                for i in range(len(self.staticBoard)):
                    self.table.board.append(self.staticBoard[i])
                    self.table.removeAvailableCard(self.staticBoard[i])

            # distribute other cards
            self.table.distributeCardsToPostRiver()


            # calculate winners
            if(self.table.players[0] in self.table.getWinner()):
                self.winNumber = self.winNumber + 1/float(len(self.table.getWinner()))

            
            # debug
            '''print("========================")
            print('- board')
            for a in range(len(self.table.board)):
                print(self.table.board[a].cardToString())

            print('- player 1')
            tmpplayer = self.table.players[0]
            print(tmpplayer.card1.cardToString())
            print(tmpplayer.card2.cardToString())
            print(tmpplayer.handStrength.toString())
            print(tmpplayer.handStrength2.toString())

            print('- player 2')
            tmpplayer = self.table.players[1]
            print(tmpplayer.card1.cardToString())
            print(tmpplayer.card2.cardToString())
            print(tmpplayer.handStrength.toString())
            print(tmpplayer.handStrength2.toString())'''


            self.table.resetTable()

        # calculate the probability to win on long term
        return self.winNumber / float(self.nbSimulation)