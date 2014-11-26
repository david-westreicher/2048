import numpy as np
import random
import os
import math
import sys

SIZE = 4
DIRECTIONS = ['n','s','e','w']

class GetchWrapper(object):
    def __init__(self):
        try:
            import getch
            self.isReal = True
            self.getch = getch.getch
            self.input = self.realgetch
        except ImportError:
            self.isReal = False
            self.input = self.virtualgetch

    def realgetch(self):
        m = self.getch()
        if m=='\033':
            # special keys
            if self.getch()=='\033':
                # ESC key
                return m
            m = self.getch()
        return m

    def virtualgetch(self):
        return raw_input()

def printGF(gamefield):
    border ='+' + ''.join([('-') for i in range(SIZE*8-1)]) + '+'
    mid ='|' + ''.join([('+' if i%8==7 else ' ') for i in range(SIZE*8-1)]) +'|'
    def getcol(n):
        if n==0:
            return '\033[49m'
        col = int(math.log(n,2))-1
        if col>=7:
            col+=1
        return '\033[48;5;'+str(col)+'m'
    def printEmptyRow(rownum):
        row = '|'
        for j,el in enumerate(rownum):
            row += getcol(el)
            for i in range(7):
                row += ' '
            row += '\033[49m'
            row += ' ' if j<SIZE-1 else '|'
        print(row)
    def spacedprINT(n):
        if n==0:
            return '       '
        retStr = getcol(n)
        digits = len(str(n))
        before = (7-digits)/2
        for i in range(before):
            retStr += ' '
        retStr += str(n)
        for i in range(7-(before+digits)):
            retStr += ' '
        return retStr + '\033[49m'

    print(border)
    for i,row in enumerate(gamefield.T):
        printEmptyRow(row)
        rowstr = '|'
        for j,el in enumerate(row):
            rowstr += spacedprINT(el)+(' ' if j<SIZE-1 else '|')
        print(rowstr)
        printEmptyRow(row)
        if i<SIZE-1:
            print(mid)
    print(border) 
    
def addRandom(gamefield):
    possPos = []
    for i,row in enumerate(gamefield):
        for j,el in enumerate(row):
            if el == 0:
                possPos.append([i,j])
    if(len(possPos)>0):
        posToChange = possPos[int(random.random()*len(possPos))]
        gamefield[posToChange[0]][posToChange[1]] = 2 if random.random()>0.1 else 4

# returns TRUE iff move did change the gamefield
def move(direction,gamefield):
    if not direction in DIRECTIONS:
        return False

    def flip(gf):
        tmpfield = gf.copy()
        if(direction=='s'):
            for i in range(SIZE):
                for j in range(SIZE):
                    tmpfield[i][SIZE-j-1] = gf[i][j]
        elif(direction=='e'):
            for i in range(SIZE):
                for j in range(SIZE):
                    tmpfield[SIZE-i-1][SIZE-j-1] = gf.T[i][j]
        elif(direction=='w'):
            tmpfield = gf.T.copy()
        return tmpfield
    
    def condense():
        lastOccupied = [0 for i in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                val = tmpfield[i][j]
                if(val==0):
                    continue
                tmpfield[i][j] = 0
                tmpfield[i][lastOccupied[i]] = val
                lastOccupied[i]+=1

    tmpfield = flip(gamefield)
    condense()
    for i in range(SIZE):
        for j in range(SIZE-1):
            if(tmpfield[i][j]==tmpfield[i][j+1]):
                tmpfield[i][j]*=2
                tmpfield[i][j+1]=0
    condense()
    newgamefield = flip(tmpfield)

    change = False
    for i,row in enumerate(newgamefield):
        for j,el in enumerate(row):
            if gamefield[i][j] != newgamefield[i][j]:
                change = True
            gamefield[i][j] = newgamefield[i][j]
    return change

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    sys.stdout.write('\033[97m')

def prettyPrint(text):
    while len(text)>SIZE*8:
        split = text.split(" ")
        curr = ""
        i = 0
        while len(curr+split[i])<SIZE*8:
            curr += split[i]+" "
            i += 1
        prettyPrint(curr)
        text = " ".join(split[i:])

    out = ""
    for i in range(SIZE*8/2-len(text)/2 + 1):
        out+=" "
    print(out+text)

def setupControls():
    dic = {}
    dic['n'] = ['w', 'A']
    dic['s'] = ['s', 'B']
    dic['e'] = ['d', 'C']
    dic['w'] = ['a', 'D']
    dic['exit'] = ['q', 'Q', '\033']
    revDic = {}
    for el in dic:
        for c in dic[el]:
            revDic[c] = el
    return revDic

def isFull(gf):
    for row in gf:
        for el in row:
            if el==0:
                return False
    return True

def movePossible(gamefield):
    for direction in DIRECTIONS:
        gf = gamefield.copy()
        if move(direction,gf):
            return True
    return False

def printDescription(hasGetch):
    prettyPrint('Welcome to 2048!')
    prettyPrint('You can use W/S/A/D or the arrow keys to shift the blocks into a direction.')
    prettyPrint('If two blocks with the same number "n" collide, they merge into a new block "n*2"')
    prettyPrint('Create a block with the number "2048" and you win!')
    if not hasGetch:
        print('\n')
        print('\033[48;5;1mWARNING!\033[49m')
        print('It seems that you haven\'t installed "getch".')
        print('Without "getch" you can\'t use the arrow keys')
        print('and you have to press enter after every move :(')
        print('Visit "https://pypi.python.org/pypi/getch"')
        print('download "getch-1.0-python2.tar.gz", untar and')
        print('enter "sudo python setup.py install"\n')
    prettyPrint('Enter your move:')

if __name__ == '__main__':
    getch = GetchWrapper()
    controls = setupControls()
    gamefield = np.zeros((SIZE,SIZE),dtype=np.int)
    for i in range(SIZE*SIZE/4):
        addRandom(gamefield)

    firstRun = True
    while(True):
        clear()
        printGF(gamefield)
        if firstRun:
            printDescription(getch.isReal)
            firstRun = False
        m = controls.get(getch.input(),None)
        if move(m,gamefield):
            addRandom(gamefield)
        elif (isFull(gamefield) and not movePossible(gamefield)) or m=='exit':
            break
    prettyPrint('GAME OVER!')
