# Import required modules
import sys, math, os.path, pickle, subprocess, time
from random import randrange, randint
version = 1.01
while True:
	try:
		import pygame, pygame.gfxdraw			# type: ignore
		from pygame.locals import *			# type: ignore
		break
	except:
	#	print("pygame is not installed, please install it to run the game")
	#	sys.exit()
		subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
while True:
	try:
		import requests, webbrowser			# type: ignore
		break
	except:
	#	print("requests webbrowser is not installed, please install it to run the game")
	#	sys.exit()
		subprocess.check_call([sys.executable, "-m", "pip", "install", "requests, webbrowser"])
try:
	response = requests.get(f"https://Flyinggema-updater.saudaliwhitgift.repl.co/update.json").json()
	response_success = True
#	print(response)
except:
	print("Error checking for updates. Will check on next run.")
	response_success = False
try:
	import RPi.GPIO as GPIO			# type: ignore		Makes vscode ignore checking this line for errors
	import joystickPS2			# type: ignore
	pi = True
except:
	pi = False
if pi:
	joystickPS2.setup()
def setup():
	global generate, pi, score, greenthing, sleeptime, running, badthings, thing, badthing, mouse_x, mouse_y, speed, points, animations, stars
	greenthing = 0
	if controls == "mouse":
		points = []
	speed = 60*(math.sqrt(2))
	thing.center = (320, 240)
	if mode == "normal":
		badthings = 100
	else:
		badthings = 150
	sleeptime = []
	badthing = []
	if animations:		# star generator/randomiser
		stars =[]
		percent_of_stars = 0.0025
		for c in range(int(percent_of_stars*640*480)):
			stars.extend([[randint(0, 640), randint(0, 480), randrange(10, 50)]])
	reshuffle = True
	for c in range(badthings):
		sleeptime.extend([[0,0]])
		while True:
			x = randrange(0, 38) * 20
			tmp = ((c % 25) - 1) * 20
			if 219 < tmp < 241:
				if x < 200 or x > 420:
					break
			else:
				break
		badthing.extend([[(badthing_surface.get_rect(topleft=(x,tmp))),0]])
	while reshuffle:
		for c in range(len(badthing)):
			if c == 0:
				reshuffle = False
			customloop = True
			while customloop:
				customloop = False
				for count in range(len(badthing)):
					if count == c or 219 < badthing[c][0].y < 249:
						continue
					if badthing[count][0].colliderect(badthing[c][0]) == 1:
						reshuffle = True
						badthing[c][0].x += 80
						customloop = True
	if mode == "normal":
		score = 0
		generate = 0
	mouse_x, mouse_y = thing.center
def pprint(place, text, size, colour, point, returnrect=False):		# easier text on screen
	colour = pygame.Color(colour)
	if place == "midtop":
		screen.blit(pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour), pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(midtop=point))
		if returnrect:
			return (pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(midtop=point))
	elif place == "center":
		screen.blit(pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour), pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(center=point))
		if returnrect:
			return (pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(center=point))
	elif place == "topleft":
		screen.blit(pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour), pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(topleft=point))
		if returnrect:
			return (pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(topleft=point))
	elif place == "topright":
		screen.blit(pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour), pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(topright=point))
		if returnrect:
			return (pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(topright=point))
	elif place == "midright":
		screen.blit(pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour), pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(midright=point))
		if returnrect:
			return (pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(midright=point))
	elif place == "midleft":
		screen.blit(pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour), pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(midleft=point))
		if returnrect:
			return (pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(midleft=point))
	elif place == "midbottom":
		screen.blit(pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour), pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(midbottom=point))
		if returnrect:
			return (pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(midbottom=point))
	else:#elif place == "bottomright":
		screen.blit(pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour), pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(bottomright=point))
		if returnrect:
			return (pygame.font.SysFont('Bitstream Vera.ttf', size).render(text, True, colour).get_rect(bottomright=point))
# Create the function gameOver
def gameOver(reason="ded"):		# Create a function for a game over
	end = time.time()
	global pi, score, highscore_normal, highscore_time, start
	pygame.display.update()
	pygame.event.get()
	pprint("center", "Game Over", 72, (randrange(205, 255), randrange(205, 255), randrange(205, 255)), (320, 50))
	pygame.display.update()
	if mode == "normal" and highscore_normal < score:
		highscore_normal = score
		pprint("center", "New Highscore!", 72, pygame.Color(randrange(205, 255), randrange(205, 255), randrange(205, 255)), (320, 180))
	elif highscore_time < round(end - start, 2):
		highscore_time = round(end - start, 2)
		pprint("center", "New Highscore!", 72, pygame.Color(randrange(205, 255), randrange(205, 255), randrange(205, 255)), (320, 180))
	if pi:
		GPIO.output(Routput, GPIO.LOW)
		GPIO.output(Goutput, GPIO.LOW)
		GPIO.output(Boutput, GPIO.LOW)
	pygame.display.update()
	if(mode == "normal" and score >= 50) or (mode == "survive" and round(end - start, 2) >= 420):
		pygame.display.set_caption("It's your time your wasting not mine")
	elif reason == "e":
		pygame.display.set_caption("you successfully chickened out")
	else:
		rand = randint(1, 10)
		if rand == 1:
			pygame.display.set_caption("Do better")
		elif rand == 2:
			pygame.display.set_caption("That the best you can do?")
		elif rand == 3:
			if mode == "normal":
				pygame.display.set_caption("I can get " + str(highscore_normal + 1) + " in a heartbeat")
			else:
				pygame.display.set_caption("I can get " + str(highscore_time + 1) + "secs in a heartbeat")
		elif rand == 4:
			pygame.display.set_caption("Actually try next time")
		elif rand == 5:
			pygame.display.set_caption("when I was born I could do better")
		elif rand == 6:
			pygame.display.set_caption("lol.")
		elif rand == 7:
			pygame.display.set_caption("that was quick")
		elif rand == 8:
			pygame.display.set_caption("that's embarrassing")
		elif rand == 9:
			pygame.display.set_caption("you ded")
		elif rand == 10:
			pygame.display.set_caption("are u 5?")
	time.sleep(1.5)
	pygame.display.set_caption("an ordinary game... nothing else...")
	pygame.event.get()
