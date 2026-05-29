### Лабораторная работа 5

**1) Код**

      import tkinter as tk
      from tkinter import ttk, messagebox
      import numpy as np
      from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
      from matplotlib.figure import Figure
      import matplotlib
      
      matplotlib.interactive(False)
      matplotlib.use('TkAgg')
      
      
      class DiscreteRVApp:
          def __init__(self, root):
              self.root = root
              self.root.title("Генерация дискретной случайной величины")
              self.root.geometry("800x700")
      
              self.theoretical_probs = np.zeros(5)
      
              self.create_input_frame()
              self.create_control_frame()
              self.create_stats_frame()
              self.create_chart_frame()
      
              self.setup_plot()
      
          def create_input_frame(self):
              input_frame = ttk.LabelFrame(self.root, text="Вероятности", padding=10)
              input_frame.pack(fill="x", padx=10, pady=5)
      
              self.prob_entries = []
              for i in range(4):
                  label = ttk.Label(input_frame, text=f"Prob {i + 1}:")
                  label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
      
                  entry = ttk.Entry(input_frame, width=15)
                  entry.grid(row=i, column=1, padx=5, pady=5)
                  entry.insert(0, "0.2")
                  entry.bind('<KeyRelease>', self.update_prob5)
                  self.prob_entries.append(entry)
      
              ttk.Label(input_frame, text="Prob 5:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
              self.prob5_var = tk.StringVar(value="0.2")
              self.prob5_entry = ttk.Entry(input_frame, textvariable=self.prob5_var, state='readonly', width=15)
              self.prob5_entry.grid(row=4, column=1, padx=5, pady=5)
      
              self.update_prob5()
      
          def update_prob5(self, event=None):
              try:
                  total = 0
                  for entry in self.prob_entries:
                      val = float(entry.get())
                      if val < 0 or val > 1:
                          self.prob5_var.set("Ошибка")
                          return
                      total += val
      
                  if total >= 1:
                      self.prob5_var.set("Ошибка")
                  else:
                      prob5 = 1 - total
                      self.prob5_var.set(f"{prob5:.4f}")
              except ValueError:
                  self.prob5_var.set("Ошибка")
      
          def create_control_frame(self):
              control_frame = ttk.Frame(self.root)
              control_frame.pack(fill="x", padx=10, pady=5)
      
              ttk.Label(control_frame, text="Объем выборки N:").pack(side="left", padx=5)
              self.n_var = tk.StringVar(value="1000")
              self.n_combo = ttk.Combobox(control_frame, textvariable=self.n_var,
                                          values=["10", "100", "1000", "10000"],
                                          state="readonly", width=10)
              self.n_combo.pack(side="left", padx=5)
      
              self.start_button = ttk.Button(control_frame, text="Start", command=self.start_experiment)
              self.start_button.pack(side="left", padx=20)
      
          def create_stats_frame(self):
              stats_frame = ttk.LabelFrame(self.root, text="Результаты", padding=10)
              stats_frame.pack(fill="x", padx=10, pady=5)
      
              self.avg_label = ttk.Label(stats_frame, text="Average: --", font=("Arial", 10))
              self.avg_label.pack(anchor="w", pady=2)
      
              self.var_label = ttk.Label(stats_frame, text="Variance: --", font=("Arial", 10))
              self.var_label.pack(anchor="w", pady=2)
      
              self.chi_label = ttk.Label(stats_frame, text="Chi-squared: --", font=("Arial", 10))
              self.chi_label.pack(anchor="w", pady=2)
      
          def create_chart_frame(self):
              chart_frame = ttk.LabelFrame(self.root, text="Гистограмма", padding=5)
              chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
      
              self.fig = Figure(figsize=(6, 4), dpi=100)
              self.ax = self.fig.add_subplot(111)
      
              self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
              self.canvas.get_tk_widget().pack(fill="both", expand=True)
      
          def setup_plot(self):
              self.ax.clear()
              self.ax.set_xlabel("Значения X")
              self.ax.set_ylabel("Частота")
              self.ax.set_title("Эмпирическая гистограмма")
              self.ax.set_xticks([1, 2, 3, 4, 5])
              self.ax.grid(True, alpha=0.3)
              self.canvas.draw()
      
          def validate_probabilities(self):
              try:
                  probs = []
                  for i, entry in enumerate(self.prob_entries):
                      val = float(entry.get())
                      if val < 0 or val > 1:
                          messagebox.showerror("Ошибка", f"Prob {i + 1} должно быть в диапазоне [0, 1]")
                          return None
                      probs.append(val)
      
                  total = sum(probs)
                  if total >= 1:
                      messagebox.showerror("Ошибка", f"Сумма Prob 1-4 = {total:.4f} ≥ 1")
                      return None
      
                  prob5 = 1 - total
                  if prob5 < 0:
                      messagebox.showerror("Ошибка", f"Prob 5 = {prob5:.4f} < 0")
                      return None
      
                  probs.append(prob5)
      
                  return np.array(probs)
              except ValueError:
                  messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа")
                  return None
      
          def generate_samples(self, probs, n):
              cdf = np.cumsum(probs)
              u = np.random.uniform(0, 1, n)
              samples = np.zeros(n, dtype=int)
              for i in range(n):
                  samples[i] = np.searchsorted(cdf, u[i]) + 1
              return samples
      
          def calculate_stats(self, samples, theoretical_probs):
              n = len(samples)
      
              empirical_freq = np.zeros(5)
              for i in range(5):
                  empirical_freq[i] = np.sum(samples == (i + 1))
              empirical_probs = empirical_freq / n
      
              empirical_mean = np.mean(samples)
              theoretical_mean = np.sum(np.arange(1, 6) * theoretical_probs)
      
              empirical_var = np.var(samples, ddof=1)
              theoretical_mean_sq = np.sum((np.arange(1, 6) ** 2) * theoretical_probs)
              theoretical_var = theoretical_mean_sq - theoretical_mean ** 2
      
              mean_error = abs((empirical_mean - theoretical_mean) / theoretical_mean) * 100 if theoretical_mean != 0 else 0
              var_error = abs((empirical_var - theoretical_var) / theoretical_var) * 100 if theoretical_var != 0 else 0
      
              chi_squared = 0
              for i in range(5):
                  expected = n * theoretical_probs[i]
                  if expected > 0:
                      chi_squared += (empirical_freq[i] - expected) ** 2 / expected
      
              critical_value = 9.488
              chi_result = chi_squared > critical_value
      
              return {
                  'empirical_mean': empirical_mean,
                  'theoretical_mean': theoretical_mean,
                  'mean_error': mean_error,
                  'empirical_var': empirical_var,
                  'theoretical_var': theoretical_var,
                  'var_error': var_error,
                  'chi_squared': chi_squared,
                  'chi_result': chi_result,
                  'empirical_freq': empirical_freq,
                  'empirical_probs': empirical_probs,
                  'critical_value': critical_value
              }
      
          def update_plot(self, empirical_freq, theoretical_probs, n):
              self.ax.clear()
      
              x = np.arange(1, 6)
              width = 0.35
      
              bars1 = self.ax.bar(x - width / 2, empirical_freq, width,
                                  label='Эмпирические', color='skyblue',
                                  alpha=0.7, edgecolor='black')
      
              bars2 = self.ax.bar(x + width / 2, theoretical_probs * n, width,
                                  label='Теоретические', color='orange',
                                  alpha=0.7, edgecolor='black')
      
              self.ax.bar_label(bars1, fmt='%.0f', padding=3, fontsize=9)
              self.ax.bar_label(bars2, fmt='%.1f', padding=3, fontsize=9)
      
              self.ax.set_xlabel("Значения X", fontsize=10)
              self.ax.set_ylabel("Частота", fontsize=10)
              self.ax.set_title(f"Гистограмма распределения (N={n})", fontsize=11, fontweight='bold')
              self.ax.set_xticks(x)
              self.ax.legend(loc='upper right')
              self.ax.grid(True, alpha=0.3, axis='y')
      
              self.canvas.draw_idle()
      
          def start_experiment(self):
              theoretical_probs = self.validate_probabilities()
              if theoretical_probs is None:
                  return
      
              try:
                  n = int(self.n_var.get())
              except ValueError:
                  messagebox.showerror("Ошибка", "Некорректный объем выборки")
                  return
      
              np.random.seed()
              samples = self.generate_samples(theoretical_probs, n)
      
              stats = self.calculate_stats(samples, theoretical_probs)
      
              self.avg_label.config(
                  text=f"Average: {stats['empirical_mean']:.4f} "
                       f"(theoretical: {stats['theoretical_mean']:.4f}, "
                       f"error = {stats['mean_error']:.2f}%)"
              )
      
              self.var_label.config(
                  text=f"Variance: {stats['empirical_var']:.4f} "
                       f"(theoretical: {stats['theoretical_var']:.4f}, "
                       f"error = {stats['var_error']:.2f}%)"
              )
      
              chi_status = "true" if stats['chi_result'] else "false"
              self.chi_label.config(
                  text=f"Chi-squared: {stats['chi_squared']:.2f} "
                       f"> {stats['critical_value']} is {chi_status}"
              )
      
              self.update_plot(stats['empirical_freq'], theoretical_probs, n)
      
      
      def main():
          root = tk.Tk()
          app = DiscreteRVApp(root)
          root.mainloop()
      
      
      if __name__ == "__main__":
          main()
   

**2) Результаты**



**3) Вывод**

В ходе лабораторной работы, я меня получилось реализовать да\нет генератор и 8-ball генератор на основе генерации событий из группы событий с попарно несовместными событиями.
