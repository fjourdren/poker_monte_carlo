class Player: 
    card1 = None
    card2 = None
    handStrength = None
    handStrength2 = None

    # reset player's cards and his handStrength
    def removeCards(self):
        self.card1 = None
        self.card2 = None
        self.handStrength = None
        self.handStrength2 = None