# Create a function for the game
def startgame():			# create a function for the entire game
	setup()
	global generate, framerate, Rrandomise, Grandomise, Brandomise, shape, Rthing, Gthing, Bthing, score, highscore_normal, highscore_time, greenthing, sleeptime, I, running, badthings, thing, badthing, screen, blackColour, whiteColour, fpsClock, mouse_x, mouse_y, speed, points, specific_colouring, stars, start, mode
	if mode == "normal" and score != 0:
		sys.exit()
	direction = [False,False,False,False]
	running = True
	if pi:			# turn on/off the light on a raspberry pi to show the colour of your character
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
	start = time.time()
	# Start the game in a loop
	while running:
		screen.fill(blackColour)

		if animations:
			for c in range(len(stars)):			# stars effects
				stars[c][0] -= stars[c][2] / framerate
				pygame.gfxdraw.pixel(screen, int(stars[c][0]), stars[c][1], pygame.Color((round((stars[c][2])/50)*255), (round((stars[c][2])/50)*255), (round((stars[c][2])/50)*255)))
				if stars[c][0] < 0:
					stars[c][0] = 640

		if timer == framerate:			# After each second, run the code in this if statement
			if mode == "normal" and generate != 0:			# create another badthing
				sleeptime.extend([[0,1]])
				badthing.extend([[(badthing_surface.get_rect(topleft=(700, (((((len(badthing)) - 1) % 25) - 1) * 20)))),0]])
				generate -= 1
			if animations:			# Add fading effect for greenthing and thing
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

		if pi and GPIO.input(I) == GPIO.HIGH: 				# End the game if the button is pressed
			time.sleep(1.5)
			if GPIO.input(I) == GPIO.HIGH:
				running = False
				gameOver()
				continue
			else:
				pause()

		if mode == "normal" and greenthing == 0:			# draw the green bar on the screen
			pygame.draw.rect(screen,pygame.Color(0, edge[0], 0),Rect(0, 460, 640, 20))
		elif mode == "normal":
			pygame.draw.rect(screen,pygame.Color(0, edge[0], 0),Rect(0, 0, 640, 20))
		if not specific_colouring:
			if backscore == "center":			# Show the background score counter
				if mode == "normal":
					if not specific_colouring:
						pprint("center", str(score), 72, pygame.Color(Rthing, Gthing, Bthing), (320, 240))
					else:
						pprint("center", str(score), 72, pygame.Color(Rrandomise, Grandomise, Brandomise), (320, 240))
				else:
					if not specific_colouring:
						pprint("center", str(round(time.time() - start)), 72, pygame.Color(Rthing, Gthing, Bthing), (320, 240))
					else:
						pprint("center", str(round(time.time() - start)), 72, pygame.Color(Rrandomise, Grandomise, Brandomise), (320, 240))					
			elif backscore == "corner":
				if mode == "normal":
					if not specific_colouring:
						pprint("topleft", str(score), 25, pygame.Color(Rthing, Gthing, Bthing), (0, 0))
					else:
						pprint("topleft", str(score), 25, pygame.Color(Rrandomise, Grandomise, Brandomise), (0, 0))
				else:
					if not specific_colouring:
						pprint("topleft", str(round(time.time() - start)), 25, pygame.Color(Rthing, Gthing, Bthing), (0, 0))
					else:
						pprint("topleft", str(round(time.time() - start)), 25, pygame.Color(Rrandomise, Grandomise, Brandomise), (0, 0))
		else:
			if backscore == "center":			# Show the background score counter
				pprint("center", str(score), 72, pygame.Color(Rrandomise, Grandomise, Brandomise), (320, 240))
			elif backscore == "corner":
				pprint("topleft", str(score), 25, pygame.Color(Rrandomise, Grandomise, Brandomise), (0, 0))	
		for c in range(len(badthing)):			# Run for every badthing
			if badthing[c][0].x >= -60:
				badthing[c][0].x -= 60 / framerate
				if badthing[c][0].x > 640 and (timer == framerate and (badthing[c][0].x != (round((badthing[c][0].x / 20))) * 20)):
					badthing[c][0].x = (round((badthing[c][0].x / 20))) * 20
				if badthing[c][0].x < 640:
					screen.blit(badthing_surface, badthing[c][0])
				if hitboxes:			# Show hitboxes of the thing
					screen.blit(badthing_hitbox_surface, badthing[c][0])
			elif badthing[c][1] != framerate and badthing[c][0].x <= 0 and sleeptime[c][1] == 0:
				badthing[c][1] += 1
			elif badthing[c][1] == framerate and badthing[c][0].x <= 0 and sleeptime[c][1] == 0:
				badthing[c][1] = 0
				tmp = randint(0, 100)
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
			if badthing[c][0].x >= 640:		# Stop overlapping with other badthings
				for count in range(c, len(badthing) - c):
					if badthing[count][0].colliderect(badthing[c][0]) == 1:
						badthing[c][0].x += 80

		if controls == "joystick":					#  Create movement of the character (From joystick)
			joy = joystickPS2.getResult()
			if joy == 1 and not thing.y == 1:
				direction[0] = True					# up
			elif joy == 2 and not thing.y == 470:
				direction[1] = True					# down
			elif joy == 3 and not thing.x <= 0:
				direction[2] = True					# left
			elif joy == 4 and not thing.x == 620:
				direction[3] = True					# right
			elif joy == 5 and not (thing.x <= 0 and thing.y == 1):
				direction[0] = True					# up-left
				direction[2] = True
			elif joy == 6 and not (thing.x == 620 and thing.y == 1):
				direction[0] = True					# up-right
				direction[3] = True
			elif joy == 7 and not (thing.x <= 0 and thing.y == 470):
				direction[1] = True					# down-left
				direction[2] = True
			elif joy == 8 and not (thing.x >= 625 and thing.y >= 470):
				direction[1] = True					# down-right
				direction[3] = True

		if controls == "keyboard" or controls == "mouse":
			for event in pygame.event.get():
				if event.type == KEYUP and controls == "keyboard":
					if event.key == K_UP or event.key == ord('w'):		#  Create movement of the character (From arrow keys)
						direction[0] = False				# up
					elif event.key == K_DOWN or event.key == ord('s'):
						direction[1] = False				# down
					elif event.key == K_LEFT or event.key == ord('a'):
						direction[2] = False				# left
					elif event.key == K_RIGHT or event.key == ord('d'):
						direction[3] = False				# right
				elif event.type == pygame.MOUSEMOTION:      
					mouse_x, mouse_y = pygame.mouse.get_pos()
				elif event.type == KEYDOWN:
					if controls == "keyboard":
						if (event.key == K_UP or event.key == ord('w')) and not thing.y <= 1:
							direction[0] = True				# up
						elif (event.key == K_DOWN or event.key == ord('s')) and not thing.y >= 470:
							direction[1] = True				# down
						elif (event.key == K_LEFT or event.key == ord('a')) and not thing.x <= 0:
							direction[2] = True				# left
						elif (event.key == K_RIGHT or event.key == ord('d')) and not thing.x >= 625:
							direction[3] = True				# right
					if event.key == K_ESCAPE or event.key == K_PAUSE:
						pause()
					if event.key == ord('e'):				# end game when the letter e is pressed
						gameOver("e")
						running = False
						continue


			if thing.y < 1 and direction[0]:				# Up
				direction[0] = False
			if thing.y > 470 and direction[1]:				# Down
				direction[1] = False
			if thing.x < 0 and direction[2]:				# Left
				direction[2] = False
			if thing.x > 625 and direction[3]:				# Right
				direction[3] = False

		for c in range(len(badthing)):		# Check (bit inaccurately) if you collided with of a badthing
			if thing.colliderect(badthing[c][0]) and ((thing.x <= (badthing[c][0].x + 39) and thing.x >= (badthing[c][0].x + 1) and thing.y <= (badthing[c][0].y + 19) and thing.y >= (badthing[c][0].y - 9)) or ((math.sqrt((thing.topright[0] - (badthing[c][0].x + 10))**2 + (thing.topright[1] - (badthing[c][0].y + 10))**2)) < 10 or (math.sqrt((thing.bottomright[0] - (badthing[c][0].x + 10))**2 + (thing.bottomright[1] - (badthing[c][0].y + 10))**2)) < 10)):
				running = False
				gameOver()
				continue
			if sleeptime[c][0] == 0 and sleeptime[c][1] == 1:
				badthing[c][0].x = 700
				sleeptime[c][1] = 0
			if sleeptime[c][0] > 0:
				sleeptime[c][0] -= 1
		if mode == "normal" and thing.y <= 20 and greenthing == 1:				# Get a point if you are inside a greenthing
			score += 1
			generate += 1
			greenthing = 0
		elif mode == "normal" and thing.y >= 450 and greenthing == 0:
			score += 1
			generate += 1
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
		if (controls == "mouse") and (not (len(points) == 0 and thing.collidepoint(mouse_x, mouse_y)) or (len(points) > 0 and thing.collidepoint(points[0]))):
			customloop = True
			while customloop:
				customloop = False
				for c in range(len(points)):
					if points[c][0] < 1:
						points.pop(c)
						customloop = True
						break

			if pygame.mouse.get_pressed()[0]:
				if len(points) > 0 and (mouse_x, mouse_y) != points[-1]:
					points.extend([[mouse_x, mouse_y]])
				elif len(points) < 1:
					points.extend([[mouse_x, mouse_y]])
			if len(points) > 0:
				for c in range(len(points)):
					points[c][0] -= 60 / framerate
					if c != 0:
						if not specific_colouring:
							pygame.draw.line(screen, pygame.Color(Rthing, Gthing, Bthing), points[c - 1], points[c])
						else:
							pygame.draw.line(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), points[c - 1], points[c])
					else:
						if not specific_colouring:
							pygame.draw.line(screen, pygame.Color(Rthing, Gthing, Bthing), thing.center, points[0])
						else:
							pygame.draw.line(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), thing.center, points[0])
				if not specific_colouring:
					pygame.draw.line(screen, pygame.Color(Rthing, Gthing, Bthing), points[-1], (mouse_x, mouse_y))
				else:
					pygame.draw.line(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), points[-1], (mouse_x, mouse_y))
				angle = math.degrees(math.atan2(thing.centerx - points[0][0], thing.centery - points[0][1]))
				if thing.collidepoint(points[0]):
					points.pop(0)
			else:
				angle = math.degrees(math.atan2(thing.centerx - mouse_x, thing.centery - mouse_y))
				if not specific_colouring:
					pygame.draw.line(screen, pygame.Color(Rthing, Gthing, Bthing), thing.center, (mouse_x, mouse_y))
				else:
					pygame.draw.line(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), thing.center, (mouse_x, mouse_y))
			thing.x -= math.sin(math.radians(angle)) * (speed / framerate)
			thing.y -= math.cos(math.radians(angle)) * (speed / framerate)
			if animations and shape == "triangle":
				screen.blit((pygame.transform.rotate(thing_surface, angle)), thing)
		if shape == "square":
			if not specific_colouring:
				pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), thing)
			else:
				pygame.draw.rect(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), thing)
		if timer == framerate and not specific_colouring:
			if shape == "triangle":
				if not specific_colouring:
					pygame.draw.polygon(thing_surface, pygame.Color(Rthing, Gthing, Bthing), ((0, 10), (10, 10), ((5, 0))))
				else:
					pygame.draw.polygon(thing_surface, pygame.Color(Rrandomise, Grandomise, Brandomise), ((0, 10), (10, 10), ((5, 0))))
		if direction[0] and not direction[2] and not direction[3]:		# Up
			thing.y -= speed / framerate
			if animations and shape == "triangle":
				screen.blit(thing_surface, thing)
			if controls == "joystick":
				direction[0] = False
		elif direction[1] and not direction[2] and not direction[3]:	# Down
			thing.y += speed / framerate
			if animations and shape == "triangle":
				screen.blit((pygame.transform.rotate(thing_surface, 180)), thing) 
			if controls == "joystick":
				direction[1] = False
		elif direction[2] and not direction[0] and not direction[1]:	# Left
			thing.x -= speed / framerate
			if animations and shape == "triangle":
				screen.blit((pygame.transform.rotate(thing_surface, 90)), thing) 
			if controls == "joystick":
				direction[2] = False
		elif direction[3] and not direction[0] and not direction[1]:	# Right
			thing.x += speed / framerate
			if animations and shape == "triangle":
				screen.blit((pygame.transform.rotate(thing_surface, 270)), thing) 
			if controls == "joystick":
				direction[3] = False
		elif direction[0] and direction[2]:				# Up-Left
			thing.y -= (speed / framerate) / math.sqrt(2)
			thing.x -= (speed / framerate) / math.sqrt(2)
			if animations and shape == "triangle":
				screen.blit((pygame.transform.rotate(thing_surface, -315)), (thing.x - 5, thing.y - 5)) 
			if controls == "joystick":
				direction[0] = False
				direction[2] = False
		elif direction[0] and direction[3]:				# Up-Right
			thing.x += (speed / framerate) / math.sqrt(2)
			thing.y -= (speed / framerate) / math.sqrt(2)
			if animations and shape == "triangle":
				screen.blit((pygame.transform.rotate(thing_surface, -45)), (thing.x, thing.y - 5))
			if controls == "joystick":
				direction[0] = False
				direction[3] = False
		elif direction[1] and direction[2]:				# Down-Left
			thing.y += (speed / framerate) / math.sqrt(2)
			thing.x -= (speed / framerate) / math.sqrt(2)
			if animations and shape == "triangle":
				screen.blit((pygame.transform.rotate(thing_surface, 135)), (thing.x - 5, thing.y)) 
			if controls == "joystick":
				direction[1] = False
				direction[2] = False
		elif direction[1] and direction[3]:				# Down-Right
			thing.y += (speed / framerate) / math.sqrt(2)
			thing.x += (speed / framerate) / math.sqrt(2)
			if animations and shape == "triangle":
				screen.blit((pygame.transform.rotate(thing_surface, 225)), thing)
			if controls == "joystick":
				direction[1] = False
				direction[3] = False
		elif animations and shape == "triangle" and (not controls == "mouse" or thing.collidepoint(mouse_x, mouse_y)):
			if not specific_colouring:
				pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing, 128), thing)
			else:
				pygame.draw.rect(screen, pygame.Color(Rrandomise, Grandomise, Brandomise, 128), thing)
		if not animations:
			screen.blit(thing_surface, thing)
		elif shape == "circle":
			if not specific_colouring:
				pygame.draw.circle(screen, pygame.Color(Rthing, Gthing, Bthing), ((thing.x + 5), (thing.y + 5)), 5)
			else:
				pygame.draw.circle(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), ((thing.x + 5), (thing.y + 5)), 5)
		if hitboxes and shape != "square":
			if not specific_colouring:
				pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), thing, 1)
			else:
				pygame.draw.rect(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), thing, 1)
		pygame.display.update()
		fpsClock.tick(framerate)
