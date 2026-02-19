using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

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
}
