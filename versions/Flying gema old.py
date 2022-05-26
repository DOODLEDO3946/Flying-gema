# Import required stuff
import sys
try:
	import pygame
	from pygame.locals import *
except:
	print("pygame is not installed, please install it to run the game")
	sys.exit()
try:
	import time
except:
	print("time is not installed, please install it to run the game")
	sys.exit()
try:
	import RPi.GPIO as GPIO
	import joystickPS2
	pi = True
except:
	pi = False
from random import randrange
if pi:
	joystickPS2.setup()
def setup():
	global generate, pi, score, greenthing, sleeptime, x, running, badthings, thing, badthing
#								Create variables to store locations and other stuff
	greenthing = 0
	thing = [320, 240]
	badthings = 50
	sleeptime = [[0,0]]
	badthing = []
	for c in range(badthings):
		sleeptime.insert(0,list([0,0]))
		while True:
			x = randrange(0, 32) * 20
			tmp = ((c % 25) - 1) * 20
			if tmp == 240:
				if x < 200 or x > 420:
					break
			else:
				break
		badthing.insert(0,list([x,tmp,0]))
	del tmp
	score = 0
	generate = 0
# Create the function gameOver
def gameOver():
	global pi, score, highscore
	pygame.event.get()
	gameOverFont = pygame.font.SysFont('dejavusans.ttf', 72)
	gameOverSurf = gameOverFont.render('Game Over', True, pygame.Color(randrange(205, 255), randrange(205, 255), randrange(205, 255)))
	gameOverRect = gameOverSurf.get_rect()
	gameOverRect.midtop = (320, 10)
	screen.blit(gameOverSurf, gameOverRect)
	pygame.display.update()
	if highscore < score:
		highscore = score
		gameOverSurf = gameOverFont.render('New Highscore!', True, pygame.Color(randrange(205, 255), randrange(205, 255), randrange(205, 255)))
		gameOverRect = gameOverSurf.get_rect()
		gameOverRect.center = (320, 240)
		screen.blit(gameOverSurf, gameOverRect)
	if pi:
		GPIO.output(Routput, GPIO.LOW)
		GPIO.output(Goutput, GPIO.LOW)
		GPIO.output(Boutput, GPIO.LOW)
	pygame.display.update()
	time.sleep(1.5)
	pygame.event.get()
# Create a function for the game
def startgame():
	setup()
	global generate, framerate, Rrandomise, Grandomise, Brandomise, shape, Rthing, Gthing, Bthing, score, highscore, greenthing, sleeptime, I, x, running, badexists, badthings, thing, badthing, screen, greenColour, redColour, blackColour, whiteColour, fpsClock
	direction = [False,False,False,False]
	running = True
	if pi:
		if Rrandomise:
			GPIO.output(Routput, GPIO.HIGH)
		elif not Rrandomise:
			GPIO.output(Routput, GPIO.LOW)
		if Grandomise:
			GPIO.output(Goutput, GPIO.HIGH)
		elif not Rrandomise:
			GPIO.output(Goutput, GPIO.LOW)
		if Brandomise:
			GPIO.output(Boutput, GPIO.HIGH)
		elif not Rrandomise:
			GPIO.output(Boutput, GPIO.LOW)
	timer = framerate
	if animations:
		edge = [145, 1]
	else:
		edge = [255]
	# Start the game in a loop
	while running:
		screen.fill(blackColour)
		if timer == framerate:
			if generate == 1:
				sleeptime.insert(0,list([0,0]))
				badthing.insert(0,list([640, (((((len(badthing)) - 1) % 25) - 1) * 20),0]))
				generate = 0
			if animations:
				if edge[0] >= 145 and not edge[0] >= 245 and edge[1] == 1:
					edge[0] += 15
				elif edge[0] >= 245 and edge[1] == 1:
					edge[1] = 0
					edge[0] -= 15
				elif edge[0] <= 245 and not edge[0] <= 145 and edge[1] == 0:
					edge[0] -= 15
				elif edge[0] <= 145 and edge[1] == 0:
					edge[1] = 1
					edge[0] += 15
			timer = 0
		else:
			timer += 1
		if backscore:
			gameOverFont = pygame.font.SysFont('dejavusans.ttf', 72)
			gameOverSurf = gameOverFont.render(str(score), True, pygame.Color(Rthing, Gthing, Bthing))
			gameOverRect = gameOverSurf.get_rect()
			gameOverRect.midtop = (320, 240)
			screen.blit(gameOverSurf, gameOverRect)
		if pi:
			if GPIO.input(I) == GPIO.HIGH:				# End the game if the button is pressed
				running = False
		if greenthing == 0:
			pygame.draw.rect(screen,pygame.Color(0, edge[0], 0),Rect(0, 460, 640, 20))
		else:
			pygame.draw.rect(screen,pygame.Color(0, edge[0], 0),Rect(0, 0, 640, 20))
		for c in range(len(badthing) - 1):														# Run for every badthing
			if badthing[c][0] >= -60:
				badthing[c][0] -= 60 / framerate
				if badthing[c][0] >= 640 and timer == framerate:
					badthing[c][0] = (round((badthing[c][0] / 20))) * 20
