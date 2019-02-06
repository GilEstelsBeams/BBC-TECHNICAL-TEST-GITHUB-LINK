"""
===================
BBC Technical Test
===================

Author: GilEstelsBeams
Date: 6/2/2019

"""

import pygame 
import random

#PARAMETERS TO SET (can be set while running the programme)

H=50 #Height of the grid in number of cells
L=50 #Length of the grid in number of cells
torus=False #option to "delete" the borders

#The starting point of the game:
#'default': random, 
#'drawn':player choses before starting, 
#'number': then define 'Prob', with Prob=1/prob(starting cell is alive)
Start='number' 
Prob=4

Speed=10 #number of iterations per second
squares=16 #size of the cell's side, between 8 and 64, needs to be even

Black=(0,0,0)
White=(255,255,255)
Blue=(16,208,234)
Yellow=(249,252,52)

Background=White
Alivecells=Black

run=False #wether or not it starts running by itself or wait for the space key to be pushed

# FUNCTIONS AND CLASS USED

class cell:
	def __init__(self,location,width,alive=True):
		width=int(width)
		self.image = pygame.Surface([width, width])
		self.state=alive
		self.location=location
		
	def paint(self):
		
		if self.state==True: self.colour=Alivecells
		else: self.colour=Background
		
	
def set_parameters(x,y,z,w,s,p,q): #asks if the user wants to manually change the parameters
	print('If you would like to change the parameters, write Y. Otherwise press Enter.')
	par=input('Answer')
	if par=='Y':
		print('Height of the grid in number of cells')
		x=int(input('Answer:'))
		print('Length of the grid in number of cells')
		y=int(input('Answer:'))
		print('Would you like a torus-like grid? (Answer True or press Enter)')
		z_a=input('Answer:')
		print("Choose the starting point:default, drawn or number")
		w=input('Answer:')
		if w=='number':
			print('Choose a positive N, with N=1/Prob(A starting cell is alive)')
			p=int(input('Answer:'))
		print('Speed: number of iterations per second')
		s=int(input('Answer:'))
		print('Size of each cell, between 8 and 64 advised, needs to be positive and even')
		q=int(input('Answer:'))
		if z_a==True:
			z=z_ab

	return [x,y,z,w,s,p,q]


def count_neighbours(h,l,c,cell_list): #counts the neighbouring cells
	n=0
	for i in range(max(h-1,0),min(h+2,H)):
		for j in range(max(l-1,0),min(L,l+2)):
			if i!=h or j!=l:
				if cell_list[i][j].state==True: n=n+1

	if torus==True: #Special case where there are no real borders
		if h==0:
			i=H-1
			for j in range(max(l-1,0),min(L,l+2)):
				if cell_list[i][j].state==True: n=n+1
		if l==0:
			j=L-1
			for i in range(max(h-1,0),min(h+2,H)):
				if cell_list[i][j].state==True: n=n+1
		if h==H-1:
			i=0
			for j in range(max(l-1,0),min(L,l+2)):
				if cell_list[i][j].state==True: n=n+1

		if l==L-1:
			j=0
			for i in range(max(h-1,0),min(h+2,H)):
				if cell_list[i][j].state==True: n=n+1

	return(n)

def life_or_death(n,s): #decides of the future of the cell
	v=False
	if s==True and n==2: v=True

	if n==3: v=True
	return(v)


#MAIN FUNCTION

print('Hello! Welcome to the Game of Life.')
print('')
print('First a few rules:')
print('')
print('Use the space key for starting and pausing the game')
print('Left click for making a cell alive, right click for killing it')
print('To stop the game just close the window')
print('')
print('Enjoy!')
print('')

[H,L,torus,Start,Speed,Prob,squares]=set_parameters(H,L,torus,Start,Speed,Prob,squares)

pygame.init()

#We first create the pygame window
r=squares/2
a=squares*H
b=squares*L
size=(int(a), int(b))
screen=pygame.display.set_mode(size)
pygame.display.set_caption("The Game of Life")

carryOn=True

clock=pygame.time.Clock()
screen.fill(Background)

#Then we create the 2D list with all the cells

cell_list=[[]for i in range(H)]

for h in range(H):
	
	for l in range(L):
        	x1=int(l*squares+r)
        	x2=int(h*squares+r)
        	
        	if Start=='default': life=random.choice([True, False])
        	if Start=='drawn': life=False
        	if Start=='number':
        		lifeb=random.choices([True,False],[1/Prob,1-1/Prob])
        		life=lifeb[0]

        	startcell=cell([x1,x2],squares,life)
        	cell_list[h].append(startcell)
        	startcell.paint()
	        pygame.draw.circle(screen,startcell.colour,startcell.location,int(squares/2))

#We create a copy of the cell_list so that it contains the future values
cell_list2=cell_list

if Start=='drawn':run=False

while carryOn:
    
    #We take into account any action taken by the player

    clock.tick(Speed)
    clicksa=[]
    clicksd=[]
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            carryOn = False 
        if event.type == pygame.KEYDOWN:
        	if event.key == pygame.K_SPACE:
        		run = not run
    	
    clicked=pygame.mouse.get_pressed()
    locm=pygame.mouse.get_pos()

    screen.fill(Background)

    #Now we deal with the cells

    for h in range(H):
    	for l in range(L):

    		c=cell_list[h][l]

    		cell_list2[h][l]=cell(c.location,squares,c.state)
    		c2=cell_list2[h][l]

    		n=count_neighbours(h,l,c,cell_list)
    		
	    	if run==True: 
	    		c2.state=life_or_death(n,c.state) #The function that updates c2 with the next states

	    	#We take care of the clicks from the player

    		loc=c.location
    		if clicked[0]:
	    				
	    		if locm[0]>(loc[0]-r) and locm[0]<loc[0]+r and locm[1]>loc[1]-r and locm[1]<loc[1]+r:
	    			c2.state= True
	    			
	    	if clicked [2]:
	    		if locm[0]>(loc[0]-r) and locm[0]<loc[0]+r and locm[1]>loc[1]-r and locm[1]<loc[1]+r:
	    			c2.state= False
	    			

	    	
    		c.paint()
    		pygame.draw.circle(screen,c.colour,c.location,int(squares/2))

    cell_list=cell_list2
    pygame.display.flip()       
    
pygame.quit()