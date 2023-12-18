# Eco System Simulator in pygame
import numpy as np
import random as rand
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time, pygame, sys

# Screen for Simulation
# ---------------------

pygame.init()
width, height = 1500, 1000
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
main = True

white = (255, 255, 255)
brown = (150, 75, 0)

# Rabbit Variables
# ----------------

class Rabbit:
	def __init__(self, speed, size, x, y):
		self.speed = speed
		self.size = size
		self.position = [x, y]
		self.hunger = 100

	def draw_rabbit(self, position):
		pygame.draw.rect(screen, brown, (self.position[0], self.position[1], self.size, self.size))

	def move(self):
		x = self.position[0]
		y = self.position[1]
		move = np.random.randint(0, 100)
		if move > 90:
			direction = rand.choice(["left", "right", "up", "down"])

			if direction == "left":
				self.position[0] -= self.speed
			elif direction == "right":
				self.position[0] += self.speed
			elif direction == "up":
				self.position[1] -= self.speed
			elif direction == "down":
				self.position[1] += self.speed

			# Constrain Rabbit to screen
			if x > 1500:
				self.position[0] = 1500
			elif x < 0:
				self.position[0] = 0

			elif y > 1000:
				self.position[1] = 1000
			elif y < 0:
				self.position[1] = 0

	def get_position(self):
		return self.position

def create_rabbit(n):
	global rpop
	while n > 0:
		speed = np.random.randint(10, 20)
		size = np.random.randint(10, 40)
		x, y = width - np.random.randint(0, width), height - np.random.randint(0, height)

		r = Rabbit(speed, size, x, y)
		rpop.append(r)
		n -= 1

while main == True:
	rpop = []
	create_rabbit(15)
	while True:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		screen.fill(white)

		for rabbit in rpop:
			rabbit.move()
			rabbit.draw_rabbit(rabbit.position)

		pygame.display.flip()

		pygame.time.Clock().tick(60)
