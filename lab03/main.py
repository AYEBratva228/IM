
import tkinter as tk
import numpy as np
import random

N = 60
CELL = 10

EMPTY = 0
TREE = 1
FIRE = 2
ASH = 3

running = False

# Параметры симуляции
TEMPERATURE = 0.6
P_lightning = 0.0001
P_growth = 0.01

# Направление ветра
WIND_DIRECTIONS = {
    "Нет ветра": (0, 0),
    "Вверх": (-1, 0),
    "Вниз": (1, 0),
    "Влево": (0, -1),
    "Вправо": (0, 1)
}

wind_direction = "Нет ветра"

grid = np.random.choice(
    [EMPTY, TREE, FIRE],
    size=(N, N),
    p=[0.4, 0.59, 0.01]
)


def update_grid():
    global grid, TEMPERATURE, P_lightning, P_growth

    new_grid = grid.copy()

    # Направление ветра
    wind_i, wind_j = WIND_DIRECTIONS[wind_direction]

    for i in range(N):
        for j in range(N):

            if grid[i][j] == FIRE:
                new_grid[i][j] = ASH

            elif grid[i][j] == TREE:

                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:

                        if di == 0 and dj == 0:
                            continue

                        ni = i + di
                        nj = j + dj

                        if 0 <= ni < N and 0 <= nj < N:
                            if grid[ni][nj] == FIRE:

                                probability = TEMPERATURE

                                dot = di * wind_i + dj * wind_j

                                if wind_i != 0 or wind_j != 0:
                                    if dot < 0:
                                        # Дерево находится по направлению ветра
                                        probability *= 1.5
                                    elif dot > 0:
                                        # Дерево находится против ветра
                                        probability *= 0.5

                                probability = min(probability, 1.0)

                                if random.random() < probability:
                                    new_grid[i][j] = FIRE


                if random.random() < P_lightning:
                    new_grid[i][j] = FIRE

            elif grid[i][j] == EMPTY:
                if random.random() < P_growth:
                    new_grid[i][j] = TREE

    grid = new_grid


def draw():
    canvas.delete("all")

    for i in range(N):
        for j in range(N):

            x1 = j * CELL
            y1 = i * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            state = grid[i][j]

            if state == EMPTY:
                color = "white"
            elif state == TREE:
                color = "green"
            elif state == FIRE:
                color = "red"
            else:
                color = "black"

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline=""
            )


def simulation():
    if running:
        update_grid()
        draw()

    root.after(100, simulation)


def toggle():
    global running

    running = not running
    button_start.config(
        text="Pause" if running else "Start"
    )


def reset():
    global grid

    grid = np.random.choice(
        [EMPTY, TREE, FIRE],
        size=(N, N),
        p=[0.4, 0.59, 0.01]
    )
    draw()


# Обработчики слайдеров

def update_temperature(val):
    global TEMPERATURE
    TEMPERATURE = float(val)


def update_lightning(val):
    global P_lightning
    P_lightning = float(val)


def update_growth(val):
    global P_growth
    P_growth = float(val)


def update_wind(val):
    global wind_direction
    wind_direction = val


# GUI

root = tk.Tk()
root.title("Forest Fire Simulation")

frame = tk.Frame(root, padx=5, pady=5)
frame.pack()

canvas = tk.Canvas(
    frame,
    width=N * CELL,
    height=N * CELL,
    bg="white"
)
canvas.grid(row=0, column=0, rowspan=10)

# Кнопки

button_start = tk.Button(
    frame, text="Start", command=toggle
)
button_start.grid(row=0, column=1, sticky="ew")

button_reset = tk.Button(
    frame, text="Reset", command=reset
)
button_reset.grid(row=1, column=1, sticky="ew")

# Температура

tk.Label(frame, text="Temperature").grid(
    row=2, column=1
)

tk.Scale(
    frame,
    from_=0,
    to=1,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    length=180,
    command=update_temperature
).set(TEMPERATURE)

temperature_slider = tk.Scale(
    frame,
    from_=0,
    to=1,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    length=180,
    command=update_temperature
)
temperature_slider.set(TEMPERATURE)
temperature_slider.grid(row=3, column=1)

# Молнии

tk.Label(frame, text="Lightning").grid(
    row=4, column=1
)

lightning_slider = tk.Scale(
    frame,
    from_=0,
    to=0.1,
    resolution=0.001,
    orient=tk.HORIZONTAL,
    length=180,
    command=update_lightning
)
lightning_slider.set(P_lightning)
lightning_slider.grid(row=5, column=1)

# Рост деревьев

tk.Label(frame, text="Tree growth").grid(
    row=6, column=1
)

growth_slider = tk.Scale(
    frame,
    from_=0,
    to=0.1,
    resolution=0.001,
    orient=tk.HORIZONTAL,
    length=180,
    command=update_growth
)
growth_slider.set(P_growth)
growth_slider.grid(row=7, column=1)

# Ветер

tk.Label(frame, text="Wind direction").grid(
    row=8, column=1
)

wind_menu = tk.OptionMenu(
    frame,
    tk.StringVar(value=wind_direction),
    *WIND_DIRECTIONS.keys(),
    command=update_wind
)
wind_menu.config(width=14)
wind_menu.grid(row=9, column=1)

draw()
simulation()

root.mainloop()
