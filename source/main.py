# Eco System Simulator
import numpy as np
import random as rand
import pandas as pd
import seaborn as sns
import time, json, sys
import matplotlib.pyplot as plt

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

def resetVar():
	global simulation, firstgame, rpop, rpopulation, rspeeds, rabbitfood, starvedr, deadrabbits, rmating, totaloffspring, fpop, fpopulation, day, year
	simulation = True
	rpop = np.empty((0,4), int)
	rpopulation = 0
	rspeeds = []
	rabbitfood = 0
	starvedr = 0
	deadrabbits = 0
	rmating = 10
	totaloffspring = 0
	fpop = []
	fpopulation = 0
	day = 1
	year = 12

# Rabbit Functions
# ----------------

def createRabbit(x):
	global rpop, rpopulation
	while(x > 0):
		n = Rabbit(rand.randint(0, 1), rand.randint(50, 70), rand.randint(3,5))
		rpop = np.vstack([rpop, n.get_arr().T])
		x -= 1
		rpopulation += 1

# generates the rabbits food for the day
def rabbitFood():
	global rpopulation, rabbitfood, starvedr
	luck = rand.randint(1, 9)
	if luck <= 8:
		rabbitfood = rpopulation
	elif luck > 8:
		rabbitfood = rpopulation - rand.randint(1, 6)
		starvedr = rpopulation - rabbitfood

"""
def slowestDie():
	global rpopulation, rpop, starvedr
	sorted_indices = rpop[1].argsort()
	rpop = rpop[:, sorted_indices]
	while starvedr > 0:
		rpop = np.delete(rpop, 0)
		rpopulation -= 1
		starvedr -= 1
"""

def reproduce(rpop):
	global rpopulation
	new_rabbits = np.empty((0, 4), int)
	for index, rabbit in enumerate(rpop):
		# If the rabbit is male or an age younger than 2, it checks the next rabbit
		if rabbit[3] == 0 or rabbit[2] <= 1:
			continue
		if rand.randint(1, 10) >= rabbit[3]+2:
			gene1 = rabbit[1]
			gene2 = rand.choice(rpop[:,1])
			new_speed = ((gene1 + gene2)/2)+rand.randint(-2, 2)

			g = rand.randint(0, 1)
			o = Rabbit(g, new_speed, 0)
			new_rabbits = np.vstack([new_rabbits, o.get_arr().T])
			rpopulation += 1
	rpop = np.vstack([rpop, new_rabbits])

# Fox Functions
# -------------

def createFox(x):
	global fpop, fpopulation
	while(x > 0):
		fpop.append(Fox(rand.randint(1, 2), rand.randint(3,5)))
		x -= 1
		fpopulation += 1

def foxEat():
	global deadrabbits, rpopulation, rpop, fpop
	deadrabbits = 0
	rpop.sort(key=lambda x: x.rarray[1])
	for fox in fpop:
		if rand.randint(1, 100) <= 40:
			for index, rabbit in enumerate(rpop):
				if fox.hunger < 1:
					break
				if rand.randint(1, 100) >= rabbit.rarray[1] and rabbit.rarray[2] > 1:
					rpop.pop(index)
					deadrabbits += 1
					rpopulation -= 1
					fox.set_hunger(fox.hunger - 1)
				else:
					continue
	if deadrabbits > 0:
		deadrabbits = 0

# Simulation Functions
# --------------------

def nextDay():
	global rpopulation, rabbitfood, starvedr, rmating, rpop, day
	#rabbitBirth()
	rpopulation = len(rpop)
	#if starvedr > 0:
		#slowestDie()
	reproduce(rpop)
	if day == year:
		nextYear()
	if fpopulation > 0:
		foxEat()
	day += 1

# every 12 days, 
def nextYear():
	global rpopulation, year, rpop, fpop, fpopulation, simulation
	if rpop.shape[0] > 0:
		rpop[:, 2] += 1
		rpassed = []
		for i, rabbit in enumerate(rpop):
			if rabbit[2] == 8:
				rpassed.append(i)
				rpopulation -= 1
			elif rabbit[2] > 2 and rabbit[2] != 7:
				c = rabbit[2] * 5
				if rand.randint(0, 100) >= c:
					prassed.append(i)
					rpopulation -= 1
		rpop = np.delete(rpop, rpassed, axis=0)
	else:
		simulation = False
	if fpop.shape[0] > 0:
		fpop[:, 2] += 1
		fpassed = []
		for i, fox in enumerate(fox):
			if fox[2] == 8:
				fpassed.append(i)
				fpopulation -= 1
			elif fox[2] > 2 and fox[2] != 7:
				c = rabbit[2] * 5
				if rand.randint(0, 100) >= c:
					fpassed.append(i)
					fpopulation -= 1
		fpop = np.delete(fpop, fpassed, axis=0)
	year += 12

def main(maxday):
	global simulation, finalstats, simnumber, rDF, rpop, rabbit_data
	createRabbit(50)
	while simulation == True:
		rabbitFood()
		nextDay()
		if rpopulation < 1:
			simulation = False
		if fpopulation > 0:
			for fox in fpop:
				if fox.hunger >= 2:
					continue
				if rand.randint(1, 100) <= 40:
					fox.set_hunger(fox.hunger + 1)
		if day == 25:
			pass
			#createFox(5)
		if day == maxday:
			simulation = False
	#print(simnumber)
	print(f"The shape of the rabbit data is: {rabbit_data.shape}")
	rabbit_data = np.vstack([rabbit_data, rpop])
	resetVar()
	simnumber += 1

def simulation():
	sims = 50
	maxday = 50

	for i in range(sims):
		main(maxday)

	rDF = pd.DataFrame(rabbit_data, columns=['Gender', 'Speed', 'Age', 'Fertility'])

	plt.plot(rDF['Speed'], rDF['Age'], 'ok')
	plt.show()


simulation()

# This function runs {sims} simulations, each one of {maxday} days





