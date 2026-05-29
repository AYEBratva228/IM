### Лабораторная работа 4

**1) Код**


    import random
    import math
    
    class SimpleRNG:
        def __init__(self, seed=42):
            self.state = seed
            self.modulus = 2**31 - 1
            self.multiplier = 1103515245
            self.increment = 12345
    
        def next(self):
            self.state = (self.multiplier * self.state + self.increment) % self.modulus
            return self.state / self.modulus
    
        def generate(self, n):
            return [self.next() for _ in range(n)]
    
    def theoretical_mean():
        return 0.5
    
    def theoretical_variance():
        return 1.0 / 12.0
    
    def compute_stats(samples):
        n = len(samples)
        mean = sum(samples) / n
        variance = sum((x - mean) ** 2 for x in samples) / (n - 1)
        return mean, variance
    
    n_samples = 100000
    
    simple_rng = SimpleRNG(seed=42)
    samples_custom = simple_rng.generate(n_samples)
    
    samples_builtin = [random.random() for _ in range(n_samples)]
    
    mean_custom, var_custom = compute_stats(samples_custom)
    mean_builtin, var_builtin = compute_stats(samples_builtin)
    
    mean_theor = theoretical_mean()
    var_theor = theoretical_variance()
    
    print(f"Размер выборки: {n_samples}")
    print(f"\nТеоретические значения:")
    print(f"  Среднее: {mean_theor}")
    print(f"  Дисперсия: {var_theor:.6f}")
    print(f"\nСамодельный датчик (LCG):")
    print(f"  Выборочное среднее: {mean_custom:.6f}")
    print(f"  Выборочная дисперсия: {var_custom:.6f}")
    print(f"\nВстроенный генератор Python (Mersenne Twister):")
    print(f"  Выборочное среднее: {mean_builtin:.6f}")
    print(f"  Выборочная дисперсия: {var_builtin:.6f}")
   

**2) Результаты**

<img width="413" height="267" alt="image" src="https://github.com/user-attachments/assets/d483a591-b536-4f98-bfcd-4eb4b6c72f48" />


**3) Вывод**

Оба генератора демонстрируют результаты, близкие к теоретическим.
Встроенный генератор показывает незначительно лучшую точность,
что объясняется более сложным алгоритмом (Mersenne Twister).
