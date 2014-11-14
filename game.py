import numpy as np
import random
import os

SIZE = 4

def printGF(gamefield):
    border ='+' + ''.join([('-') for i in range(SIZE*8-1)]) + '+'
    emptyRow ='|' + ''.join([('|' if i%8==7 else ' ') for i in range(SIZE*8)])
    mid ='|' + ''.join([('|' if i%8==7 else '-') for i in range(SIZE*8)])
    def printEmptyRow():
        for k in range(1):
            print(emptyRow)
    print(border)
    def spacedprINT(n):
        if n==0:
            return '      '
        digits = len(str(n))
        if digits==1:
            return '  ' + str(n)+ '   '
        if digits==2:
            return ' ' + str(n)+ '   '
        if digits==3:
            return ' ' + str(n)+ '  '
    for i,row in enumerate(gamefield.T):
        printEmptyRow()
        print('|'),
        for j,el in enumerate(row):
            print(spacedprINT(el)+'|'),
        print('\n'),
        printEmptyRow()
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
    else:
        print("ALL NODES ARE OCCUPIED!")

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

def step(gamefield):
    move('s',gamefield)
    move('n',gamefield)
    move('w',gamefield)
    move('e',gamefield)

if __name__ == '__main__':
    gamefield = np.zeros((SIZE,SIZE),dtype=np.int)
    for i in range(5):
        addRandom(gamefield)
    m = ' '
    while(True):
        clear()
        print('Made move: '+m)
        if m=='w':
            m='n'
        elif m=='a':
            m='w'
        elif m=='s':
            m='s'
        elif m=='d':
            m='e'
        if m in ['n','s','e','w']:
            move(m,gamefield)
            addRandom(gamefield)
        printGF(gamefield)
        m = raw_input("\nmove: ")
