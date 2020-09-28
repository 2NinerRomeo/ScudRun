#!/usr/bin/python3
#import random
class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
    def show(self):
        print ("{} of {}".format(self.value, self.suit))

        

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        
    def show(self):
        for c in self.cards:
            c.show()
        print ("there are " +str(len(self.cards))+ " total cards")
    def build(self):
        # to do: there are 3 great parades, 3 magic eyes, 3 mind readers
        for s in ["acrobat",
                  "aerialist",
                  "clown",
                  "contortionist",
                  "dancer",
                  "magician",
                  "sharp-shooter",
                  "sideshow",
                  "strongman",
                  "tamer"]:
            for v in range(0, 8):
                self.cards.append(Card(s, v))
class Player:
    def __init__(self):
        pass

    
#=============    Definitions above here, action below  =============
deck = Deck()
deck.show()
