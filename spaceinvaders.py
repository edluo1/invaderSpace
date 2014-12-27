#SPACE INVADERS
#Byoung Sul Lee, Eddy Luo, Zhi Wei Fang, Jason Yung, Dennis Your
from pygame import *
import random
import sys

#the sprite class for the hero and aliens
class Sprite:
	#initializes the position, imagefile
	def __init__(self, xpos, ypos, filename):
		self.x = xpos
		self.y = ypos
		self.bitmap = image.load(filename)
		self.bitmap.set_colorkey((0,0,0))
	#function if the position of sprite needs changing
	def set_position(self, xpos, ypos):
		self.x = xpos
		self.y = ypos
	#update the sprite on screen
	def render(self, pxX = 0):
		screen.blit(self.bitmap, (self.x + pxX, self.y))

#tests if there is a collision given the x,y positions of the two sprites
def collide(s1_x, s1_y, s2_x, s2_y):
	if (s1_x > s2_x - 32) and (s1_x < s2_x + 32) and (s1_y > s2_y - 32) and (s1_y < s2_y + 32):
		return True
	else:
		return False

#the game (NOT the main initialization)
#enemyrow1 = the list of alien sprites
#score = enemies hit
#x = int count for enemyrow creation
#shotsfired = checks to see if there is already a heromissile fired
def maingame():
	enemyrow1 = []
	enemyrow2 = []
	enemyrow3 = []
	score = 0
	shotsfired = False

	# music. because everyone loves retro music
	mixer.music.load('data/SpaceInvadersSoundtrack.wav')
	mixer.music.play(-1, 0)
	boom = mixer.Sound ('data/boom.wav')

	hero = Sprite(300, 530, 'data/hero.jpg')
	heromissile = Sprite(50, 560, 'data/heromissle.jpg')
	enemymissile = Sprite(0, 560, 'data/projectile.png')
	enemyrow = [enemyrow1, enemyrow2, enemyrow3]
	
	enemyspeed = 1
	heromissilespeed = 10

	while True:
		screen.blit(backdrop, (0, 0))
		# checks if ships reached the right
		# this is checked once per iteration so that the ships aren't confused
		if shipsReachedRight(enemyrow, 590):
			enemyspeed = -enemyspeed
			for i in range(len(enemyrow)):
				for count in range(len(enemyrow[i])):
					enemyrow[i][count].y += 5
		# checks if ships reached the left
		if shipsReachedLeft(enemyrow, 10):
			enemyspeed = -enemyspeed
			for i in range(len(enemyrow)):
				for count in range(len(enemyrow[i])):
					enemyrow[i][count].y += 5

		for i in range(len(enemyrow)):
			for count in range(len(enemyrow[i])):
				enemyrow[i][count].x += enemyspeed 
				enemyrow[i][count].render()
				
		for i in range(len(enemyrow)):
			for count in range(0, len(enemyrow[i])):
				if collide(heromissile.x, heromissile.y, enemyrow[i][count].x, enemyrow[i][count].y):
					del enemyrow[i][count]
					shotsfired = False
					score += 1
					heromissile.y = 0
					mixer.Sound.play(boom)
					break
			
			if len(enemyrow[i]) > 0:
				if (enemyrow[i][0].y >= hero.y-30):
					gameover(screen, score)
			
		if heromissile.y < 559 and heromissile.y > 0:
			heromissile.render()
			heromissile.y -= heromissilespeed
		else:
			shotsfired = False

		if enemymissile.y >= 560 and len(enemyrow[0]) > 0:
			enemymissile.x = enemyrow[0][random.randint(0, len(enemyrow[0]) - 1)].x
			enemymissile.y = enemyrow[0][0].y

		if collide(hero.x + 16, hero.y, enemymissile.x, enemymissile.y):
			gameover(screen, score)

		#check if there are enemies left
		if len(enemyrow[0]) == 0 and len(enemyrow[1]) == 0 and len(enemyrow[2]) == 0:
			for i in range(len(enemyrow)):
				enemyrow[i] = newenemies(0+40*i, str(i+1))
			enemyspeed = abs(enemyspeed) + 1

		for ourevent in event.get():
			if ourevent.type == QUIT:
				sys.exit(0)
			if ourevent.type == KEYDOWN:
				keys = key.get_pressed()
				if keys[K_RIGHT] and hero.x < 590:
					hero.x += 5
				if keys[K_LEFT] and hero.x > 10:
					hero.x -= 5
				if keys[K_SPACE] and shotsfired == False:
					heromissile.x = hero.x + 19
					heromissile.y = hero.y + 8
					shotsfired = True
				#CHEATS!!!!! freezes the aliens in place
				if ourevent.key == K_n:
					enemyspeed = 0
				if ourevent.key == K_t: # speeds up the enemies
					if enemyspeed <= 0:
						enemyspeed -= 1
					else:
						enemyspeed += 1
				if ourevent.key == K_b: # speeds up the missiles
					heromissilespeed = 30
				if ourevent.key == K_r: # slows down the missiles
					heromissilespeed = 10

		textfont=font.SysFont('Arial', 30)
		text=textfont.render('Score: '+str(score), True, (255, 255, 255))
		screen.blit(text, (10, 560))
		
		enemymissile.render(12)
		enemymissile.y += 3

		hero.render()

		display.update()
		time.delay(5)

