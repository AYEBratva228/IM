КОД

    import tkinter as tk
    from tkinter import ttk, messagebox
    import numpy as np
    import matplotlib.pyplot as plt
    
    
    class PoissonServerApp:
        """Моделирование пуассоновского потока заявок на сервер."""
    
        def __init__(self, root):
            self.root = root
            self.root.title("Лабораторная работа — Пуассоновский поток")
            self.root.geometry("950x700")
            self.root.minsize(850, 620)
    
            self.times = []
            self.counts = []
            self.interval = 10.0
            self.lam = 2.0
    
            self.build_ui()
    
        def build_ui(self):
            main = ttk.Frame(self.root, padding=12)
            main.pack(fill="both", expand=True)
    
            ttk.Label(
                main, text="Пуассоновский поток. События на сервере",
                font=("Arial", 16, "bold")
            ).pack(anchor="w", pady=(0, 8))
    
            ttk.Label(
                main,
                text="Моделирование поступления заявок на сервер за интервал времени T."
            ).pack(anchor="w", pady=(0, 12))
    
            params = ttk.LabelFrame(main, text="Параметры моделирования", padding=10)
            params.pack(fill="x", pady=(0, 10))
    
            row = ttk.Frame(params)
            row.pack(fill="x")
            ttk.Label(row, text="Интервал T:").pack(side="left")
            self.t_entry = ttk.Entry(row, width=10)
            self.t_entry.insert(0, "10")
            self.t_entry.pack(side="left", padx=(5, 18))
    
            ttk.Label(row, text="Интенсивность λ (заявок в единицу времени):").pack(side="left")
            self.lambda_entry = ttk.Entry(row, width=10)
            self.lambda_entry.insert(0, "2")
            self.lambda_entry.pack(side="left", padx=5)
    
            ttk.Label(row, text="Число экспериментов:").pack(side="left", padx=(18, 0))
            self.n_entry = ttk.Entry(row, width=10)
            self.n_entry.insert(0, "10000")
            self.n_entry.pack(side="left", padx=5)
    
            buttons = ttk.Frame(main)
            buttons.pack(fill="x", pady=(0, 10))
            ttk.Button(buttons, text="Смоделировать", command=self.simulate).pack(side="left")
            ttk.Button(buttons, text="Очистить", command=self.clear).pack(side="left")
    
            self.summary = ttk.LabelFrame(main, text="Результаты", padding=10)
            self.summary.pack(fill="x", pady=(0, 10))
            self.result_text = tk.Text(self.summary, height=9, wrap="word", font=("Consolas", 10))
            self.result_text.pack(fill="x")
    
            chart_frame = ttk.LabelFrame(main, text="Распределение числа заявок", padding=8)
            chart_frame.pack(fill="both", expand=True)
            self.chart_frame = chart_frame
            self.canvas_widget = None
    
        def simulate(self):
            try:
                T = float(self.t_entry.get())
                lam = float(self.lambda_entry.get())
                n = int(self.n_entry.get())
                if T <= 0 or lam < 0 or n <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Ошибка ввода",
                    "Введите T > 0, λ ≥ 0 и положительное целое число экспериментов."
                )
                return
    
            # В пуассоновском потоке число событий за интервал T:
            # N(T) ~ Poisson(λT).
            self.interval, self.lam = T, lam
            self.counts = np.random.poisson(lam * T, size=n)
            self.times = np.arange(1, n + 1)
    
            mean_emp = float(np.mean(self.counts))
            var_emp = float(np.var(self.counts, ddof=0))
            mean_theory = lam * T
            var_theory = lam * T
    
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(
                tk.END,
                f"Интервал времени T:             {T:g}\n"
                f"Интенсивность λ:                {lam:g}\n"
                f"Число экспериментов:            {n}\n\n"
                f"Среднее число заявок (опыт):    {mean_emp:.4f}\n"
                f"Дисперсия (опыт):               {var_emp:.4f}\n"
                f"Среднее число заявок (теория):  {mean_theory:.4f}\n"
                f"Дисперсия (теория):             {var_theory:.4f}\n"
                f"Разница средних:                {mean_emp - mean_theory:+.4f}\n"
                f"Разница дисперсий:              {var_emp - var_theory:+.4f}\n\n"
                "Вывод: для пуассоновского потока теоретические среднее и дисперсия\n"
                "равны λT. При увеличении числа экспериментов экспериментальные\n"
                "значения обычно приближаются к теоретическим."
            )
    
            self.draw_chart()
    
        def draw_chart(self):
            if not len(self.counts):
                return
    
            if self.canvas_widget is not None:
                self.canvas_widget.destroy()
    
            fig, ax = plt.subplots(figsize=(8.2, 3.2), dpi=90)
            max_k = int(np.max(self.counts))
            bins = np.arange(-0.5, max_k + 1.5, 1)
            ax.hist(self.counts, bins=bins, density=True, rwidth=0.85)
            ax.set_title("Эмпирическое распределение числа заявок")
            ax.set_xlabel("Число заявок за интервал T")
            ax.set_ylabel("Относительная частота")
            ax.set_xticks(range(max_k + 1))
            ax.grid(axis="y", alpha=0.3)
            fig.tight_layout()
    
            # Встраиваем график в окно Tkinter через стандартный backend.
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.pack(fill="both", expand=True)
            canvas.get_tk_widget()._figure_canvas = canvas
    
        def clear(self):
            self.counts = []
            self.times = []
            self.result_text.delete("1.0", tk.END)
            if self.canvas_widget is not None:
                self.canvas_widget.destroy()
                self.canvas_widget = None
    
    
    if __name__ == "__main__":
        root = tk.Tk()
        app = PoissonServerApp(root)
        root.mainloop()


РЕЗУЛЬТАТЫ
<img width="913" height="490" alt="image" src="https://github.com/user-attachments/assets/c9028bcb-a487-4309-a47c-15b8b76b4e6d" />
