# functions
import numpy as np
import random as rand
import pandas as pd
import seaborn as sns
import time, json, sys
import matplotlib.pyplot as plt
from variables import *

def createRabbit(x):
	global rpop, rpopulation
	while(x > 0):
		n = Rabbit(rand.randint(0, 1), rand.randint(50, 70), rand.randint(3,5))
		rpop = np.append(rpop, n.get_arr().T, axis=0)
		x -= 1
		rpopulation += 1

def createFox(x):
	global fpop, fpopulation
	while(x > 0):
		fpop.append(Fox(rand.randint(1, 2), rand.randint(3,5)))
		x -= 1
		fpopulation += 1

# generates the rabbits food for the day
def rabbitFood():
	global rpopulation, rabbitfood, starvedr
	luck = rand.randint(1, 9)
	if luck <= 8:
		rabbitfood = rpopulation
	elif luck > 8:
		rabbitfood = rpopulation - rand.randint(1, 6)
		starvedr = rpopulation - rabbitfood

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

def reproduce(rpop):
	global rpopulation
	offspring = 0
	for index, row in enumerate(rpop):
		# If the rabbit is male or an age younger than 2, it checks the next rabbit
		if row[3] == 0 or row[2] <= 1:
			continue

		if rand.randint(1, 10) >= row[3]:
			gene1 = row[1]
			gene2 = rand.choice(rpop[:,1])

			g = rand.randint(0, 1)
			if g == 0:
				o = Rabbit(0, ((gene1 + gene2)/2)+rand.randint(-2, 2), 0)
				rpop = np.append(rpop, o.get_arr().T, axis=0)
				rpopulation += 1
			elif g == 1:
				o = Rabbit(1, ((gene1 + gene2)/2)+rand.randint(-2, 2), 0)
				rpop = np.append(rpop, o.get_arr().T, axis=0)
				rpopulation += 1


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
	if len(rpop):
		rpop[:, 2] += 1

		mask = (rpop[:, 2] == 7) | ((rpop[:, 2] > 2) & (np.random.randint(0, 100, size=len(rpop)) <= rpop[:, 2] * 5))

		rpop = rpop[~mask]

		rpopulation -= np.sum(mask)
	else:
		simulation = False
	if len(fpop):
		for index, fox in enumerate(fpop):
			fox.set_age(fox.age + 1)
			if fox.age == 6:
				fpop.pop(index)
				fpopulation -= 1
				break
			if fox.age > 2:
				c = fox.age * 5
				c -= 5
				if rand.randint(0, 100) <= c:
					fpop.pop(index)
					fpopulation -= 1
	year += 12

def main():
	global simulation, finalstats, simnumber, rDF
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
	print(rpop.shape)
	rDF = pd.DataFrame(rpop, columns=['Gender', 'Speed', 'Age', 'Fertility'])
	print(rDF)

	#setVariables()
	simnumber += 1

def setVariables():
	global simulation, firstgame, rpop, rpopulation, rspeeds, rabbitfood, starvedr, deadrabbits, rmating, totaloffspring, fpop, fpopulation, day, year
	simulation = True
	rpop = []
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

def showPlots():
	sns.pairplot(rDF)
	plt.show()