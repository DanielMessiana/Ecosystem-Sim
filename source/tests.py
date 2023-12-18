# Eco System Simulator in pygame
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random as rand
import time, pygame, sys

np.random.seed()

def sigma(x):
	return 1/1+np.exp(-x)

# Define Neural Network
class DirectionPredictor(nn.Module):
	def __init__(self):
		super(DirectionPredictor, self).__init__()
		self.input_size = 2  # Input size (x, y)
		self.output_size = 4  # Output size (left, right, up, down)

		self.fc = nn.Linear(self.input_size, self.output_size)

	def forward(self, x):
		x = self.fc(x)
		return x

# Rabbit Variables
# ----------------

class Rabbit:
	def __init__(self, speed, size, x, y):
		self.speed = speed
		self.size = size
		self.size += self.speed
		self.position = np.array([x, y], dtype=np.float32)
		self.nn = DirectionPredictor()
		self.optimizer = optim.Adam(self.nn.parameters(), lr=0.0001)
		self.last_position = self.position.copy()
		self.total_reward = 0
		self.max_hunger = 100
		self.hunger = 100
		self.hunger_decay_rate = 0.1
		self.target_position = np.array([rand.uniform(0, width), rand.uniform(0, height)])
		self.age = 0
		self.energy = 100

	def draw_rabbit(self, position):
		pygame.draw.circle(rabbit_surface, brown, (int(self.position[0]), int(self.position[1])), self.size)

	def move(self, food_src):
		self.last_position = self.position.copy()

		# Check if the rabbit has reached its target position
		if np.linalg.norm(self.position - self.target_position) < 10:
			# If reached, set a new random target position
			self.target_position = np.array([rand.uniform(0, width), rand.uniform(0, height)])

		# Calculate the center and radius of the visual field (circle)
		visual_field_center = self.position
		visual_field_radius = 50  # Adjust the radius as needed

		# Filter food items within the visual field
		food_in_visual_field = [food for food in food_src if np.linalg.norm(self.position - np.array([food.x, food.y])) < visual_field_radius]

		if food_in_visual_field:
			# If there is food in the visual field, move towards the closest one
			closest_food = min(food_in_visual_field, key=lambda food: np.linalg.norm(self.position - np.array([food.x, food.y])))
			food_direction = np.array([closest_food.x, closest_food.y]) - self.position
			food_direction /= np.linalg.norm(food_direction)  # Normalize to unit vector
			velocity = food_direction * self.speed
			self.position += velocity
		else:
			# If no food in the visual field, move towards the target position
			target_direction = self.target_position - self.position
			target_direction /= np.linalg.norm(target_direction)  # Normalize to unit vector
			velocity = target_direction * self.speed
			self.position += velocity

		# Constrain Rabbit to screen
		self.position[0] = np.clip(self.position[0], 0, width)
		self.position[1] = np.clip(self.position[1], 0, height)

		self.hunger -= self.hunger_decay_rate
		self.energy -= 0.1

		self.speed = max(2, self.speed - 0.05 * (self.max_hunger - self.hunger))

		self.age += 1

		age_death_probability = self.age / 100.0

		if np.random.rand() < age_death_probability:
			self.reset

	def eat_food(self):
		for food in food_src:
			distance = np.linalg.norm(self.position - np.array([food.x, food.y]))
			if distance < 5:  # You can adjust this distance threshold
				food.hp -= 1
				self.hunger += 1
				self.energy += 10
				self.total_reward += 2

	def reproduce(self):
		# Check conditions for reproduction (e.g., age, energy level)
		if self.age >= 20 and self.energy >= 50:
			# Create a new rabbit with inherited traits
			new_rabbit = Rabbit(self.speed, self.size, self.position[0], self.position[1])
			new_rabbit.nn.load_state_dict(self.nn.state_dict())  # Inherit neural network weights
			new_rabbit.max_hunger = self.max_hunger  # Inherit max_hunger
			# You can add more traits to inherit

			return new_rabbit
		else:
			return None

	def calculate_reward(self, food_src):
		# Example: Reward based on staying within the screen boundaries
		reward = 0

		for food in food_src:
			if (self.position[0] > food.x + 2 or self.position[0] < food.x - 2) and (self.position[1] > food.y + 2 or self.position[1] < food.y - 2):
				reward += 2
			else:
				reward -= 1 

		if 0 <= self.position[0] <= width and 0 <= self.position[1] <= height:
		    reward += 5
		else:
		    reward -= 1

		reward += sigma(self.hunger) * 2


		# You can add more complex reward mechanisms here based on your specific requirements

		return reward

	def update_reward(self, food_src):
		reward = self.calculate_reward(food_src)
		self.total_reward += reward

		self.total_reward -= self.hunger_decay_rate

		if self.hunger <= 0:
			self.total_reward -= 1000
			self.reset()

	def reset(self):
		# Reset rabbit properties to initial values
		self.position = np.array([rand.uniform(0, width), rand.uniform(0, height)], dtype=np.float32)
		self.speed = np.random.randint(2, 8)
		self.hunger = self.max_hunger
		self.target_position = np.array([rand.uniform(0, width), rand.uniform(0, height)])
		self.age = 0
		self.energy = 100

