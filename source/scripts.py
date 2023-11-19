# functions
import numpy as np
import random as rand
import pandas as pd
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
	
def slowestDie():
	global rpopulation, rpop, starvedr
	rpop = rpop[rpop[0].argsort()]
	while starvedr > 0:
		rpop = np.delete(rpop, 0)
		rpopulation -= 1
		starvedr -= 1

# Old reproduction functions
"""
def rabbitBirth():
	global rmating, offspring, totaloffspring
	if day == rmating:
		offspring = 0
		for rabbit in rpop:
			if rabbit.gender == 1:
				offspring += rabbit.fertility
		createOffspring(offspring)
		rmating += rand.randint(18, 32)
"""

"""
def createOffspring(offspring):
	global rpopulation, rmating, rpop
	while offspring > 0:
		for rabbit in rpop:
			if rabbit.age >= 1 and rabbit.age <= 4 and rabbit.gender == 0:
				s = rabbit.speed + rand.randint(-3, 3)
				rpop.append(Rabbit(rand.randint(0, 1), s, 0))
				offspring -= 1
				rpopulation += 1
"""

def nextDay():
	global rpopulation, rabbitfood, starvedr, rmating, rpop, day
	#rabbitBirth()
	rpopulation = len(rpop)
	if starvedr > 0:
		slowestDie()
	if day == year:
		nextYear()
	if fpopulation > 0:
		foxEat()
	day += 1

# every 12 days, 
def nextYear():
	global rpopulation, year, rpop, fpop, fpopulation, simulation
	if len(rpop):
		print(rpop.shape)
		rpop[:, 2] += 1
		for index, row in enumerate(rpop):	
			if row[2] == 7:
				rpop = np.delete(rpop, index, axis=0)
				rpopulation -= 1
				break
			if row[2] > 2:
				c = row[2] * 5
				if rand.randint(0, 100) <= c:
					rpop = np.delete(rpop, index, axis=0)
					rpopulation -= 1
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
			createFox(5)
		if day == maxday:
			simulation = False
	#print(simnumber)
	rDF = pd.DataFrame(rpop, columns=['Gender', 'Speed', 'Age', 'Fertility'])

	setVariables()
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
	print(rDF)