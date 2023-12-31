# Eco System Simulator
import numpy as np
import random as rand
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time

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
		2: Energy
		3: Age
		4: Fertility
		5: Birthday
		6: Simnumber

		"""
		# Female Rabbits have fertility 1-5 at birth
		if gender == 1:
			self.rarray = np.array([[1], [speed],  [age], [rand.randint(1,5)], [simnumber]])
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

fpop = np.empty((0,3), int)
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
		r = Rabbit(np.random.randint(2), np.random.randint(30, 60+1), np.random.randint(7), simnumber)
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
	speed_check = f_rabbits[:, 1] > np.random.randint(100+1)+30
	f_rabbits = f_rabbits[speed_check]

	new_genes = np.empty((0, 4), int)

	for index, rabbit in enumerate(f_rabbits):
		offspring = np.random.randint(1, 5)
		while offspring > 0:
			speed1 = np.random.choice(f_rabbits[:, 1])
			speed2 = np.random.choice(m_rabbits[:, 1])

			speed3 = ((speed1 + speed2 / 2) + np.random.randint(-2, 2+1)).round()
			if np.random.randint(0, 100) < 2:
				speed3 += np.random.randint(-20, 20+1)
			g = rand.randint(0, 1)

			o = Rabbit(g, speed3, 0, simnumber)
			o.add_to_pop()
			offspring -= 1

# Fox Functions
# -------------

def createFox(x):
	global fpop, fpopulation
	while(x > 0):
		f = Fox(rand.randint(0, 1), np.random.randint(1, 3+1), np.random.randint(2,5+1))
		f.add_to_pop()
		x -= 1

def foxHunt():
	global fpop, fpopulation, rpop, rpopulation

	for i, fox in enumerate(fpop):
		if 65 > np.random.randint(100+11):
			random_indices = np.random.choice(rpop.shape[0], size=min(fox[1], rpop.shape[0]), replace=True)

			rand_rabbits = rpop[random_indices]

			filter_caught = rand_rabbits[:, 1] > np.random.randint(100, size=rand_rabbits.shape[0])
			caught_rabbits = random_indices[filter_caught]

			rpop = np.delete(rpop, caught_rabbits, axis=0)
			rpopulation -= len(caught_rabbits)
			fpop[i, 1] = fox[1] - len(caught_rabbits)

# Simulation Functions
# --------------------

# every day
def nextDay():
	global day, fpop, fpopulation
	#reproduce()
	day += 1
	if day == year:
		nextYear()
		day = 1
	if  day >= 60 and day <= 273:
		reproduce()
	if fpopulation > 0:
		foxHunt()
		if np.random.randint(0, 100+1) < 80:
			random_hungers = np.random.randint(5, size=fpop.shape[0])

			fpop[:, 1] += random_hungers
		filter_fpop = fpop[:, 1] < 7
		fpop = fpop[filter_fpop]
		fpopulation = fpop.shape[0]

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

		rpopulation = rpop.shape[0]
 
	# Ages Foxes
	if fpop.shape[0] > 0:
		fpop[:, 2] += 1
		# Only the foxes below age 9 survive
		filter_fpop = fpop[:, 2] < 9
		fpop = fpop[filter_fpop]

		filter_fpop_survival = np.random.randint(1, 100, size=rpop.shape[0]) > rpop[:, 2] * 2
		fpop = fpop[filter_fpop_survival]

		fpopulation = fpop.shape[0]


# The main function is one simulation. It starts with [rinput] rabbits and ends at [maxday] days
def main(rinput, maxday):
    global simulation, rabbit_data
    createRabbit(rinput)
    dataday = 100

    while simulation == True:

        nextDay()
        if rpop.shape[0] < 1:
        	simulation = False

        # Creates foxes on day 25
        if day == 250:
            createFox(finput)

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
	st.subheader(f"{sims} Simulations of {maxday} days")
	show_chart = st.checkbox("Show Chart")
	if show_chart:
		x_axis = st.selectbox(
			'Set x label.',
			('Age', 'Gender', 'Speed', 'Fertility', 'Iteration'))
		y_axis = st.selectbox(
			'Set y label.',
			('Speed', 'Age', 'Gender', 'Fertility', 'Iteration'))
		if x_axis == y_axis:
			"------ You cannot use the same x and y axis! ------"
		else:
			plt.plot(rDF[x_axis], rDF[y_axis] , 'o')
			plt.xlabel(x_axis)
			plt.ylabel(y_axis)
			st.pyplot(plt)
	f"Avg speed in {maxday} days from {sims} sims is: {np.mean(rDF['Speed'])}"
	f"Avg surivors in {maxday} days from {sims} sims is: {rDF.shape[0]/sims}"

# Streamlit Output
# ---------------

st.title('Ecosystem Simulator')

st.divider()

st.header("Starting Variables")
sims = st.number_input("No. of sims (50 is a good amount)", min_value=1, max_value=500, value=50)
maxday = st.number_input("No. of days (365 days is one year)", min_value=1, max_value=5000, value=1000)
rinput = st.number_input("No. of starting rabbits", min_value=5, max_value=500, value=150)
finput = st.number_input("No. of starting foxes", min_value=0, max_value=100, value=15)
st.divider()
st.button(f"Run {sims} Simulations of {maxday} days.", on_click=runSims(sims))

st.divider()

st.subheader("About the Simulator:")
st.write("This simulator shows rabbits and foxes living together. The rabbits reproduce and pass on their genes, which are [Gender, Speed, Age, Fertility]")
" "
st.write("The foxes hunt the rabbits and catch them based on how high their speed is. The higher the speed of a rabbit, the more unlikely it is for a fox to catch it. Hopefully this shows natural selection in the rabbits.")

st.divider()

"Data in the simulator: "
st.caption("Starting Speeds = 30-60")
st.caption("Starting Ages = 0-6")
st.caption("What day foxes are added = 250")
st.caption("   ")
st.caption("Above are arbirary scalars I chose at random.")


