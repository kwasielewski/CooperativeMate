from numpy import  empty, zeros, full 
import copy
from queue import PriorityQueue 


class situation():
    def __init__(self, move, whiteKingX,whiteKingY,  whiteRookX,whiteRookY, blackKingX,blackKingY ,RookMovement):
        self.move = move
        self.wKX = whiteKingX
        self.wKY = whiteKingY
        self.wRX = whiteRookX
        self.wRY = whiteRookY
        self.bKX = blackKingX
        self.bKY = blackKingY
        self.Rm = RookMovement
        self.prev = None

        
    def __str__(self):
    	return str(self.move)+' '+str(self.wKX)+' '+str(self.wKY)+' '+str(self.wRX)+' '+str(self.wRY)+' '+str(self.bKX)+' '+str(self.bKY)+' '+str(self.Rm)

    def __copy__(self):
    	return type(self)(self.move, self.wKX, self.wKY, self.wRX, self.wRY, self.bKX, self.bKY, self.Rm)

    def __lt__(self, a):
    	return False

    def checkmate(self):
    	#zwroć czy mat

    	if self.wKX == self.wRX or self.wKY == self.wRY:
    		return False

    	if abs(self.bKX-self.wRX)+abs(self.bKY - self.wRY) < 2:
    		return False

    	locked = zeros(shape=[8]*2)
    	for i in range(8):
    		locked[i-1][self.wRY] = 1
    		locked[self.wRX][i-1] = 1

    	for i in range(self.wKX-1, self.wKX+2):
    		for j in range(self.wKY-1, self.wKY+2):
    			if i > -1 and i < 8 and j > -1 and  j < 8:
    				locked[i][j] = 1
    	#print(locked)
    	possible = False
    	for i in range(self.bKX-1, self.bKX+2):
    		for j in range(self.bKY-1, self.bKY+2):
    			if i > -1 and i < 8 and j > -1 and  j < 8:
    				if locked[i][j] == 0:
    					possible = True

    	#if not possible:
    		#print("Mat")

    	return not possible



mode = 1 #0 - wsadowy, 1 - debug
start = 1


#print(previous)

#print(visited)
def numToAns(a, b):
	return str(chr(97+a))+str(b+1)

#file = open("zad1_input.txt", "r")
#output = open("zad1_output.txt", "w")
#line = file.readline()
line = input()
queue = PriorityQueue()
#visited = zeros(shape=[64]*3+[2])
visited = full((64, 64,64, 2), 0)
prev = empty([64, 64, 64, 2], dtype=object)#((64,64,64, 2), -1)
start = 1
if line.split()[0]=='black':
	start = 0
#print(m)
s = situation(0, 	ord(line.split()[1][0])-97, int(line.split()[1][1])-1,
 					ord(line.split()[2][0])-97, int(line.split()[2][1])-1,
 					ord(line.split()[3][0])-97, int(line.split()[3][1])-1, 0)
