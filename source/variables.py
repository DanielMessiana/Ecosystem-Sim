# variables
import random as rand
import time, json

class Rabbit:
	def __init__(self, number, gender, speed, age):
		self.number = number
		self.gender = gender
		self.speed = speed
		self.age = age
		# Female
		if gender == 1:
			self.fertility = rand.randint(1,5)
	def set_age(self, age):
		self.age = age

	def set_number(self, number):
		self.number = number

class Fox: 
	def __init__(self, number, hunger):
		self.number = number
		self.hunger = hunger

	def set_hunger(self, hunger):
		self.hunger = hunger

simulation = True
firstgame = True
rpop = []
rpopulation = 0
rnumber = 0
rspeeds = []
rabbitfood = 0
deadrabbits = 0
rmating = 10
totaloffspring = 0
g = 0
s = 0
# Fox Variables
fpop = []
fpopulation = 0
fnumber = 0
lesshunger = 0
day = 1
dayrecord = {}
year = 12