def customize():
	global shape, Rrandomise, Grandomise, Brandomise, Rthing, Gthing, Bthing, specific_colouring
	screen.fill(blackColour)
	while True:
		tmp = randint(205, 255)
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
		if not specific_colouring:			# Draw the shapes onto the screen
			pygame.draw.circle(screen, pygame.Color(Rthing, Gthing, Bthing), (100, 245), 5)
			pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), Rect(535, 240, 10, 10))
			pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((315, 45), (325, 45), (320, 35)))
		else:
			pygame.draw.circle(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), (100, 245), 5)
			pygame.draw.rect(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), Rect(535, 240, 10, 10))
			pygame.draw.polygon(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), ((315, 45), (325, 45), (320, 35)))
		screen.blit(arrow, (arrow.get_rect(midtop=(210, 240))))		# Draw arrows onto the screen
		screen.blit((pygame.transform.rotate(arrow, 180)), (arrow.get_rect(midtop=(430, 240))))
		screen.blit((pygame.transform.rotate(arrow, -90)), (arrow.get_rect(center=(320, 130))))

		pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()[0]
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
			pprint("midtop", "Hold button / e or", 24, whiteColour, (320, 240))
			if (pprint("midtop", "click to exit", 24, whiteColour, (320, 260), True).collidepoint(pos) and click) or GPIO.input(I) == GPIO.HIGH:
				time.sleep(0.3)
				break
		elif pprint("midtop", "click / e to exit", 24, whiteColour, (320, 240), True).collidepoint(pos) and click:
			time.sleep(0.3)
			break
		if pprint("midtop", "Select square", 24, whiteColour, (540, 215), True).collidepoint(pos) and click:
			shape = "square"
			break
		if pprint("midtop", "Select circle", 24, whiteColour, (100, 215), True).collidepoint(pos) and click:
			shape = "circle"
			break
		if pprint("midtop", "Select triangle", 24, whiteColour, (320, 10), True).collidepoint(pos) and click:
			shape = "triangle"
			break
		pygame.display.update()
		fpsClock.tick(5)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RIGHT or event.key == ord('d'):
					shape = "square"
					break
				elif event.key == K_LEFT or event.key == ord('a'):
					shape = "circle"
					break
				elif event.key == K_UP or event.key == ord('w'):
					shape = "triangle"
					break
				elif event.key == ord('e'):
					break
		else:
			continue
		break
	while True:
		screen.fill(blackColour)
		pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()[0]
		if pi:
			if joystickPS2.getResult() == 1:	# Up
				specific_colouring = False
				Rrandomise = True
				Grandomise = True
				Brandomise = True
				break
			elif joystickPS2.getResult() == 2:	# Down
				if not specific_colouring:
					specific_colouring = True
					Rrandomise = 255
					Grandomise = 255
					Brandomise = 255
				break
			pprint("midtop", "Hold button / e or", 24, whiteColour, (320, 240))
			if (pprint("midtop", "click to exit", 24, whiteColour, (320, 260), True).collidepoint(pos) and click) or GPIO.input(I) == GPIO.HIGH:
				time.sleep(0.3)
				break
		elif pprint("midtop", "click / e to exit", 24, whiteColour, (320, 240), True).collidepoint(pos) and click:
			time.sleep(0.3)
			break
		if pprint("midbottom", "Manual/specific colouring", 24, whiteColour, (320, 470), True).collidepoint(pos) and click:
			if not specific_colouring:
				specific_colouring = True
				Rrandomise = 255
				Grandomise = 255
				Brandomise = 255
			break
		if pprint("midtop", "Non-specific colouring (default)", 24, whiteColour, (320, 10), True).collidepoint(pos) and click:
			specific_colouring = False
			Rrandomise = True
			Grandomise = True
			Brandomise = True
			break
		pygame.display.update()
		fpsClock.tick(5)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_UP or event.key == ord('w'):
					specific_colouring = False
					Rrandomise = True
					Grandomise = True
					Brandomise = True
					break
				elif event.key == K_DOWN or event.key == ord('s'):
					if not specific_colouring:
						specific_colouring = True
						Rrandomise = 255
						Grandomise = 255
						Brandomise = 255
					break
				elif event.key == ord('e'):
					break
		else:
			continue
		break
	keys = pygame.key.get_pressed()
	while True:
		screen.fill(blackColour)
		pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()[0]
		if pprint("center", "Add / remove red", 24, whiteColour, (110, 240), True).collidepoint(pos):
			if not specific_colouring and click:
				Rrandomise = not Rrandomise
			elif specific_colouring and keys[K_DOWN]:
				change_colour("R", "down")
			elif specific_colouring and keys[K_UP]:
				change_colour("R", "up")
		if pprint("midtop", "Add / remove green", 24, whiteColour, (320, 30), True).collidepoint(pos):
			if not specific_colouring and click:
				Grandomise = not Grandomise
			elif specific_colouring and keys[K_DOWN]:
				change_colour("G", "down")
			elif specific_colouring and keys[K_UP]:
				change_colour("G", "up")
		if pprint("center", "Add / remove blue", 24, whiteColour, (550, 240), True).collidepoint(pos):
			if not specific_colouring and click:
				Brandomise = not Brandomise
			elif specific_colouring and keys[K_DOWN]:
				change_colour("B", "down")
			elif specific_colouring and keys[K_UP]:
				change_colour("B", "up")
		if pi:												  # Write stuff on screen
			pprint("midtop", "Hold button / e or", 24, whiteColour, (320, 240))
			if pprint("midtop", "click to exit", 24, whiteColour, (320, 260), True).collidepoint(pos) and click:
				time.sleep(0.3)
				break
			if GPIO.input(I) == GPIO.HIGH:
				break
		elif pprint("midtop", "e to exit", 24, whiteColour, (320, 260), True).collidepoint(pos) and click:
			time.sleep(0.3)
			break
		pprint("midtop", ("Red - " + str(Rrandomise)), 24, whiteColour, (110, 210))
		pprint("midtop", ("Green - " + str(Grandomise)), 24, whiteColour, (320, 10))
		pprint("midtop", ("Blue - " + str(Brandomise)), 24, whiteColour, (550, 210))
		tmp = randrange(205, 255)
		if Rrandomise:
			Rthing = tmp
			if pi:					# Randomise Red if it needs to be done
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
				if specific_colouring:
					Grandomise = not Grandomise
				while joystickPS2.getResult() == 1:
					None
			elif joystickPS2.getResult() == 3:
				if specific_colouring:
					Rrandomise = not Rrandomise
				while joystickPS2.getResult() == 3:
					None
			elif joystickPS2.getResult() == 4:
				if specific_colouring:
					Brandomise = not Brandomise
				while joystickPS2.getResult() == 4:
					None
			elif joystickPS2.getResult() == 2:
				break
		if shape == "square":
			if not specific_colouring:
				pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), Rect(315, 220, 10, 10))
			else:
				pygame.draw.rect(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), Rect(315, 220, 10, 10))
		elif shape == "circle":
			if not specific_colouring:
				pygame.draw.circle(screen, pygame.Color(Rthing, Gthing, Bthing), (320, 230), 5)
			else:
				pygame.draw.circle(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), (320, 230), 5)
		elif shape == "triangle":
			if not specific_colouring:
				pygame.draw.polygon(screen, pygame.Color(Rthing, Gthing, Bthing), ((315, 230), (325, 230), (320, 220)))
			else:
				pygame.draw.polygon(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), ((315, 230), (325, 230), (320, 220)))
		screen.blit(arrow, (arrow.get_rect(midtop=(210, 240))))
		screen.blit((pygame.transform.rotate(arrow, 180)), (arrow.get_rect(midtop=(430, 240))))
		screen.blit((pygame.transform.rotate(arrow, -90)), (arrow.get_rect(center=(320, 130))))
		pygame.display.update()
		fpsClock.tick(20)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if (event.key == K_RIGHT or event.key == ord('d')) and not specific_colouring:
					Brandomise = not Brandomise
				elif (event.key == K_LEFT or event.key == ord('a')) and not specific_colouring:
					Rrandomise = not Rrandomise
				elif (event.key == K_UP or event.key == ord('w')) and not specific_colouring:
					Grandomise = not Grandomise
				elif event.key == ord('e'):
					break
		else:
			keys = pygame.key.get_pressed()
			continue
		break
	if pi:
		GPIO.output(Routput, GPIO.LOW)
		GPIO.output(Goutput, GPIO.LOW)
		GPIO.output(Boutput, GPIO.LOW)
	if not Rrandomise and not Grandomise and not Brandomise:
		Rrandomise = True
		Rthing = 255
		Grandomise = True
		Gthing = 255
		Brandomise = True
		Bthing = 255
	if shape == "triangle":
		thing_surface.fill(pygame.SRCALPHA)
		if not specific_colouring:
			pygame.draw.polygon(thing_surface, pygame.Color(Rthing, Gthing, Bthing), ((0, 10), (10, 10), ((5, 0))))
		else:
			pygame.draw.polygon(thing_surface, pygame.Color(Rrandomise, Grandomise, Brandomise), ((0, 10), (10, 10), ((5, 0))))
	elif shape == "circle":
		thing_surface.fill(pygame.SRCALPHA)
		if not specific_colouring:
			pygame.draw.circle(thing_surface, pygame.Color(Rthing, Gthing, Bthing), (5, 5), 5)
		else:
			pygame.draw.circle(thing_surface, pygame.Color(Rrandomise, Grandomise, Brandomise), (5, 5), 5)
	elif shape == "square":
		if not specific_colouring:
			pygame.draw.rect(thing_surface, pygame.Color(Rthing, Gthing, Bthing), Rect(0, 0, 10, 10))
		else:
			pygame.draw.rect(thing_surface, pygame.Color(Rrandomise, Grandomise, Brandomise), Rect(0, 0, 10, 10))
	pygame.display.set_icon(thing_surface)
