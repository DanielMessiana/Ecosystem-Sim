# variables
import random as rand
import time, json, pygame, sys

class Rabbit:
	def __init__(self, gender, speed, age):
		self.gender = gender
		self.speed = speed
		self.age = age
		# Female
		if gender == 1:
			self.fertility = rand.randint(1,5)
	def set_age(self, age):
		self.age = age

class Fox: 
	def __init__(self, hunger):
		self.hunger = hunger

	def set_hunger(self, hunger):
		self.hunger = hunger

simulation = True
# Rabbit Variables
rpop = []
rpopulation = 0
rspeeds = []
rabbitfood = 0
starvedr = 0
deadrabbits = 0
rmating = 10
totaloffspring = 0
# Fox Variables
fpop = []
fpopulation = 0
day = 1
dayrecord = {}
year = 12
finalstats = []
simnumber = 1