#print(s)
queue.put((0, s))
while not queue.empty():
	item = queue.get()
	item = item[1]
	
		
	if visited[8*item.wKX +item.wKY][8*item.wRX +item.wRY][8*item.bKX +item.bKY][(item.move+start)%2] ==1 or item.Rm > 2:
		continue
	else:
		visited[8*item.wKX +item.wKY][8*item.wRX +item.wRY][8*item.bKX +item.bKY][(item.move+start)%2 ] = 1
	#print(item)
	if item.checkmate():
		#output.write(str(item.move))
		#print(item.move)
		if mode == 0:
			break
		#wypisz od tyłu
		odp = ""
		op = item
		while op.prev != None:
			#print(op)
			if op.wKX != op.prev.wKX or op.wKY != op.prev.wKY:
				odp = " " +numToAns(op.prev.wKX, op.prev.wKY)+numToAns(op.wKX, op.wKY)+ odp
			elif op.wRX != op.prev.wRX or op.wRY != op.prev.wRY:
				odp = " " + numToAns(op.prev.wRX, op.prev.wRY)+numToAns(op.wRX, op.wRY)+ odp
			else:
				odp = " " + numToAns(op.prev.bKX, op.prev.bKY)+numToAns(op.bKX, op.bKY)+ odp
			op = op.prev

		odp = odp[1:]
		print(odp)
		#print(s)
		break
	else:
		if item.Rm == 2:
			continue
		#ruch czarnego króla
		#print("Zakresy" ,item.bKX-1, item.bKX+1, item.bKY-1, item.bKY+1)
		if (item.move+start)%2 == 0:
			for i in range(item.bKX-1, item.bKX+2):
				for j in range(item.bKY-1, item.bKY+2):
					if i > -1 and i < 8 and j > -1 and  j < 8:
						#print("Elo", i , j)
						if (i == item.bKX and j == item.bKY):
							continue
						if max(abs(item.wKX-i), abs(item.wKY-j))>1:
							#print("XY", i , j)
							if not (
								(i== item.wRX and (item.wKX != i or item.wKY < min(item.wRY, j) or item.wKY > max(item.wRY, j))) 
								or 
								(j== item.wRY and (item.wKY != j or item.wKX < min(item.wRX, i) or item.wKX > max(item.wRX, i)))):
								newItem =copy.copy(item)
								newItem.bKX = i
								newItem.bKY = j
								newItem.move = newItem.move + 1
								newItem.prev = item
								#print(newItem.move)
								#print(newItem)
								if visited[8*newItem.wKX +newItem.wKY][8*newItem.wRX +newItem.wRY][8*newItem.bKX +newItem.bKY][(newItem.move+start)%2 ] == 0:
									queue.put((newItem.move, newItem))
		else:
			#ruch białego króla
			for i in range(item.wKX-1, item.wKX+2):
				for j in range(item.wKY-1, item.wKY+2):
					if (i == item.wKX and j == item.wKY):
							continue
					if i > -1 and i < 8 and j > -1 and  j < 8:
						#print("Elo", i , j)
						if max(abs(item.bKX-i), abs(item.bKY-j))>1:
							#print("Elo", i , j)
							if not (i == item.wRX and j == item.wRY):
								newItem =copy.copy(item)
								newItem.wKX = i
								newItem.wKY = j
								newItem.move = newItem.move + 1
								newItem.prev = item
								#print(newItem.move)
								#print(newItem)
								if visited[8*newItem.wKX +newItem.wKY][8*newItem.wRX +newItem.wRY][8*newItem.bKX +newItem.bKY][(newItem.move+start)%2 ] ==0:
									queue.put((newItem.move, newItem))
			
			#ruch białej wieży
			for i in range(1, 8):
				if item.wRX + i > 7:
					break
				if (item.wRX + i == item.wKX and item.wRY == item.wKY) or (item.wRX + i == item.bKX and item.wRY == item.bKY):
					break
				newItem = copy.copy(item)
				newItem.wRX = newItem.wRX+i
				newItem.move = newItem.move+1
				newItem.Rm = newItem.Rm + 1
				newItem.prev = item
				if visited[8*newItem.wKX +newItem.wKY][8*newItem.wRX +newItem.wRY][8*newItem.bKX +newItem.bKY][(newItem.move+start)%2 ] == 0:
					queue.put((newItem.move, newItem))
			for i in range(1, 8):
				if item.wRX - i < 0:
					break
				if (item.wRX - i == item.wKX and item.wRY == item.wKY) or (item.wRX - i == item.bKX and item.wRY == item.bKY):
					break
				newItem = copy.copy(item)
				newItem.wRX = newItem.wRX-i
				newItem.move = newItem.move+1
				newItem.Rm = newItem.Rm + 1
				newItem.prev = item
				if visited[8*newItem.wKX +newItem.wKY][8*newItem.wRX +newItem.wRY][8*newItem.bKX +newItem.bKY][(newItem.move+start)%2 ] == 0:
					queue.put((newItem.move, newItem))
			for i in range(1, 8):
				if item.wRY + i > 7:
					break
				if (item.wRY + i == item.wKY and item.wRX == item.wKX) or (item.wRY + i == item.bKY and item.wRX == item.bKX):
					break
				newItem = copy.copy(item)
				newItem.wRY = newItem.wRY+i
				newItem.move = newItem.move+1
				newItem.Rm = newItem.Rm + 1
				newItem.prev = item
				if visited[8*newItem.wKX +newItem.wKY][8*newItem.wRX +newItem.wRY][8*newItem.bKX +newItem.bKY][(newItem.move+start)%2 ] == 0:
					queue.put((newItem.move, newItem))
			for i in range(1, 8):
				if item.wRY - i < 0:
					break
				if (item.wRY - i == item.wKY and item.wRX == item.wKX) or (item.wRY - i == item.bKY and item.wRX == item.bKX):
					break
				newItem = copy.copy(item)
				newItem.wRY = newItem.wRY-i
				newItem.move = newItem.move+1
				newItem.Rm = newItem.Rm + 1
				newItem.prev = item
				if visited[8*newItem.wKX +newItem.wKY][8*newItem.wRX +newItem.wRY][8*newItem.bKX +newItem.bKY][(newItem.move+start)%2 ] ==0:
					queue.put((newItem.move, newItem))
	'''for i in range(8):
		for j in range(8):
			print( int(visited[1][35][i*8+j][0]), end=' ')
		print('\n')		
	#print(line.split())'''
