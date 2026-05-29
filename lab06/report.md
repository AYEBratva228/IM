### Лабораторная работа 6

**1) Код**

lab6.1

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
          
lab6.2   

      import tkinter as tk
      from tkinter import ttk, messagebox
      import numpy as np
      import matplotlib.pyplot as plt
      from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
      from scipy.stats import chi2, norm
      import math
      
      
      class NormalDistributionSimulator:
          def __init__(self, root):
              self.root = root
              self.root.title("Normal Distribution Simulator")
              self.root.geometry("800x700")
              self.root.resizable(False, False)
      
              main_frame = ttk.Frame(self.root, padding="10")
              main_frame.pack(fill=tk.BOTH, expand=True)
      
              input_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
              input_frame.pack(fill=tk.X, pady=(0, 10))
      
              ttk.Label(input_frame, text="Mean:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
              self.mean_entry = ttk.Entry(input_frame, width=15)
              self.mean_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
              self.mean_entry.insert(0, "0")
      
              ttk.Label(input_frame, text="Variance:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
              self.var_entry = ttk.Entry(input_frame, width=15)
              self.var_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
              self.var_entry.insert(0, "1")
      
              ttk.Label(input_frame, text="Sample size:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
              self.size_var = tk.StringVar(value="1000")
              size_combo = ttk.Combobox(input_frame, textvariable=self.size_var, values=["10", "100", "1000", "10000"],
                                        width=10, state="readonly")
              size_combo.grid(row=0, column=5, sticky=tk.W)
      
              self.start_button = ttk.Button(input_frame, text="Start", command=self.run_simulation)
              self.start_button.grid(row=0, column=6, padx=(20, 0))
      
              plot_frame = ttk.LabelFrame(main_frame, text="Histogram and Density Curve", padding="5")
              plot_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
      
              self.figure, self.ax = plt.subplots(figsize=(7, 4))
              self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
              self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
      
              stats_frame = ttk.LabelFrame(main_frame, text="Statistical Results", padding="10")
              stats_frame.pack(fill=tk.X, pady=(0, 10))
      
              self.stats_label = ttk.Label(stats_frame, text="Average: --- (error = ---%)\nVariance: --- (error = ---%)",
                                           font=("Courier", 10))
              self.stats_label.pack(anchor=tk.W)
      
              chi_frame = ttk.LabelFrame(main_frame, text="Chi-squared Test", padding="10")
              chi_frame.pack(fill=tk.X)
      
              self.chi_label = ttk.Label(chi_frame, text="Chi-squared: ---", font=("Courier", 10))
              self.chi_label.pack(anchor=tk.W)
      
              self.bins = [-3, -2, -1, 0, 1, 2, 3, 4]
              self.bin_labels = [f"({self.bins[i]}; {self.bins[i + 1]}]" for i in range(len(self.bins) - 1)]
      
          def generate_normal_samples(self, mean, variance, size):
              std = np.sqrt(variance)
              samples = np.zeros(size)
              for i in range(0, size, 2):
                  u1 = np.random.random()
                  u2 = np.random.random()
                  z1 = np.sqrt(-2.0 * np.log(u1)) * np.cos(2.0 * np.pi * u2)
                  z2 = np.sqrt(-2.0 * np.log(u1)) * np.sin(2.0 * np.pi * u2)
                  if i < size:
                      samples[i] = mean + std * z1
                  if i + 1 < size:
                      samples[i + 1] = mean + std * z2
              return samples
      
          def compute_histogram(self, samples, mean, variance):
              counts = np.zeros(len(self.bins) - 1)
              total = len(samples)
              for sample in samples:
                  for i in range(len(self.bins) - 1):
                      if self.bins[i] < sample <= self.bins[i + 1]:
                          counts[i] += 1
                          break
              observed = counts
              expected = []
              std = np.sqrt(variance)
              for i in range(len(self.bins) - 1):
                  lower = (self.bins[i] - mean) / std
                  upper = (self.bins[i + 1] - mean) / std
                  prob = 0.5 * (1.0 + math.erf(upper / math.sqrt(2.0))) - 0.5 * (1.0 + math.erf(lower / math.sqrt(2.0)))
                  expected.append(prob * total)
              return observed, expected
      
          def run_simulation(self):
              try:
                  mean = float(self.mean_entry.get())
                  variance = float(self.var_entry.get())
                  size = int(self.size_var.get())
      
                  if variance <= 0:
                      messagebox.showerror("Error", "Variance must be positive")
                      return
      
                  samples = self.generate_normal_samples(mean, variance, size)
      
                  sample_mean = np.mean(samples)
                  sample_var = np.var(samples, ddof=0)
      
                  if abs(mean) < 1e-10:
                      mean_error = abs(sample_mean - mean) * 100
                  else:
                      mean_error = abs((sample_mean - mean) / mean) * 100
      
                  var_error = abs((sample_var - variance) / variance) * 100
      
                  self.stats_label.config(
                      text=f"Average: {sample_mean:.3f} (error = {mean_error:.2f}%)\n"
                           f"Variance: {sample_var:.3f} (error = {var_error:.2f}%)"
                  )
      
                  observed, expected = self.compute_histogram(samples, mean, variance)
      
                  valid_indices = [i for i in range(len(expected)) if expected[i] >= 5]
                  if len(valid_indices) < 2:
                      chi2_message = "Chi-squared: insufficient expected frequencies (need ≥5 per bin)"
                      self.chi_label.config(text=chi2_message)
                  else:
                      observed_filtered = [observed[i] for i in valid_indices]
                      expected_filtered = [expected[i] for i in valid_indices]
                      chi2_stat = np.sum(
                          (np.array(observed_filtered) - np.array(expected_filtered)) ** 2 / np.array(expected_filtered))
                      df = len(valid_indices) - 3
                      if df > 0:
                          critical_value = chi2.ppf(0.95, df)
                          is_consistent = chi2_stat < critical_value
                          chi2_message = f"Chi-squared: {chi2_stat:.3f} {'<' if chi2_stat < critical_value else '>'} {critical_value:.3f} (is {is_consistent})"
                      else:
                          chi2_message = f"Chi-squared: {chi2_stat:.3f} (insufficient degrees of freedom)"
                      self.chi_label.config(text=chi2_message)
      
                  # Очистка графика
                  self.ax.clear()
                  
                  # Построение гистограммы (нормированной на плотность)
                  counts, bin_edges, patches = self.ax.hist(samples, bins=self.bins, edgecolor='black', 
                                                            alpha=0.6, color='steelblue', density=True,
                                                            label='Histogram (normalized)')
                  
                  # Построение теоретической кривой плотности нормального распределения
                  std_dev = np.sqrt(variance)
                  x_range = np.linspace(min(self.bins), max(self.bins), 1000)
                  theoretical_pdf = norm.pdf(x_range, mean, std_dev)
                  self.ax.plot(x_range, theoretical_pdf, 'r-', linewidth=2, label='Theoretical normal PDF')
                  
                  # Настройка графика
                  self.ax.set_xticks(self.bins)
                  self.ax.set_xlabel('Intervals')
                  self.ax.set_ylabel('Density')
                  self.ax.set_title(f'Histogram and Density Curve (n={size})')
                  self.ax.grid(True, alpha=0.3)
                  self.ax.legend(loc='upper right')
                  
                  # Добавление текста с частотами
                  hist_counts, _ = np.histogram(samples, bins=self.bins)
                  max_density = max(counts) if len(counts) > 0 else 1
                  for i, (count, label) in enumerate(zip(hist_counts, self.bin_labels)):
                      if i < len(self.bins) - 1:
                          self.ax.text(self.bins[i] + 0.5, 
                                      max_density * 0.95,
                                      f'n={int(count)}', ha='center', fontsize=8, 
                                      bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
                  
                  self.canvas.draw()
      
              except ValueError as e:
                  messagebox.showerror("Error", f"Invalid input: {str(e)}")
              except Exception as e:
                  messagebox.showerror("Error", f"Unexpected error: {str(e)}")
      
      
      if __name__ == "__main__":
          root = tk.Tk()
          app = NormalDistributionSimulator(root)
          root.mainloop()


**2) Результаты**




**3) Вывод**

В ходе лабораторной работы, я меня получилось реализовать да\нет генератор и 8-ball генератор на основе генерации событий из группы событий с попарно несовместными событиями.
