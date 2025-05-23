import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation

# Pemdulo simple 
# d²θ/dt² = −(g/L)·sin(θ)

# 


# Constantes físicas
g = 9.81
L = 1.0 # Longitud del pendulo

# Condiciones iniciales
theta0 = np.pi/4 # El péndulo empieza desde un ángulo de 45 grados.
omega0 = 0.0 # Empieza quieto (sin movimiento inicial).

# Tiempo de simulación
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 300)

def pendulum(t, y):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = -(g / L) * np.sin(theta)
    return [dtheta_dt, domega_dt]

# Aquí se resuelve!!
sol = solve_ivp(pendulum, t_span, [theta0, omega0], t_eval=t_eval)

# convierte angulos en coordenadas x, y
x = L * np.sin(sol.y[0])
y = -L * np.cos(sol.y[0])

fig, ax = plt.subplots()
ax.set_xlim(-L-0.2, L+0.2)
ax.set_ylim(-L-0.2, L+0.2)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)

def animate(i):
    line.set_data([0, x[i]], [0, y[i]])
    return line,

ani = FuncAnimation(fig, animate, frames=len(t_eval), interval=30, blit=True)

plt.title("Simulador de péndulo simple")
plt.show()