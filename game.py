import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt
import random
import os

SIZE = 4

def plotGF(H):
	fig = plt.figure(figsize=(6, 3.2))
	ax = fig.add_subplot(111)
	ax.set_title('colorMap')
	plt.imshow(H, cmap='Greys',  interpolation='nearest')
	ax.set_aspect('equal')

	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(0)
	cax.set_frame_on(False)
	plt.colorbar(orientation='vertical')
	plt.show()
def printGF(gamefield):
	print("##########\n"),
	for i,row in enumerate(gamefield.T):
		for j,el in enumerate(row):
			print(el),
		print("\n"),
	
def addRandom(gamefield):
	possPos = []
	for i,row in enumerate(gamefield):
		for j,el in enumerate(row):
			if el == 0:
				possPos.append(posfield[i][j])
	#print(possPos)
	if(len(possPos)>0):
		posToChange = possPos[int(random.random()*len(possPos))]
		#print(posToChange)
		gamefield[posToChange[0]][posToChange[1]] = 2 if random.random()>0.5 else 4
	else:
		print("ALL NODES ARE OCCUPIED!")

def move(direction,gamefield):
	print(direction)
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
	printGF(newgamefield)

def clear():
	os.system('cls' if os.name=='nt' else 'clear')

def step(gamefield):
	move('s',gamefield)
	move('n',gamefield)
	#clear()
	move('w',gamefield)
	move('e',gamefield)

if __name__ == '__main__':
	gamefield = np.zeros((SIZE,SIZE),dtype=np.int)
	posfield = [[(j,i) for i in range(SIZE)] for j in range(SIZE)]
	for i in range(5):
		addRandom(gamefield)
	clear()
	while(True):
		printGF(gamefield)
		step(gamefield)
		raw_input("asd"+str(random.random()))
		clear()
