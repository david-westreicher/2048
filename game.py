import numpy as np
import random
import os
import math
import sys
import time
from collections import Counter

SIZE = 4
DIRECTIONS = ['u', 'd', 'r', 'l']

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
        if m == '\033':
            # special keys
            if self.getch() == '\033':
                # ESC key
                return m
            m = self.getch()
        return m

    def virtualgetch(self):
        return input()

def printGF(gamefield, depth=0):
    border = ('\t' * depth) + '+' + ''.join([('-') for i in range(SIZE * 8 - 1)]) + '+'
    mid = '|' + ''.join([('+' if i % 8 == 7 else ' ') for i in range(SIZE * 8 - 1)]) + '|'

    def getcol(n):
        if n == 0:
            return '\033[49m'
        col = int(math.log(n, 2)) - 1
        if col >= 7:
            col += 1
        return '\033[48;5;' + str(col) + 'm'

    def printEmptyRow(rownum):
        row = '|'
        for j, el in enumerate(rownum):
            row += getcol(el)
            for i in range(7):
                row += ' '
            row += '\033[49m'
            row += ' ' if j < SIZE - 1 else '|'
        print('\t' * depth + row)

    def spacedprINT(n):
        if n == 0:
            return '       '
        retStr = getcol(n)
        digits = len(str(n))
        before = (7 - digits) // 2
        for i in range(before):
            retStr += ' '
        retStr += str(n)
        for i in range(7 - (before + digits)):
            retStr += ' '
        return retStr + '\033[49m'

    print(border)
    for i, row in enumerate(gamefield.T):
        printEmptyRow(row)
        rowstr = '|'
        for j, el in enumerate(row):
            rowstr += spacedprINT(el) + (' ' if j < SIZE - 1 else '|')
        print('\t' * depth + rowstr)
        printEmptyRow(row)
        if i < SIZE - 1:
            print('\t' * depth + mid)
    print(border)

def addRandom(gamefield):
    possPos = []
    for i, row in enumerate(gamefield):
        for j, el in enumerate(row):
            if el == 0:
                possPos.append([i, j])
    if(len(possPos) > 0):
        posToChange = possPos[int(random.random() * len(possPos))]
        gamefield[posToChange[0]][posToChange[1]] = 2 if random.random() > 0.1 else 4

