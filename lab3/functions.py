import math

def func1(x):
    return -x**3 - x**2 - 2*x + 1

def func2(x):
    return x**2

def func3(x):
    return math.sin(x)

def func4(x):                  # ln(x)/sqrt(x)  (разрыв в a = 0)
    return math.log(x) / math.sqrt(x)

def func5(x):                  # 1 / sqrt(1-x)   (разрыв в b = 1)
    return 1.0 / math.sqrt(1.0 - x)

def func6(x):                  # 1/sqrt(|x-0.5|) разрыв в точке 0.5
    return 1.0 / math.sqrt(abs(x - 0.5))
