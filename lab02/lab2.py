import tkinter as tk
from tkinter import ttk, messagebox
import time


# Параметры меди
rho = 8960.0
c = 385.0
lambd = 401.0
a = lambd / (rho * c)


def solve_tridiagonal(T, T_prev, r, N, T_left, T_right):
    alpha = [0.0] * (N + 1)
    beta = [0.0] * (N + 1)

    alpha[1] = 0.0
    beta[1] = T_left

    for i in range(1, N):
        A = -r
        B = 1 + 2 * r
        C = -r
        D = T_prev[i]

        denom = B + A * alpha[i]

        alpha[i + 1] = -C / denom
        beta[i + 1] = (D - A * beta[i]) / denom

    T[N] = T_right

    for i in range(N - 1, 0, -1):
        T[i] = alpha[i + 1] * T[i + 1] + beta[i + 1]

    T[0] = T_left


def calculate():
    # Очистка таблицы
    for row in grid.get_children():
        grid.delete(row)

    try:
        L = float(entry_L.get())
        T_left = float(entry_T_left.get())
        T_right = float(entry_T_right.get())
        t_model = float(entry_t_model.get())
    except ValueError:
        messagebox.showerror(
            "Ошибка",
            "Введите корректные числовые значения."
        )
        return

    dt_values = [0.1, 0.01, 0.001]
    dx_values = [0.1, 0.01, 0.001, 0.0001]

    for dx in dx_values:
        for dt in dt_values:

            N = int(L / dx)
            time_steps = int(t_model / dt)

            T = [0.0] * (N + 1)
            T_prev = [T_right] * (N + 1)

            T_prev[0] = T_left
            T_prev[N] = T_right

            r = a * dt / (dx * dx)

            start_time = time.perf_counter()

            for n in range(time_steps):
                solve_tridiagonal(
                    T,
                    T_prev,
                    r,
                    N,
                    T_left,
                    T_right
                )

                T_prev[:] = T[:]

            elapsed = time.perf_counter() - start_time

            T_center = T[N // 2]

            grid.insert(
                "",
                "end",
                values=(
                    f"{dx:.4f}",
                    f"{dt:.4f}",
                    f"{T_center:.6f}",
                    f"{elapsed:.6f}"
                )
            )


# -----------------------------
# Создание окна
# -----------------------------

root = tk.Tk()
root.title("Расчёт температурного поля")
root.geometry("700x500")


# -----------------------------
# Поля ввода
# -----------------------------

frame_input = tk.Frame(root)
frame_input.pack(pady=10)


tk.Label(frame_input, text="L:").grid(row=0, column=0, padx=5, pady=5)
entry_L = tk.Entry(frame_input, width=15)
entry_L.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="T_left:").grid(row=1, column=0, padx=5, pady=5)
entry_T_left = tk.Entry(frame_input, width=15)
entry_T_left.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="T_right:").grid(row=2, column=0, padx=5, pady=5)
entry_T_right = tk.Entry(frame_input, width=15)
entry_T_right.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="t_model:").grid(row=3, column=0, padx=5, pady=5)
entry_t_model = tk.Entry(frame_input, width=15)
entry_t_model.grid(row=3, column=1, padx=5, pady=5)


# -----------------------------
# Кнопка расчёта
# -----------------------------

button = tk.Button(
    root,
    text="Рассчитать",
    command=calculate,
    width=20
)
button.pack(pady=10)


# -----------------------------
# Таблица результатов
# -----------------------------

columns = (
    "dx",
    "dt",
    "T_center",
    "time"
)

grid = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

grid.heading("dx", text="dx")
grid.heading("dt", text="dt")
grid.heading("T_center", text="T_center")
grid.heading("time", text="Время, с")

grid.column("dx", width=100, anchor="center")
grid.column("dt", width=100, anchor="center")
grid.column("T_center", width=150, anchor="center")
grid.column("time", width=150, anchor="center")

grid.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# -----------------------------
# Запуск программы
# -----------------------------

root.mainloop()