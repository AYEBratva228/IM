import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


def simulate_mm1(lam, mu, n, warmup, seed=42):
    if lam >= mu:
        raise ValueError("Для устойчивой системы необходимо λ < μ.")
    if n < 2:
        raise ValueError("Количество заявок N должно быть не меньше 2.")
    if warmup < 0 or warmup >= n:
        raise ValueError("Число начальных заявок должно быть от 0 до N−1.")

    rng = np.random.default_rng(seed)
    arrivals = np.cumsum(rng.exponential(scale=1 / lam, size=n))
    service = rng.exponential(scale=1 / mu, size=n)

    starts = np.zeros(n)
    departures = np.zeros(n)
    starts[0] = arrivals[0]
    departures[0] = starts[0] + service[0]

    for i in range(1, n):
        starts[i] = max(arrivals[i], departures[i - 1])
        departures[i] = starts[i] + service[i]

    wait = starts - arrivals
    total_time = departures - arrivals

    wait = wait[warmup:]
    total_time = total_time[warmup:]
    observed_arrivals = arrivals[warmup:]

    rho = lam / mu
    lq_theory = rho**2 / (1 - rho)
    l_theory = rho / (1 - rho)
    wq_theory = rho / (mu - lam)
    w_theory = 1 / (mu - lam)

    wq = float(np.mean(wait))
    w = float(np.mean(total_time))
    effective_lambda = len(wait) / (departures[-1] - observed_arrivals[0])
    lq = effective_lambda * wq
    l = effective_lambda * w
    fraction_waiting = float(np.mean(wait > 1e-12))
    idle_gaps = np.maximum(0, arrivals[1:] - departures[:-1])
    idle_fraction = float(np.sum(idle_gaps) / (departures[-1] - arrivals[0]))

    return {
        "lambda": lam, "mu": mu, "n": n, "warmup": warmup, "rho": rho,
        "rows": [
            ("Lq — среднее число заявок в очереди", lq, lq_theory),
            ("L — среднее число заявок в системе", l, l_theory),
            ("Wq — среднее ожидание в очереди", wq, wq_theory),
            ("W — среднее время в системе", w, w_theory),
            ("Заявки, ожидавшие в очереди", fraction_waiting, rho),
            ("Доля времени простоя прибора", idle_fraction, 1 - rho),
        ]
    }


def show_results(result):
    # Результаты показываются в отдельном окне.
    window = tk.Toplevel(root)
    window.title("Результаты моделирования M/M/1")
    window.geometry("800x410")
    window.minsize(700, 350)

    heading = ttk.Label(
        window,
        text="РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ СМО M/M/1",
        font=("Arial", 14, "bold")
    )
    heading.pack(pady=(14, 8))

    summary = (
        f"λ = {result['lambda']:g}    μ = {result['mu']:g}    "
        f"N = {result['n']}    Исключено начальных заявок = {result['warmup']}\n"
        f"Коэффициент загрузки ρ = λ/μ = {result['rho']:.4f}"
    )
    ttk.Label(window, text=summary, justify="center").pack(pady=(0, 12))

    frame = ttk.Frame(window, padding=(12, 0, 12, 0))
    frame.pack(fill="both", expand=True)

    columns = ("metric", "simulation", "theory")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
    tree.heading("metric", text="Показатель")
    tree.heading("simulation", text="Моделирование")
    tree.heading("theory", text="Теория")
    tree.column("metric", width=440, anchor="w")
    tree.column("simulation", width=130, anchor="center")
    tree.column("theory", width=130, anchor="center")

    for metric, simulation, theory in result["rows"]:
        tree.insert("", "end", values=(metric, f"{simulation:.4f}", f"{theory:.4f}"))

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


    ttk.Button(window, text="Закрыть", command=window.destroy).pack(pady=(0, 12))


def run_simulation():
    try:
        lam = float(lambda_entry.get().replace(",", "."))
        mu = float(mu_entry.get().replace(",", "."))
        n = int(n_entry.get())
        warmup = int(warmup_entry.get())

        if lam <= 0 or mu <= 0:
            raise ValueError("λ и μ должны быть больше нуля.")

        result = simulate_mm1(lam, mu, n, warmup)
        show_results(result)
    except ValueError as error:
        messagebox.showerror("Ошибка ввода", str(error))
    except Exception as error:
        messagebox.showerror("Ошибка", f"Не удалось выполнить моделирование:\n{error}")


root = tk.Tk()
root.title("Система массового обслуживания M/M/1")
root.geometry("520x350")
root.resizable(False, False)

main = ttk.Frame(root, padding=22)
main.pack(fill="both", expand=True)

ttk.Label(
    main,
    text="Моделирование СМО M/M/1",
    font=("Arial", 16, "bold")
).grid(row=0, column=0, columnspan=2, pady=(0, 8))

ttk.Label(
    main,
    text="Введите параметры и нажмите «Запустить моделирование».\nРезультаты откроются в отдельном окне.",
    justify="center"
).grid(row=1, column=0, columnspan=2, pady=(0, 18))

fields = [
    ("λ — интенсивность поступления", "4"),
    ("μ — интенсивность обслуживания", "6"),
    ("N — количество заявок", "20000"),
    ("Начальных заявок исключить", "1000"),
]
entries = []
for row, (label, default) in enumerate(fields, start=2):
    ttk.Label(main, text=label).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=6)
    entry = ttk.Entry(main, width=18)
    entry.insert(0, default)
    entry.grid(row=row, column=1, sticky="ew", pady=6)
    entries.append(entry)

lambda_entry, mu_entry, n_entry, warmup_entry = entries

ttk.Button(
    main,
    text="Запустить моделирование",
    command=run_simulation
).grid(row=6, column=0, columnspan=2, pady=(22, 0), ipadx=12, ipady=5)

main.columnconfigure(1, weight=1)
root.mainloop()
