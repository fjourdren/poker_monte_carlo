from .Utils import Diff
from .Card import CardsFollow

class handStrength:
    typeStrength = 0
    high = 0
    cards = []


    # default constructor 
    def __init__(self, typeStrength, high, cards): 
        self.typeStrength = typeStrength
        self.high = high
        self.cards = cards


    # check who win beetween two handStrength
    def winVersus(self, versus):
        output = 0

        if(self.typeStrength > versus.typeStrength):
            output = 1
        elif(self.typeStrength == versus.typeStrength):
            if(self.high > versus.high):
                output = 1
            elif(self.high == versus.high):
                output = 0.5

        return output

    
    def toString(self):
        return str(self.typeStrength) + ' ' + str(self.high)


def calculateHandStrength(cards):
    output = None

    tmpVar = haveHigh(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None

    tmpVar = havePair(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None

    tmpVar = haveDouble(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None
    
    tmpVar = haveBrelan(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None
    
    tmpVar = haveQuinte(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None

    tmpVar = haveFlush(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None

    tmpVar = haveFull(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None

    tmpVar = haveFour(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None

    tmpVar = haveQuinteFlush(cards)
    if(tmpVar != None):
        output = tmpVar
    tmpVar = None

    return output



def haveQuinteFlush(cards):
    quinteFlush = None

    flush = haveFlush(cards)
    if(flush != None):
        quinte = haveQuinte(flush.cards)
        if(quinte != None):
            quinteFlush = handStrength(8, flush.high, flush.cards)

    return quinteFlush


def haveFour(cards):
    four = None
    cardsFour = []

    for high in range(14, 1, -1):
        cardsFour = []
        for card in cards:
            if(card.value == high):
                cardsFour.append(card)

        count = len(cardsFour)
        
        if(count == 4):
            four = high

        if(four != None):
            break

    if(four != None):
        return handStrength(7, four, cardsFour)
    else:
        return four


def haveFull(cards):
    full = None

    brelan = haveBrelan(cards)
    if(brelan != None):
        cards = Diff(cards, brelan.cards)
        pair = havePair(cards)
        if(pair != None):
            full = handStrength(6, brelan.high, brelan.cards)

    return full


def haveFlush(cards):
    flush = None

    cards.sort(key=lambda x: x.value, reverse=True)

    Scards = list(filter(lambda x: x.kind == "S", cards))[:5]
    Hcards = list(filter(lambda x: x.kind == "H", cards))[:5]
    Dcards = list(filter(lambda x: x.kind == "D", cards))[:5]
    Ccards = list(filter(lambda x: x.kind == "C", cards))[:5]
    
    lenScards = len(Scards)
    lenHcards = len(Hcards)
    lenDcards = len(Dcards)
    lenCcards = len(Ccards)

    flushHigh = 0

    if(lenScards == 5):
        flushHigh = Scards[0].value
        flush = handStrength(5, Scards[0].value, Scards)
    
    if(lenHcards == 5 and Hcards[0].value > flushHigh):
        flushHigh = Hcards[0].value
        flush = handStrength(5, Hcards[0].value, Hcards)
    
    if(lenDcards == 5 and Dcards[0].value > flushHigh):
        flushHigh = Dcards[0].value
        flush = handStrength(5, Dcards[0].value, Dcards)

    if(lenCcards == 5 and Ccards[0].value > flushHigh):
        flushHigh = Ccards[0].value
        flush = handStrength(5, Ccards[0].value, Ccards)

    return flush


def haveQuinte(cards): #suite
    quinte = None

    cards.sort(key=lambda x: x.value, reverse=True) 

    # remove duplication
    outputWithoutDuplication = []
    for cardEquivalent in cards:
        if(sum([cardEquivalent.value == cardInTest for cardInTest in outputWithoutDuplication]) == 0):
            outputWithoutDuplication.append(cardEquivalent)

    if(len(outputWithoutDuplication) >= 5):
        for cardFollowId in range(len(outputWithoutDuplication)):
            outputCards = outputWithoutDuplication[cardFollowId:]
            outputCards = outputWithoutDuplication[:(cardFollowId + 5)]
            
            if(CardsFollow(outputCards)):
                quinte = handStrength(4, outputCards[0].value, outputCards)
                break

    return quinte


def haveBrelan(cards):
    brelan = None
    cardsBrelan = []

    for high in range(14, 1, -1):
        cardsBrelan = []
        for card in cards:
            if(card.value == high):
                cardsBrelan.append(card)

        count = len(cardsBrelan)
        
        if(count == 3):
            brelan = high

        if(brelan != None):
            break

    if(brelan != None):
        return handStrength(3, brelan, cardsBrelan)
    else:
        return brelan


def haveDouble(cards):
    double = None

    pair1 = havePair(cards)
    if(pair1 != None):
        cardsWithoutPair1 = Diff(cards, pair1.cards)
        pair2 = havePair(cardsWithoutPair1)
        if(pair2 != None):
            double = handStrength(2, pair1.high, pair1.cards)

    return double


def havePair(cards):
    pair = None
    cardsPair = []

    for high in range(14, 1, -1):
        cardsPair = []
        for card in cards:
            if(card.value == high):
                cardsPair.append(card)

        count = len(cardsPair)

        if(count == 2):
            pair = high

        if(pair != None):
            break

    if(pair != None):
        return handStrength(1, pair, cardsPair)
    else:
        return pair


def haveHigh(cards):
    output = None
    highestCard = None
    for i in range(len(cards)):
        if(highestCard == None  or highestCard.value < cards[i].value):
            highestCard = cards[i]

    if(highestCard != None):
        return handStrength(0, highestCard.value, [highestCard])
    else:
        return output