def newenemies(n,num):
	enemyrownum = []
	x = 0
	for count in range(10):
		enemyrownum.append(Sprite(50 * x + 50, 50 + n, 'data/enemy'+num+'.png'))
		x += 1
	return enemyrownum
		
def shipsReachedRight(enemyrow, rightEdge):
	# have the ships reached the rightEdge (pixels)?
	rightReached = []
	for i in range(len(enemyrow)):
		if len(enemyrow[i]) != 0:
			rightReached.append(enemyrow[i][len(enemyrow[i])-1].x >= rightEdge)
	for j in range(len(rightReached)):
		return(True in rightReached)
	return False

def shipsReachedLeft(enemyrow, leftEdge):
	# have the ships crossed the leftEdge pixels?
	leftReached = []
	for i in range(len(enemyrow)):
		if len(enemyrow[i]) != 0:
			leftReached.append(enemyrow[i][0].x <= leftEdge)
	for j in range(len(leftReached)):
		return(True in leftReached)
	return False
		
def gameover(screen, score):
		time.wait(300)
		screen.fill((255,255,255))
		textfont=font.SysFont('Arial', 30)
		text=textfont.render('Score: '+str(score), True, (0, 0, 0))
		screen.blit(text, (10, 560))
		text=textfont.render('You died!', True, (0, 0, 0))
		screen.blit(text, (100, 100))
		display.update()
		time.wait(1000)

		text=textfont.render('Press Enter to Play Again', True, (0, 0, 0))
		screen.blit(text, (150, 250))
		display.update()
		baseTimer = time.get_ticks()
		nowTime = time.get_ticks()
		while nowTime - baseTimer < 10000:
			for ourevent in event.get():
				if ourevent.type == QUIT:
					sys.exit(0)
				if ourevent.type ==KEYDOWN and ourevent.key==K_RETURN:
					maingame()
			timeRect= Rect(150, 300, 300, 30)
			draw.rect(screen, (255,255,255), timeRect)
			timeLeft=textfont.render(str(10-int((nowTime-baseTimer) / 1000))+' Seconds Left', True, (0, 0, 0))
			screen.blit(timeLeft, (150, 300)) 
			display.update()
			nowTime = time.get_ticks()
		sys.exit(0)

#starts the game
init()
screen = display.set_mode((640,640))
key.set_repeat(1, 1)
display.set_caption('Space Invaders')
backdrop = image.load('data/background.png')
maingame()
