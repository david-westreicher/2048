import numpy as np
import random
import os
import math
import sys
import getch

SIZE = 4

def printGF(gamefield):
    border ='+' + ''.join([('-') for i in range(SIZE*8-1)]) + '+'
    mid ='|' + ''.join([('+' if i%8==7 else ' ') for i in range(SIZE*8-1)]) +'|'
    print(border)
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

# returns TRUE iff move did change the gamefield
def move(direction,gamefield):
    if not direction in ['n','s','e','w']:
        #print('Cant move to ' + str(direction))
        return False
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

def printGameOver():
    out = ""
    goStr = "GAME OVER!"
    for i in range(SIZE*8/2-len(goStr)/2 + 1):
        out+=" "
    print(out+goStr)

def setupControls():
    dic = {}
    dic['n'] = ['w', 'A']
    dic['s'] = ['s', 'B']
    dic['e'] = ['d', 'C']
    dic['w'] = ['a', 'D']
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

if __name__ == '__main__':
    gamefield = np.zeros((SIZE,SIZE),dtype=np.int)
    for i in range(SIZE*SIZE/4):
        addRandom(gamefield)
    controls = setupControls()
    m = ' '
    while(True):
        clear()
        print('\033[4mMade move:\033[24m '+m)
        c = controls.get(m,None)
        if move(c,gamefield):
            if addRandom(gamefield) is None:
                break
        elif isFull(gamefield):
                break
        printGF(gamefield)
        print("\nmove:"),
        m = getch.getch()
        if m=='\033':
            m = getch.getch()
            m = getch.getch()
    printGF(gamefield)
    printGameOver()
