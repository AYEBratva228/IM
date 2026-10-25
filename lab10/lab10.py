import random
import tkinter as tk
from tkinter import ttk, messagebox


def simulate_mm_c_impatient(lam, mu, theta, servers, n_requests, seed=None):
    """
    СМО M/M/c с неограниченной FIFO-очередью и нетерпеливостью.
    lam     — интенсивность поступления заявок;
    mu      — интенсивность обслуживания ОДНОГО прибора;
    theta   — интенсивность ухода из очереди (экспоненциальное терпение);
    servers — число параллельных обслуживающих приборов;
    n_requests — число поступивших заявок.
    """
    if lam <= 0 or mu <= 0 or theta <= 0:
        raise ValueError("Интенсивности λ, μ и θ должны быть больше нуля.")
    if servers < 1 or n_requests < 1:
        raise ValueError("Число приборов и заявок должно быть не меньше 1.")

    rng = random.Random(seed)
    now = 0.0
    next_arrival = rng.expovariate(lam)
    arrivals_generated = 0

    # Для каждого занятого прибора храним время завершения и заявку.
    # Событие завершения: (время, номер прибора, заявка)
    active = {}
    service_events = []  # мини-очередь событий завершения
    queue = []  # заявки: arrival, patience_end

    served = 0
    abandoned = 0
    waiting_times = []
    system_times = []
    busy_time_per_server = [0.0] * servers

    total_in_system = 0
    last_state_time = 0.0
    queue_area = 0.0
    system_area = 0.0
    busy_area = 0.0

    while arrivals_generated < n_requests or active or queue:
        next_service_end = min((event[0] for event in service_events), default=float("inf"))
        next_abandon = min((req["patience_end"] for req in queue), default=float("inf"))
        next_arrival_event = next_arrival if arrivals_generated < n_requests else float("inf")
        event_time = min(next_arrival_event, next_service_end, next_abandon)

        if event_time == float("inf"):
            break

        dt = event_time - last_state_time
        queue_area += len(queue) * dt
        system_area += total_in_system * dt
        busy_area += len(active) * dt
        last_state_time = event_time
        now = event_time

        # При совпадении времени приоритет: уход из очереди, затем завершение,
        # затем поступление. Совпадения для непрерывных распределений почти невозможны.
        if next_abandon <= next_service_end and next_abandon <= next_arrival_event:
            idx = min(range(len(queue)), key=lambda i: queue[i]["patience_end"])
            queue.pop(idx)
            abandoned += 1
            total_in_system -= 1

        elif next_service_end <= next_arrival_event:
            # Завершить все обслуживания, завершившиеся в этот момент.
            completed = [event for event in service_events if event[0] == next_service_end]
            service_events = [event for event in service_events if event[0] != next_service_end]

            for end_time, server_id, req in completed:
                active.pop(server_id, None)
                served += 1
                system_times.append(end_time - req["arrival"])
                total_in_system -= 1

            # Освободившиеся приборы сразу забирают первые заявки из очереди.
            for _, server_id, _ in sorted(completed, key=lambda x: x[1]):
                if queue:
                    req = queue.pop(0)
                    wait = now - req["arrival"]
                    waiting_times.append(wait)
                    duration = rng.expovariate(mu)
                    busy_time_per_server[server_id] += duration
                    active[server_id] = req
                    service_events.append((now + duration, server_id, req))

        else:
            # Приход новой заявки.
            arrivals_generated += 1
            req = {
                "arrival": now,
                "patience_end": now + rng.expovariate(theta)
            }
            total_in_system += 1

            free_servers = [i for i in range(servers) if i not in active]
            if free_servers:
                server_id = free_servers[0]
                waiting_times.append(0.0)
                duration = rng.expovariate(mu)
                busy_time_per_server[server_id] += duration
                active[server_id] = req
                service_events.append((now + duration, server_id, req))
            else:
                queue.append(req)

            if arrivals_generated < n_requests:
                next_arrival = now + rng.expovariate(lam)
            else:
                next_arrival = float("inf")

    total_time = now if now > 0 else 1.0
    avg_wait = sum(waiting_times) / len(waiting_times) if waiting_times else 0.0
    avg_system = sum(system_times) / len(system_times) if system_times else 0.0

    return {
        "Поступило заявок": arrivals_generated,
        "Число обслуживающих приборов": servers,
        "Обслужено заявок": served,
        "Ушло из очереди": abandoned,
        "Доля обслуженных": served / arrivals_generated if arrivals_generated else 0.0,
        "Доля ушедших": abandoned / arrivals_generated if arrivals_generated else 0.0,
        "Среднее ожидание обслуженных": avg_wait,
        "Среднее время в системе": avg_system,
        "Средняя длина очереди": queue_area / total_time,
        "Среднее число заявок в системе": system_area / total_time,
        "Средняя загрузка одного прибора": busy_area / (servers * total_time),
        "Время моделирования": total_time,
    }


class MMImpatientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("СМО M/M/c с очередью и нетерпеливостью")
        self.root.geometry("570x440")
        self.root.resizable(False, False)

        main = ttk.Frame(root, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Модель M/M/c с очередью и нетерпеливостью",
            font=("Arial", 13, "bold"),
            wraplength=520
        ).pack(pady=(0, 14))

        self.entries = {}
        fields = [
            ("Интенсивность поступления λ", "4.0"),
            ("Интенсивность обслуживания одного прибора μ", "3.0"),
            ("Интенсивность нетерпеливости θ", "0.5"),
            ("Количество обслуживающих приборов c", "2"),
            ("Количество поступающих заявок", "20000"),
            ("Начальное значение генератора (seed)", "42"),
        ]

        form = ttk.Frame(main)
        form.pack(fill="x")
        for row, (label, default) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=6)
            entry = ttk.Entry(form, width=18)
            entry.insert(0, default)
            entry.grid(row=row, column=1, sticky="e", pady=6)
            self.entries[label] = entry
        form.columnconfigure(0, weight=1)

        ttk.Button(main, text="Запустить моделирование", command=self.run).pack(pady=16)
        ttk.Label(
            main,
            text="Очередь FIFO общая для всех приборов. Если прибор свободен, заявка начинает обслуживание сразу. "
                 "Если все приборы заняты, заявка ждёт или уходит по истечении времени терпения.",
            wraplength=520,
            justify="left"
        ).pack(anchor="w")

    def run(self):
        try:
            lam = float(self.entries["Интенсивность поступления λ"].get())
            mu = float(self.entries["Интенсивность обслуживания одного прибора μ"].get())
            theta = float(self.entries["Интенсивность нетерпеливости θ"].get())
            servers = int(self.entries["Количество обслуживающих приборов c"].get())
            n = int(self.entries["Количество поступающих заявок"].get())
            seed = int(self.entries["Начальное значение генератора (seed)"].get())
            if lam <= 0 or mu <= 0 or theta <= 0 or servers < 1 or n < 1:
                raise ValueError("λ, μ и θ должны быть больше нуля, а число приборов и заявок — не меньше 1.")
        except ValueError as exc:
            messagebox.showerror("Ошибка ввода", str(exc) or "Проверьте введённые значения.")
            return

        try:
            results = simulate_mm_c_impatient(lam, mu, theta, servers, n, seed)
        except Exception as exc:
            messagebox.showerror("Ошибка моделирования", str(exc))
            return

        self.show_results(results, lam, mu, theta, servers)

    def show_results(self, results, lam, mu, theta, servers):
        window = tk.Toplevel(self.root)
        window.title("Результаты моделирования")
        window.geometry("720x500")
        window.transient(self.root)

        ttk.Label(
            window,
            text=f"Параметры: λ={lam:g}, μ={mu:g}, θ={theta:g}, c={servers}; среднее терпение = {1/theta:.4g}",
            font=("Arial", 10, "bold")
        ).pack(padx=12, pady=12, anchor="w")

        table_frame = ttk.Frame(window, padding=(12, 0, 12, 8))
        table_frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(table_frame, columns=("metric", "value"), show="headings", height=14)
        tree.heading("metric", text="Показатель")
        tree.heading("value", text="Значение")
        tree.column("metric", width=430, anchor="w")
        tree.column("value", width=220, anchor="e")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for name, value in results.items():
            shown = f"{value:.5f}" if isinstance(value, float) else str(value)
            tree.insert("", "end", values=(name, shown))

        ttk.Button(window, text="Закрыть", command=window.destroy).pack(pady=(0, 12))


if __name__ == "__main__":
    root = tk.Tk()
    app = MMImpatientApp(root)
    root.mainloop()
