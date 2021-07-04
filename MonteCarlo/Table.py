from .Player import Player
from .Card import Card
from .HandStrength import calculateHandStrength
from .Utils import Diff
import random

class Table:
    players = []
    board = []
    cardsAvailables = []
  

    # constructor 
    def __init__(self): 
        self.players = []
        self.board = []
        self.cardsAvailables = []

        self.fillCardsAvailables()
    

    # search a card inside cardsAvailables array
    def getCard(self, card):
        output = None

        # navigate trough cardsAvailables
        for i in range(len(self.cardsAvailables)):
            cardinChech = self.cardsAvailables[i]
            if(card.equalsTo(cardinChech)) :
                output = cardinChech
        
        return output


    # add a player to the table
    def addPlayer(self, player):
        self.players.append(player)


    # fill the table with x players
    def fillPlayers(self, nbPlayer):
        for _ in range(nbPlayer - len(self.players)):
            self.addPlayer(Player())


    # fill cardsAvailables array with all cards possible
    def fillCardsAvailables(self):
        # "SPADE", "HEART", "DIAMOND", "CLUB"
        for high in range(2, 15):
            self.cardsAvailables.append(Card("S", high))
            self.cardsAvailables.append(Card("H", high))
            self.cardsAvailables.append(Card("D", high))
            self.cardsAvailables.append(Card("C", high))


    # distribute cards to all players and place the board
    def distributeCardsToPostRiver(self):
        for p in range(len(self.players)):
            player = self.players[p]
            if(player.card1 == None and player.card2 == None):
                self.addTwoCardToAPlayerRandom(player)
        
        self.addFullBoardRandom()


    def getRandomCard(self):
        card = random.choice(self.cardsAvailables)
        return card


    def removeAvailableCard(self, card):
        self.cardsAvailables.remove(card)


    # give two random card to this player
    def addTwoCardToAPlayerRandom(self, player):
        card1 = self.getRandomCard()
        player.card1 = card1
        self.removeAvailableCard(card1)

        card2 = self.getRandomCard()
        player.card2 = card2
        self.removeAvailableCard(card2)


    # add 3 cards from the flop to the board (random)
    def addBoardFlopRandom(self):
        self.addBoard(self.getRandomCard())
        self.addBoard(self.getRandomCard())
        self.addBoard(self.getRandomCard())
    

    # add 1 card from the river to the board (random)
    def addBoardRiverRandom(self):
        self.addBoard(self.getRandomCard())


    # add 1 card from the turn to the board (random)
    def addBoardTurnRandom(self):
        self.addBoard(self.getRandomCard())
    

    # add 5 cards from flop, river and turn to the board (random)
    def addFullBoardRandom(self):
        if(len(self.board) == 0):
            self.addBoardFlopRandom()

        if(len(self.board) == 3):
            self.addBoardRiverRandom()

        if(len(self.board) == 4):
            self.addBoardTurnRandom()


    # add a card to the board and remove it from removeAvailableCard
    def addBoard(self, card):
        self.board.append(card)
        self.removeAvailableCard(card)


    # calculate the winner of the round
    def getWinner(self):
        output = []

        # calculate for each players their main HandStrength and they secondary by removing the first one from the array which contains the concatenation of player cards and board cards
        for p in range(len(self.players)):
            player = self.players[p]
            cards = []

            cards.append(player.card1)
            cards.append(player.card2)

            cardsBoardAndHand = self.board + cards
            player.handStrength = calculateHandStrength(cardsBoardAndHand)

            cardsBoardAndHand = Diff(cardsBoardAndHand, player.handStrength.cards)
            player.handStrength2 = calculateHandStrength(cardsBoardAndHand)

        
        # determine who won/loose/draw the round by comparing handStrengths
        for p in range(len(self.players)):
            player = self.players[p]

            if(len(output) == 0):
                output.append(player)
            elif(player not in output):
                winValue = output[0].handStrength.winVersus(player.handStrength)

                # if equality, we check the second handStrength
                if(winValue == 0.5):
                    # TEMP
                    winValue2 = 0
                    if(output[0].handStrength2.high == player.handStrength2.high):
                        winValue2 = 0.5
                    elif(output[0].handStrength2.high > player.handStrength2.high):
                        winValue2 = 1


                    # if the two players are again egality, we add the player to the winners
                    if(winValue2 == 0.5):
                        output.append(player)
                    elif(winValue2 == 0):
                        output = []
                        output.append(player)
                elif(winValue == 0):
                    output = []
                    output.append(player)

        return output
        

    # reset table and players
    def resetTable(self):
        for p in range(len(self.players)):
            player = self.players[p]

            self.cardsAvailables.append(player.card1)
            self.cardsAvailables.append(player.card2)

            player.removeCards()

        self.cardsAvailables = self.cardsAvailables + self.board
        self.board = []