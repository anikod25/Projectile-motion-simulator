import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import messagebox

g = 9.81
time_step = 0.01

def simulate_projectile_motion(initial_velocity, launch_angle, air_density, time_step):
    x = []
    y = []
    launch_angle_rad = np.deg2rad(launch_angle)
    x.append(0)
    y.append(0)
    vx = initial_velocity * np.cos(launch_angle_rad)
    vy = initial_velocity * np.sin(launch_angle_rad)

    drag_coefficient = 0.47  
    radius = 0.1  
    area = np.pi * radius**2  

    while y[-1] >= 0:        
        speed = np.sqrt(vx**2 + vy**2)

        drag_force = 0.5 * air_density * speed**2 * drag_coefficient * area

        ax = -drag_force * (vx / speed)  
        ay = -g - (drag_force * (vy / speed))  

        vx += ax * time_step
        vy += ay * time_step

        x.append(x[-1] + vx * time_step)
        y.append(y[-1] + vy * time_step)

    max_height = max(y)
    range_distance = x[-1]
    return x, y, max_height, range_distance

def update_plot():
    initial_velocity = float(velocity_entry.get())
    launch_angle = float(angle_entry.get())
    air_density = float(air_density_entry.get())

    if initial_velocity < 0.1:
        messagebox.showerror("Invalid Initial Velocity", "Initial velocity must be greater than 0.1 m/s.")
        return

    if launch_angle < 1 or launch_angle > 89:
        messagebox.showerror("Invalid Launch Angle", "Launch angle must be between 1 and 89 degrees.")
        return

    if air_density < 0:
        messagebox.showerror("Invalid Air Density", "Air density must be a non-negative value.")
        return

    x, y, max_height, range_distance = simulate_projectile_motion(initial_velocity, launch_angle, air_density, time_step)

    ax.clear()
    ax.plot(x, y, 'k', label='Trajectory')
    ax.set_title('Projectile Motion with Air Resistance')
    ax.set_xlabel('Horizontal Distance (m)')
    ax.set_ylabel('Vertical Distance (m)')
    ax.grid()
    ax.set_facecolor('white')
    ax.legend()
    ax.set_xlim(0, max(x) * 1.1)  
    ax.set_ylim(0, max_height * 1.1)  

    max_height_label.config(text=f"Max Height: {max_height:.3f} m")  
    range_label.config(text=f"Range: {range_distance:.3f} m") 

    canvas.draw()

root = Tk()
root.title("Projectile Motion Simulation")
root.configure(bg="black")
root.geometry("1000x800")

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

style = ttk.Style()
style.configure("TButton", font=("Arial", 18))
style.configure("TLabel", font=("Arial", 18))  
style.configure("TEntry", font=("Arial", 18))   

velocity_label = ttk.Label(input_frame, text="Initial Velocity (m/s):")
velocity_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
velocity_entry = ttk.Entry(input_frame, font=("Arial", 18), width=20)
velocity_entry.grid(row=0, column=1, padx=10, pady=10)
velocity_entry.insert(0, "20.0")

angle_label = ttk.Label(input_frame, text="Launch Angle (degrees):")
angle_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
angle_entry = ttk.Entry(input_frame, font=("Arial", 18), width=20)
angle_entry.grid(row=1, column=1, padx=10, pady=10)
angle_entry.insert(0, "45.0")


air_density_label = ttk.Label(input_frame, text="Air Density (kg/m³):")
air_density_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
air_density_entry = ttk.Entry(input_frame, font=("Arial", 18), width=20)
air_density_entry.grid(row=2, column=1, padx=10, pady=10)
air_density_entry.insert(0, "1.225") 

update_button = ttk.Button(input_frame, text="Update Plot", command=update_plot)
update_button.grid(row=4, column=1, padx=10, pady=10)

max_height_label = ttk.Label(input_frame, text="Max Height: 0.000 m", font=("Arial", 18), foreground="black")
max_height_label.grid(row=5,column=1, padx=10, pady=10)

range_label = ttk.Label(input_frame, text="Range: 0.000 m", font=("Arial", 18), foreground="black")
range_label.grid(row=6, column=1, padx=10, pady=10)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

ax.set_facecolor('white')
update_plot()

root.mainloop()
