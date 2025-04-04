
def read_ab_eps_keyboard():
    print("Введите a,b:")
    line= input("> ").strip()
    a_str,b_str= line.split()
    a,b= float(a_str), float(b_str)
    if a>b:
        a,b= b,a
    print("Введите eps:")
    eps= float(input("> ").strip())
    return a,b,eps

def read_ab_eps_file(filename="input_equation.txt"):
    try:
        with open(filename,"r",encoding="utf-8") as f_in:
            line1= f_in.readline().strip()
            a_str,b_str= line1.split()
            a,b= float(a_str), float(b_str)
            if a>b:
                a,b= b,a
            eps_str= f_in.readline().strip()
            eps= float(eps_str)
        return a,b,eps
    except:
        return None,None,None

def read_xy_eps_keyboard():
    print("Введите x0,y0:")
    line= input("> ").strip()
    x0_str,y0_str= line.split()
    x0,y0= float(x0_str), float(y0_str)
    print("Введите eps:")
    eps= float(input("> ").strip())
    return x0,y0,eps

def read_xy_eps_file(filename="input_system.txt"):
    try:
        with open(filename,"r",encoding="utf-8") as f_in:
            line1= f_in.readline().strip()
            x0_str,y0_str= line1.split()
            x0,y0= float(x0_str), float(y0_str)
            eps_str= f_in.readline().strip()
            eps= float(eps_str)
        return x0,y0,eps
    except:
        return None,None,None

def output_root(root, fx, iters):
    print("Куда вывести результат? (1-экран, 2-файл)")
    ans= input("> ").strip()
    if ans=="2":
        with open("output.txt","a",encoding="utf-8") as f_out:
            f_out.write(f"Корень x={root:.6f}, f(x)={fx:.3e}, итераций={iters}\n")
        print("Записано в output.txt")
    else:
        print(f"Корень x={root:.6f}, f(x)={fx:.3e}, итераций={iters}")

def output_system_solution(X,Y, iters, F1, F2):
    r1= abs(F1(X,Y))
    r2= abs(F2(X,Y))
    print("Куда вывести результат? (1-экран, 2-файл)")
    ans= input("> ").strip()
    if ans=="2":
        with open("output.txt","a",encoding="utf-8") as f_out:
            f_out.write(f"Решение системы: x={X:.6f}, y={Y:.6f}, итераций={iters}\n")
            f_out.write(f"Вектор погрешностей: |F1|={r1:.3e}, |F2|={r2:.3e}\n")
        print("Записано в output.txt")
    else:
        print(f"Решение системы: x={X:.6f}, y={Y:.6f}, итераций={iters}")
        print(f"Вектор погрешностей: |F1|={r1:.3e}, |F2|={r2:.3e}")