#				if (randrange(0, 100)) >= 50 and not badthing[c][2] >= 79:
#					badthing[c][2] += 5
#				elif not badthing[c][2] <= 19:
#					badthing[c][2] -= 10
				screen.blit(badthing_surface, (badthing[c][0], badthing[c][1]))
			elif badthing[c][2] != framerate and badthing[c][0] <= 0 and sleeptime[c][1] == 0:
				badthing[c][2] += 1
			elif badthing[c][2] == framerate and badthing[c][0] <= 0 and sleeptime[c][1] == 0:
				badthing[c][2] = 0
				tmp = randrange(1, 100)
				if tmp >= 1 and tmp <= 25:						# 25% chance - 1 frame delay
					sleeptime[c][0] = framerate
				elif tmp >= 26 and tmp <= 38:						# 12% chance - 2 frame delay
					sleeptime[c][0] = 2 * framerate
				elif tmp >= 39 and tmp <= 45:						# 6% channce - 3 frame delay
					sleeptime[c][0] = 3 * framerate
				else:
					sleeptime[c][0] = 0						# 57% chance - no frame delay
				sleeptime[c][1] = 1
				del tmp
			if badthing[c][0] >= 640:
				for count in range(1, (((len(badthing)) - c) // 25) - 1):
					if c <= (len(badthing) - 26):
#						if badthing[c][0] <= badthing[(c + (25 * count))][0] and (badthing[c][0] + 60) >= badthing[(c + (25 * count))][0]:
#							badthing[c][0] += 80
#						if badthing[c][0] >= badthing[(c + (25 * count))][0] and (badthing[c][0] - 60) <= badthing[(c + (25 * count))][0]:
#							badthing[c][0] += 80
						if badthing[c][0] >= badthing[(c + (25 * count))][0] <= (badthing[c][0] + 60):
							badthing[c][0] += 80
						if badthing[c][0] <= badthing[(c + (25 * count))][0] >= (badthing[c][0] - 60):
							badthing[c][0] -= 80
#					if not badthing[c][1] == badthing[(c + (25 * count))][1]:
#						print("comparing the wrong 2")
		if joystick:
			joy = joystickPS2.getResult()
			if joy == 1 and not thing[1] == 0:		#  Create movement of the character (From joystick)
				direction[0] = True					# up
			elif joy == 2 and not thing[1] == 470:
				direction[1] = True					# down
			elif joy == 3 and not thing[0] <= 0:
				direction[2] = True					# left
			elif joy == 4 and not thing[0] == 620:
				direction[3] = True					# right
			elif joy == 5 and not (thing[0] <= 0 and thing[1] == 0):
				direction[0] = True					# up-left
				direction[2] = True
			elif joy == 6 and not (thing[0] == 620 and thing[1] == 0):
				direction[0] = True					# up-right
				direction[3] = True
			elif joy == 7 and not (thing[0] <= 0 and thing[1] == 470):
				direction[1] = True					# down-left
				direction[2] = True
			elif joy == 8 and not (thing[0] >= 625 and thing[1] >= 470):
				direction[1] = True					# down-right
				direction[3] = True
		if not joystick or not pi:
			for event in pygame.event.get():
				if event.type == KEYUP:
					if event.key == K_UP or event.key == ord('w'):		#  Create movement of the character (From arrow keys)
						direction[0] = False				# up
					elif event.key == K_DOWN or event.key == ord('s'):
						direction[1] = False				# down
					elif event.key == K_LEFT or event.key == ord('a'):
						direction[2] = False				# left
					elif event.key == K_RIGHT or event.key == ord('d'):
						direction[3] = False				# right
				if event.type == KEYDOWN:
					if (event.key == K_UP or event.key == ord('w')) and not thing[1] <= 0:
						direction[0] = True				# up
					elif (event.key == K_DOWN or event.key == ord('s')) and not thing[1] >= 470:
						direction[1] = True				# down
					elif (event.key == K_LEFT or event.key == ord('a')) and not thing[0] <= 0:
						direction[2] = True				# left
					elif (event.key == K_RIGHT or event.key == ord('d')) and not thing[0] >= 625:
						direction[3] = True				# right
					if event.key == ord('e'):
						running = False								 # end game when the letter e is pressed
		if thing[1] <= 0 and direction[0]:				# Up
			direction[0] = False
		if thing[1] >= 470 and direction[1]:				# Down
			direction[1] = False
		if thing[0] <= 0 and direction[2]:				# Left
			direction[2] = False
		if thing[0] >= 625 and direction[3]:				# Right
			direction[3] = False
		for c in range(len(badthing) - 1):
			if thing[0] <= (badthing[c][0] + 39) and thing[0] >= (badthing[c][0] - 9) and thing[1] <= (badthing[c][1] + 19) and thing[1] >= (badthing[c][1] - 9):
				running = False
			if sleeptime[c][0] == 0 and sleeptime[c][1] == 1:
				badthing[c][0] = 700
				sleeptime[c][1] = 0
			if sleeptime[c][0] >= 1:
				sleeptime[c][0] -= 1
		if thing[1] == 0 and greenthing == 1:				# Get a point if you are inside a greenthing
			score += 1
			generate = 1
			greenthing = 0
		elif thing[1] >= 470 and greenthing == 0:
			score += 1
			generate = 1
			greenthing = 1
		if Rrandomise:
			Rthing = edge[0]
		else:
			Rthing = 0
		if Grandomise:
			Gthing = edge[0]
		else:
			Gthing = 0
		if Brandomise:
			Bthing = edge[0]
		else:
			Bthing = 0
		pygame.draw.polygon(thing_surface, pygame.Color(Rthing, Gthing, Bthing), ((0, 9), (9, 9), ((5, 0))))
		if direction[0] and not direction[2] and not direction[3]:		# Up
			thing[1] -= 60 / framerate
			if animations and shape == "triangle":
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((thing[0], (thing[1] + 10)), ((thing[0] + 10), (thing[1] + 10)), ((thing[0] + 5), thing[1])))
			if joystick:
				direction[0] = False
		elif direction[1] and not direction[2] and not direction[3]:	# Down
			thing[1] += 60 / framerate
			if animations and shape == "triangle":
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((thing[0], thing[1]), ((thing[0] + 10), thing[1]), ((thing[0] + 5), (thing[1] + 10))))
			if joystick:
				direction[1] = False
		elif direction[2] and not direction[0] and not direction[1]:	# Left
			thing[0] -= 60 / framerate
			if animations and shape == "triangle":
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), (((thing[0] + 10), thing[1]), ((thing[0] + 10), (thing[1] + 10)), (thing[0], (thing[1] + 5))))
			if joystick:
				direction[2] = False
		elif direction[3] and not direction[0] and not direction[1]:	# Right
			thing[0] += 60 / framerate
			if animations and shape == "triangle":
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((thing[0], thing[1]), (thing[0], (thing[1] + 10)), ((thing[0] + 10), (thing[1] + 5))))
			if joystick:
				direction[3] = False
		elif direction[0] and direction[2]:								# Up-Left
			thing[1] -= 60 / framerate
			thing[0] -= 60 / framerate
			if animations and shape == "triangle":
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), (((thing[0] + 5), (thing[1] + 10)), ((thing[0] + 10), (thing[1] + 5)), (thing[0], thing[1])))
			if joystick:
				direction[0] = False
				direction[2] = False
		elif direction[0] and direction[3]:								# Up-Right
			thing[0] += 60 / framerate
			thing[1] -= 60 / framerate
			if animations and shape == "triangle":
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((thing[0], (thing[1] + 5)), ((thing[0] + 5), (thing[1] + 10)), ((thing[0] + 10), thing[1])))
			if joystick:
				direction[0] = False
				direction[3] = False
		elif direction[1] and direction[2]:								# Down-Left
			thing[1] += 60 / framerate
			thing[0] -= 60 / framerate
			if animations and shape == "triangle":
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), (((thing[0] + 5), thing[1]), ((thing[0] + 10), (thing[1] + 5)), (thing[0], (thing[1] + 10))))
			if joystick:
				direction[1] = False
				direction[2] = False
		elif direction[1] and direction[3]:								# Down-Right
			thing[1] += 60 / framerate
			thing[0] += 60 / framerate
			if animations and shape == "triangle":
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((thing[0], (thing[1] + 5)), ((thing[0] + 5), thing[1]), ((thing[0] + 10), (thing[1] + 10))))
			if joystick:
				direction[1] = False
				direction[3] = False
		elif animations and shape == "triangle":
			pygame.draw.rect(screen, pygame.Color(Rthing // 2, Gthing // 2, Bthing // 2), Rect(thing[0], thing[1], 10, 10))
		if not animations:
			pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((thing[0], (thing[1] + 9)), ((thing[0] + 9), (thing[1] + 9)), ((thing[0] + 5), thing[1])))
		elif shape == "circle":
#			pygame.draw.rect(screen, pygame.Color(Rthing // 2, Gthing // 2, Bthing // 2), Rect(thing[0], thing[1], 10, 10))
			pygame.draw.circle(screen, pygame.Color(Rthing, Gthing, Bthing), ((thing[0] + 5), (thing[1] + 5)), 5)
		elif not shape == "triangle":
			pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), Rect(thing[0], thing[1], 10, 10))
		pygame.display.update()
		fpsClock.tick(framerate)
	gameOver()
