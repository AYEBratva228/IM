### Лабораторная работа 2

**1) Код**

    using System;
    using System.Diagnostics;
    using System.Windows.Forms;
    
    namespace Plate
    {
        public partial class Form1 : Form
        {
            // Параметры меди
            const double rho = 8960.0;
            const double c = 385.0;
            const double lambda = 401.0;
            static readonly double a = lambda / (rho * c);
    
            public Form1()
            {
                InitializeComponent();
            }
    
            
            private void button1_Click_1(object sender, EventArgs e)
            {
                Grid.Rows.Clear();
                
    
                double L = double.Parse(textBox1.Text);
                double T_left = double.Parse(textBox2.Text);
                double T_right = double.Parse(textBox3.Text);
                double t_model = double.Parse(textBox4.Text);
    
                double[] dt_values = { 0.1, 0.01, 0.001 };
                double[] dx_values = { 0.1, 0.01, 0.001, 0.0001 };
    
                foreach (double dx in dx_values)
                {
                    foreach (double dt in dt_values)
                    {
                        int N = (int)(L / dx);
                        int timeSteps = (int)(t_model / dt);
    
                        double[] T = new double[N + 1];
                        double[] T_prev = new double[N + 1];
    
                        T_prev[0] = T_left;
                        T_prev[N] = T_right;
    
                        double r = a * dt / (dx * dx);
    
                        Stopwatch sw = Stopwatch.StartNew();
    
                        for (int n = 0; n < timeSteps; n++)
                        {
                            SolveTridiagonal(T, T_prev, r, N, T_left, T_right);
                            Array.Copy(T, T_prev, N + 1);
                        }
    
                        sw.Stop();
    
                        double T_center = T[N / 2];
    
                        Grid.Rows.Add(
                            dx,
                            dt,
                            T_center.ToString("F6"),
                            sw.Elapsed.TotalSeconds.ToString("F6")
                        );
                    }
                }
            }
    
            private static void SolveTridiagonal(
                double[] T,
                double[] T_prev,
                double r,
                int N,
                double T_left,
                double T_right)
            {
                double[] alpha = new double[N + 1];
                double[] beta = new double[N + 1];
    
                alpha[1] = 0.0;
                beta[1] = T_left;
    
                for (int i = 1; i < N; i++)
                {
                    double A = -r;
                    double B = 1 + 2 * r;
                    double C = -r;
                    double D = T_prev[i];
    
                    double denom = B + A * alpha[i];
                    alpha[i + 1] = -C / denom;
                    beta[i + 1] = (D - A * beta[i]) / denom;
                }
    
                T[N] = T_right;
    
                for (int i = N - 1; i >= 0; i--)
                {
                    T[i] = alpha[i + 1] * T[i + 1] + beta[i + 1];
                }
            }
    
        }
    }


**2) Результаты**

При начальных данных:
L = 0.3
t_left = -30
t_right = 10
Time = 5

Для меди:
rho = 8960.0
c = 385.0
lambda = 401.0

<img width="433" height="190" alt="image" src="https://github.com/user-attachments/assets/ff81739f-fb7a-4001-9726-88adb68053e0" />

**3) Вывод**

У меня получилось реализовать моделирование изменения температуры в пластине на основе одномерного уравнения теплопроводности с использованием метода конечных разностей.
