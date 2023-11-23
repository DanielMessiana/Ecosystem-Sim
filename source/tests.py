# Eco System Simulator
import numpy as np
import random as rand
import pandas as pd
import streamlit as st
import time, json, sys, os
import matplotlib.pyplot as plt
rpop = np.empty((0,5), int)
rabbit_data = np.empty((0,5), int)
rpopulation = 0
rabbitfood = 0
starvedr = 0
deadrabbits = 0
rmating = 10
simnumber = 1
clear = lambda: os.system('clear')

class Rabbit:
	def __init__(self, gender, speed, age, simnumber):
		# Female Rabbits have fertility 1-5 at birth
		if gender == 1:
			self.rarray = np.array([[gender], [speed], [age], [rand.randint(1,5)], [simnumber]])
		# Male Rabbits have fertiliy 0
		if gender == 0:
			self.rarray = np.array([[gender], [speed], [age], [0], [simnumber]])


	def get_arr(self):
		return self.rarray.T

	def add_to_pop(self):
		global rpop, rpopulation
		rpop = np.vstack([rpop, self.rarray.T]) 
		rpopulation += 1

def createRabbit(x):
	global rpop, rpopulation
	while(x > 0):
		n = Rabbit(rand.randint(0, 1), rand.randint(50, 70), rand.randint(3,8), simnumber)
		n.add_to_pop()
		x -= 1

def resetVar():
	global simulation, firstgame, rpop, rpopulation, rspeeds, rabbitfood, starvedr, deadrabbits, rmating, totaloffspring, fpop, fpopulation, day, year, simnumber
	simulation = True
	rpop = np.empty((0,5), int)
	rpopulation = 0
	rspeeds = []
	rabbitfood = 0
	starvedr = 0
	deadrabbits = 0
	rmating = 10
	totaloffspring = 0

	fpop = np.empty((0,2), int)
	fpopulation = 0

	day = 1
	year = 365
	simnumber += 1

createRabbit(200)

g = np.random.choice(rpop[:, 1])

print(g)


