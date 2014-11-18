import numpy as np
import random
import os
import math

SIZE = 4

def printGF(gamefield):
    border ='+' + ''.join([('-') for i in range(SIZE*8-1)]) + '+'
    mid ='|' + ''.join([('+' if i%8==7 else ' ') for i in range(SIZE*8-1)]) +'|'
    print(border)
    def getcol(n):
        if n==0:
            return '\033[49m'
        col = int(math.log(n,2))-1
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
    #print(possPos)
    if(len(possPos)>0):
        posToChange = possPos[int(random.random()*len(possPos))]
        #print(posToChange)
        gamefield[posToChange[0]][posToChange[1]] = 2 if random.random()>0.5 else 4
        return posToChange 
    else:
        return None

def move(direction,gamefield):
    if not direction in ['n','s','e','w']:
        print('Cant move to ' + direction)
        return
    # print(direction)
    tmpfield = gamefield.copy()
    if(direction=='s'):
        #flip y
        for i in range(SIZE):
            for j in range(SIZE):
                tmpfield[i][SIZE-j-1] = gamefield[i][j]
    elif(direction=='e'):
        #flip x,y
        for i in range(SIZE):
            for j in range(SIZE):
                tmpfield[SIZE-i-1][SIZE-j-1] = gamefield.T[i][j]
    elif(direction=='w'):
        #flip x,y
        tmpfield = gamefield.T.copy()
    
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
    
    condense()
    for i in range(SIZE):
        for j in range(SIZE-1):
            if(tmpfield[i][j]==tmpfield[i][j+1]):
                tmpfield[i][j]*=2
                tmpfield[i][j+1]=0
    condense()

    newgamefield = tmpfield.copy()
    if(direction=='s'):
        #flip y
        for i in range(SIZE):
            for j in range(SIZE):
                newgamefield[i][SIZE-j-1] = tmpfield[i][j]
    elif(direction=='e'):
        #flip x,y
        for i in range(SIZE):
            for j in range(SIZE):
                newgamefield[SIZE-i-1][SIZE-j-1] = tmpfield.T[i][j]
    elif(direction=='w'):
        #flip x,y
        newgamefield = tmpfield.T.copy()
    # printGF(newgamefield)
    for i,row in enumerate(newgamefield):
        for j,el in enumerate(row):
            gamefield[i][j] = newgamefield[i][j]

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    print(c_WHITE),

def step(gamefield):
    move('s',gamefield)
    move('n',gamefield)
    move('w',gamefield)
    move('e',gamefield)

def printGameOver():
    out = ""
    goStr = "GAME OVER!"
    for i in range(SIZE*8/2-len(goStr)/2 + 1):
        out+=" "
    print(out+goStr)
c_WHITE = '\033[97m'
if __name__ == '__main__':
    gamefield = np.zeros((SIZE,SIZE),dtype=np.int)
    for i in range(SIZE*SIZE/4):
        addRandom(gamefield)
    m = ' '
    while(True):
        clear()
        print('Made move: '+m)
        #for i in range(30,54):
        #    print('\033['+str(i)+'mBlue')
        if m=='w':
            m='n'
        elif m=='a':
            m='w'
        elif m=='s':
            m='s'
        elif m=='d':
            m='e'
        gameOver = False
        if m in ['n','s','e','w']:
            move(m,gamefield)
            gameOver = True if addRandom(gamefield) is None else False
        printGF(gamefield)
        if gameOver:
            printGameOver()
            break
        m = raw_input("\nmove: ")
