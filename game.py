import pygame
import time
import random

class Game:
	windowsize = (800,600)

	white = (255, 255, 255)
	black = (0, 0, 0)
	red = (255, 0, 0)
	green = (0, 155, 0)

	fps = 60

	block_size = 10

	def __init__(self):
		pygame.init()
		self.crashed = False
		self.clock = pygame.time.Clock()
		self.gamedisplay = pygame.display.set_mode(self.windowsize)
		pygame.display.set_caption('Sither')

	def newgame(self):
		self.snake = [[self.windowsize[0]/2, self.windowsize[1]/2]]
		self.change_x = self.block_size
		self.change_y = 0
		self.direction = 'r'
		self.tail = 4
		self.time = 0

		self.randapple()
		self.gameloop()

	def startscreen(self):
		intro = True

		while intro:
			self.screenwrap = False
			self.gamedisplay.fill(self.black)
			self.text_to_screen("Slither", color=self.green, size = 100)
			
			self.text_to_screen("C to play w/o screen wrap", 0, 55, self.white)
			self.text_to_screen("V to play w/ screen wrap", 0, 80, self.white)
			self.text_to_screen("Q to quit", 0, 105, self.white)
			pygame.display.update()

			for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.quitgame()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							intro = False
							self.quitgame()
						if event.key == pygame.K_c:
							intro = False
							self.screenwrap = False
							self.newgame()
						if event.key == pygame.K_v:
							self.screenwrap = True
							intro = False
							self.newgame()

			self.clock.tick(self.fps/4)

	def randapple(self):
		self.apple_x = round(random.randrange(10, self.windowsize[0]-10)/10.0) * 10.0
		self.apple_y = round(random.randrange(10, self.windowsize[1]-10)/10.0) * 10.0

	def quitgame(self):
		pygame.quit()
		quit()

	def text_objects(self, text, color=red, size=20, font_type='fonts/Courier New.ttf'):
		text = str(text)
		font = pygame.font.Font(font_type, size)
		textsurf = font.render(text, True, color)
		return textsurf, textsurf.get_rect()

	def text_to_screen(self, text, x_displace=0, y_displace=0, color=red, size=20):
		textsurf, textrect = self.text_objects(text, color, size)
		textrect.center = (self.windowsize[0]/2), (self.windowsize[1]/2) + y_displace
		self.gamedisplay.blit(textsurf, textrect)

	def gameover(self):
		self.gamedisplay.fill(self.black)
		over = True
		while over:
			self.text_to_screen("Game Over", 0, -25, self.red, 80)
			self.text_to_screen("C to play w/o screen wrap", 0, 55, self.white)
			self.text_to_screen("V to play w/ screen wrap", 0, 80, self.white)
			self.text_to_screen("Q to quit", 0, 105, self.white)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quitgame()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameover = False
						self.crashed = True
						self.quitgame()
					if event.key == pygame.K_c:
						over = False
						self.screenwrap = False
						self.newgame()
					if event.key == pygame.K_v:
						self.screenwrap = True
						over = False
						self.newgame()

	def gameloop(self):
		while not self.crashed:
			# Key Listeners
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quitgame()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT and self.direction != 'r':
						self.change_x = -self.block_size
						self.change_y = 0
						self.direction = 'l'
					elif event.key == pygame.K_RIGHT and self.direction != 'l':
						self.change_x = self.block_size
						self.change_y = 0
						self.direction = 'r'
					elif event.key == pygame.K_UP and self.direction != 'd':
						self.change_y = -self.block_size
						self.change_x = 0
						self.direction = 'u'
					elif event.key == pygame.K_DOWN and self.direction != 'u':
						self.change_y = self.block_size
						self.change_x = 0
						self.direction = 'd'
					elif event.key == pygame.K_q:
						self.crashed = True
						self.quitgame()

			# Border
			if self.screenwrap:
				if self.snake[0][0] > self.windowsize[0]:
					self.snake[0][0] = 0
				elif self.snake[0][0] < 0:
					self.snake[0][0] = self.windowsize[0]
				if self.snake[0][1] > self.windowsize[1]:
					self.snake[0][1] = 0
				elif self.snake[0][1] < 0:
					self.snake[0][1] = self.windowsize[1]
			else:
				if self.snake[0][0] > self.windowsize[0] or self.snake[0][0] < 0 or self.snake[0][1] > self.windowsize[1] or self.snake[0][1] < 0:
					self.gameover()

			# Keep moving
			'''
			for i in range(len(self.snake)):
				self.snake[0][0] += self.snake[0][1]
				self.snake[1][0] += self.snake[1][1]

				if i != 0:
					self.snake[0][1] = self.snake[0][1]
					self.snake[1][1] = self.snake[1][1]
			'''

			self.snake[0][0] += self.change_x
			self.snake[0][1] += self.change_y

			# Display
			self.gamedisplay.fill(self.black)
			pygame.draw.rect(self.gamedisplay, self.red, [self.apple_x, self.apple_y, self.block_size, self.block_size])
			
			self.text_to_screen("Score: " + str(self.tail-4), -300, -280, self.white, 25)

			# Display snake
			for item in self.snake:
				pygame.draw.rect(self.gamedisplay, self.white, [item[0], item[1], self.block_size, self.block_size])

			if self.time > 100:
				for item in self.snake[1:]:
					if item == self.snake[0]:
						self.gameover()

			pygame.display.update()

			self.snake.append([self.snake[0][0], self.snake[0][1]])
			if len(self.snake) > self.tail:
				del self.snake[1]

			# if eatapple
			if abs(self.snake[0][0] - self.apple_x) < self.block_size*2 and abs(self.snake[0][1] - self.apple_y) < self.block_size*2:
				self.randapple()

				self.tail += 1

			# tick clock @ fps
			self.clock.tick(self.fps)

			self.time += 1
			