def customize():
	global shape, Rrandomise, Grandomise, Brandomise, Rthing, Gthing, Bthing
	screen.fill(blackColour)
	time.sleep(1)
	customloop = True
	while customloop:
		tmp = randrange(205, 255)
		if Rrandomise:
			Rthing = tmp				# Randomise Red if it needs to be done
		else:
			Rthing = 0
		if Grandomise:					# Randomise Green if it needs to be done
			Gthing = tmp
		else:
			Gthing = 0
		if Brandomise:					# Randomise Blue if it needs to be done
			Bthing = tmp
		else:
			Bthing = 0
		del tmp
		pygame.draw.circle(screen, pygame.Color(Rthing, Gthing, Bthing), (170, 245), 5)	# Draw the shapes onto the screen
		pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), Rect(480, 240, 10, 10))
		pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((315, 45), (325, 45), (320, 35)))
		gameFont = pygame.font.SysFont('dejavusans.ttf', 24)
		if pi:												  # Write stuff on screen
			if joystickPS2.getResult() == 3:
				shape = "circle"
				break
			elif joystickPS2.getResult() == 4:
				shape = "square"
				break
			elif joystickPS2.getResult() == 1:
				shape = "triangle"
				break
			gameSurf = gameFont.render('Hold button / e to exit', True, whiteColour)
			gameRect = gameSurf.get_rect()
			gameRect.midtop = (330, 260)
			screen.blit(gameSurf, gameRect)
			if GPIO.input(I) == GPIO.HIGH:
				customloop = False
		else:
			gameSurf = gameFont.render('e to exit', True, whiteColour)
			gameRect = gameSurf.get_rect()
			gameRect.midtop = (330, 260)
			screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render('Select square', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (490, 215)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render('Select circle', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (170, 215)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render('Select triangle', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (320, 10)
		screen.blit(gameSurf, gameRect)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RIGHT or event.key == ord('d'):
					shape = "square"
					customloop = False
				elif event.key == K_LEFT or event.key == ord('a'):
					shape = "circle"
					customloop = False
				elif event.key == K_UP or event.key == ord('w'):
					shape = "triangle"
					customloop = False
				elif event.key == ord('e'):
					customloop = False
		fpsClock.tick(framerate)
	customloop = True
	while customloop:
		screen.fill(blackColour)
		gameSurf = gameFont.render('Add / remove green', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 30)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render('Add / remove red', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (110, 230)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render('Add / remove blue', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (550, 230)
		screen.blit(gameSurf, gameRect)
		if pi:												  # Write stuff on screen
			gameSurf = gameFont.render('Hold button / e to exit', True, whiteColour)
			gameRect = gameSurf.get_rect()
			gameRect.midtop = (330, 260)
			screen.blit(gameSurf, gameRect)
			if GPIO.input(I) == GPIO.HIGH:
				break
		else:
			gameSurf = gameFont.render('e to exit', True, whiteColour)
			gameRect = gameSurf.get_rect()
			gameRect.midtop = (330, 260)
			screen.blit(gameSurf, gameRect)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render(('Red - ' + str(Rrandomise)), True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (110, 210)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render(('Green - ' + str(Grandomise)), True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 10)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render(('Blue - ' + str(Brandomise)), True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (550, 210)
		screen.blit(gameSurf, gameRect)
		tmp = randrange(205, 255)
		if Rrandomise:
			Rthing = tmp
			if pi:				# Randomise Red if it needs to be done
				GPIO.output(Routput, GPIO.HIGH)
		else:
			Rthing = 0
			if pi:
				GPIO.output(Routput, GPIO.LOW)
		if Grandomise:				# Randomise Green if it needs to be done
			Gthing = tmp
			if pi:
				GPIO.output(Goutput, GPIO.HIGH)
		else:
			Gthing = 0
			if pi:
				GPIO.output(Goutput, GPIO.LOW)
		if Brandomise:				# Randomise Blue if it needs to be done
			Bthing = tmp
			if pi:
				GPIO.output(Boutput, GPIO.HIGH)
		else:
			Bthing = 0
			if pi:
				GPIO.output(Boutput, GPIO.LOW)
		del tmp
		if pi:
			if joystickPS2.getResult() == 1:
				if Grandomise:
					Grandomise = False
				else:
					Grandomise = True
				while joystickPS2.getResult() == 1:
					None
			elif joystickPS2.getResult() == 3:
				if Rrandomise:
					Rrandomise = False
				else:
					Rrandomise = True
				while joystickPS2.getResult() == 3:
					None
			elif joystickPS2.getResult() == 4:
				if Brandomise:
					Brandomise = False
				else:
					Brandomise = True
				while joystickPS2.getResult() == 4:
					None
			elif joystickPS2.getResult() == 2:
				break
		if shape == "square":
			pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), Rect(320, 220, 10, 10))
		elif shape == "circle":
			pygame.draw.circle(screen, pygame.Color(Rthing, Gthing, Bthing), (330, 230), 5)
		elif shape == "triangle":
			pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((330, 240), (340, 240), (335, 230)))
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RIGHT or event.key == ord('d'):
					if Brandomise:
						Brandomise = False
					else:
						Brandomise = True
				elif event.key == K_LEFT or event.key == ord('a'):
					if Rrandomise:
						Rrandomise = False
					else:
						Rrandomise = True
				elif event.key == K_UP or event.key == ord('w'):
					if Grandomise:
						Grandomise = False
					else:
						Grandomise = True
				elif event.key == ord('e'):
					customloop = False
		pygame.display.update()
		fpsClock.tick(framerate)
	del customloop
	if pi:
		GPIO.output(Routput, GPIO.LOW)
		GPIO.output(Goutput, GPIO.LOW)
		GPIO.output(Boutput, GPIO.LOW)
	if not Rrandomise and not Grandomise and not Brandomise:
		Rrandomise = True
		Grandomise = True
		Brandomise = True
def rightarrowkey():
	global pointer, backscore, animations, framerate, badthing_surface, joystick
	if pointer == 40:
		if backscore:
			backscore = False
		else:
			backscore = True
	elif pointer == 60:
		tmp = randrange(205, 255) // 3
		if animations:
			animations = False
			badthing_surface = pygame.Surface((40, 20), pygame.SRCALPHA)
			pygame.draw.rect(badthing_surface,pygame.Color((tmp * 3), 0, 0),Rect(0, 0, 40, 20))
		else:
			animations = True
			badthing_surface = pygame.Surface((60, 20), pygame.SRCALPHA)
			pygame.draw.rect(badthing_surface,pygame.Color(255, 0, 0),Rect(10, 0, 10, 20))
			pygame.draw.circle(badthing_surface,pygame.Color(255, 0, 0), (10, 10), 10)
			for c in range(40):
				pygame.draw.rect(badthing_surface,pygame.Color((round(5.1 * (50 - c))), 0, 0),Rect(10 + c, 0, 1, 20))
		del tmp
	elif pointer == 80:
		if framerate == 60:
			framerate = 12
		elif framerate == 15:
			framerate = 30
		elif framerate == 30:
			framerate = 60
		else:
			framerate += 3
	elif pi and pointer == 100:
		if joystick:
			joystick = False
		else:
			joystick = True
def leftarrowkey():
	global pointer, backscore, animations, framerate, badthing_surface, joystick
	if pointer == 40:
		if backscore:
			backscore = False
		else:
			backscore = True
	elif pointer == 60:
		tmp = randrange(205, 255) // 3
		if animations:
			animations = False
			badthing_surface = pygame.Surface((40, 20), pygame.SRCALPHA)
			pygame.draw.rect(badthing_surface,pygame.Color((tmp * 3), 0, 0),Rect(0, 0, 40, 20))
		else:
			animations = True
			badthing_surface = pygame.Surface((60, 20), pygame.SRCALPHA)
			pygame.draw.rect(badthing_surface,pygame.Color(255, 0, 0),Rect(10, 0, 10, 20))
			pygame.draw.circle(badthing_surface,pygame.Color(255, 0, 0), (10, 10), 10)
			for c in range(40):
				pygame.draw.rect(badthing_surface,pygame.Color((round(5.1 * (50 - c))), 0, 0),Rect(10 + c, 0, 1, 20))
		del tmp
	elif pointer == 80:
		if framerate == 12:
			framerate = 60
		elif framerate == 30:
			framerate = 15
		elif framerate == 60:
			framerate = 30
		else:
			framerate -= 3
	elif pi and pointer == 100:
		if joystick:
			joystick = False
		else:
			joystick = True
def settings():
	global pointer, backscore, animations, framerate
	gameFont = pygame.font.SysFont('dejavusans.ttf', 22)
	customloop = True
	global backscore, screen, animations, framerate
	while customloop:
		screen.fill(blackColour)
		if pi:												  # Write stuff on screen
			gameSurf = gameFont.render('Hold button / e to exit', True, whiteColour)
			gameRect = gameSurf.get_rect()
			gameRect.midtop = (330, 220)
			screen.blit(gameSurf, gameRect)
			gameSurf = gameFont.render(('joystick controls? - ' + str(joystick)), True, whiteColour)
			gameRect = gameSurf.get_rect()
			gameRect.midtop = (330, 100)
			screen.blit(gameSurf, gameRect)
			if GPIO.input(I) == GPIO.HIGH:
				break
			if joystickPS2.getResult() == 1 and pointer > 40:
				pointer -= 20
			elif joystickPS2.getResult() == 2 and pointer < 100:
				pointer += 20
			elif joystickPS2.getResult() == 3:
				leftarrowkey()
			elif joystickPS2.getResult() == 4:
				rightarrowkey()
		else:
			gameSurf = gameFont.render('e to exit', True, whiteColour)
			gameRect = gameSurf.get_rect()
			gameRect.midtop = (330, 220)
			screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render(('Background score counter - ' + str(backscore)), True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 40)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render(('Improved animations - ' + str(animations)), True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 60)
		screen.blit(gameSurf, gameRect)
		gameSurf = gameFont.render(('Frames per second - ' + str(framerate)), True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 80)
		screen.blit(gameSurf, gameRect)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if (event.key == K_UP or event.key == ord('w')) and pointer > 40:
					pointer -= 20
				elif event.key == K_RIGHT or event.key == ord('d'):
					rightarrowkey()
				elif event.key == ord('e'):
					customloop = False
				elif event.key == K_LEFT or event.key == ord('a'):
					leftarrowkey()
				if pi and (event.key == K_DOWN or event.key == ord('s')) and pointer < 100:
					pointer += 20
				elif not pi and (event.key == K_DOWN or event.key == ord('s')) and pointer < 80:
					pointer += 20
		tmp = randrange(204, 255)
		if Rrandomise:
			Rthing = tmp
		else:
			Rthing = 0
		if Grandomise:
			Gthing = tmp
		else:
			Gthing = 0
		if Brandomise:
			Bthing = tmp
		else:
			Bthing = 0
		del tmp
		if shape == "square":
			pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), Rect(615, pointer, 10, 10))
		elif shape == "circle":
			pygame.draw.circle(screen, pygame.Color(Rthing, Gthing, Bthing), (625, (pointer + 10)), 5)
		elif shape == "triangle":
			pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((625, (pointer + 10)), (635, (pointer + 10)), (630, pointer)))
		fpsClock.tick(framerate)
		pygame.display.update()
	del customloop
def drawmenu():
	global game
	gameFont = pygame.font.SysFont('dejavusans.ttf', 22)
	gameSurf = gameFont.render('Start game', True, whiteColour)
	gameRect = gameSurf.get_rect()
	gameRect.midtop = (500, 230)
	screen.blit(gameSurf, gameRect)
	gameSurf = gameFont.render('Customize', True, whiteColour)
	gameRect = gameSurf.get_rect()
	gameRect.midtop = (100, 230)
	screen.blit(gameSurf, gameRect)
	gameSurf = gameFont.render(("Highscore - " + str(highscore)), True, whiteColour)
	gameRect = gameSurf.get_rect()
	gameRect.midtop = (330, 240)
	screen.blit(gameSurf, gameRect)
	gameSurf = gameFont.render("Settings", True, whiteColour)
	gameRect = gameSurf.get_rect()
	gameRect.midtop = (330, 460)
	screen.blit(gameSurf, gameRect)
	if pi:												  # Write stuff on screen
		gameSurf = gameFont.render('Hold button / e to exit', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 220)
		screen.blit(gameSurf, gameRect)
		gameFont = pygame.font.SysFont('dejavusans.ttf', 16)
		gameSurf = gameFont.render('Joystick or Keyboard mode', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 10)
		screen.blit(gameSurf, gameRect)
		if GPIO.input(I) == GPIO.HIGH:
			game = False
	else:
		gameSurf = gameFont.render('e to exit', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 220)
		screen.blit(gameSurf, gameRect)
		gameFont = pygame.font.SysFont('dejavusans.ttf', 16)
		gameSurf = gameFont.render('Keyboard only mode', True, whiteColour)
		gameRect = gameSurf.get_rect()
		gameRect.midtop = (330, 10)
		screen.blit(gameSurf, gameRect)
#							make variable for fps counter
fpsClock = pygame.time.Clock()
#							set up pygame window
pygame.init()
screen = pygame.display.set_mode((760, 480))
pygame.display.set_caption("game... nothing else...")
#							Create variables
framerate = 60
pointer = 40
animations = True
backscore = True
R = 130
G = 130
B = 130
#							Create variables to store colours
#redColour = pygame.Color(255, 0, 0)
blackColour = pygame.Color(0, 0, 0)
whiteColour = pygame.Color(255, 255, 255)
#greenColour = pygame.Color(0, 255, 0)
game = True
shape = "triangle"
Rrandomise = True
Grandomise = True
Brandomise = True
Rthing = 255
Gthing = 255
Bthing = 255
highscore = 0
#							Create a surface to store the picture of the badthing so it can be blitted
badthing_surface = pygame.Surface((60, 20), pygame.SRCALPHA)
#pygame.draw.rect(badthing_surface,pygame.Color(255, 0, 0),Rect(10, 0, 10, 20))
pygame.draw.circle(badthing_surface,pygame.Color(255, 0, 0), (10, 10), 10)
#pygame.draw.rect(badthing_surface,pygame.Color(170, 0, 0),Rect(20, 0, 20, 20))
#pygame.draw.rect(badthing_surface,pygame.Color(85, 0, 0),Rect(40, 0, 20, 20))

thing_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
pygame.draw.polygon(thing_surface, pygame.Color(Rthing, Gthing, Bthing), ((0, 9), (9, 9), ((5, 0))))
#del tmp
for c in range(50):
	pygame.draw.rect(badthing_surface,pygame.Color((round(5.1 * (50 - c))), 0, 0),Rect(10 + c, 0, 1, 20))
if pi:
	joystick = True
	Routput = 35
	Goutput = 37
	Boutput = 33
	I = 15
	GPIO.setup(Routput, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(Goutput, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(Boutput, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(I, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
else:
	joystick = False
while game:							# Start game menu
	tmp = randrange(0, 100)					# Randomise a background colour
	if tmp <= 50 and not R >= 245:
		R += 10
	elif not tmp <= 50 and not R <= 55:
		R -= 10
	tmp = randrange(0, 100)
	if tmp <= 50 and not G >= 245:
		G += 10
	elif not tmp <= 50 and not G <= 55:
		G -= 10
	tmp = randrange(0, 100)
	if tmp <= 50 and not B >= 245:
		B += 10
	elif not tmp <= 50 and not B <= 55:
		B -= 10
	del tmp
	drawmenu()
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game = False
		elif event.type == KEYDOWN:
			if event.key == K_RIGHT or event.key == ord('d'):
				pygame.display.update()
				time.sleep(1)
				startgame()
			elif event.key == ord('e'):
				game = False
			elif event.key == K_LEFT or event.key == ord('a'):
				customize()
			elif event.key == K_DOWN or event.key == ord('s'):
				settings()
	if pi:
		if joystickPS2.getResult() == 3:
			customize()
		elif joystickPS2.getResult() == 4:
			startgame()
		elif joystickPS2.getResult() == 2:
			settings()
	screen.fill((R, G, B))
	fpsClock.tick(2)
if pi:
	GPIO.cleanup()
	joystickPS2.destory()
pygame.quit()
sys.exit()
