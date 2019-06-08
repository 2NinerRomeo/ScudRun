#!/usr/bin/python

import random
import os
import curses

def intro(win):
    #Game Message
    win.addstr("\nYou have 20 turns to guess the position of a 1 x 1 battleship\n");
    win.addstr("Move the cursor with the arrows. SPACE to fire\n");

class game:
    def rand_col(self):
        return random.randint(0, len(self.board[0]) - 1)
    def rand_row(self):
        return random.randint(0, len(self.board) - 1)
    def shot(self,row,col):
        if row == self.shipRow and col == self.shipCol:
           self.board[row][col] = '#'
           return True
        else:
           self.board[row][col] = chr(46)
           return False
    def __init__(self):
        self.board = []
        for x in range(10):
            self.board.append(['O'] * 10)
        #Define Random Selection
        #Define Ship Position
        self.shipRow = self.rand_row()
        self.shipCol = self.rand_col()
        print("Dev Row: ", self.shipRow)
        print("Dev Col: ", self.shipCol)


class gameInterface:
    def __init__(self,theGame):
        self.cursor = [4,4];
        self.height = len(theGame.board);
        self.width = len(theGame.board[0]);
    def cursorHorz(self,right):
        if(right and self.cursor[1] < self.width -1):
           self.cursor[1] = self.cursor[1] + 1;
        if(not right and self.cursor[1] > 0):
           self.cursor[1] = self.cursor[1] - 1;
        print self.cursor;
    def cursorVert(self,up):
        if(up and self.cursor[0] > 0):
           self.cursor[0] = self.cursor[0] - 1;
        if(not up and self.cursor[0] < self.height -1):
           self.cursor[0] = self.cursor[0] + 1;
        print self.cursor;
    def printBoard(self,win):
        win.clear();
        for row in range(len(theGame.board)):
            if(row == self.cursor[0]):
                if(0 == self.cursor[1]):
                    win.addstr(" ".join(theGame.board[row][0:self.cursor[1]]) + "[" + theGame.board[row][self.cursor[1]] + "]" + " ".join(theGame.board[row][self.cursor[1]+1:len(theGame.board[row])]) + "\n")
                else:
                    win.addstr(" " + " ".join(theGame.board[row][0:self.cursor[1]]) + "[" + theGame.board[row][self.cursor[1]] + "]" + " ".join(theGame.board[row][self.cursor[1]+1:len(theGame.board[row])]) + "\n")
            else:
                win.addstr(" " + " ".join(theGame.board[row]) + "\n");
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
#   printBoard(board,cursor);

theGame = game();
iface = gameInterface(theGame);


def main(win):
    win.nodelay(True)
    key=""
    win.clear()
    iface.printBoard(win)
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
                 iface.printBoard(win)
            if key == "KEY_LEFT":
                 iface.cursorHorz(False)
                 iface.printBoard(win)
            if key == "KEY_UP":
                 try:
                     iface.cursorVert(True)
                 except Exception as e:
                     win.addstr(str(e))
                 iface.printBoard(win)
            if key == "KEY_DOWN":
                 iface.cursorVert(False)
                 iface.printBoard(win)
            if key == " ":
                 shotstr = "FIRE!\n"
                 if(theGame.shot(iface.cursor[0],iface.cursor[1])):
                     shotstr = "****Hit!*****\n"
                 else:
                     shotstr =  "----Miss!---\n"
                 iface.printBoard(win)
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

curses.wrapper(main)