def arrowkey(key="right"):
	global pointer, backscore, animations, framerate, badthing_surface, controls, hitboxes, fullscreen, mode
	if pointer == 40:
		if backscore == "center":
			if key == "left":
				backscore = "off"
			else:
				backscore = "corner"
		elif backscore == "off":
			if key == "left":
				backscore = "corner"
			else:
				backscore = "center"
		else:
			if key == "left":
				backscore = "center"
			else:
				backscore = "off"
	elif pointer == 60:
		if animations:
			animations = False
			badthing_surface = pygame.Surface((40, 20), pygame.SRCALPHA)
			pygame.draw.rect(badthing_surface,pygame.Color(255, 0, 0),Rect(10, 0, 30, 20))
			pygame.draw.circle(badthing_surface,pygame.Color(255, 0, 0), (10, 10), 10)
		else:
			animations = True
			badthing_surface = pygame.Surface((60, 20), pygame.SRCALPHA)
			for c in range(40):
				pygame.draw.circle(badthing_surface, pygame.Color(255, 0, 0, round(6.375 * c)), (50 - c, 10), 10)
	elif pointer == 80:
		if framerate == 12:
			if key == "left":
				framerate = 60
			else:
				framerate = 15
		elif framerate == 30:
			if key == "left":
				framerate = 15
			else:
				framerate = 60
		elif framerate == 60:
			if key == "left":
				framerate = 30
			else:
				framerate = 12
		else:
			if key == "left":
				framerate = 12
			else:
				framerate = 30
	elif pointer == 100:
		hitboxes = not hitboxes
	elif pointer == 120:
		fullscreen = not fullscreen
		pygame.display.toggle_fullscreen()
		pygame.display.set_icon(thing_surface)
	elif pointer == 140:
		if controls == "joystick":
			if key == "left":
				controls = "mouse"
				if framerate == 60:
					framerate = 30
			else:
				controls = "keyboard"
		elif controls == "mouse":
			if key == "left":
				controls = "keyboard"
			elif pi:
				controls = "joystick"
		else:
			if pi:
				controls = "joystick"
			elif key == "left":
				controls = "keyboard"
			else:
				controls = "mouse"
				if framerate == 60:
					framerate = 30
	elif pointer == 160:
		if mode == "normal":
			mode = "survive"
		else:
			mode = "normal"
	elif pointer == 180 and response_success:
		webbrowser.open(response["url"])