class Food:
	def __init__(self, hp, decay_rate=0.05):
		self.hp = hp
		self.decay_rate = decay_rate
		self.x = np.random.randint(0, width)
		self.y = np.random.randint(0, height)

	def draw_food(self):
		if self.hp > 0:
			pygame.draw.circle(food_surface, green, (self.x, self.y), self.hp)

	def update(self):
		self.hp -= self.decay_rate

def create_food(food_src):
	if np.random.randint(0, 100) > 97:
		n = np.random.randint(0, 10)
		while n > 0:
			f = Food(np.random.randint(10, 30))
			food_src.append(f)
			n -= 1

def update_food(food_src):
	for food in food_src:
		food.update()

	return [food for food in food_src if food.hp > 0]

pygame.init()
width, height = 1900, 1150
screen = pygame.display.set_mode((width, height))
screen_buffer = pygame.Surface((width, height), pygame.SRCALPHA)
clock = pygame.time.Clock()
main = True

white = (255, 255, 255)
brown = (150, 75, 0)
green = (0, 255, 0)

food_surface = pygame.Surface((width, height), pygame.SRCALPHA)
rabbit_surface = pygame.Surface((width, height), pygame.SRCALPHA)

def run_simulation(food_src):
	# Create a set of rabbits and food sources for each simulation
	speed = np.random.randint(2, 8)
	size = np.random.randint(20, 30)
	x, y = width - np.random.randint(0, width), height - np.random.randint(0, height)

	food_src = [Food(np.random.randint(10, 30)) for _ in range(10)]
	rpop = [Rabbit(speed, size, x, y) for _ in range(20)]

	num_epochs = 200
	for epoch in range(num_epochs):
		for rabbit in rpop:
			rabbit.move(food_src)
			rabbit.update_reward(food_src)

			new_rabbit = rabbit.reproduce()
			if new_rabbit is not None:
				rpop.append(new_rabbit)

			# Generate random training data
			input_data = torch.tensor([[rand.uniform(0, width), rand.uniform(0, height)]], dtype=torch.float32)

			# Get the current position of the rabbit
			current_position = rabbit.position.copy()

			# Calculate the target direction based on the movement
			target_direction = np.array(rabbit.position - current_position, dtype=np.float32)

			# Reset the rabbit position
			rabbit.position = current_position

			# Inside the training loop
			target_direction = np.array(rabbit.position - current_position, dtype=np.float32)
			target_direction_tensor = torch.tensor([target_direction[0], target_direction[1], 0, 0], dtype=torch.float32)

			# Train the neural network
			rabbit.optimizer.zero_grad()
			output = rabbit.nn(input_data)
			loss = nn.functional.mse_loss(output, target_direction_tensor)
			loss.backward()
			rabbit.optimizer.step()

		food_src = update_food(food_src)

	return rpop, food_src

# Run multiple simulations
num_simulations = 10
all_rabbit_populations = []
all_food_sources = []

food_src = []

for simulation in range(num_simulations):
	rpop, food_src = run_simulation(food_src)
	all_rabbit_populations.append(rpop)
	all_food_sources.append(food_src)

# Main game loop
current_simulation = 0
num_simulations = 10
simulation_running = True
seconds_per_simulation = 20
simulation_duration = seconds_per_simulation * 1000
current_simulation_time = 0

while main:
	screen_buffer.fill(white)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			main = False

	if simulation_running:
		# Draw food surfaces for the current simulation
		food_src = all_food_sources[current_simulation]
		create_food(food_src)
		food_src = update_food(food_src)
		food_surface.fill((0, 0, 0, 0))  # Clear the surface
		for food in food_src:
			food.draw_food()

		# Blit the food surface onto the screen
		screen_buffer.blit(food_surface, (0, 0))

		# Draw rabbit surfaces for the current simulation
		rpop = all_rabbit_populations[current_simulation]
		rabbit_surface.fill((0, 0, 0, 0))
		for rabbit in rpop:
			if np.random.randint(0, 100) > 60:
			    rabbit.hunger -= np.random.randint(0, 3)
			rabbit.move(food_src)
			new_rabbit = rabbit.reproduce()
			if new_rabbit is not None:
				rabbit_population.append(new_rabbit)
			rabbit.eat_food()
			rabbit.draw_rabbit(rabbit.position)

		screen_buffer.blit(rabbit_surface, (0, 0))

		current_simulation_time += clock.get_time()

		if current_simulation_time >= simulation_duration:
			current_simulation += 1
			current_simulation_time = 0

			if current_simulation >= num_simulations:
				main = False

		screen.blit(screen_buffer, (0,0))

		pygame.display.flip()

		clock.tick(120)

pygame.quit()
sys.exit()
