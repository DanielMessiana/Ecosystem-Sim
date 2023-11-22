# Eco System Simulator
import numpy as np
import random as rand
import pandas as pd
import streamlit as st
import seaborn as sns
import time, json, sys, os
import matplotlib.pyplot as plt

st.title('Ecosystem Simulator')

# Rabbit Variables
# ----------------

class Rabbit:
	def __init__(self, gender, speed, age, simnumber):
		"""
		Constructor Args/Rabbit Array Indices:
		
		0: Gender
		1: Speed
		2: Age
		3: Fertility
		4: Simnumber

		"""
		# Female Rabbits have fertility 1-5 at birth
		if gender == 1:
			self.rarray = np.array([[1], [speed], [age], [rand.randint(1,5)], [simnumber]])
		# Male Rabbits have fertiliy 0
		if gender == 0:
			self.rarray = np.array([[0], [speed], [age], [0], [simnumber]])

	def add_to_pop(self):
		global rpop, rpopulation
		rpop = np.vstack([rpop, self.rarray.T]) 
		rpopulation += 1

rpop = np.empty((0,5), int)
rabbit_data = np.empty((0,5), int)
rpopulation = 0

# Fox Variables
# ------------

class Fox: 
	def __init__(self, gender, hunger, age):
		"""
		Constructor Args/Fox Array Indices:

		0: Gender
		1: Hunger
		2: Age
		"""
		self.farray = np.array([[gender], [hunger], [age]])

	def add_to_pop(self):
		global fpop, fpopulation
		fpop = np.vstack([fpop, self.farray.T]) 
		fpopulation += 1

fpop = np.empty((0,2), int)
fpopulation = 0

# Simulator Variables and Functions
simulation = True
clear = lambda: os.system('clear')
day = 1
year = 365
simnumber = 1

def resetVar():
	global simulation, rpop, rpopulation, fpop, fpopulation, day, year, simnumber
	simulation = True
	rpop = np.empty((0,5), int)
	rpopulation = 0

	fpop = np.empty((0,3), int)
	fpopulation = 0

	day = 1
	year = 365
	simnumber += 1

def sigmoid(x):
	return np.exp(x)/1 + np.exp(x)

# Rabbit Functions
# ----------------

def createRabbit(x):
	global rpop, rpopulation
	while(x > 0):
		r = Rabbit(rand.randint(0, 1), rand.randint(40, 70), rand.randint(3,5), simnumber)
		r.add_to_pop()
		x -= 1

def reproduce():
	for index, rabbit in enumerate(rpop):
		# If the rabbit is male or an age younger than 2, it checks the next rabbit
		if rabbit[3] == 0 or rabbit[2] < 2:
			continue
		if rand.randint(1, 10) < rabbit[3]+1 and rabbit[1] > rand.randint(1, 100):
			
			i = rand.randint(1,3)
			while i > 0:
				sgene1 = rabbit[1]
				sgene2 = rand.choice(rpop[:,1])
				new_speed = (((sgene1 + sgene2)/2)+rand.randint(-2, 2)).round()
				if rand.randint(1,100) < 5:
					new_speed += rand.randint(-20, 20)

				g = rand.randint(0, 1)

				o = Rabbit(g, new_speed, 0, simnumber)
				o.add_to_pop()
				i -= 1

# Fox Functions
# -------------

def createFox(x):
	global fpop, fpopulation
	while(x > 0):
		fpop.append(Fox(rand.randint(1, 2), rand.randint(3,5)))
		f = Fox(rand.randint(0, 1), rand.randint())
		x -= 1

def foxEat():
	global rpopulation, rpop, fpop
	eaten = []

	for i, fox in enumerate(fpop):
		if rand.randint(1, 100) < 40:
			h = fox[1]

# Simulation Functions
# --------------------

# every day
def nextDay():
	global day
	#reproduce()
	if day == year:
		nextYear()
	if day == day + rand.randint(-15,15):
		reproduce()
	if fpopulation > 0:
		foxEat()
	day += 1

# every 365 days
def nextYear():
	global year, rpopulation, rpop, fpop, fpopulation, simulation

	# Ages Rabbits
	if rpop.shape[0] > 0:
		rpop[:, 2] += 1
		rpassed = []
		for i, rabbit in enumerate(rpop):
			if rabbit[2] == 8:
				rpassed.append(i)
				rpopulation -= 1
			elif rabbit[2] > 2:
				c = rabbit[2] * 3
				if rand.randint(1, 100) <= c:
					rpassed.append(i)
					rpopulation -= 1
		rpop = np.delete(rpop, rpassed, axis=0)

	# Ages Foxes
	if fpop.shape[0] > 0:
		fpop[:, 2] += 1
		fpassed = []
		for i, fox in enumerate(fox):
			if fox[2] == 8:
				fpassed.append(i)
				fpopulation -= 1
			elif fox[2] > 2 and fox[2] != 7:
				c = fox[2] * 10
				if rand.randint(0, 100) >= c:
					fpassed.append(i)
					fpopulation -= 1
		fpop = np.delete(fpop, fpassed, axis=0)
	year += 365

# The main function is one simulation. It starts with [rinput] rabbits and ends at [maxday] days
def main(rinput, maxday):
    global simulation, rabbit_data
    createRabbit(rinput)
    #print(f"The rpop in sim {simnumber} is(at the start):\n {rpop} \n")

    while simulation == True:

        nextDay()
        if rpop.shape[0] < 1:
        	simulation = False

        # If there are foxes
        if fpopulation > 0:
            for fox in fpop:
                if fox.hunger >= 2:
                    continue
                if rand.randint(1, 100) <= 40:
                    fox.set_hunger(fox.hunger + 1)
        # Creates foxes on day 25
        if day == 25:
            pass
            #createFox(5)

        if day == maxday:
            simulation = False

    rabbit_data = np.vstack([rabbit_data, rpop])  # Store rpop data in rabbit_data
    #print(f"The rpop in sim {simnumber} is(at the end):\n {rpop} \n")
    #print(f"The shape of the rabbit data is: {rabbit_data.shape}")
    #print(f"The day that sim {simnumber} ended at is: {day} \n")
    print(f"This simulation ended at {rpop.shape[0]}")

    resetVar()

# Runs x amount of simulations.
def runSims(x):
	rinput = 100
	maxday = 1500
	
	while x > 0:
		main(rinput, maxday)
		x -= 1

	rDF = pd.DataFrame(rabbit_data, columns=['Gender', 'Speed', 'Age', 'Fertility', 'Iteration'])

	rDF
	f"The average speed by {maxday} days in {sims} sims is: {np.mean(rDF['Speed'])}"

clear()

sims = st.number_input("No. of sims", min_value=1, max_value=50, step=1)
st.button(f"Run {sims} Simulations", on_click=runSims(sims))


# This function runs {sims} simulations, each one of {maxday} days