def change_colour(colour, change):
	global Rrandomise, Grandomise, Brandomise
	if colour == "R":
		if change == "down":
			if 1 <= Rrandomise <= 255:
				Rrandomise -= 1
		elif 0 <= Rrandomise <= 254 and change == "up":
			Rrandomise += 1
	elif colour == "G":
		if 1 <= Grandomise <= 255 and change == "down":
			Grandomise -= 1
		elif 0 <= Grandomise <= 254 and change == "up":
			Grandomise += 1
	elif colour == "B":
		if 1 <= Brandomise <= 255 and change == "down":
			Brandomise -= 1
		elif 0 <= Brandomise <= 254 and change == "up":
			Brandomise += 1
def settings():
	global pointer, backscore, animations, framerate, screen, fullscreen, mode
	while True:
		screen.fill(blackColour)
		pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()[0]
		if pi:												  # Write stuff on screen
			pprint("midtop", "Hold button / e or", 24, whiteColour, (320, 240))
			if pprint("midtop", "click to exit", 24, whiteColour, (320, 260), True).collidepoint(pos) and click:
				time.sleep(0.3)
				break
			if GPIO.input(I) == GPIO.HIGH:
				break
			if joystickPS2.getResult() == 1 and pointer > 40:
				pointer -= 20
			elif joystickPS2.getResult() == 2 and ((response["version"] > version and pointer < 180) or (not response["version"] > version and pointer < 160)):
				pointer += 20
			elif joystickPS2.getResult() == 3:
				arrowkey("left")
			elif joystickPS2.getResult() == 4:
				arrowkey("right")
		elif pprint("midtop", "e to exit", 22, whiteColour, (320, 220), True).collidepoint(pos) and click:
			time.sleep(0.3)
			break
		backscore_rect = pprint("midtop", 'Background score counter - ' + str(backscore), 22, whiteColour, (320, 40), True)
		if backscore_rect.collidepoint(pos) and click:
			time.sleep(0.3)
			pointer = 40
			arrowkey("right")
		animations_rect = pprint("midtop", 'Improved animations - ' + str(animations), 22, whiteColour, (320, 60), True)
		if animations_rect.collidepoint(pos) and click:
			time.sleep(0.3)
			pointer = 60
			arrowkey("right")
		fps_rect = pprint("midtop", 'Frames per second - ' + str(framerate), 22, whiteColour, (320, 80), True)
		if fps_rect.collidepoint(pos) and click:
			time.sleep(0.3)
			pointer = 80
			arrowkey("right")
		hitboxes_rect = pprint("midtop", 'Hitboxes shown - ' + str(hitboxes), 22, whiteColour, (320, 100), True)
		if hitboxes_rect.collidepoint(pos) and click:
			time.sleep(0.3)
			pointer = 100
			arrowkey("right")
		fullscreen_rect = pprint("midtop", 'Fullscreen - ' + str(fullscreen), 22, whiteColour, (320, 120), True)
		if fullscreen_rect.collidepoint(pos) and click:
			time.sleep(0.3)
			pointer = 120
			arrowkey("right")
		controls_rect = pprint("midtop", "controls - " + controls, 22, whiteColour, (320, 140), True)
		if controls_rect.collidepoint(pos) and click:
			time.sleep(0.3)
			pointer = 140
			arrowkey("right")
		modes_rect = pprint("midtop", "mode - " + mode, 22, whiteColour, (320, 160), True)
		if modes_rect.collidepoint(pos) and click:
			time.sleep(0.3)
			pointer = 160
			arrowkey("right")
		if response_success and response["version"] > version:
			version_rect = pprint("midtop", "Update Available " + str(version) + " to " + str(response["version"]), 22, whiteColour, (320, 180), True)
			if version_rect.collidepoint(pos) and click:
				time.sleep(0.3)
				pointer = 180
				arrowkey()
		if pointer == 40:
			if backscore == "center":
				pprint("midright", "off", 18, pygame.Color(200, 200, 200), (backscore_rect.midleft[0] - 10, backscore_rect.midright[1]))
				pprint("midleft", "corner", 18, pygame.Color(200, 200, 200), (backscore_rect.midright[0] + 10, backscore_rect.midright[1]))
			elif backscore == "off":
				pprint("midright", "corner", 18, pygame.Color(200, 200, 200), (backscore_rect.midleft[0] - 10, backscore_rect.midright[1]))
				pprint("midleft", "center", 18, pygame.Color(200, 200, 200), (backscore_rect.midright[0] + 10, backscore_rect.midright[1]))
			else:
				pprint("midright", "center", 18, pygame.Color(200, 200, 200), (backscore_rect.midleft[0] - 10, backscore_rect.midright[1]))
				pprint("midleft", "off", 18, pygame.Color(200, 200, 200), (backscore_rect.midright[0] + 10, backscore_rect.midright[1]))
		elif pointer == 60:
			if animations:
				pprint("midleft", "False", 18, pygame.Color(200, 200, 200), (animations_rect.midright[0] + 10, animations_rect.midright[1]))
			else:
				pprint("midright", "True", 18, pygame.Color(200, 200, 200), (animations_rect.midleft[0] - 10, animations_rect.midleft[1]))
		elif pointer == 80:
			if framerate == 12:
				pprint("midright", "60", 18, pygame.Color(200, 200, 200), (fps_rect.midleft[0] - 10, fps_rect.midleft[1]))
				pprint("midleft", "15", 18, pygame.Color(200, 200, 200), (fps_rect.midright[0] + 10, fps_rect.midright[1]))
			elif framerate == 30:
				pprint("midright", "15", 18, pygame.Color(200, 200, 200), (fps_rect.midleft[0] - 10, fps_rect.midleft[1]))
				pprint("midleft", "60", 18, pygame.Color(200, 200, 200), (fps_rect.midright[0] + 10, fps_rect.midright[1]))
			elif framerate == 60:
				pprint("midright", "30", 18, pygame.Color(200, 200, 200), (fps_rect.midleft[0] - 10, fps_rect.midleft[1]))
				pprint("midleft", "12", 18, pygame.Color(200, 200, 200), (fps_rect.midright[0] + 10, fps_rect.midright[1]))
			else:
				pprint("midright", "12", 18, pygame.Color(200, 200, 200), (fps_rect.midleft[0] - 10, fps_rect.midleft[1]))
				pprint("midleft", "30", 18, pygame.Color(200, 200, 200), (fps_rect.midright[0] + 10, fps_rect.midright[1]))
		elif pointer == 100:
			if hitboxes:
				pprint("midright", "False", 18, pygame.Color(200, 200, 200), (hitboxes_rect.midleft[0] - 10, hitboxes_rect.midleft[1]))
			else:
				pprint("midleft", "True", 18, pygame.Color(200, 200, 200), (hitboxes_rect.midright[0] + 10, hitboxes_rect.midright[1]))
		elif pointer == 120:
			if fullscreen:
				pprint("midright", "False", 18, pygame.Color(200, 200, 200), (fullscreen_rect.midleft[0] - 10, fullscreen_rect.midleft[1]))
			else:
				pprint("midleft", "True", 18, pygame.Color(200, 200, 200), (fullscreen_rect.midright[0] + 10, fullscreen_rect.midright[1]))
		elif pi:
			if controls == "keyboard":
				pprint("midright", "joystick", 18, pygame.Color(200, 200, 200), (controls_rect.midleft[0] - 10, controls_rect.midleft[1]))	
			elif controls == "joystick":
				pprint("midright", "mouse", 18, pygame.Color(200, 200, 200), (controls_rect.midleft[0] - 10, controls_rect.midleft[1]))
				pprint("midleft", "keyboard", 18, pygame.Color(200, 200, 200), (controls_rect.midright[0] + 10, controls_rect.midright[1]))
			else:
				pprint("midright", "keyboard", 18, pygame.Color(200, 200, 200), (controls_rect.midleft[0] - 10, controls_rect.midleft[1]))
				pprint("midleft", "joystick", 18, pygame.Color(200, 200, 200), (controls_rect.midright[0] + 10, controls_rect.midright[1]))
		elif controls == "mouse" and pointer == 140:
			pprint("midright", "keyboard", 18, pygame.Color(200, 200, 200), (controls_rect.midleft[0] - 10, controls_rect.midleft[1]))
		if controls == "keyboard" and pointer == 140:
			pprint("midleft", "mouse", 18, pygame.Color(200, 200, 200), (controls_rect.midright[0] + 10, controls_rect.midright[1]))
		elif pointer == 160:
			if mode == "survive":
				pprint("midright", "normal", 18, pygame.Color(200, 200, 200), (modes_rect.midleft[0] - 10, modes_rect.midleft[1]))
			else:
				pprint("midleft", "survive", 18, pygame.Color(200, 200, 200), (modes_rect.midright[0] + 10, modes_rect.midright[1]))
		tmp = randint(205, 255)
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
			if not specific_colouring:
				pygame.draw.rect(screen, pygame.Color(Rthing, Gthing, Bthing), Rect(615, pointer, 10, 10))
			else:
				pygame.draw.rect(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), Rect(615, pointer, 10, 10))
		elif shape == "circle":
			if not specific_colouring:
				pygame.draw.circle(screen, pygame.Color(Rthing, Gthing, Bthing), (625, (pointer + 10)), 5)
			else:
				pygame.draw.circle(screen, pygame.Color(Rrandomise, Grandomise, Brandomise), (625, (pointer + 10)), 5)
		elif shape == "triangle":
			screen.blit(thing_surface, (615, pointer))
		fpsClock.tick(framerate)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if (event.key == K_UP or event.key == ord('w')) and pointer > 40:
					pointer -= 20
				elif event.key == K_RIGHT or event.key == ord('d'):
					arrowkey("right")
				elif event.key == ord('e'):
					break
				elif event.key == K_LEFT or event.key == ord('a'):
					arrowkey("left")
				elif (event.key == K_DOWN or event.key == ord('s')) and ((response["version"] > version and pointer < 180) or (not response["version"] > version and pointer < 160)):
					pointer += 20
		else:
			continue
		break
