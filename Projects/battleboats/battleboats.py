#!/usr/bin/python

import random
import os
import curses
import pdb

def intro(win):
    #Game Message
    win.addstr("\nYou have 20 turns to guess the position of a 1 x 1 battleship\n");
    win.addstr("Move the cursor with the arrows. SPACE to fire\n");

class Space:
    def __init__(self):
        self.isBoat = False;
        self.cleared = False;

class Board:
    def __init__(self,rows,cols):
         self.rows = rows
         self.cols = cols
         self.spaces = []
         self.disp = []
         self.xray = []
         for x in range(rows):
             self.spaces.append([Space() for count in range(cols)])
             self.disp.append(['O'] * cols)
             self.xray.append([chr(46)] * cols)
    def set_boat(self,row,col,char):
        self.spaces[row][col].isBoat = True;
        self.xray[row][col] = char
    def shot(self,row,col):
        if(self.spaces[row][col].isBoat):
           self.disp[row][col] = char
        else:
           self.disp[row][col] = chr(46)
        return self.spaces[row][col].isBoat

class Boat:
    def __init__(self, size, name, char):
        self.size = size
        placed = False
        self.spaces = []
        self.name = name
        self.char = char
    def checkPlacement(self,boats,board):
        #Check for fit on board
        #if self.boatOffBoard(board):
        #    pass
        #check for conflict with other boats
        for boat in boats:
            if self.collidedWithOtherBoat(boat):
                return False
        #If we get through all the checks...
        return True

    def boatOffBoard(self,board):
        if self.vert:
            if self.length + self.row > board.rows:
                print("Vert Boat at: " +
                      str(self.length + self.row) +
                      " > board rows: " +
                      str(board.rows))
                return True
        else:
            if self.length + self.cols > board.rows:
                print("Horz Boat at: " +
                      str(self.length + self.row) +
                      " > board rows: " +
                      str(board.rows))
                return True
        #TODO: See if the boad is contained within the board
        return False;
    def collidedWithOtherBoat(self,boat):
        # See if the boat conflicts with other boats
        def spaceCollision(self,rowcol,boat):
            for s in boat.spaces:
                if s[0] == rowcol:
                    print(f"Boat collision at {s[0]} - Resetting {self.name}")
                    return True
            return False
        if self.vert:  #search this column
            for row in range(self.row,self.row+self.size):
                if spaceCollision(self,(row,self.col),boat):
                    return True
        else: #search this row
            for col in range(self.col,self.col+self.size):
                if spaceCollision(self,(self.row,col),boat):
                    return True
        return False

    def randomPosition(self,board):
        self.vert = random.choice([True, False])
        if(self.vert):
            self.row = random.randint(0,board.rows -1 -self.size)
            self.col = random.randint(0,board.cols -1)
        else:
            self.row = random.randint(0,board.rows -1)
            self.col = random.randint(0,board.cols -1 -self.size)

    def autoPlace(self,boats,board):
        placementOk = False
        while(not placementOk):
            #Choose a place for the boat.
            self.randomPosition(board)
            placementOk = self.checkPlacement(boats,board)

        #Indicate occupation of spaces on the board
        for i in range(self.size):
            if(self.vert):
                self.spaces.append([(self.row+i,self.col), False])
                board.set_boat(self.row+i,self.col,self.char);
            else:
                self.spaces.append([(self.row,self.col+i), False])
                board.set_boat(self.row,self.col+i,self.char);

class Game:
    #def rand_col(self):
    #    return random.randint(0, self.board.cols - 1)
    #def rand_row(self):
    #    return random.randint(0, self.board.rows - 1)
    def shot(self,row,col):
        return self.board.shot(row,col)
    def createBoats(self):
        self.allBoats = []
        self.allBoats.append(Boat(5,"Carrier","A"))
        self.allBoats.append(Boat(4,"Battleship","B"))
        self.allBoats.append(Boat(3,"Cruiser","C"))
        self.allBoats.append(Boat(3,"Submarine","S"))
        self.allBoats.append(Boat(2,"PT Boat","T"))
    def placeBoatsAuto(self):
        #place boats on board
        self.activeBoats = []
        for boat in self.allBoats:
            boat.autoPlace(self.activeBoats,self.board)
            self.activeBoats.append(boat)
    def placeBoats(self):
        self.placeBoatsAuto()
        #TODO: branch for manual boat placement
        #Might require the interface to place them, or check
    def __init__(self):
        self.board = Board(10,10)
        self.createBoats()
        self.placeBoats()


