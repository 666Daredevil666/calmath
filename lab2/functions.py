import math

def f1(x):
    """ 2.74x^3 -1.93x^2 -15.28x -3.72 """
    return 2.74*(x**3) - 1.93*(x**2) - 15.28*x - 3.72

def df1(x):
    """ Производная для f1 """
    return 3*2.74*(x**2) - 2*1.93*x - 15.28

def f2(x):
    """ sin(x) - 0.5x """
    return math.sin(x) - 0.5*x

def df2(x):
    return math.cos(x) - 0.5

def f3(x):
    """ e^x - x^2 + 1 """
    return math.e**x - x**2 + 1

def df3(x):
    return math.e**x - 2*x

FUNCTIONS = {
    "1": (f1, df1, "f1(x)=2.74x^3 -1.93x^2 -15.28x -3.72"),
    "2": (f2, df2, "f2(x)=sin(x) - 0.5x"),
    "3": (f3, df3, "f3(x)=e^x - x^2 +1")
}
