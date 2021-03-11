from math import sin, log, sqrt
from numpy import sign
from scipy.optimize import minimize_scalar


def f(x: float):
    return sin(x)*x**3


def dichotomy_method(a: float, b: float, epsilon: float):
    if a > b:
        return None
    if b-a < epsilon:
        return b
    sigma = 0.1*epsilon/2
    x1 = (a+b)/2-sigma
    x2 = (a+b)/2+sigma
    if f(x1) < f(x2):
        return dichotomy_method(a, x2, epsilon)
    elif f(x1) > f(x2):
        return dichotomy_method(x1, b, epsilon)
    else:
        return dichotomy_method(x1, x2, epsilon)


def golden_ratio_method(a: float, b: float, epsilon: float):
    if a > b:
        return None
    if b-a < epsilon:
        return b
    # x1 = a + ((sqrt(5)-1)/2)*(b-a)
    # x2 = b - ((sqrt(5)-1)/2)*(b-a)
    x1 = a + ((3-sqrt(5))/2)*(b-a)
    x2 = b - ((3-sqrt(5))/2)*(b-a)
    if f(x1) < f(x2):
        return golden_ratio_method(a, x2, epsilon)
    elif f(x1) > f(x2):
        return golden_ratio_method(x1, b, epsilon)
    else:
        return golden_ratio_method(x1, x2, epsilon)


def fib(n: int):
    return 1/sqrt(5)*(((sqrt(5)+1)/2)**n - ((1-sqrt(5))/2)**n)


def fibonacci_submethod(a: float, b: float, epsilon: float, fib_n, fib_n1, fib_n2):
    if a > b:
        return None
    if b-a < epsilon:
        return b
    x1 = a+fib_n/fib_n2*(b-a)
    x2 = a+fib_n1/fib_n2*(b-a)
    if f(x1) < f(x2):
        return fibonacci_submethod(a, x2, epsilon, fib_n, fib_n1, fib_n2)
    elif f(x1) > f(x2):
        return fibonacci_submethod(x1, b, epsilon, fib_n, fib_n1, fib_n2)
    else:
        return fibonacci_submethod(x1, x2, epsilon, fib_n, fib_n1, fib_n2)


def fibonacci_method(a0: float, b0: float, epsilon: float):
    n = 0
    while (b0-a0)/epsilon >= fib(n+2):
        n += 1
    fib_n = fib(n)
    fib_n1 = fib(n+1)
    fib_n2 = fib(n+2)
    return fibonacci_submethod(a0, b0, epsilon, fib_n, fib_n1, fib_n2)


def parabola_submethod(a: float, b: float, epsilon: float, f1: float, f3: float):
    if a > b:
        return None
    if b-a < epsilon:
        return b
    x = (a+b)/2
    f2 = f(x)
    # if not(f2 < f1 and f2 < f3):
    #     return None
    u = x-((x-a)**2 * (f2-f3) - (x-b)**2 * (f2-f1))/(2*((x-a) * (f2-f3) - (x-b) * (f2-f1)))
    left = min(u, x)  # u
    right = max(u, x)  # x
    fl, fr = 0, 0
    if left == u:
        fl = f(u)
        fr = f2
    else:
        fl = f2
        fr = f(u)
    if f(left) < f(right):
        return parabola_submethod(a, right, epsilon, f1, fr)
    elif f(left) > f(right):
        return parabola_submethod(left, b, epsilon, fl, f3)
    else:
        return parabola_submethod(left, right, epsilon, fl, fr)


def parabola_method(a: float, b: float, epsilon: float):
    return parabola_submethod(a, b, epsilon, f(a), f(b))


def Brent_combined_method(a: float, c: float, epsilon: float):
    K = (3-sqrt(5))/2
    x = (a + c)/2
    w = x
    v = x
    fx = f(x)
    fw = fx
    fv = fx
    d = c-a
    e = d
    # epsilon2 = epsilon/2
    while c-a >= epsilon:
        # print("c, a:", c, a)
        # print("x, w, v:", x, w, v)
        g = e  # e
        e = d
        parabola_fit = False
        if (x != w) and (x != v) and (w != v) and (fx != fw) and (fx != fv) and (fw != fv):
            print("PARABOLA")
            f_val = dict()
            f_val[x] = fx
            f_val[w] = fw
            f_val[v] = fv
            l = sorted([x, w, v])[0]
            m = sorted([x, w, v])[1]
            r = sorted([x, w, v])[2]
            f1, f2, f3 = f_val[l], f_val[m], f_val[r]
            u = m-((m-l)**2 * (f2-f3) - (m-r)**2 * (f2-f1))/(2*((m-l) * (f2-f3) - (m-r) * (f2-f1)))
            if u >= a+epsilon and u <= c-epsilon and abs(u-x) < g/2:
                print("parabola fit")
                d = abs(u-x)
                parabola_fit = True
        # else:
        if not parabola_fit:
            # print("not parabola fit")
            if x < (c-a)/2:
                u = x + K*(c - x)
                d = c - x
            else:
                u = x - K*(x - a)
                d = x - a
            if abs(u-x) < epsilon:
                # print("< epsilon")
                u = x + sign(u-x)*epsilon
        fu = f(u)
        if fu <= fx:
            # print("fu<=fx")
            if u >= x:
                a = x
            else:
                c = x
            v = w
            w = x
            x = u
            fv = fw
            fw = fx
            fx = fu
        else:
            if u >= x:
                # print("u>=x")
                c = u
            else:
                a = u
            # print("a,c =", a, c)
            if fu <= fw or w == x:
                v = w
                w = u
                fv = fw
                fw = fu
            elif fu <= fv or v == x or v == w:
                v = u
                fv = fu

    return c


print("Ответ:", dichotomy_method(2, 10, 0.01))
print("Ответ:", golden_ratio_method(2, 10, 0.01))
print("Ответ:", fibonacci_method(2, 10, 0.01))
print("Ответ:", parabola_method(2, 10, 0.01))
# print("Ответ:", minimize_scalar(f,  bounds=(2, 10), method='bounded').x)
print("Ответ:", Brent_combined_method(3, 6, 0.01))