thing_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flying_gema_save.pkl')):
	try:
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flying_gema_save.pkl'), 'rb') as file:		# (save loader code) this and the next line are from https://www.geeksforgeeks.org/how-to-use-pickle-to-save-and-load-variables-in-python/#:~:text=Pickle%20is%20a%20python%20module,which%20JSON%20fails%20to%20serialize and reddit.
			highscore_normal, Rrandomise, Grandomise, Brandomise, Rthing, Gthing, Bthing, shape, pointer, controls, backscore, fullscreen, hitboxes, specific_colouring, mode, highscore_time = pickle.load(file)
	except ValueError and EOFError:
		print("Please delete flying_gema_save.pkl due to older save detected and unable to import")
		exit()
	if shape == "triangle":
		thing_surface.fill(pygame.SRCALPHA)
		if not specific_colouring:
			pygame.draw.polygon(thing_surface, pygame.Color(Rthing, Gthing, Bthing), ((0, 10), (10, 10), ((5, 0))))
		else:
			pygame.draw.polygon(thing_surface, pygame.Color(Rrandomise, Grandomise, Brandomise), ((0, 10), (10, 10), ((5, 0))))
	elif shape == "circle":
		thing_surface.fill(pygame.SRCALPHA)
		if not specific_colouring:
			pygame.draw.circle(thing_surface, pygame.Color(Rthing, Gthing, Bthing), (5, 5), 5)
		else:
			pygame.draw.circle(thing_surface, pygame.Color(Rrandomise, Grandomise, Brandomise), (5, 5), 5)
	elif shape == "square":
		if not specific_colouring:
			pygame.draw.rect(thing_surface, pygame.Color(Rthing, Gthing, Bthing), Rect(0, 0, 10, 10))
		else:
			pygame.draw.rect(thing_surface, pygame.Color(Rrandomise, Grandomise, Brandomise), Rect(0, 0, 10, 10))
	pygame.display.set_icon(thing_surface)  
