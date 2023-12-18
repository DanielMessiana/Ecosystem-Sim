# Eco System Simulator in pygame
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random as rand
import time, pygame, sys

np.random.seed()

def sigma(x):
	return 1 / (1 + np.exp(-x))

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
	def __init__(self, speed, size, x=None, y=None):
		self.speed = speed
		self.size = size
		self.size += self.speed
		if x is None or y is None:
			# If x and y are not provided, generate random starting position
			self.position = np.array([rand.uniform(0, width), rand.uniform(0, height)], dtype=np.float32)
		else:
			self.position = np.array([x, y], dtype=np.float32)
		self.nn = DirectionPredictor()
		self.optimizer = optim.Adam(self.nn.parameters(), lr=0.0001)
		self.last_position = self.position.copy()
		self.total_reward = 0
		self.max_hunger = 100
		self.hunger = 100
		self.hunger_decay_rate = 0.01
		self.target_position = np.array([rand.uniform(0, width), rand.uniform(0, height)])
		self.age = 0
		self.energy = 100
		self.reproduction_cooldown = 0
		self.max_offspring = 3

		self.resting = False
		self.resting_cooldown = 0
		self.max_resting_duration = 500
		self.resting_duration = 0

	def draw_rabbit(self, position):
		pygame.draw.circle(rabbit_surface, brown, (int(self.position[0]), int(self.position[1])), self.size)

	def move(self, food_src):
		self.last_position = self.position.copy()

		near_burrow = any(burrow.is_inside(self.position) for burrow in burrow_src)

		if near_burrow:
			# Increase resting duration even if not already resting
			self.resting_duration += clock.get_time()

			# If not already resting, start resting
			if not self.resting and self.resting_cooldown <= 0:
				self.resting = True
				self.resting_duration = 0

			# Check if the rabbit has rested enough, reset speed and cooldown
			if self.resting_duration >= self.max_resting_duration:
				self.resting = False
				self.resting_cooldown = 100  # Cooldown before the rabbit can rest again
				self.speed = np.random.randint(2, 8)

		else:
			if self.resting:

				self.speed = min(self.speed + 0.1, np.random.randint(2, 8))
			else:
				if self.resting_cooldown > 0:
					self.resting_cooldown -= 1

				# Check if the rabbit has reached its target position
				if np.linalg.norm(self.position - self.target_position) < 10:
					# If reached, set a new random target position
					self.target_position = np.array([rand.uniform(0, width), rand.uniform(0, height)])

				if self.hunger > 70 and np.random.rand() < 0.1:
					# Wander slowly or sit in place
					self.speed = 1  # Adjust the speed as needed
					self.wander_during_break()
					return

				# Calculate the center and radius of the visual field (circle)
				visual_field_center = self.position
				visual_field_radius = 30  # Adjust the radius as needed

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

				self.reproduction_cooldown = max(0, self.reproduction_cooldown - 1)



	def wander_during_break(self):
		if np.random.rand() < 0.5:
			random_direction = np.array([rand.uniform(-1, 1), rand.uniform(-1, 1)])
			random_direction /= np.linalg.norm(random_direction)  # Normalize to unit vector
			velocity = random_direction * self.speed
			self.position += velocity
			self.total_reward += 3
		else:
			pass

	def eat_food(self):
		for food in food_src:
			distance = np.linalg.norm(self.position - np.array([food.x, food.y]))
			if distance < 5:  # You can adjust this distance threshold
				food.hp -= 1
				self.hunger += 1
				self.energy += 10
				self.total_reward += 1

	def reproduce(self):
		# Check conditions for reproduction (e.g., age, energy level)
		if self.age >= 20 and self.energy >= 50 and self.reproduction_cooldown <= 0:
			# Create a new rabbit with inherited traits
			new_rabbit = Rabbit(self.speed, self.size, self.position[0], self.position[1])
			new_rabbit.nn.load_state_dict(self.nn.state_dict())  # Inherit neural network weights
			new_rabbit.max_hunger = self.max_hunger  # Inherit max_hunger
			# You can add more traits to inherit

			self.reproduction_cooldown = 100
			self.max_offspring -= 1

			return new_rabbit
		else:
			return None

	def calculate_reward(self, food_src):
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
	decay_rate = 0.05

	def __init__(self, hp):
		self.hp = hp
		self.x = np.random.randint(0, width)
		self.y = np.random.randint(0, height)

		self.x = int(self.x)
		self. y = int(self.y)

	def draw_food(self):
		if self.hp > 0:
			pygame.draw.circle(food_surface, green, (int(self.x), int(self.y)), self.hp)

	def update(self):
		self.hp -= self.decay_rate

def create_food(food_src):
	if np.random.randint(0, 100) > 97:
		n = np.random.randint(0, 10)
		while n > 0:
			f = Food(np.random.randint(1, 30))
			food_src.append(f)
			n -= 1

def update_food(food_src):
	for food in food_src:
		food.update()

	return [food for food in food_src if food.hp > 0]

class Burrow:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.radius = 40

	def draw_burrow(self):
		pygame.draw.circle(burrow_surface, light_brown, (int(self.x), int(self.y)), self.radius)

	def is_inside(self, position):
		distance = np.linalg.norm(np.array([self.x, self.y]) - position)
		return distance < self.radius

pygame.init()
width, height = 1900, 1150
scale_factor = width / 2
screen = pygame.display.set_mode((width, height))
screen_buffer = pygame.Surface((width, height), pygame.SRCALPHA)
clock = pygame.time.Clock()
main = True

