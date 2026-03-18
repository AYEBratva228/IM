### Лабораторная работа 2

**1) Код**

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
                      
                      # начальные значения
                      P_fire = 0.6
                      P_lightning = 0.0001
                      P_growth = 0.01
                      speed = 100
                      
                      grid = np.random.choice([EMPTY, TREE, FIRE], size=(N, N), p=[0.4, 0.59, 0.01])
                      
                      
                      def update_grid():
                          global grid, P_fire, P_lightning, P_growth
                      
                          new_grid = grid.copy()
                      
                          for i in range(N):
                              for j in range(N):
                      
                                  if grid[i][j] == FIRE:
                                      new_grid[i][j] = ASH
                      
                                  elif grid[i][j] == TREE:
                      
                                      for di in [-1,0,1]:
                                          for dj in [-1,0,1]:
                      
                                              ni = i + di
                                              nj = j + dj
                      
                                              if 0 <= ni < N and 0 <= nj < N:
                                                  if grid[ni][nj] == FIRE:
                                                      if random.random() < P_fire:
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
                      
                                  canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                      
                      
                      def simulation():
                          global speed
                      
                          if running:
                              update_grid()
                              draw()
                      
                          root.after(int(speed), simulation)
                      
                      
                      def toggle():
                          global running
                      
                          running = not running
                          button_start.config(text="Pause" if running else "Start")
                      
                      
                      def reset():
                          global grid
                          grid = np.random.choice([EMPTY, TREE, FIRE], size=(N, N), p=[0.4, 0.59, 0.01])
                          draw()
                      
                      
                      # === обработчики слайдеров ===
                      
                      def update_fire(val):
                          global P_fire
                          P_fire = float(val)
                      
                      def update_lightning(val):
                          global P_lightning
                          P_lightning = float(val)
                      
                      def update_growth(val):
                          global P_growth
                          P_growth = float(val)
                      
                      
                      # === GUI ===
                      
                      root = tk.Tk()
                      root.title("Forest Fire Simulation")
                      
                      frame = tk.Frame(root)
                      frame.pack()
                      
                      canvas = tk.Canvas(frame, width=N*CELL, height=N*CELL)
                      canvas.grid(row=0, column=0, rowspan=6)
                      
                      # кнопки
                      button_start = tk.Button(frame, text="Start", command=toggle)
                      button_start.grid(row=0, column=1)
                      
                      button_reset = tk.Button(frame, text="Reset", command=reset)
                      button_reset.grid(row=1, column=1)
                      
                      # слайдеры
                      tk.Label(frame, text="Fire spread").grid(row=2, column=1)
                      tk.Scale(frame, from_=0, to=1, resolution=0.01,
                               orient=tk.HORIZONTAL, command=update_fire).grid(row=3, column=1)
                      
                      tk.Label(frame, text="Lightning").grid(row=4, column=1)
                      tk.Scale(frame, from_=0, to=0.1, resolution=0.001,
                               orient=tk.HORIZONTAL, command=update_lightning).grid(row=5, column=1)
                      
                      tk.Label(frame, text="Growth").grid(row=6, column=1)
                      tk.Scale(frame, from_=0, to=0.1, resolution=0.001,
                               orient=tk.HORIZONTAL, command=update_growth).grid(row=7, column=1)
                      
                      draw()
                      simulation()
                      
                      root.mainloop()


**2) Результаты**









**3) Вывод**

В ходе лабораторной работы, я научился моделироавть симуляцию лесного пожара и внедрять в нее дополнительные условия.
