import math
import numpy as np

# ----- СИСТЕМА №1 -----
def F1_1(x,y):
    return math.sin(x+1) - y -1.2
def F2_1(x,y):
    return 2*x + math.cos(y) -2

def dF1_1dx(x,y):
    return math.cos(x+1)
def dF1_1dy(x,y):
    return -1
def dF2_1dx(x,y):
    return 2
def dF2_1dy(x,y):
    return -math.sin(y)

# ----- СИСТЕМА №2 -----
def F1_2(x,y):
    return x*x + y*y -4
def F2_2(x,y):
    return x - y -1

def dF1_2dx(x,y):
    return 2*x
def dF1_2dy(x,y):
    return 2*y
def dF2_2dx(x,y):
    return 1
def dF2_2dy(x,y):
    return -1

# ----- СИСТЕМА №3 -----
def F1_3(x,y):
    return math.e**x - y
def F2_3(x,y):
    return x + y -2

def dF1_3dx(x,y):
    return math.e**x
def dF1_3dy(x,y):
    return -1
def dF2_3dx(x,y):
    return 1
def dF2_3dy(x,y):
    return 1

SYSTEMS = {
    "1": {
        "name":"System1: { sin(x+1)-y=1.2,  2x+cos(y)=2 }",
        "F1": F1_1, "F2": F2_1,
        "dF1dx": dF1_1dx, "dF1dy": dF1_1dy,
        "dF2dx": dF2_1dx, "dF2dy": dF2_1dy
    },
    "2": {
        "name":"System2: { x^2+y^2=4,  x-y=1 }",
        "F1": F1_2, "F2": F2_2,
        "dF1dx": dF1_2dx, "dF1dy": dF1_2dy,
        "dF2dx": dF2_2dx, "dF2dy": dF2_2dy
    },
    "3": {
        "name":"System3: { e^x - y=0,  x+y=2 }",
        "F1": F1_3, "F2": F2_3,
        "dF1dx": dF1_3dx, "dF1dy": dF1_3dy,
        "dF2dx": dF2_3dx, "dF2dy": dF2_3dy
    }
}

def newton_system(F1,F2, dF1dx,dF1dy,dF2dx,dF2dy,
                  x0,y0, eps=1e-3, max_iter=100):
    x,y= x0,y0
    for i in range(max_iter):
        J11= dF1dx(x,y)
        J12= dF1dy(x,y)
        J21= dF2dx(x,y)
        J22= dF2dy(x,y)
        det= J11*J22 - J12*J21
        if abs(det)<1e-15:
            raise ZeroDivisionError("Якобиан вырожден.")
        Fx= -F1(x,y)
        Fy= -F2(x,y)
        dx= (Fx*J22 - Fy*J12)/det
        dy= (J11*Fy - J21*Fx)/det
        x_new= x+dx
        y_new= y+dy
        if math.hypot(dx,dy)< eps:
            return (x_new,y_new, i+1)
        x,y= x_new,y_new
    return (x,y, max_iter)

def simple_iter_system(F1,F2, x0,y0, alpha=0.01, eps=1e-3, max_iter=100):
    x,y= x0,y0
    for i in range(max_iter):
        x_new= x - alpha*F1(x,y)
        y_new= y - alpha*F2(x,y)
        if math.hypot(x_new - x, y_new - y)< eps:
            return (x_new,y_new, i+1)
        x,y= x_new,y_new
    return (x,y, max_iter)

def check_system_iter_convergence(dF1dx,dF1dy,dF2dx,dF2dy,
                                  x_min,x_max,y_min,y_max,
                                  alpha=0.01, steps=10):
    """
    Проверяем max-норму Якобиана phi'(x,y) для
    phi_1(x,y)= x - alpha*F1(x,y),
    phi_2(x,y)= y - alpha*F2(x,y).

    J_phi= [ 1 - alpha*dF1dx   -alpha*dF1dy ]
            [ -alpha*dF2dx     1-alpha*dF2dy]

    Берём максимум построчной нормы (строка 1= |j11|+|j12|, строка2=|j21|+|j22|).
    Возвращаем (ok, max_val).
    """
    xs= np.linspace(x_min, x_max, steps+1)
    ys= np.linspace(y_min, y_max, steps+1)
    max_val= 0.0
    for xx in xs:
        for yy in ys:
            j11= 1 - alpha*dF1dx(xx,yy)
            j12= -alpha*dF1dy(xx,yy)
            j21= -alpha*dF2dx(xx,yy)
            j22= 1 - alpha*dF2dy(xx,yy)
            row1= abs(j11)+ abs(j12)
            row2= abs(j21)+ abs(j22)
            loc= max(row1,row2)
            if loc> max_val:
                max_val= loc
    is_ok= (max_val<1)
    return (is_ok, max_val)
