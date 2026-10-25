import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
import threading


class HeatConductionSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Теплопроводность")
        self.root.geometry("1050x650")
        self.root.configure(bg="#f0f0f0")

        self.running = False
        self.create_ui()

    def create_ui(self):
        params_frame = tk.LabelFrame(
            self.root,
            text="Исходные данные",
            font=("Arial", 11, "bold"),
            bg="#90EE90",
            padx=10,
            pady=8
        )
        params_frame.pack(fill="x", padx=10, pady=8)

        # Основные параметры
        params = [
            ("L (м):", "0.1"),
            ("λ (Вт/(м·К)):", "1000"),
            ("ρ (кг/м³):", "3500"),
            ("c (Дж/(кг·К)):", "500"),
            ("Tl (°C):", "100"),
            ("Tr (°C):", "50"),
            ("T нач. (°C):", "20"),
            ("Время (с):", "2.0"),
        ]

        self.entries = {}

        for i, (label, value) in enumerate(params):
            row = i // 4
            col = (i % 4) * 2

            tk.Label(
                params_frame,
                text=label,
                bg="#90EE90"
            ).grid(row=row, column=col, sticky="w", padx=4, pady=5)

            entry = tk.Entry(params_frame, width=10)
            entry.insert(0, value)
            entry.grid(row=row, column=col + 1, padx=4, pady=5)

            self.entries[label] = entry

        # Сетка расчёта
        grid_frame = tk.LabelFrame(
            self.root,
            text="Шаги расчёта",
            font=("Arial", 11, "bold"),
            bg="#90EE90",
            padx=10,
            pady=8
        )
        grid_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            grid_frame,
            text="Шаги времени τ (с), через запятую:",
            bg="#90EE90"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.tau_entry = tk.Entry(grid_frame, width=40)
        self.tau_entry.insert(0, "0.1, 0.01, 0.001, 0.0001")
        self.tau_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            grid_frame,
            text="Шаги пространства h (м), через запятую:",
            bg="#90EE90"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.h_entry = tk.Entry(grid_frame, width=40)
        self.h_entry.insert(0, "0.1, 0.01, 0.001, 0.0001")
        self.h_entry.grid(row=1, column=1, padx=5, pady=5)

        self.start_btn = tk.Button(
            grid_frame,
            text="Запуск расчёта",
            font=("Arial", 11, "bold"),
            bg="#87CEEB",
            padx=15,
            pady=5,
            command=self.start_calculation
        )
        self.start_btn.grid(
            row=0, column=2, rowspan=2, padx=20, pady=5
        )

        self.status = tk.Label(
            self.root,
            text="Введите параметры и нажмите «Запуск расчёта».",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.status.pack(pady=5)

        # Таблица результатов
        table_frame = tk.LabelFrame(
            self.root,
            text="Результаты расчёта: температура в центре пластины, °C",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.tree = ttk.Treeview(
            table_frame,
            show="headings",
            height=12
        )

        y_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        x_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure(
            "Treeview",
            font=("Arial", 11),
            rowheight=28
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    def get_parameters(self):
        p = self.entries

        L = float(p["L (м):"].get())
        lam = float(p["λ (Вт/(м·К)):"] .get())
        rho = float(p["ρ (кг/м³):"].get())
        c = float(p["c (Дж/(кг·К)):"] .get())
        T_l = float(p["Tl (°C):"].get())
        T_r = float(p["Tr (°C):"].get())
        T_initial = float(p["T нач. (°C):"].get())
        t_max = float(p["Время (с):"].get())

        taus = [
            float(x.strip())
            for x in self.tau_entry.get().split(",")
            if x.strip()
        ]

        hs = [
            float(x.strip())
            for x in self.h_entry.get().split(",")
            if x.strip()
        ]

        if L <= 0 or lam <= 0 or rho <= 0 or c <= 0:
            raise ValueError(
                "L, λ, ρ и c должны быть положительными."
            )

        if t_max <= 0:
            raise ValueError("Время расчёта должно быть больше нуля.")

        if not taus or not hs:
            raise ValueError("Укажите шаги времени и пространства.")

        if any(x <= 0 for x in taus + hs):
            raise ValueError("Все шаги сетки должны быть положительными.")

        if any(h > L for h in hs):
            raise ValueError("Шаг пространства h не должен превышать L.")

        return (
            L, lam, rho, c, T_l, T_r,
            T_initial, t_max, taus, hs
        )

    @staticmethod
    def calculate_temperature(
        L, lam, rho, c, T_l, T_r,
        T_initial, t_max, tau, h
    ):
        # Численное решение неявной схемой:
        # rho*c*dT/dt = lambda*d²T/dx²

        N = max(3, int(round(L / h)) + 1)
        dx = L / (N - 1)

        alpha = lam / (rho * c)
        r = alpha * tau / dx**2

        T = np.full(N, T_initial, dtype=float)
        T[0] = T_l
        T[-1] = T_r

        # Число внутренних узлов
        m = N - 2

        # Коэффициенты трёхдиагональной системы
        diagonal = 1.0 + 2.0 * r
        lower = -r
        upper = -r

        # Предварительно рассчитываем коэффициенты прогонки
        c_prime = np.empty(m)
        denom = np.empty(m)

        denom[0] = diagonal
        c_prime[0] = upper / denom[0]

        for i in range(1, m):
            denom[i] = diagonal - lower * c_prime[i - 1]

            if i < m - 1:
                c_prime[i] = upper / denom[i]
            else:
                c_prime[i] = 0.0

        # Расчёт до заданного физического времени
        t = 0.0
        while t < t_max:
            dt = min(tau, t_max - t)
            r_step = alpha * dt / dx**2

            # Если последний шаг короче tau, пересчитываем
            # коэффициенты для этого шага.
            if dt != tau:
                diagonal_step = 1.0 + 2.0 * r_step
                lower_step = -r_step
                upper_step = -r_step

                cp = np.empty(m)
                den = np.empty(m)
                den[0] = diagonal_step
                cp[0] = upper_step / den[0]

                for i in range(1, m):
                    den[i] = (
                        diagonal_step - lower_step * cp[i - 1]
                    )
                    cp[i] = (
                        upper_step / den[i]
                        if i < m - 1 else 0.0
                    )
            else:
                cp = c_prime
                den = denom
                lower_step = lower
                r_step = r

            rhs = T[1:-1].copy()
            rhs[0] += r_step * T_l
            rhs[-1] += r_step * T_r

            # Прямой ход
            d_prime = np.empty(m)
            d_prime[0] = rhs[0] / den[0]

            for i in range(1, m):
                d_prime[i] = (
                    rhs[i] - lower_step * d_prime[i - 1]
                ) / den[i]

            # Обратный ход
            new_inner = np.empty(m)
            new_inner[-1] = d_prime[-1]

            for i in range(m - 2, -1, -1):
                new_inner[i] = (
                    d_prime[i] - cp[i] * new_inner[i + 1]
                )

            T[1:-1] = new_inner
            T[0] = T_l
            T[-1] = T_r

            t += dt

        return float(T[N // 2])

    def start_calculation(self):
        if self.running:
            return

        try:
            params = self.get_parameters()
        except ValueError as error:
            messagebox.showerror("Ошибка ввода", str(error))
            return

        self.running = True
        self.start_btn.config(state="disabled")
        self.status.config(text="Выполняется расчёт...")
        self.tree.delete(*self.tree.get_children())

        thread = threading.Thread(
            target=self.calculate_all,
            args=(params,),
            daemon=True
        )
        thread.start()

    def calculate_all(self, params):
        (
            L, lam, rho, c, T_l, T_r,
            T_initial, t_max, taus, hs
        ) = params

        results = []

        try:
            for tau in taus:
                row = []

                for h in hs:
                    value = self.calculate_temperature(
                        L, lam, rho, c,
                        T_l, T_r, T_initial,
                        t_max, tau, h
                    )
                    row.append(value)

                results.append(row)

            self.root.after(
                0,
                lambda: self.show_results(taus, hs, results)
            )

        except Exception as error:
            self.root.after(
                0,
                lambda msg=str(error): self.show_error(msg)
            )

    def show_results(self, taus, hs, results):
        columns = ["tau"] + [
            f"h={h:g}" for h in hs
        ]

        self.tree["columns"] = columns

        self.tree.heading(
            "tau",
            text="Шаг по времени τ (с) / шаг по пространству h (м)"
        )
        self.tree.column("tau", width=330, anchor="center")

        for col, h in zip(columns[1:], hs):
            self.tree.heading(col, text=f"{h:g}")
            self.tree.column(col, width=110, anchor="center")

        for tau, row in zip(taus, results):
            values = [f"{tau:g}"] + [
                f"{value:.2f}" for value in row
            ]
            self.tree.insert("", "end", values=values)

        self.status.config(text="Расчёт завершён.")
        self.start_btn.config(state="normal")
        self.running = False

    def show_error(self, error):
        self.status.config(text="При расчёте возникла ошибка.")
        self.start_btn.config(state="normal")
        self.running = False
        messagebox.showerror("Ошибка расчёта", error)


if __name__ == "__main__":
    root = tk.Tk()
    app = HeatConductionSimulation(root)
    root.mainloop()