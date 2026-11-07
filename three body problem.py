import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import numpy as np


class Body:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0

        self.mass = mass
        self.color = color

        self.path_x = []
        self.path_y = []

plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(10, 10))

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

ax.set_aspect("equal")

ax.set_xticks([])
ax.set_yticks([])

stars_x = np.random.uniform(-10, 10, 300)
stars_y = np.random.uniform(-10, 10, 300)

ax.scatter(
    stars_x,
    stars_y,
    s=2,
    color="white",
    alpha=0.4,
    zorder=0
)

G=1

def set_circular_velocity(self, central):

    dx = self.x - central.x
    dy = self.y - central.y

    r = np.sqrt(dx**2 + dy**2)

    v = np.sqrt(G * central.mass / r)

    tx = -dy / r
    ty = dx / r

    self.vx = v * tx
    self.vy = v * ty

sun = Body(0, 0, 1000, "gold")

planet1 = Body(-4, 3, 5, "deepskyblue")
set_circular_velocity(planet1, sun)

planet2 = Body(5, -2, 8, "tomato")
set_circular_velocity(planet2, sun)

bodies = [sun, planet1, planet2]

planets = ax.scatter(
    [sun.x, planet1.x, planet2.x],
    [sun.y, planet1.y, planet2.y],
    s=[400, 150, 180],
    c=[sun.color, planet1.color, planet2.color]
)


def acceleration(body1, bodies):
    bodiess = [body for body in bodies if body != body1]
    Fx = 0
    Fy = 0
    for body in bodiess:
        Gx, Gy = gravity(body1, body)
        Fx += Gx
        Fy += Gy
    ax = Fx/body1.mass
    ay = Fy/body1.mass
    return ax, ay

def gravity(body1, body2):

    dx = body2.x - body1.x
    dy = body2.y - body1.y

    r = (dx**2 + dy**2)**0.5

    if r == 0:
       return 0, 0

    F = G * body1.mass * body2.mass / r**2

    Fx = F * dx / r
    Fy = F * dy / r

    return Fx, Fy

dt = 0.001

def update(frame, bodies):
    old = []

    for body in bodies:
        old.append(acceleration(body, bodies))    

    for body, (ax, ay) in zip(bodies, old):
        body.x += body.vx*dt + 0.5*ax*dt**2
        body.y += body.vy*dt + 0.5*ay*dt**2  

    new = []

    for body in bodies:
        new.append(acceleration(body, bodies))    

    for body, (a_old, a_new) in zip(bodies, zip(old, new)):

        ax_old, ay_old = a_old
        ax_new, ay_new = a_new

        body.vx += 0.5*(ax_old+ax_new)*dt
        body.vy += 0.5*(ay_old+ay_new)*dt

    planets.set_offsets([[body.x, body.y] for body in bodies])

    return (planets,)

animation = FuncAnimation(
    fig,
    update,
    frames=1000,
    interval=20,
    blit=True,
    fargs=(bodies,)
)


plt.show()
