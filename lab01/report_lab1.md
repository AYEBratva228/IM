### ОТЧЕТ

**1) Код**


    namespace Lab_1
    {
        public partial class Form1 : Form
        {
            public Form1()
            {
                InitializeComponent();
            }
    
            const decimal g = 9.81M;
            const decimal C = 0.15M;
            const decimal rho = 1.29M;
            decimal dt;
            decimal x1;
            int line = -1;
    
            private void chart1_Click(object sender, EventArgs e)
            {
    
            }
    
            decimal t, x, y, v0, cosa, sina, S, m, k, vx, vy;
    
            private void Form1_Load(object sender, EventArgs e)
            {
                Step.SelectedItem = "0.1";
            }
    
            private void button1_Click(object sender, EventArgs e)
            {
                line++;
                if (line == 6)
                {
                    line = 0;
                }
                chart1.Series[line].Points.Clear();
                if (!timer1.Enabled)
                {
                    t = 0;
                    x = 0;
                    y = Height.Value;
                    v0 = Speed.Value;
                    dt = Convert.ToDecimal(Step.SelectedItem, CultureInfo.InvariantCulture);
                    double a = (double)Angle.Value * Math.PI / 180;
                    cosa = (decimal)Math.Cos(a);
                    sina = (decimal)Math.Sin(a);
                    S = Size.Value;
                    m = Weight.Value;
                    k = 0.5M * C * rho * S / m;
                    vx = v0 * cosa;
                    vy = v0 * sina;
                    chart1.Series[line].Points.AddXY(x, y);
                    timer1.Start();
                }
                x1 = 0;
            }
    
            private void timer1_Tick(object sender, EventArgs e)
            {
                t += dt;
                decimal v = (decimal)Math.Sqrt((double)(vx * vx + vy * vy));
                vx = vx - k * vx * v * dt;
                vy = vy - (g + k * vy * v) * dt;
                x = x + vx * dt;
                y = y + vy * dt;
                chart1.Series[line].Points.AddXY(x, y);
                if (x1 < y)
                {
                    x1 = y;
                }
                if (y <= 0)
                {
                    timer1.Stop();
                    DistanceLabel.Text = "" + Math.Round(x, 3);
                    StepLabel.Text = "" + dt;
                    MaxHeightLabel.Text = "" + Math.Round(x1, 3);
                    FinalSpeedLabel.Text = "" + Math.Round(v, 3);
                }
    
            }
        }


**2) Моделирование графиков**

<img width="580" height="233" alt="image" src="https://github.com/user-attachments/assets/60cec29e-cce2-42a7-8f81-0782739abd8d" />


**3) Таблица с результатами**

С начальными данными:
h = 10
S = 10
W = 10
a = 45
v = 10

| Шаг моделирования, с | 1 | 0.1 | 0.01 | 0.001 | 0.0001 |
|----------------------|---|-----|------|-------|--------|
| Дальность полёта, м |  0.249 |  8.166   |  8,785    |   8.851    |     8.858   |
| Максимальная высота, м | 0.420 | 11.424 | 11.824 | 11.865 | 11.869 |
| Скорость в конечной точке, м/с | 9.583 | 9.499 | 9.531 | 9.538 | 9.539 |

**4) Выводы**

В ходе лабораторной работы я научился моделировать полет объекта в иделаьных условиях, выяснил, как отражается шаг времени на рехультатах и понял, что в заданным условиях при выбранных мной данных брать шаг меньше 0.001 не имеет смысла.