class GameInterface:
    def __init__(self,theGame):
        self.cursor = [4,4]
        self.height = theGame.board.rows
        self.width = theGame.board.cols
    def cursorHorz(self,right):
        if(right and self.cursor[1] < self.width -1):
           self.cursor[1] = self.cursor[1] + 1
        if(not right and self.cursor[1] > 0):
           self.cursor[1] = self.cursor[1] - 1
        print(self.cursor)
    def cursorVert(self,up):
        if(up and self.cursor[0] > 0):
           self.cursor[0] = self.cursor[0] - 1;
        if(not up and self.cursor[0] < self.height -1):
           self.cursor[0] = self.cursor[0] + 1;
        print(self.cursor)
    def print_board(self,win):
        win.clear();
        for row in range(theGame.board.rows):
            if(row == self.cursor[0]):
                if(0 == self.cursor[1]):
                    win.addstr(" ".join(theGame.board.disp[row][0:self.cursor[1]]) +
                               "[" + theGame.board.disp[row][self.cursor[1]] + "]" +
                               " ".join(theGame.board.disp[row][self.cursor[1]+1:len(theGame.board.disp[row])]) + "\n")
                else:
                    win.addstr(" " + " ".join(theGame.board.disp[row][0:self.cursor[1]]) +
                               "[" + theGame.board.disp[row][self.cursor[1]] + "]" +
                               " ".join(theGame.board.disp[row][self.cursor[1]+1:len(theGame.board.disp[row])]) + "\n")
            else:
                win.addstr(" " + " ".join(theGame.board.disp[row]) + "\n");
        win.addstr(str(self.cursor[0]) + " "+ str(self.cursor[1]) + "\n")
    def print_xray(self,win):
        win.clear();
        for row in range(theGame.board.rows):
            if(row == self.cursor[0]):
                if(0 == self.cursor[1]):
                    win.addstr(" ".join(theGame.board.xray[row][0:self.cursor[1]]) +
                               "[" + theGame.board.xray[row][self.cursor[1]] + "]" +
                               " ".join(theGame.board.xray[row][self.cursor[1]+1:len(theGame.board.xray[row])]) + "\n")
                else:
                    win.addstr(" " + " ".join(theGame.board.xray[row][0:self.cursor[1]]) +
                               "[" + theGame.board.xray[row][self.cursor[1]] + "]" +
                               " ".join(theGame.board.xray[row][self.cursor[1]+1:len(theGame.board.xray[row])]) + "\n")
            else:
                win.addstr(" " + " ".join(theGame.board.xray[row]) + "\n");
        win.addstr(str(self.cursor[0]) + " "+ str(self.cursor[1]) + "\n")
        #print row;
        #print cur;
        #print cur[0];
        #print cur[1];

#get input from the user
def getInput(rowOrCol):
   val = -1;
   while(val < 0 or val > 10):
      val = input(rowOrCol);
   return val - 1;
#Get user Column



#Display Board

#for turn in range(20):
#   print "Turn: " + str(turn + 1);
#   guessRow = getInput("row: ");
#   guessCol = getInput("col: ");
#   board[guessRow][guessCol] = 'x';
#   print_board(board,cursor);

theGame = Game();
iface = GameInterface(theGame);


def main(win):
    win.nodelay(True)
    key=""
    win.clear()
    iface.print_board(win)
    iface.print_xray(win)
    intro(win)
    #win.addstr("Detected key:")
    while 1:
        try:
            key = win.getkey()
            if key == os.linesep or key == 'q':
                break;
            if key == "KEY_RIGHT":
                 #pass
                 try:
                     iface.cursorHorz(True)
                 except Exception as e:
                     win.addstr(str(e))
                 iface.print_board(win)
            if key == "KEY_LEFT":
                 iface.cursorHorz(False)
                 iface.print_board(win)
            if key == "KEY_UP":
                 try:
                     iface.cursorVert(True)
                 except Exception as e:
                     win.addstr(str(e))
                 iface.print_board(win)
            if key == "KEY_DOWN":
                 iface.cursorVert(False)
                 iface.print_board(win)
            if key == " ":
                 shotstr = "FIRE!\n"
                 if(theGame.shot(iface.cursor[0],iface.cursor[1])):
                     shotstr = "****Hit!*****\n"
                 else:
                     shotstr =  "----Miss!---\n"
                 iface.print_board(win)
                 win.addstr(shotstr)
            #win.addstr(key + "\n")
            #win.addstr("0 "+ str(iface.cursor[0]) + "\n")
            #win.addstr("1 "+ str(iface.cursor[1]) + "\n")
            #else:
            #    win.clear()
            #    win.addstr("Detected key: ")
            #    win.addstr(str(key))
        except Exception as e:
            pass


if(__name__ == "__main__"):
   import argparse
   
   parser = argparse.ArgumentParser(description = "Battle Boats! - Programming for fun.")
   parser.add_argument("--debug", action ="store_true", help="Debug for the developer")

   curses.wrapper(main)
