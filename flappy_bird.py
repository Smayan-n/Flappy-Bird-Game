import pygame, sys, random, json, time
pygame.init()


class Powerup():
	def __init__(self):
		self.powerups = {}
		self.hitbox = {}
		self.diameter = 6


	def generate(self, key):
		
		#initially making powerups
		self.powerups[key] = (pipes.pipes[key][0] - (pipes.pipe_width//2), random.randint(50, 350))


	def draw(self):
		
		#drawing all powerups in dict and changig x as well
		for key in self.powerups:
			y = self.powerups[key][1]
										 #the key + x is the num of pipes ahead the current one u want powerup to spawn
			self.powerups[key] = (pipes.pipes[key + 2][0] - 110, y )
			powerup = self.powerups[key]

			#making and drawing hitbox
			self.hitbox[key] = (powerup[0] - 6, powerup[1] - 6, self.diameter + 5, self.diameter + 5)
			#pygame.draw.rect(screen, (255, 0, 0), self.hitbox[key], 2)


			pygame.draw.circle(screen, (10, 10, 200), powerup, self.diameter)



class Bird():
	def __init__(self, x , y):
		self.pos_x = x
		self.pos_y = y
		self.down_vel = 1
		self.jump_vel = -30
		self.diameter = 30
		self.hitbox = (self.pos_x - self.diameter//2, self.pos_y - self.diameter//2, self.diameter, self.diameter)
		self.start = False
		self.score = 0
		self.high_score = 0
		self.const = 0
		self.immune = False
		self.circle_rad = self.diameter//2
		self.animate_num = 0
	


	def draw(self):
		#drawing hitbox
		self.hitbox = (self.pos_x - self.diameter//2, self.pos_y - self.diameter//2, self.diameter, self.diameter)
		#pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)

		pygame.draw.circle(screen, (224, 212, 0), (self.pos_x, self.pos_y), self.diameter//2)

		#exponential fall calculation of bird
		if self.start:
			self.pos_y += int((self.const)**1.1)
			self.const += 0.05

		
		#drawing animation for immunity
		if self.immune:
				
			pygame.draw.circle(screen, (210, 0, 0), (self.pos_x, self.pos_y), self.circle_rad, 2)

			if self.animate_num % 2 == 0:
				self.circle_rad += 2
			else:
				self.circle_rad -= 2

			self.animate_num += 1

		else:
			pass

	def move(self):
		if self.start:
			self.pos_y += self.jump_vel
			
			self.const = 0.15

		


class Pipes():
	def __init__(self):
		self.pipes = {}
		self.in_between_space = 92
		self.velocity = -2
		self.pipe_width = 65
		self.dict_no = 0
		self.hitbox = {}


	#randomly generates the pipes pos and heights
	def generate(self, x = 770):
		self.height1 = random.randint(50, 240)
		self.height2 = screen_height - (self.height1+self.in_between_space)
		self.x = x
		self.pipes[self.dict_no] = [self.x, (self.height1, self.height2)]

		self.dict_no += 1
		
	def draw(self):

		for key in self.pipes:
			pipe = self.pipes[key]

			#makes pipes move left(increments vel to x (to move) and adds it bact to dict)
			x = pipe[0]
			if bird.start:
				x += self.velocity
				self.pipes[key][0] = x

			height1 = pipe[1][0]
			height2 = pipe[1][1]

			#checking if bird passes pipe and increments score
			if x == bird.pos_x - 80:
				if bird.score == bird.high_score:
					bird.high_score += 1
				
				bird.score += 1 

				#forgenerating powerups randomly
				if (random.randint(0, 5)) == 1: #1/5 chance
					if not(bird.immune):
						powerup.generate(key)


			self.hitbox[key] = [pygame.Rect(x, 0, self.pipe_width, height1)
									,pygame.Rect(x, screen_height, self.pipe_width, height2 * -1)]
			
			
			#drawing pipes --------- this part of code changed due to bottom pipes not being visible by previos code.
            
            #pygame.draw.rect(screen, (0, 207, 17), self.hitbox[key][0])#pipe 1
			#pygame.draw.rect(screen, (0, 207, 17), self.hitbox[key][1])#pipe 2
        
			
			pygame.draw.rect(screen, (0, 207, 17), pygame.Rect(x, 0, self.pipe_width, height1))#pipe 1
			pygame.draw.rect(screen, (0, 207, 17), pygame.Rect(x, screen_height - height2, self.pipe_width, height2))#pipe 2

			#drawing pipe hitboxes
			#pygame.draw.rect(screen, (255, 0, 0), self.hitbox[key][0], 2)
			#pygame.draw.rect(screen, (255, 0, 0), self.hitbox[key][1], 2)
			

		#generating new pipes
		#the num determines the frequency of pipes(higher is greater)
		if bird.start:
			if x > 480 and x < 484:
				pipes.generate()



gameOver = False
k=0
def collision():
	global gameOver, start_num, k
	for key in pipes.hitbox:
		pipe_hitbox1 = pipes.hitbox[key][0]
		pipe_hitbox2 = pipes.hitbox[key][1]

		#checking powerup collisions:
		try:
			powerup_hitbox = powerup.hitbox[key]
			
			if bird.hitbox[1] + bird.diameter > powerup_hitbox[1] and bird.hitbox[1] < powerup_hitbox[1] + powerup.diameter:
				if bird.hitbox[0] + bird.diameter > powerup_hitbox[0] and bird.hitbox[0] < powerup_hitbox[0] + powerup.diameter:
					
					bird.immune = True
					k+=1
					

		except:
			pass
							

		#checking hitbox collisions between bird and all pipes(both bottom and top pipes)
		if bird.hitbox[1] < pipe_hitbox1[3] and (bird.hitbox[0] + bird.diameter > pipe_hitbox1[0] 
								and bird.hitbox[0] < pipe_hitbox1[0] + pipes.pipe_width):
			gameOver = True



		#calculate pipe 2 height from top
		pipe2_height = screen_height - (pipe_hitbox2[3]*-1)
		
		if bird.hitbox[1] + bird.diameter > pipe2_height and (bird.hitbox[0] + bird.diameter > pipe_hitbox2[0]
							and bird.hitbox[0] < pipe_hitbox1[0] +  pipes.pipe_width):
	
			gameOver = True


		#checking if bird exits screen (top or bottom)
		if bird.hitbox[1] + bird.diameter < 0 or bird.hitbox[1] > screen_height:
			gameOver = True
			bird.immune = False





	if not(bird.immune):
		if gameOver:
			
			start_num += 1
			i = 0
			bird.pos_y = 200
			bird.score = 0
			bird.const = 0

			pipes.dict_no = 0
			powerup.powerups.clear()
			powerup.hitbox.clear()
			pipes.pipes.clear()
			pipes.hitbox.clear()

			gameOver_text = font.render('Game over', 5, (255, 0, 0))
			#setting ms exactly to center screen
			screen.blit(gameOver_text, (screen_width//2 - gameOver_text.get_width()//2, screen_height//2 - gameOver_text.get_height()//2))
			pygame.display.update()

			#for displaying msg longer
			while i < 75:
				pygame.time.delay(10)
				i += 1

			gameOver = False
			bird.start = False

	else:
		if gameOver:

			bird.pos_y = 200
			bird.const = 0
			pipes.dict_no = 0
			powerup.powerups.clear()
			powerup.hitbox.clear()
			pipes.pipes.clear()
			pipes.hitbox.clear()

			number = 3
			#to display 3....2....1
			for count in range(3):
				#to reset screen every num blit to stop overlapping
				screen.blit(bg, (0,0))
				bird.draw()

				immune_text = font.render('Immune:  '+ str(number), 5, (255, 0, 0))
				#setting msg exactly to center screen
				screen.blit(immune_text, (screen_width//2 - immune_text.get_width()//2, screen_height//2 - immune_text.get_height()//2))
				pygame.display.update()

				time.sleep(0.6)

				number -= 1

			pipes.generate(x = 490) #to prevent error of x refrenced before assignment
			bird.immune = False
			gameOver = False



def redrawGameWin():
	
	screen.blit(bg, (0,0))

	bird.draw()
	
	pipes.draw()

	powerup.draw()

	collision()

	#displaying scores to screen
	score_text = font2.render('Score: '+ str(bird.score), 5, (100, 0, 255))
	screen.blit(score_text, (screen_width - 600, 0))

	high_score_text = font2.render('High Score: '+ str(bird.high_score), 5, (100, 0, 255))
	screen.blit(high_score_text, (screen_width - 350, 0))

	pygame.display.update()
	clock.tick(120)


screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("bouncy bird")
clock = pygame.time.Clock()

bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (screen_width, screen_height))

bird = Bird(140,200)
pipes = Pipes()
powerup = Powerup()
pipes.generate()

#opening and retreiving high score from json file when game first opens
try:
	with open('score.json', 'r') as f:
		data = json.load(f)
		bird.high_score = data["highscore"]
except:
	pass


font = pygame.font.SysFont('arial', 50, True)
font2 = pygame.font.SysFont('arial', 25, True)


#variable to determine if game started after loosing again or fresh start
start_num = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:

			#saving highscore in json file
			high_score = {"highscore": bird.high_score}
			with open('score.json', 'w') as f:
				json.dump(high_score, f, indent = 2)

			pygame.quit()
			sys.exit()
		
		#juming (cheking key press)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird.move()



	keys = pygame.key.get_pressed()

	#starting game by enter
	if not(bird.start):
		if keys[pygame.K_RETURN]:
			bird.start = True

			if start_num != 0:
				pipes.generate()



	redrawGameWin()