else:
	highscore_time = 0
	highscore_normal = 0
	specific_colouring = True
	Rrandomise = True
	Grandomise = True
	Brandomise = True
	Rthing = 255
	Gthing = 255
	Bthing = 255
	shape = "triangle"
	pointer = 40
	controls = "keyboard"
	backscore = "center"
	pygame.draw.polygon(thing_surface, pygame.Color(Rthing, Gthing, Bthing), ((0, 10), (10, 10), ((5, 0))))
	fullscreen = False
	hitboxes = False
	mode = "normal"
#							make variable for fps counter
fpsClock = pygame.time.Clock()
#							set up pygame
pygame.init()
screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("game... nothing else...")
#							Create variables
framerate = 60
animations = True
R = 130
G = 130
B = 130
blackColour = pygame.Color(0, 0, 0)
whiteColour = pygame.Color(255, 255, 255)
game = True
Rthing = 255
Gthing = 255
Bthing = 255
tm = pygame.Surface((29, 20), pygame.SRCALPHA)
pygame.draw.rect(tm, pygame.Color(255, 0, 0), Rect(-1, 0, 30, 20), 1)
badthing_hitbox_surface = pygame.Surface((40, 20), pygame.SRCALPHA)
badthing_hitbox_surface.blit(tm, (10, 0))
del tm
thing = thing_surface.get_rect()
#							Create a surface to store the image of the badthing so it can be blitted

