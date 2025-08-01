import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Data
length = np.array([20, 21, 21, 22, 24, 32, 35, 36.5, 38, 39, 41, 43, 43,
                   44.5, 45, 46, 46, 47, 47, 48, 48.5, 48.5, 49, 50, 50, 50, 50, 51, 51.5])
length *= 0.001
pressure = np.array([-60, -50, -45, -40, -35, -30, -25, -20, -15, -10,
                     -5, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130,
                     140, 160, 180, 200])

# 4th order polynomial model
def poly4(x, a, b, c, d, e):
    return a * x**4 + b * x**3 + c * x**2 + d * x + e

# Fit the curve
popt, _ = curve_fit(poly4, length, pressure)
a, b, c, d, e = popt
print(f"Fitted equation: pressure = {a:.5f} * length^4 + {b:.5f} * length^3 + {c:.5f} * length^2 + {d:.5f} * length + {e:.5f}")

# Generate smooth curve for plotting
x_fit = np.linspace(min(length), max(length), 200)
y_fit = poly4(x_fit, *popt)

# Plot the results
plt.scatter(length, pressure, label='Data', color='blue')
plt.plot(x_fit, y_fit, label='Fitted Curve (4th Order)', color='purple')
plt.xlabel('Length')
plt.ylabel('Pressure')
plt.title('Length vs. Pressure Curve Fit (4th Order Polynomial)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Fitted equation: pressure = 797192270.26400 * length^4 + -84918177.62388 * length^3 + 3165367.07235 * length^2 + -45766.30128 * length + 147.49474
