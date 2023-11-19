# Eco System Simulator
import numpy as np
import random as rand
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

	def set_age(self, age):
		self.rarray[2] = age

	def get_arr(self):
		return self.rarray


rpop = np.empty((0,4), int) 
n = Rabbit(rand.randint(0, 1), rand.randint(50, 70), 6)
rpop = np.append(rpop, n.get_arr().T, axis=0)
n = Rabbit(rand.randint(0, 1), rand.randint(50, 70), rand.randint(3,5))
rpop = np.append(rpop, n.get_arr().T, axis=0)
n = Rabbit(rand.randint(0, 1), rand.randint(50, 70), rand.randint(3,5))
rpop = np.append(rpop, n.get_arr().T, axis=0)
n = Rabbit(rand.randint(0, 1), rand.randint(50, 70), rand.randint(3,5))
rpop = np.append(rpop, n.get_arr().T, axis=0)

def nextYear():
	global rpopulation, year, rpop, fpop, fpopulation, simulation
	if len(rpop):
		rpop[:, 2] += 1
		for index, row in enumerate(rpop):
			print(index)
			print(row[2])
			if row[2] == 7:
				rpop = np.delete(rpop, index, axis=0)
		print(rpop)

print(rpop[:, 2])
print(rpop)
nextYear()
