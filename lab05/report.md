### Лабораторная работа 5

**1) Код**


    import tkinter as tk
    import random
    
    
    class YesNoApp:
        def __init__(self):
            self.window = tk.Tk()
            self.window.title("Да или Нет")
            self.window.geometry("400x300")
    
            tk.Label(self.window, text="Задайте свой вопрос:", font=("Arial", 12)).pack(pady=10)
    
            self.question_entry = tk.Entry(self.window, width=40, font=("Arial", 10))
            self.question_entry.pack(pady=10)
    
            self.get_answer_btn = tk.Button(self.window, text="Получить ответ", command=self.get_answer, font=("Arial", 10))
            self.get_answer_btn.pack(pady=10)
    
            self.answer_label = tk.Label(self.window, text="", font=("Arial", 16, "bold"), fg="blue")
            self.answer_label.pack(pady=20)
    
            self.switch_btn = tk.Button(self.window, text="Перейти к Магическому шару", command=self.switch_to_magic,
                                        font=("Arial", 10))
            self.switch_btn.pack(pady=10)
    
        def get_answer(self):
            answer = random.choice(["Да", "Нет"])
            self.answer_label.config(text=answer)
    
        def switch_to_magic(self):
            self.window.destroy()
            MagicBallApp()
    
        def run(self):
            self.window.mainloop()
    
    
    class MagicBallApp:
        def __init__(self):
            self.window = tk.Tk()
            self.window.title("Магический шар 8")
            self.window.geometry("500x400")
    
            self.responses = [
                ("Бесспорно", 0.06),
                ("Предрешено", 0.06),
                ("Никаких сомнений", 0.06),
                ("Определённо да", 0.06),
                ("Можешь быть уверен в этом", 0.06),
                ("Мне кажется — да", 0.05),
                ("Вероятнее всего", 0.05),
                ("Хорошие перспективы", 0.05),
                ("Знаки говорят — да", 0.05),
                ("Да", 0.05),
                ("Пока не ясно, попробуй снова", 0.04),
                ("Спроси позже", 0.04),
                ("Лучше не рассказывать", 0.04),
                ("Сейчас нельзя предсказать", 0.04),
                ("Сконцентрируйся и спроси опять", 0.04),
                ("Даже не думай", 0.05),
                ("Мой ответ — нет", 0.05),
                ("По моим данным — нет", 0.05),
                ("Перспективы не очень", 0.05),
                ("Весьма сомнительно", 0.05)
            ]
    
            total_prob = sum(prob for _, prob in self.responses)
            if abs(total_prob - 1.0) > 0.0001:
                raise ValueError(f"Сумма вероятностей должна быть равна 1, а не {total_prob}")
    
            tk.Label(self.window, text="Задайте вопрос магическому шару:", font=("Arial", 12)).pack(pady=10)
    
            self.question_entry = tk.Entry(self.window, width=50, font=("Arial", 10))
            self.question_entry.pack(pady=10)
    
            self.shake_btn = tk.Button(self.window, text="Трясти шар", command=self.get_prediction, font=("Arial", 12),
                                       bg="purple", fg="white")
            self.shake_btn.pack(pady=10)
    
            self.prediction_label = tk.Label(self.window, text="", font=("Arial", 14, "bold"), fg="green", wraplength=450)
            self.prediction_label.pack(pady=30)
    
            self.back_btn = tk.Button(self.window, text="Назад к Да/Нет", command=self.back_to_yesno, font=("Arial", 10))
            self.back_btn.pack(pady=5)
    
        def generate_event(self):
            alpha = random.random()
    
            remaining = alpha
            for i, (_, prob) in enumerate(self.responses):
                remaining -= prob
                if remaining <= 0:
                    return i
    
            return len(self.responses) - 1
    
        def get_prediction(self):
            event_index = self.generate_event()
            prediction = self.responses[event_index][0]
            self.prediction_label.config(text=prediction)
    
        def back_to_yesno(self):
            self.window.destroy()
            YesNoApp().run()
    
        def run(self):
            self.window.mainloop()
    
    
    if __name__ == "__main__":
        app = YesNoApp()
        app.run()
   

**2) Результаты**

<img width="401" height="331" alt="image" src="https://github.com/user-attachments/assets/388e5e33-a71f-41de-94a7-30a0c8d0d869" />


<img width="498" height="420" alt="image" src="https://github.com/user-attachments/assets/eb58fc1c-f087-476d-bcb7-580f4c840fc9" />



**3) Вывод**

В ходе лабораторной работы, я меня получилось реализовать да\нет генератор и 8-ball генератор на основе генерации событий из группы событий с попарно несовместными событиями.
