import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# From GeeksForGeeks
interval = int(input('Enter an interval (Positive Non-Zero Integer): '))

circle_points = 0
total_points = 0

points = []

# Total Random numbers generated= possible x
# values* possible y values
for i in range(interval**2):

	# Randomly generated x and y values from a uniform distribution
	# Range of x and y values is -1 to 1
	rand_x = random.uniform(-1, 1)
	rand_y = random.uniform(-1, 1)

	# vvv This is a very dangerous line, do not uncomment vvv
	# print(points)

	# Distance between (x, y) from the origin
	origin_dist = rand_x**2 + rand_y**2

	colors = ''

	# Appending tuples
	pointTuple = (rand_x, rand_y, origin_dist, colors)
	points.append(pointTuple)

	# Checking if (x, y) lies inside the circle
	if origin_dist <= 1:
		circle_points += 1

	total_points += 1
	

	# Estimating value of pi,
	# pi= 4*(no. of points generated inside the
	# circle)/ (no. of points generated inside the square)
	pi = 4 * circle_points / total_points

	hitPercent = (circle_points / total_points)*100


## print(rand_x, rand_y, circle_points, square_points, "-", pi)
# print("\n")
print("Total Points: " + str(total_points))
print("Total Points Hit: " + str(circle_points))
print("Final Estimation of Pi: ", pi)

# Visualizing Output
# Creating the graph / SQUARE
fig = plt.figure()
ax = fig.add_subplot()
plt.plot(-1, 1)
ax.set_aspect('equal', adjustable='box')

# PLOTTING POINTS
x_values, y_values, origin_dist, _ = zip(*points)
x_values = np.array(x_values)
y_values = np.array(y_values)
origin_dist = np.array(origin_dist)

colors = np.where((origin_dist > 1), 'red', 'green')

plt.scatter(x_values, y_values, c=colors)

# CIRCLE
# Define the center and radius of the circle
center = (0, 0)
radius = 1
# Create a circle patch
circle = patches.Circle(center, radius, edgecolor='black', facecolor='none')
# Add the circle to the axes
ax.add_patch(circle)
# Set the limits of the plot to ensure the circle is visible
ax.set_xlim((-1, 1))
ax.set_ylim((-1, 1))
ax.set_aspect('equal', adjustable='box')

plt.title("Finding the Area of a Circle with Interval: " + str(interval))
plt.figtext(0.01, 0.0005, "Estimated Area: " + str(pi) + "\nHit Percent: " + str(round(hitPercent, 2)) + "%", ha="left", fontsize=10, fontstyle = "oblique")

plt.show()