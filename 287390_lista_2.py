import math
import random
from time import perf_counter
from itertools import repeat
import matplotlib.pyplot as plt
import gc

## zadanie 1
def Newton_rekurencja(n, k):
    if n == k or k == 0:
        return 1
    else:
        return Newton_rekurencja(n-1,k-1) + Newton_rekurencja(n-1,k)

def Newton_iteracja(n, k):
    tp = [[1 if p==0 else 0 for p in range(k+1)] for _ in range(n+1)]

    for i in range(n):
        for j in range(1, k+1):
            poprz = tp[i][j-1]
            akt = tp[i][j]
            tp[i+1][j] = poprz + akt

    return tp[n][k]


def Newton_silnia(n, k):
    n_fact = math.factorial(n)
    k_fact = math.factorial(k)
    n_subt_k_fact = math.factorial(n-k)

    return int(n_fact/(n_subt_k_fact*k_fact))


## Mierzenie czasu
def zmierz_raz(f, min_time=0.2):
    czas = 0
    ile_teraz = 1
    stan_gc = gc.isenabled()
    gc.disable()

    while czas < min_time:
        if ile_teraz == 1:
            start = perf_counter()
            f
            stop = perf_counter()
        else:
            iterator = repeat(None, ile_teraz)
            start = perf_counter()
            for _ in iterator:
                f
            stop = perf_counter()

        czas = stop - start
        ile_teraz *= 2

    if stan_gc:
        gc.enable()

    return czas / ile_teraz

def zmierz_min(f, serie_min=5, min_time=0.2):
    pomiary = []
    generator = random.getstate()
    random.seed()
    my_seed = random.randrange(1000)
    for _ in repeat(None, serie_min):
        random.seed(my_seed)
        pomiary.append(zmierz_raz(f, min_time=min_time))
    random.setstate(generator)
    return min(pomiary)

## ZADANIE 2
def xgcd(a, b):
    '''a*x + b*y = gcd(a, b)'''
    if b == 0:
        return (a, 1, 0)
    else:
        (gcd, x_prim, y_prim) = xgcd(b, a % b)

    return (gcd, y_prim, x_prim - a // b * y_prim)

def diofantyczne_ma_rozwiazanie(a, b, c):
    gcd = xgcd(a, b)[0]
    if c % gcd == 0:
        return True
    else:
         return False

def diofantyczne_rozwiazanie(a, b, c):
    if diofantyczne_ma_rozwiazanie(a, b, c):
        gcd, xp, yp = xgcd(a, b)
        x = (xp * c) / gcd
        y = (yp * c) / gcd

        return x, y


if __name__ == '__main__':
    def zadanie_1():
        time_res = {'Newton_silnia':[], 'Newton_iteracja':[], 'Newton_rekurencja':[]}
        n_params = [x for x in range(50, 100)]
        k_params = [x for x in range(0, 50)]

        for func in time_res:
            for i  in range(len(n_params)):
                gen_list = eval(func)(n_params[i], k_params[i])
                czas = zmierz_raz(gen_list)
                time_res[func].append(czas)
        print(time_res)

    ## plot
        plt.figure(figsize=(10, 6))
        for func_name, czasy in time_res.items():
            plt.plot(n_params, czasy, label=func_name, marker='o')

        plt.autoscale(enable=True, axis='both')
        plt.xlabel('parametry')
        plt.ylabel('Czas wykonania (s)')
        plt.title(f'Czas wykonania funkcji ')
        plt.legend()
        plt.grid(True)

        plt.show()

    def zadanie_2():
        print(diofantyczne_ma_rozwiazanie(18, 16, 500))
        print(diofantyczne_rozwiazanie(18, 16, 500))

    # zadanie_1()
    zadanie_2()