badthing_surface = pygame.Surface((60, 20), pygame.SRCALPHA)
#pygame.draw.rect(badthing_surface,pygame.Color(255, 0, 0),Rect(10, 0, 10, 20))
#pygame.draw.circle(badthing_surface,pygame.Color(255, 0, 0), (10, 10), 10)
#pygame.draw.rect(badthing_surface,pygame.Color(170, 0, 0),Rect(20, 0, 20, 20))
#pygame.draw.rect(badthing_surface,pygame.Color(85, 0, 0),Rect(40, 0, 20, 20))
for c in range(40):
#	pygame.draw.rect(badthing_surface,pygame.Color(255, 0, 0, 255 - (round(5.1 * c))),Rect(10 + c, 0, 1, 20))
	pygame.draw.circle(badthing_surface, pygame.Color(255, 0, 0, round(6.375 * c)), (50 - c, 10), 10)

pygame.display.set_icon(thing_surface)
arrow = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.polygon(arrow, (255, 255, 255), ((0, 10), (5, 0), (5, 5), (20, 5), (20, 15), (5, 15), (5, 20)), 1)

if fullscreen:
	pygame.display.toggle_fullscreen()

if pi:
	Routput = 35
	Goutput = 37
	Boutput = 33
	I = 15
	GPIO.setup(Routput, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(Goutput, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(Boutput, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(I, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def pause():
	screen.blit(thing_surface, thing)
	temp_surface = pygame.Surface((640, 480))
	temp_surface.fill((0, 0, 0))
	temp_surface.set_alpha(100)
	screen.blit(temp_surface, (0, 0))
	rectangle_continue = pprint("midtop", "Continue", 22, whiteColour, (320, 240), True)
	pprint("midtop", ('Highscore(normal mode) - ' + str(highscore_normal)), 22, whiteColour, (320, 220))
	pprint("midtop", ('Highscore(survive mode) - ' + str(highscore_time)), 22, whiteColour, (320, 200))
	pygame.display.update()
	while True:
		if pi and GPIO.input == GPIO.HIGH:
			time.sleep(0.5)
			break
		pos = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()[0]
		if rectangle_continue.collidepoint(pos) and click:
			break
		if pi and GPIO.input(I) == GPIO.HIGH:
			break
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_PAUSE:
					break
		else:
			continue
		break
while game:							# Start game menu
	screen.fill((R, G, B))
	if fpsClock.get_fps() == 0:
		fps = 2
	else:
		fps = fpsClock.get_fps()
	tmp = randrange(0, 7)					# Randomise a background colour change
	if tmp == 1 and not R >= 205:
		R += (10 / fps)
	elif tmp == 4 and not R <= 55:
		R -= (10 / fps)
	tmp = randrange(0, 100)
	if tmp == 2 and not G >= 205:
		G += (10 / fps)
	elif tmp <= 5 and not G <= 55:
		G -= (10 / fps)
	tmp = randrange(0, 100)
	if tmp == 3 and not B >= 205:
		B += (10 / fps)
	elif tmp == 6 and not B <= 55:
		B -= (10 / fps)
	pos = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()[0]
	if pprint("midtop", "Start game", 22, whiteColour, (540, 240), True).collidepoint(pos) and click:
		startgame()
		fpsClock = pygame.time.Clock()
	if pprint("midtop", "Customize", 22, whiteColour, (100, 240), True).collidepoint(pos) and click:
		customize()
		fpsClock = pygame.time.Clock()
	if pprint("midtop", "Settings", 22, whiteColour, (320, 460), True).collidepoint(pos) and click:
		settings()
		fpsClock = pygame.time.Clock()
	pprint("midtop", ('Highscore(normal mode) - ' + str(highscore_normal)), 22, whiteColour, (320, 220))
	pprint("midtop", ('Highscore(survive mode) - ' + str(highscore_time)), 22, whiteColour, (320, 200))
	pprint("bottomright","version: " + str(version), 22, whiteColour, (640, 480))
	if pi:											# Write stuff on screen
		pprint("midtop", "Hold button / e or", 22, whiteColour, (320, 240))
		if pprint("midtop", "click to exit", 22, whiteColour, (320, 260), True).collidepoint(pos) and click:
			break
		pprint("midtop", "Joystick & Keyboard detected", 16, whiteColour, (320, 10))
		if GPIO.input(I) == GPIO.HIGH:
			break
	else:
		if pprint("midtop", "e / click to exit", 22, whiteColour, (320, 240), True).collidepoint(pos) and click:
			break
		pprint("midtop", "Keyboard only detected", 16, whiteColour, (320, 10))
	screen.blit(arrow, (arrow.get_rect(midtop=(210, 240))))
	screen.blit((pygame.transform.rotate(arrow, 180)), (arrow.get_rect(midtop=(430, 240))))
	screen.blit((pygame.transform.rotate(arrow, 90)), (arrow.get_rect(midtop=(320, 350))))
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game = False
		elif event.type == KEYDOWN:
			if event.key == K_RIGHT or event.key == ord('d'):
				startgame()
				fpsClock = pygame.time.Clock()
			elif event.key == ord('e'):
				game = False
			elif event.key == K_LEFT or event.key == ord('a'):
				customize()
				fpsClock = pygame.time.Clock()
			elif event.key == K_DOWN or event.key == ord('s'):
				settings()
				fpsClock = pygame.time.Clock()
	if pi:
		if joystickPS2.getResult() == 3:
			customize()
		elif joystickPS2.getResult() == 4:
			startgame()
		elif joystickPS2.getResult() == 2:
			settings()
#	fpsClock.tick(2)
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'flying_gema_save.pkl'), 'wb') as file:			# (game saver code) this and the next line are from https://www.geeksforgeeks.org/how-to-use-pickle-to-save-and-load-variables-in-python/#:~:text=Pickle%20is%20a%20python%20module,which%20JSON%20fails%20to%20serialize and reddit.
	pickle.dump((highscore_normal, Rrandomise, Grandomise, Rthing, Gthing, Bthing, Brandomise, shape, pointer, controls, backscore, fullscreen, hitboxes, specific_colouring, mode, highscore_time), file)
if pi:
	GPIO.cleanup()
	joystickPS2.destory()
pygame.quit()
sys.exit()