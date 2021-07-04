# substract array li2 to li1
def Diff(li1, li2): 
    return list(set(li1) - set(li2))


# calculate the promise of win
def ELV(probWin, reward, payed):
    return (probWin * reward) - ((1 - probWin) * payed)