# variables
import numpy as np
import random as rand
import pandas as pd
import seaborn as sns
import time, json, sys

class Rabbit:
	def __init__(self, gender, speed, age):
		# Female Rabbits have fertility 1-5 at birth
		if gender == 1:
			self.rarray = np.array([[gender], [speed], [age], [rand.randint(1,5)]])
		# Male Rabbits have fertiliy 0
		if gender == 0:
			self.rarray = np.array([[gender], [speed], [age], [0]])

	def get_arr(self):
		return self.rarray

class Fox: 
	def __init__(self, hunger, age):
		self.farray = np.array([[hunger], [age]])

	def set_hunger(self, hunger):
		self.farray[0] = hunger

simulation = True

# Rabbit Variables
rpop = np.empty((0,4), int)
rabbit_data = np.empty((0,4), int)
rpopulation = 0
rabbitfood = 0
starvedr = 0
deadrabbits = 0
rmating = 10

# Fox Variables
fpop = np.empty((0,2), int)
fpopulation = 0

# Simulator Variables
day = 1
year = 12
simnumber = 1