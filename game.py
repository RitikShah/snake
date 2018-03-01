import pygame
import time
import random

class Game:
	windowsize = (800,600)

	white = (255, 255, 255)
	black = (0, 0, 0)
	red = (255, 0, 0)

	fps = 30

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
		self.tail = 5
		self.time = 0

		self.apple_x = random.randrange(10, self.windowsize[0]-10)
		self.apple_y = random.randrange(10, self.windowsize[1]-10)
		self.gameloop()

	def quitgame(self):
		pygame.quit()
		quit()

	def text_objects(text, objects):
		text = str(text)
	    font = pygame.font.Font(font_type, size)
		textsurf = font.render(text, True, color)

	def text_to_screen(self, screen, text, x, y, color = red, size = 20, font_type = 'fonts/Courier New.ttf'):
		textsurf, textrect = text_objects(text)
		textrect.center = (windowsize[0]/2) , (windowsize[1]/2)

	    
	    
	    screen.blit(textsurf, textrect)

	def gameover(self, deathmessage):
		self.gamedisplay.fill(self.black)
		over = True
		while over:
			if event.type == pygame.QUIT:
				self.quitgame()

			self.text_to_screen(self.gamedisplay, deathmessage, self.windowsize[0]/8, self.windowsize[1]/2, self.red)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameover = False
						self.crashed = True
						self.quitgame()
					if event.key == pygame.K_c:
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

			# Border
			if self.snake[0][0] >= self.windowsize[0] or self.snake[0][0] < 0 or self.snake[0][1] >= self.windowsize[1] or self.snake[0][1] < 0:
				self.gameover("Game Over, press C to play again, or Q to quit")

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
			
			# Display snake
			for item in self.snake:
				pygame.draw.rect(self.gamedisplay, self.white, [item[0], item[1], self.block_size, self.block_size])

			if self.time > 100:
				for item in self.snake:
					if item == self.snake[0]:
						continue

					if abs(self.snake[0][0] - item[0]) < self.block_size or abs(self.snake[0][1] - item[1]) < self.block_size:
						self.gameover("Game Over, press C to play again, or Q to quit")

			pygame.display.update()

			self.snake.append([self.snake[0][0], self.snake[0][1]])
			if len(self.snake) > self.tail:
				del self.snake[1]

			# if eatapple
			if abs(self.snake[0][0] - self.apple_x) < self.block_size*2 and abs(self.snake[0][1] - self.apple_y) < self.block_size*2:
				self.apple_x = round(random.randrange(10, self.windowsize[0]-10)/10.0) * 10.0
				self.apple_y = round(random.randrange(10, self.windowsize[1]-10)/10.0) * 10.0

				self.tail += 10

			# tick clock @ fps
			self.clock.tick(self.fps)

			self.time += 1
			