white = (255, 255, 255)
brown = (150, 75, 0)
light_brown = (194, 164, 132, 140)
green = (0, 255, 0)

food_surface = pygame.Surface((width, height), pygame.SRCALPHA)
burrow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
rabbit_surface = pygame.Surface((width, height), pygame.SRCALPHA)

def run_simulation():
	# Create a set of rabbits and food sources for each simulation
	speed = np.random.randint(2, 8)
	size = np.random.randint(5, 20)

	food_src = [Food(np.random.randint(10, 20)) for _ in range(10)]
	#burrow_src = [Burrow(np.random.randint(0, width), np.random.randint(0, height)) for _ in range(np.random.randint(2,6))]
	rpop = [Rabbit(speed, size) for _ in range(20)]

	num_epochs = 1
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
			target_direction /= np.linalg.norm(target_direction)  # Normalize to unit vector
			target_direction_tensor = torch.tensor([target_direction[0], target_direction[1], 0, 0], dtype=torch.float32)

			# Train the neural network
			rabbit.optimizer.zero_grad()
			output = rabbit.nn(input_data)
			loss = nn.functional.mse_loss(output, target_direction_tensor)
			loss.backward()
			rabbit.optimizer.step()

		food_src = update_food(food_src)
		move_rabbits(rpop, food_src, burrow_src)

	return rpop, food_src


def move_rabbits(rpop, food_src, burrow_src):
	if not food_src:
		return

	# Ensure food_positions is an array of shape (num_food, 2)
	food_positions = np.array([[food.x, food.y] for food in food_src])

	for rabbit in rpop:
		# Check if the rabbit is close to any burrow
		near_burrow = any(burrow.is_inside(rabbit.position) for burrow in burrow_src)

		if near_burrow:
			# If near a burrow, the rabbit can rest
			rabbit.wander_during_break()
		else:
			# If not near a burrow, continue normal behavior
			distances = np.linalg.norm(rabbit.position - food_positions, axis=1)
			closest_food_index = np.argmin(distances)
			closest_food = food_positions[closest_food_index]
			food_direction = closest_food - rabbit.position
			food_direction /= np.linalg.norm(food_direction)
			velocity = food_direction * rabbit.speed
			rabbit.position += velocity

			# Constrain rabbits to the screen
			rabbit.position[0] = np.clip(rabbit.position[0], 0, width)
			rabbit.position[1] = np.clip(rabbit.position[1], 0, height)

			rabbit.hunger -= rabbit.hunger_decay_rate
			rabbit.energy -= 0.1

			rabbit.speed = max(2, rabbit.speed - 0.05 * (rabbit.max_hunger - rabbit.hunger))

			rabbit.age += 1

			age_death_probability = rabbit.age / 100.0

			if np.random.rand() < age_death_probability:
				rabbit.reset()


# Run multiple simulations
num_simulations = 10
all_rabbit_populations = []
all_food_sources = []

food_src = []
burrow_src = []

def create_burrow(burrow_src):
	burrow_src.clear()
	n = np.random.randint(2, 6)
	while n > 0:
		b = Burrow(np.random.randint(0, width), np.random.randint(0, height))
		burrow_src.append(b)
		n -= 1

for simulation in range(num_simulations):
	rpop, food_src = run_simulation()
	all_rabbit_populations.append(rpop)
	all_food_sources.append(food_src)

	create_burrow(burrow_src)

# Main game loop
current_simulation = 0
num_simulations = 10
simulation_running = True
seconds_per_simulation = 20
simulation_duration = seconds_per_simulation * 1000
current_simulation_time = 0

font = pygame.font.Font(None, 40) 

while main:
	screen.fill(white)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			main = False

	if simulation_running:
		rabbit_surface.fill((0, 0, 0, 0))

		# Draw food surfaces for the current simulation
		food_src = all_food_sources[current_simulation]
		create_food(food_src)
		food_src = update_food(food_src)
		food_surface.fill((0, 0, 0, 0))  # Clear the surface
		for food in food_src:
			food.draw_food()

		# Blit the food surface onto the screen
		screen_buffer.blit(food_surface, (0, 0))

		burrow_surface.fill((0, 0, 0, 0))
		for burrow in burrow_src:
			burrow.draw_burrow()
		screen_buffer.blit(burrow_surface, (0, 0))

		# Draw rabbit surfaces for the current simulation
		rpop = all_rabbit_populations[current_simulation]
		move_rabbits(rpop, food_src, burrow_src)

		for rabbit in rpop:
			new_rabbit = rabbit.reproduce()
			if new_rabbit is not None:
				rpop.append(new_rabbit)
			rabbit.eat_food()
			rabbit.draw_rabbit(rabbit.position)

		screen_buffer.blit(rabbit_surface, (0, 0))

		simulation_number_text = font.render(f"Simulation: {current_simulation + 1}/{num_simulations}", True, (1, 0, 0))
		screen.blit(simulation_number_text, (width - simulation_number_text.get_width() - 10, 10))

		current_simulation_time += clock.get_time()

		if current_simulation_time >= simulation_duration:
			current_simulation += 1
			current_simulation_time = 0

			if current_simulation >= num_simulations:
				main = False

		screen.blit(food_surface, (0, 0))
		screen.blit(burrow_surface, (0, 0))
		screen.blit(rabbit_surface, (0, 0))

		pygame.display.flip()

		clock.tick(120)

pygame.quit()
sys.exit()
