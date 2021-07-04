import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
import glob
from threading import Thread

from MonteCarlo.MonteCarloSimulation import MonteCarloSimulation
from MonteCarlo.Card import Card

class Example():
    def __init__(self):
        # init
        self.allButtons = []
        self.playerCards = []
        self.boardCards = []

        # gui
        self.root = tk.Tk()
        self.root.title("Poker action calculator")

        self.can_call = tk.IntVar()

        # action
        self.action = tk.Label(self.root, text='...', font='Times 20 bold')
        self.action.grid(row=0, column=0, columnspan=2, sticky="NSEW")

        # nb player
        self.nbPlayer = tk.Label(self.root, text='Player number :')
        self.nbPlayer.grid(row=1, column=0, sticky="E", padx=20)

        self.nbPlayerEntry = tk.Entry(self.root)
        self.nbPlayerEntry.insert(0, 2)
        self.nbPlayerEntry.grid(row=1, column=1, sticky="W")


        # calculation time
        self.calculationTime = tk.Label(self.root, text='Calculation time :')
        self.calculationTime.grid(row=2, column=0, sticky="E", padx=20)

        self.calculationTimeEntry = tk.Entry(self.root)
        self.calculationTimeEntry.insert(0, 1000)
        self.calculationTimeEntry.grid(row=2, column=1, sticky="W")


        # can check
        self.checkboxCanCall = tk.Checkbutton(self.root, text="Can check", variable=self.can_call)
        self.checkboxCanCall.grid(row=3, column=0, columnspan=2, sticky='WESN')


        # player's card
        self.playerCard = tk.Label(self.root, text='Player\'s card :')
        self.playerCard.grid(row=4, column=0, sticky="W")


        # players cards
        cardTypes = {'c', 's', 'd', 'h'}
        typeCardPlayerId = 0
        for typeLetter in cardTypes:
            self.cardButton_frame_player = tk.Frame(self.root)

            for imgCardPath in glob.glob('cards/*'+typeLetter+'.png'):
                rot = Image.open(imgCardPath)
                rot = rot.resize((20, 20), Image.ANTIALIAS)
                rotunda = ImageTk.PhotoImage(rot)
                cardButton = tk.Button(self.cardButton_frame_player, image=rotunda, relief=tk.FLAT)
                cardButton.image = rotunda
                addPlayerCardFunc = partial(self.addCardToPlayer, imgCardPath, cardButton)
                cardButton.configure(command=addPlayerCardFunc)
                cardButton.pack(side=tk.LEFT)
                self.allButtons.append(cardButton)

            self.cardButton_frame_player.grid(row=5 + typeCardPlayerId, column=0, columnspan=2, sticky="EW")
            typeCardPlayerId += 1


        # board's card
        self.playerCard = tk.Label(self.root, text='Board\'s card :')
        self.playerCard.grid(row=5 + typeCardPlayerId + 1, column=0, sticky="W")


        # board cards
        typeCardBoardId = 0
        for typeLetter in cardTypes:
            self.cardButton_frame_board = tk.Frame(self.root)

            for imgCardPath in glob.glob('cards/*'+typeLetter+'.png'):
                rot = Image.open(imgCardPath)
                rot = rot.resize((20, 20), Image.ANTIALIAS)
                rotunda = ImageTk.PhotoImage(rot)
                cardButton = tk.Button(self.cardButton_frame_board, image=rotunda, relief=tk.FLAT)
                cardButton.image = rotunda
                addBoardCardFunc = partial(self.addCardToBoard, imgCardPath, cardButton)
                cardButton.configure(command=addBoardCardFunc)
                cardButton.pack(side=tk.LEFT)
                self.allButtons.append(cardButton)

            self.cardButton_frame_board.grid(row=5 + typeCardPlayerId + 2 + typeCardBoardId, column=0, columnspan=2, sticky="EW")
            typeCardBoardId += 1


        # buttons
        self.goButton = tk.Button(self.root, text="Go !", command=self.run)
        self.goButton.grid(row=5 + typeCardPlayerId + 1 + typeCardBoardId + 1, column=0, sticky="NSEW")

        self.clearButton = tk.Button(self.root, text="Clear", command=self.clear)
        self.clearButton.grid(row=5 + typeCardPlayerId + 1 + typeCardBoardId + 1, column=1, sticky="NSEW")



        # grid config
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.action['text'] = '...'

        self.root.mainloop()




    def run(self):
        self.action['text'] = 'Processing...'
        thread = Thread(target = self.threadedCalcul)

        thread.start()



    def clear(self):
        for buttonCard in self.allButtons:
            buttonCard.configure(state="normal")

        self.playerCards = []
        self.boardCards = []

        self.action['text'] = '...'


    def addCardToPlayer(self, value, button):
        button.configure(state="disabled")
        cardArray = value.split(".png")
        cardArray = cardArray[0].split("cards\\")
        card = cardArray[1]
        
        numberCard = str(int(card[:-1]))
        typeCard = (card[-1:]).upper()

        card = Card(typeCard, numberCard)
        self.playerCards.append(card)



    def addCardToBoard(self, value, button):
        button.configure(state="disabled")
        cardArray = value.split(".png")
        cardArray = cardArray[0].split("cards\\")
        card = cardArray[1]
        
        numberCard = str(int(card[:-1]))
        typeCard = (card[-1:]).upper()

        card = Card(typeCard, numberCard)
        self.boardCards.append(card)



    def threadedCalcul(self):
        playerCard1 = self.playerCards[0].toString() if len(self.playerCards) >= 1 else None
        playerCard2 = self.playerCards[1].toString() if len(self.playerCards) >= 2 else None

        boardCard1 = self.boardCards[0].toString() if len(self.boardCards) >= 1 else None
        boardCard2 = self.boardCards[1].toString() if len(self.boardCards) >= 2 else None
        boardCard3 = self.boardCards[2].toString() if len(self.boardCards) >= 3 else None
        boardCard4 = self.boardCards[3].toString() if len(self.boardCards) >= 4 else None
        boardCard5 = self.boardCards[4].toString() if len(self.boardCards) >= 5 else None
        

        win_rate = MonteCarloSimulation(int(self.calculationTimeEntry.get()), int(self.nbPlayerEntry.get()), playerCard1, playerCard2, boardCard1, boardCard2, boardCard3, boardCard4, boardCard5).run()
        
        print(win_rate)

        call_amount = 0
        mini = 1
        maxi = 100

        amount = 0
        rateToPlay = (1 / int(self.nbPlayerEntry.get()))
        if win_rate > rateToPlay:
            if win_rate > rateToPlay * 1.3:
                # If it is extremely likely to win, then raise as much as possible
                action = 'raise'
                amount = maxi
            elif win_rate > rateToPlay * 1.10:
                # If it is likely to win, then raise by the minimum amount possible
                action = 'raise'
                amount = mini
            else:
                # If there is a chance to win, then call
                action = 'call'
        else:
            action = 'call' if self.can_call.get() == 1 and call_amount == 0 else 'fold'
        
        self.action['text'] = 'Action: ' + action + ', Value:' + str(amount) + ', (probability : ' + str(win_rate) + ')'


Example()