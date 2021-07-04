class Card: 
    kind = ""
    value = 0
  
  
    # constructor 
    def __init__(self, kind, value): 
        self.kind = str(kind)
        self.value = int(value)


    def toString(self):
        return self.kind + str(self.value)


    def equalsTo(self, otherCard):
        return (self.kind == otherCard.kind and self.value == otherCard.value)


def stringToCard(stringCard):
        kind = stringCard[0]
        return Card(kind, stringCard[1:])


# check if the card array represente a suite (cards need to be reverse sort)
def CardsFollow(cards):
    output = True

    for i in range(len(cards) - 1):
        if(cards[i].value - 1 != cards[i + 1].value):
            output = False
    
    return output