# returns TRUE iff move did change the gamefield
def move(direction, gamefield):
    if direction not in DIRECTIONS:
        return False

    def flip(gf):
        tmpfield = gf.copy()
        if(direction == 'd'):
            for i in range(SIZE):
                for j in range(SIZE):
                    tmpfield[i][SIZE - j - 1] = gf[i][j]
        elif(direction == 'r'):
            for i in range(SIZE):
                for j in range(SIZE):
                    tmpfield[SIZE - i - 1][SIZE - j - 1] = gf.T[i][j]
        elif(direction == 'l'):
            tmpfield = gf.T.copy()
        return tmpfield

    def condense():
        lastOccupied = [0 for i in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                val = tmpfield[i][j]
                if(val == 0):
                    continue
                tmpfield[i][j] = 0
                tmpfield[i][lastOccupied[i]] = val
                lastOccupied[i] += 1

    tmpfield = flip(gamefield)
    condense()
    for i in range(SIZE):
        for j in range(SIZE - 1):
            if(tmpfield[i][j] == tmpfield[i][j + 1]):
                tmpfield[i][j] *= 2
                tmpfield[i][j + 1] = 0
    condense()
    newgamefield = flip(tmpfield)

    change = False
    for i, row in enumerate(newgamefield):
        for j, el in enumerate(row):
            if gamefield[i][j] != newgamefield[i][j]:
                change = True
            gamefield[i][j] = newgamefield[i][j]
    return change

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write('\033[97m')

def prettyPrint(text):
    while len(text) > SIZE * 8:
        split = text.split(' ')
        curr = ''
        i = 0
        while len(curr + split[i]) < SIZE * 8:
            curr += split[i] + ' '
            i += 1
        prettyPrint(curr)
        text = ' '.join(split[i:])

    out = ''
    for i in range(SIZE * 8 // 2 - len(text) // 2 + 1):
        out += ' '
    print(out + text)

def setupControls():
    dic = {}
    dic['u'] = ['w', 'A', 'k']
    dic['d'] = ['s', 'B', 'j']
    dic['r'] = ['d', 'C', 'l']
    dic['l'] = ['a', 'D', 'h']
    dic['exit'] = ['q', 'Q', '\033']
    revDic = {}
    for el in dic:
        for c in dic[el]:
            revDic[c] = el
    return revDic

def isFull(gf):
    for row in gf:
        for el in row:
            if el == 0:
                return False
    return True

def movePossible(gamefield):
    for direction in DIRECTIONS:
        gf = gamefield.copy()
        if move(direction, gf):
            return True
    return False

def printDescription(hasGetch):
    prettyPrint('Welcome to 2048!')
    prettyPrint('You can use W/S/A/D or the arrow keys to shift the blocks into a direction.')
    prettyPrint('If two blocks with the same number "n" collide, they merge into a new block "n*2"')
    prettyPrint('Create a block with the number "2048" and you win!')
    print('\n')
    prettyPrint('Press \'Q\' or ESC twice to exit. ')
    if not hasGetch:
        print('\n')
        print('\033[48;5;1mWARNING!\033[49m')
        print('It seems that you haven\'t installed "getch".')
        print('Without "getch" you can\'t use the arrow keys')
        print('and you have to press enter after every move :(')
        print('Visit "https://pypi.python.org/pypi/getch"')
        print('download "getch-1.0-python2.tar.gz", untar and')
        print('enter "sudo python setup.py install"\n')
    print('\n')
    prettyPrint('Enter your move:')

def heuristic(gf):
    empties = 0
    max_cell = np.max(gf)
    corner_max = False
    for i, row in enumerate(gf):
        for j, el in enumerate(row):
            # corner
            if i in [0, SIZE - 1] and j in [0, SIZE - 1]:
                if el == max_cell:
                    corner_max = True
            if el == 0:
                empties += 1
    return max_cell * (empties + 1) * (2 if corner_max else 1)
    # return 10000 if corner_max else 1

def heuristic(gf):
    points = 0
    cells = []
    empty_cells = 0
    max_cell = np.max(gf)
    corner_max = False
    for i in range(SIZE):
        for j in range(SIZE):
            cell = gf[i][j]
            if cell == 0:
                empty_cells += 1
                continue
            if i in [0, SIZE - 1] and j in [0, SIZE - 1]:
                if cell == max_cell:
                    corner_max = True
            cells.append(cell)
            neighs = []
            for ox, oy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                x = i + ox
                y = j + oy
                if x < 0 or y < 0 or x >= SIZE or y >= SIZE:
                    continue
                neigh = gf[x][y]
                if neigh == 0:
                    continue
                neighs.append(neigh)
    for cell, count in Counter(cells).items():
        if count == 1:
            points += cell
    return points * (empty_cells + 1) * (2 if corner_max else 1)

def gen_children_player(gamefield):
    for direction in ['l', 'd', 'u', 'r']:
        gf = gamefield.copy()
        if move(direction, gf):
            assert not np.array_equal(gf, gamefield)
            yield gf, direction

def gen_children_computer(gamefield):
    possPos = []
    for i, row in enumerate(gamefield):
        for j, el in enumerate(row):
            if el == 0:
                possPos.append([i, j])

    for cell in [2, 4]:
        for i, j in possPos:
            gf = gamefield.copy()
            gf[i][j] = cell
            if cell == 2:
                probability = 0.9 / len(possPos)
            if cell == 4:
                probability = 0.1 / len(possPos)
            yield gf, probability

def minimax(gf, depth, player):
    # printGF(gf, max_depth - depth)
    if depth == 0 or not movePossible(gamefield):
        h = heuristic(gf)
        # print('\t' * (max_depth - depth), 'heuristic', h)
        return h, None

    if player:
        bestval = -10**10
        best_m = None
        for child, m in gen_children_player(gf):
            # print('\t' * (max_depth - depth + 1), 'player', m)
            v, _ = minimax(child, depth - 1, False)
            if v > bestval:
                bestval = max(bestval, v)
                best_m = m
        return bestval, best_m
    else:
        a = 0
        for child, prob in gen_children_computer(gf):
            v, _ = minimax(child, depth - 1, True)
            a += v * prob
            # print('\t' * (max_depth - depth + 1), 'computer', a)
        return a, None


max_depth = 4
def ai(gamefield, step):
    '''
    # for direction in (["w","s","n","e"] if random.random()>0.5 else ["s","w","n","e"]):
    for direction in (['l', 'd', 'u', 'r'] if step % 2 == 1 else ['d', 'l', 'u', 'r']):
        gf = gamefield.copy()
        if move(direction, gf):
            return direction
    return 'exit'
    '''
    # print('#' * 80, 'Start')
    v, m = minimax(gamefield.copy(), max_depth, True)
    return m


if __name__ == '__main__':
    hasAI = True if len(sys.argv) > 1 else False

    getch = GetchWrapper()
    controls = setupControls()
    gamefield = np.zeros((SIZE, SIZE), dtype=np.int)
    for i in range(SIZE * SIZE // 4):
        addRandom(gamefield)

    '''
    printGF(gamefield)
    for child, m in gen_children_player(gamefield):
        print('child', m)
        printGF(child)
    print(np.max(gamefield))
    '''

    step = 0
    while(True):
        if not hasAI:
            # clear()
            pass
        printGF(gamefield)
        if step == 0:
            printDescription(getch.isReal)
        step += 1
        if hasAI:
            # time.sleep(0.1)
            m = ai(gamefield, step)
        else:
            m = controls.get(getch.input(), None)
        print(m)
        if move(m, gamefield):
            addRandom(gamefield)
        elif (isFull(gamefield) and not movePossible(gamefield)) or m == 'exit':
            break
    prettyPrint('GAME OVER!')
    if hasAI:
        prettyPrint(str(step) + ' steps')
