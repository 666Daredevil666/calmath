import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

def plot_function(f, a, b, step=0.01):
    xs = np.arange(a, b+step, step)
    ys = [f(x) for x in xs]
    plt.figure()
    plt.axhline(0, color='k', linewidth=1)
    plt.plot(xs, ys, label='f(x)')
    plt.title(f"Graph of f(x) on [{a},{b}]")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_system(F1, F2, x_min=-3, x_max=3, y_min=-3, y_max=3, step=0.05):
    xs = np.arange(x_min, x_max+step, step)
    ys = np.arange(y_min, y_max+step, step)
    X, Y= np.meshgrid(xs, ys)
    Z1= np.zeros_like(X)
    Z2= np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            xx= X[i,j]
            yy= Y[i,j]
            Z1[i,j]= F1(xx, yy)
            Z2[i,j]= F2(xx, yy)
    plt.figure()
    c1= plt.contour(X, Y, Z1, levels=[0], colors='blue')
    c2= plt.contour(X, Y, Z2, levels=[0], colors='red')
    plt.clabel(c1, inline=True, fontsize=8)
    plt.clabel(c2, inline=True, fontsize=8)
    plt.title("System: F1=0(blue), F2=0(red)")
    plt.grid(True)
    plt.show()
