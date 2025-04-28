import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Set up the figure and axes
fig = plt.figure(figsize=(12, 8))
grid = plt.GridSpec(3, 2, height_ratios=[1, 4, 1])

# Title
title_ax = plt.subplot(grid[0, :])
title_ax.axis('off')
title_text = title_ax.text(0.5, 0.5, "Monte Carlo Pi Estimation", ha='center', va='center', fontsize=16)

# Main plot for points
points_ax = plt.subplot(grid[1, 0])
points_ax.set_xlim(-1.05, 1.05)
points_ax.set_ylim(-1.05, 1.05)
points_ax.set_aspect('equal')
points_ax.set_title("Points Distribution")
points_ax.grid(True, linestyle='--', alpha=0.6)

# Create the circle patch
circle = patches.Circle((0, 0), 1, edgecolor='black', facecolor='none')
points_ax.add_patch(circle)
points_ax.add_patch(patches.Rectangle((-1, -1), 2, 2, edgecolor='black', facecolor='none'))

# Error plot
error_ax = plt.subplot(grid[1, 1])
error_ax.set_title("Error vs. Number of Points")
error_ax.set_xlabel("Number of Points")
error_ax.set_ylabel("Error (%)")
error_ax.grid(True, linestyle='--', alpha=0.6)

# Controls area
control_ax = plt.subplot(grid[2, :])
control_ax.axis('off')

# Stats display
stats_ax = fig.add_axes([0.15, 0.02, 0.7, 0.1])
stats_ax.axis('off')

# Function to get user input
def get_point_count():
    while True:
        try:
            count = int(input('Enter the number of points to generate (positive integer): '))
            if count > 0:
                return count
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

# Get user input
total_points_to_generate = get_point_count()

# Initialize variables
points_inside = 0
total_points = 0
points_x = []
points_y = []
colors = []
error_x = []
error_y = []
update_frequency = 50  # Points to add per frame (fixed)
finished = False
paused = False

# Set x-axis limits for error plot based on total points
error_ax.set_xlim(0, total_points_to_generate * 1.1)
error_ax.set_ylim(0, 15)  # Initial error range in percentage

# Initialize plots
inside_points, = points_ax.plot([], [], 'go', markersize=3, alpha=0.7)
outside_points, = points_ax.plot([], [], 'ro', markersize=3, alpha=0.7)
error_line, = error_ax.plot([], [], 'b-')

# Stats text objects
stats_text = stats_ax.text(0.5, 0.5, "", ha='center', va='center', fontsize=12)

# Create button for pause/resume
pause_ax = fig.add_axes([0.4, 0.14, 0.15, 0.03])
pause_button = Button(pause_ax, 'Pause')

# Create button for reset and start over
reset_ax = fig.add_axes([0.6, 0.14, 0.15, 0.03])
reset_button = Button(reset_ax, 'Reset')

def toggle_pause(event):
    global paused
    paused = not paused
    pause_button.label.set_text('Resume' if paused else 'Pause')

def reset(event):
    global points_inside, total_points, points_x, points_y, colors, error_x, error_y, finished, paused
    points_inside = 0
    total_points = 0
    points_x = []
    points_y = []
    colors = []
    error_x = []
    error_y = []
    finished = False
    paused = False
    pause_button.label.set_text('Pause')
    
    inside_points.set_data([], [])
    outside_points.set_data([], [])
    error_line.set_data([], [])
    stats_text.set_text("")
    
    # Get new user input
    global total_points_to_generate
    total_points_to_generate = get_point_count()
    error_ax.set_xlim(0, total_points_to_generate * 1.1)
    
    fig.canvas.draw_idle()

pause_button.on_clicked(toggle_pause)
reset_button.on_clicked(reset)

def init():
    inside_points.set_data([], [])
    outside_points.set_data([], [])
    error_line.set_data([], [])
    stats_text.set_text("")
    return inside_points, outside_points, error_line, stats_text

def update(frame):
    global points_inside, total_points, points_x, points_y, colors, error_x, error_y, finished
    
    if paused or finished:
        return inside_points, outside_points, error_line, stats_text
    
    # Add new points
    points_to_add = min(update_frequency, total_points_to_generate - total_points)
    
    for _ in range(points_to_add):
        x = np.random.uniform(-1, 1)
        y = np.random.uniform(-1, 1)
        points_x.append(x)
        points_y.append(y)
        
        # Check if point is inside circle
        if x**2 + y**2 <= 1:
            points_inside += 1
            colors.append(True)  # Inside
        else:
            colors.append(False)  # Outside
            
        total_points += 1
        
        # Calculate pi estimate and error
        if total_points > 0:
            pi_estimate = 4 * points_inside / total_points
            error_percent = abs((np.pi - pi_estimate) / np.pi * 100)
            
            error_x.append(total_points)
            error_y.append(error_percent)
    
    # Check if we've reached the total
    if total_points >= total_points_to_generate:
        finished = True
    
    # Update plots
    inside_indices = [i for i, inside in enumerate(colors) if inside]
    outside_indices = [i for i, inside in enumerate(colors) if not inside]
    
    inside_x = [points_x[i] for i in inside_indices]
    inside_y = [points_y[i] for i in inside_indices]
    
    outside_x = [points_x[i] for i in outside_indices]
    outside_y = [points_y[i] for i in outside_indices]
    
    inside_points.set_data(inside_x, inside_y)
    outside_points.set_data(outside_x, outside_y)
    error_line.set_data(error_x, error_y)
    
    # Update statistics text
    if total_points > 0:
        pi_estimate = 4 * points_inside / total_points
        hit_percent = (points_inside / total_points) * 100
        stats_str = f"Total Points: {total_points} / {total_points_to_generate}\n"
        stats_str += f"Points Inside Circle: {points_inside}\n"
        stats_str += f"Pi Estimate: {pi_estimate:.6f} (True π: {np.pi:.6f})\n"
        stats_str += f"Error: {error_percent:.4f}%"
        
        if finished:
            stats_str += "\nSimulation complete!"
            
        stats_text.set_text(stats_str)
    
    return inside_points, outside_points, error_line, stats_text

# Create animation
ani = animation.FuncAnimation(fig, update, frames=None, init_func=init, 
                              interval=20, blit=True)

plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.show()