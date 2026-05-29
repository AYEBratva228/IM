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
