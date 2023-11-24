# Eco System Simulator
import numpy as np
import random as rand
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Rabbit Variables
# ----------------

class Rabbit:
	def __init__(self, gender, speed, age, simnumber):
		"""
		Constructor Args/Rabbit Array Indices:
		
		0: Gender
			1 = Female 
			2 = Male
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
		r = Rabbit(np.random.randint(2), np.random.randint(40, 61), np.random.randint(3,6), simnumber)
		r.add_to_pop()
		x -= 1

def reproduce():
	# Filters to get the females that will reproduce

	# Gets all males
	filter_sex = rpop[:, 0] == 1
	m_rabbits = rpop[filter_sex]

	# Gets all females 
	filter_sex = rpop[:, 0] == 1
	f_rabbits = rpop[filter_sex]

	# above the age of 1
	filter_age = f_rabbits[:, 2] > 1
	f_rabbits = f_rabbits[filter_age]

	# Uses fertility as chance to reproduce
	fertility_check = f_rabbits[:, 3]+1 > np.random.randint(10)
	f_rabbits = f_rabbits[fertility_check]

	# Uses speed as chance to reproduce
	speed_check = f_rabbits[:, 1] > np.random.randint(100)+20
	f_rabbits = f_rabbits[speed_check]

	new_genes = np.empty((0, 4), int)

	for index, rabbit in enumerate(f_rabbits):
		offspring = np.random.randint(1, 4)
		while offspring > 0:
			speed1 = np.random.choice(f_rabbits[:, 1])
			speed2 = np.random.choice(m_rabbits[:, 1])

			speed3 = ((speed1 + speed2 / 2) + np.random.randint(-5, 6)).round()
			g = rand.randint(0, 1)

			o = Rabbit(g, speed3, 0, simnumber)
			o.add_to_pop()
			offspring -= 1

# Fox Functions
# -------------

def createFox(x):
	global fpop, fpopulation
	while(x > 0):
		f = Fox(rand.randint(0, 1), rand.randint())
		f.add_to_pop()
		x -= 1

def foxHunt():
	global fpop, fpopulation, rpop

	if fpopulation > 0 and rpopulation > 0:
	
		random_rabbits = np.random.randint(0, rpopulation, fpopulation)

		caught_rabits = 

		


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
		foxHunt()
	day += 1

# every 365 days
def nextYear():
	global year, rpopulation, rpop, fpop, fpopulation, simulation

	# Ages Rabbits
	if rpop.shape[0] > 0:
		rpop[:, 2] += 1
		# Only the rabbits below age 9 survive
		filter_rpop = rpop[:, 2] < 9
		rpop = rpop[filter_rpop]

		filter_rpop_survival = np.random.randint(1, 100, size=rpop.shape[0]) > rpop[:, 2] * 2
		rpop = rpop[filter_rpop_survival]
 
	# Ages Foxes
	if fpop.shape[0] > 0:
		fpop[:, 2] += 1
		fpassed = []
		# For Loop
		for i, fox in enumerate(fox):
			if fox[2] == 8:
				fpassed.append(i)
				fpopulation -= 1
			elif fox[2] > 2:
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
            #createFox(finput)

        if day == maxday:
            simulation = False

    rabbit_data = np.vstack([rabbit_data, rpop])  # Store rpop data in rabbit_data
    resetVar() # Resets variables to 0

# Runs x amount of simulations.
def runSims(x):
	
	while x > 0:
		main(rinput, maxday)
		x -= 1

	rDF = pd.DataFrame(rabbit_data, columns=['Gender', 'Speed', 'Age', 'Fertility', 'Iteration'])

	st.header("All Surviors (across all simulations)")
	rDF
	#plt.plot(range(1, sims), average_speeds[:, 1], 'o')
	f"Avg speed in {maxday} days from {sims} sims is: {np.mean(rDF['Speed'])}"
	f"Avg surivors in {maxday} days from {sims} sims is: {rDF.shape[0]/sims}"

# Streamlit Output
# ---------------

st.title('Ecosystem Simulator')

st.divider()

st.header("Starting Variables")
sims = st.number_input("No. of sims (20 is a good amount)", min_value=1, max_value=500, value=20)
maxday = st.number_input("No. of days (365 days is one year)", min_value=1, max_value=5000, value=1000)
rinput = st.number_input("No. of starting rabbits", min_value=5, max_value=500, value=100)
finput = st.number_input("No. of starting foxes", min_value=0, max_value=100, value=15)
st.divider()
st.button(f"Run {sims} Simulations of {maxday} days.", on_click=runSims(sims))

# This function runs {sims} simulations, each one of {maxday} days
st.divider()

f"Data on the sim: "
st.caption("Starting Speeds = 40-60")
st.caption("Starting Ages = 3-5")
st.caption("   ")
st.caption("Above are arbirary scalars I chose at random.")


