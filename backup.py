import random as rand
import numpy as np
import time, json
import matplotlib.pyplot as plt

from variables import *
from scripts import *

# Eco System Simulator

class Rabbit:
	def __init__(self, number, gender, speed, age):
		self.number = number
		self.gender = gender
		self.speed = speed
		self.age = age
		# Female
		if gender == 1:
			self.fertility = rand.randint(1,3)
	def set_age(self, age):
		self.age = age

	def set_number(self, number):
		self.number = number

class Fox: 
	def __init__(self, number, hunger):
		self.number = number
		self.hunger = hunger

	def set_hunge(self, hunger):
		self.hunger = hunger




createrabbit(50)
#listrabbits()
while simulation == True:
	genrabbitfood()
	nextday()

	if rpopulation >= 1:
		rabbitbirth()
		fixrnumbers()
		if rpopulation >= 100000:
			time.sleep(1)

		day += 1
		if day == year:
			nextyear()
	elif rpopulation <= 0:
		simulation = False
	