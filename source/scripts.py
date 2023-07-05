# functions
import random as rand
import numpy as np
import time, json
import matplotlib.pyplot as plt
from variables import *

def createRabbit(x):
	global rnumber, rpop, rpopulation
	while(x > 0):
		rnumber += 1
		rpop.append(Rabbit(rnumber, rand.randint(0, 1), rand.randint(50, 70), rand.randint(3,5)))
		x -= 1
		rpopulation += 1

def createFox(x):
	global fnumber, fpop, fpopulation
	while(x > 0):
		fnumber += 1
		fpop.append(Fox(fnumber, rand.randint(3, 5)))
		x -= 1
		fpopulation += 1

# generates the rabbits food for the day
def rabbitFood():
	global rpopulation, rabbitfood, deadrabbits
	luck = rand.randint(1, 9)
	if luck <= 8:
		rabbitfood = rpopulation
	elif luck > 8:
		rabbitfood = rpopulation - rand.randint(5, 10)
	deadrabbits = rpopulation - rabbitfood

def foxEat():
	global deadrabbits, rpopulation, rpop, lesshunger
	for obj in fpop:
		rpop.sort(key=lambda x: x.speed)
		if rand.randint(1, 100) > 40:
			while obj.hunger > 0:
				for obj in rpop:
					if rand.randint(1, 100) <= obj.speed:
						rpop.pop(obj.number)
						deadrabbits += 1
						rpopulation -= 1
						lesshunger += 1
		obj.set_hunger(obj.hunger - lesshunger)
		lesshunger = 0
	if deadrabbits > 0:
		print("Foxes have eaten " + str(deadrabbits) + " rabbits!")
		deadrabbits = 0
	
def slowestDie(deadrabbits):
	global rpopulation, rpop
	rpop.sort(key=lambda x: x.speed)
	while deadrabbits > 0:
		rpop.pop()
		rpopulation -= 1
		deadrabbits -= 1
	rpop.sort(key=lambda x: x.number)

def rabbitBirth():
	global rmating, offspring, totaloffspring
	if day == rmating:
		offspring = 0
		for obj in rpop:
			if obj.gender == 1:
				offspring += obj.fertility
		createOffspring(offspring)
		rmating += rand.randint(18, 25)
		# listRabbits()
		print(" ")
		print("There has been " + str(offspring) + " offspring.")

def createOffspring(offspring):
	global rnumber, rpopulation, rmating, rpop
	while offspring > 0:
		for obj in rpop:
			if obj.age >= 1 and obj.age <= 4:
				if obj.gender == 0:
					rnumber += 1
					s = obj.speed + rand.randint(-3, 3)
					rpop.append(Rabbit(rnumber, rand.randint(0, 1), s, 0))
					offspring -= 1
					rpopulation += 1

# json_string = json.dumps([ob.__dict__ for ob in rpop])
# print(json_string)
def listRabbits():
	for obj in rpop:
		rspeeds.append(obj.speed)
	rspeeds.sort()
	plt.plot(rspeeds)
	plt.show()

def nextDay():
	global rpopulation, rabbitfood, deadrabbits, rmating, rpop
	print(" ")
	print("Day: " + str(day))
	rpopulation = len(rpop)
	if rabbitfood < rpopulation:
		print("There was a food shortage!! The " + str(deadrabbits) + " slowest rabbits starved.")
		slowestDie(deadrabbits)
	print("Rabbit Population: " + str(rpopulation))

# every 12 days, 
def nextYear():
	global rpopulation, day, year, rpop
	passers = 0
	fixRNumbers()
	rpop.sort(key=lambda x: x.number)
	for obj in rpop:
		obj.set_age(obj.age + 1)
		if obj.age == 9:
			rpop.pop(int(obj.number))
			rpopulation -= 1
			passers += 1
		if obj.age > 2:
			c = obj.age * 5
			c -= 5
			if rand.randint(0, 100) <= c:
				rpop.pop(int(obj.number))
				rpopulation -= 1
				passers += 1
	year += 12
	print(str(passers) + " rabbits have died of old age.")

# make all rnumbers equivalent to index
def fixRNumbers():
	for i in range(len(rpop)):
		rpop[i].set_number(i)

def checkRabbitPop():
	global day, simulation
	if rpopulation >= 1:
		rabbitBirth()
		fixRNumbers()
		
		time.sleep(1)

		day += 1
		if day == year:
			nextYear()
	elif rpopulation <= 0:
		simulation = False


def main():
	while simulation == True:
		rabbitFood()
		foxEat()
		nextDay()
		checkRabbitPop()
		if day == 10:
			createFox(10)