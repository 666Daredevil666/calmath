
from functions import FUNCTIONS
from methods import (
    bisection, secant, newton_method, simple_iteration,
    check_interval_for_root, check_single_iter_convergence
)
from systems import (
    SYSTEMS, newton_system, simple_iter_system,
    check_system_iter_convergence
)
from plot_utils import plot_function, plot_system
from io_utils import (
    read_ab_eps_keyboard, read_ab_eps_file,
    read_xy_eps_keyboard, read_xy_eps_file,
    output_root, output_system_solution
)

def main():
    print("=== Программа: решить одиночное уравнение или систему ===")
    print("1) Одиночное уравнение")
    print("2) Система (3 варианта)")
    choice= input("> ").strip()

    if choice=="1":
        print("Выберите уравнение:")
        for key,(f,df,desc) in FUNCTIONS.items():
            print(f"{key}) {desc}")
        fch= input("> ").strip()
        if fch not in FUNCTIONS:
            fch="1"
        f, df, desc= FUNCTIONS[fch]
        print(f"Вы выбрали:", desc)

        print("Откуда брать [a,b,eps]? (1 - клавиатура, 2 - файл)")
        ans= input("> ").strip()
        if ans=="2":
            a,b,eps= read_ab_eps_file("input_equation.txt")
            if a is None:
                print("Не удалось прочесть файл, переходим к клавиатуре.")
                a,b,eps= read_ab_eps_keyboard()
        else:
            a,b,eps= read_ab_eps_keyboard()

        c= check_interval_for_root(f,a,b)
        if c==0:
            print("На [a,b] нет корня.")
            return
        elif c>1:
            print("На [a,b] несколько корней.")
            return

        print("Выберите метод:")
        print("1) Бисекция\n2) Секущие\n3) Ньютона\n4) Итерация")
        mm= input("> ").strip()
        if mm not in ["1","2","3","4"]:
            mm="1"

        try:
            if mm=="1":
                root,iters= bisection(f,a,b, eps=eps)
            elif mm=="2":
                root,iters= secant(f,a,b, eps=eps)
            elif mm=="3":
                x0= (a+b)/2
                root,iters= newton_method(f, df, x0, eps=eps)
            else:
                ok,mv= check_single_iter_convergence(f, df, a,b, alpha=0.01)
                if not ok:
                    print(f"Внимание: max|phi'(x)|={mv:.3f}>=1 => может не сойтись. Продолжить? (y/n)")
                    c2= input("> ").strip().lower()
                    if c2!="y":
                        return
                x0= (a+b)/2
                root,iters= simple_iteration(f, df, a,b, x0, eps=eps, alpha=0.01)
        except Exception as e:
            print("Ошибка вычисления:", e)
            return

        fx= f(root)
        output_root(root, fx, iters)

        print("Построить график f(x) на [a,b]? (y/n)")
        ga= input("> ").strip().lower()
        if ga=="y":
            plot_function(f,a,b)

    elif choice=="2":
        print("Выберите систему:")
        for key,info in SYSTEMS.items():
            print(f"{key}) {info['name']}")
        sch= input("> ").strip()
        if sch not in SYSTEMS:
            sch="1"
        sys_data= SYSTEMS[sch]
        F1= sys_data["F1"]
        F2= sys_data["F2"]
        dF1dx= sys_data["dF1dx"]
        dF1dy= sys_data["dF1dy"]
        dF2dx= sys_data["dF2dx"]
        dF2dy= sys_data["dF2dy"]
        print(f"Выбрана:", sys_data["name"])

        print("Построить график F1=0, F2=0 сейчас? (y/n)")
        ga= input("> ").strip().lower()
        if ga=="y":
            print("Введите x_min,x_max (напр. -3 3):")
            line1= input("> ").strip()
            xm_str,xM_str= line1.split()
            x_min,x_max= float(xm_str), float(xM_str)

            print("Введите y_min,y_max (напр. -3 3):")
            line2= input("> ").strip()
            ym_str,yM_str= line2.split()
            y_min,y_max= float(ym_str), float(yM_str)

            plot_system(F1,F2, x_min,x_max,y_min,y_max)

        print("Откуда брать x0,y0,eps? (1 - клавиатура, 2 - файл)")
        ans= input("> ").strip()
        if ans=="2":
            x0,y0,eps= read_xy_eps_file("input_system.txt")
            if x0 is None:
                print("Не удалось прочесть, переходим к клавиатуре.")
                x0,y0,eps= read_xy_eps_keyboard()
        else:
            x0,y0,eps= read_xy_eps_keyboard()

        print("Метод? (6 - Ньютона, 7 - итерация)")
        mm= input("> ").strip()
        if mm not in ["6","7"]:
            mm="6"

        try:
            if mm=="6":
                X,Y,iters= newton_system(F1,F2, dF1dx,dF1dy,dF2dx,dF2dy,
                                         x0,y0, eps=eps)
            else:
                print("Для проверки итерации укажите [x_min,x_max,y_min,y_max], напр. -3 3 -3 3")
                line3= input("> ").strip()
                xmi_str,xma_str, ymi_str,yma_str= line3.split()
                xmi,xma= float(xmi_str), float(xma_str)
                ymi,yma= float(ymi_str), float(yma_str)

                ok, val= check_system_iter_convergence(dF1dx,dF1dy, dF2dx,dF2dy,
                                                      xmi,xma, ymi,yma,
                                                      alpha=0.01)
                if not ok:
                    print(f"Внимание: max row-sum={val:.3f}>=1 => может не сойтись. Продолжить? (y/n)")
                    c2= input("> ").strip().lower()
                    if c2!="y":
                        return

                X,Y,iters= simple_iter_system(F1,F2, x0,y0, alpha=0.01, eps=eps)

            output_system_solution(X,Y, iters, F1,F2)

        except Exception as e:
            print("Ошибка при решении системы:", e)

    else:
        print("Неверный выбор. Завершаем.")

if __name__=="__main__":
    main()
