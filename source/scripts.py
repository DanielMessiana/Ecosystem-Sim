# functions
import random as rand
import time, json, pygame, sys
import matplotlib.pyplot as plt
from variables import *

def createRabbit(x):
	global rpop, rpopulation
	while(x > 0):
		rpop.append(Rabbit(rand.randint(0, 1), rand.randint(50, 70), rand.randint(3,5)))
		x -= 1
		rpopulation += 1

def createFox(x):
	global fpop, fpopulation
	while(x > 0):
		fpop.append(Fox(rand.randint(1, 3)))
		x -= 1
		fpopulation += 1

# generates the rabbits food for the day
def rabbitFood():
	global rpopulation, rabbitfood, starvedr
	luck = rand.randint(1, 9)
	if luck <= 8:
		rabbitfood = rpopulation
	elif luck > 8:
		rabbitfood = rpopulation - rand.randint(5, 10)
		starvedr = rpopulation - rabbitfood

def foxEat():
	global deadrabbits, rpopulation, rpop
	for fox in fpop:
		rpop.sort(key=lambda x: x.speed)
		if rand.randint(1, 100) > 40:
			while fox.hunger > 0:
				for index, rabbit in enumerate(rpop):
					if rand.randint(1, 100) <= rabbit.speed and rabbit.age > 1:
						rpop.pop(index)
						deadrabbits += 1
						rpopulation -= 1
						fox.set_hunger(fox.hunger - 1)
					if fox.hunger == 0:
						break
	if deadrabbits > 0:
		print("Foxes have eaten " + str(deadrabbits) + " rabbits!")
		deadrabbits = 0
	
def slowestDie(starvedr):
	global rpopulation, rpop
	rpop.sort(key=lambda x: x.speed)
	while starvedr > 0:
		rpop.pop()
		rpopulation -= 1
		starvedr -= 1

def rabbitBirth():
	global rmating, offspring, totaloffspring
	if day == rmating:
		offspring = 0
		for rabbit in rpop:
			if rabbit.gender == 1:
				offspring += rabbit.fertility
		createOffspring(offspring)
		rmating += rand.randint(18, 25)
		# listRabbits()
		print("There has been " + str(offspring) + " offspring.")

def createOffspring(offspring):
	global rpopulation, rmating, rpop
	while offspring > 0:
		for rabbit in rpop:
			if rabbit.age >= 1 and rabbit.age <= 4:
				if rabbit.gender == 0:
					s = rabbit.speed + rand.randint(-3, 3)
					rpop.append(Rabbit(rand.randint(0, 1), s, 0))
					offspring -= 1
					rpopulation += 1

# json_string = json.dumps([ob.__dict__ for ob in rpop])
# print(json_string)
def listRabbits():
	for rabbit in rpop:
		rspeeds.append(rabbit.speed)
	rspeeds.sort()
	plt.plot(rspeeds)
	plt.show()

def nextDay():
	global rpopulation, rabbitfood, starvedr, rmating, rpop
	print(" ")
	print("Day: " + str(day))
	if fpopulation > 0:
			foxEat()
	rabbitBirth()
	rpopulation = len(rpop)
	if starvedr > 0:
		print("There was a food shortage!! The " + str(starvedr) + " slowest rabbits starved.")
		slowestDie(starvedr)
		starvedr = 0
	if day == year:
		nextYear()
	print("Rabbit Population: " + str(rpopulation))

# every 12 days, 
def nextYear():
	global rpopulation, day, year, rpop
	passers = 0
	for index, rabbit in enumerate(rpop):
		rabbit.set_age(rabbit.age + 1)
		if rabbit.age == 9:
			rpop.pop(index)
			rpopulation -= 1
			passers += 1
		if rabbit.age > 2:
			c = rabbit.age * 5
			c -= 5
			if rand.randint(0, 100) <= c:
				rpop.pop(index)
				rpopulation -= 1
				passers += 1
	year += 12
	print(str(passers) + " rabbits have died of old age.")

def checkRabbitPop():
	global day, simulation
	if rpopulation >= 1:
		if rpopulation >= 200:
			time.sleep(1)

		day += 1
	elif rpopulation <= 0:
		simulation = False

def main():
	while simulation == True:
		rabbitFood()
		nextDay()
		checkRabbitPop()
		for fox in fpop:
			if rand.randint(1, 100) < 65:
				fox.set_hunger(fox.hunger + 1)
		if day == 15:
			createFox(10)