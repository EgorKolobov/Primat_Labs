from math import sin, log, sqrt


def f(x: float):
    return sin(x)*x**3


def dichotomy(a: float, b: float, epsilon: float):
    if a > b:
        return None
    if b-a < epsilon:
        return b
    sigma = 0.1*epsilon/2
    x1 = (a+b)/2-sigma
    x2 = (a+b)/2+sigma
    if f(x1) < f(x2):
        return dichotomy(a, x2, epsilon)
    elif f(x1) > f(x2):
        return dichotomy(x1, b, epsilon)
    else:
        return dichotomy(x1, x2, epsilon)


def gold(a: float, b: float, epsilon: float):
    if a > b:
        return None
    if b-a < epsilon:
        return b
    # x1 = a + ((sqrt(5)-1)/2)*(b-a)
    # x2 = b - ((sqrt(5)-1)/2)*(b-a)
    x1 = a + ((3-sqrt(5))/2)*(b-a)
    x2 = b - ((3-sqrt(5))/2)*(b-a)
    if f(x1) < f(x2):
        return gold(a, x2, epsilon)
    elif f(x1) > f(x2):
        return gold(x1, b, epsilon)
    else:
        return gold(x1, x2, epsilon)


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


print("Ответ:", dichotomy(2, 10, 1))
print("Ответ:", gold(-10, -2, 0.00005))
print("Ответ:", fibonacci_method(-1, 1, 0.5))
print("Ответ:", parabola_method(2, 10, 0.5))
