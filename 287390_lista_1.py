import random
import string
from time import perf_counter
from itertools import repeat
import gc
import matplotlib.pyplot as plt
import math
import numpy as np

# zadanie 1

## Funkcje szukania

### Wersja z petla for przez indeks
def minimum_for_index(lista):
    minelem = lista[0]
    if lista:
        for i in range(len(lista) - 1):
            if lista[i+1] < minelem:
                minelem = lista[i+1]
        return minelem
    else: return None

### Wersja z petla for przez element
def minimum_for_element(lista):
    minelem = lista[0]
    if lista:
        for i in lista:
            if i < minelem:
                minelem = i
        return minelem
    else: return None

### Wersja z petla for pomijajac pierwszy index w petli
def minimum_for(lista):
    minelem = lista[0]
    if lista:
        for i in lista[1:]:
            if i < minelem:
                minelem = i
        return minelem
    else: return None

### Wersja z petla while
def minimum_while(lista):
    if lista:
        minelem = lista[0]
        n = 1
        while n < len(lista):
            if lista[n] < minelem:
                minelem = lista[n]
            n += 1
        return minelem
    else: return None


## Generatory
### Listy liczb
def gen_liczby(length):
    return [random.randint(0, 1000) for _ in range(length)]

### Losowe znaki z alfabetu
def gen_alfabet(length, string_length=6):
    return [''.join(random.choices(string.ascii_letters, k=string_length)) for _ in range(length)]

### A-5%, B-95%
def gen_AB(length, string_length=6):
    return [''.join(random.choices(['A', 'B'], weights=[95, 5], k=string_length)) for _ in range(length)]


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

def test(generator=gen_liczby):
    # dlugosc list do testow
    list_lengths = [10, 100, 1000, 10000]

    ## wyniki
    ###liczby
    results = {'minimum_for_index': [],
               'minimum_for_element': [],
               'minimum_for': [],
               'minimum_while': []
               }
    for func in results:
        for length in list_lengths:
            gen_list = eval(func)(generator(length))
            czas = zmierz_raz(gen_list)
            results[func].append(czas)
    print(results)

    ## plot
    plt.figure(figsize=(10, 6))
    for func_name, czasy in results.items():
        plt.plot(list_lengths, czasy, label=func_name, marker='o')

    plt.autoscale(enable=True, axis='y')
    plt.xlabel('Długość listy')
    plt.ylabel('Czas wykonania (s)')
    plt.title(f'Czas wykonania funkcji w zależności od długości listy {generator.__name__} i wykorzystanej pętli')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')

    plt.show()


# ZADANIE 2
def bisekcja(f, a, b, tolerancja=1e-6):
    c = (a+b)/2
    pol_dlugosci = (b-a)/2
    if pol_dlugosci <= tolerancja:
        return c
    f_a = f(a) - 1
    while pol_dlugosci > tolerancja:
        f_c = f(c) - 1
        if f_a*f_c < 0:
            b = c
        elif f_a*f_c > 0:
            a = c
            f_a = f_c
        else:
            return c
        pol_dlugosci /= 2
        c = (a+b)/2
    return c

def test2(funkcja):
    results = {}
    for i in range(100):
        n = 10 * (i+1)
        results[10*n] = zmierz_min(bisekcja(funkcja, 0, n))
        print(n)

    print(results)
    plt.figure(figsize=(10, 6))
    for przedzial, czasy in results.items():
        plt.plot(przedzial, czasy, label=przedzial, marker='o')

    plt.autoscale(enable=True, axis='both')
    plt.xlabel('Przedział 0-')
    plt.ylabel('Czas wykonania (s)')
    plt.title(f'Czas znalezienia miejsca zerowego w zależnosci od przedziału')
    plt.grid(True)
    plt.show()

# ZADANIE 3
def sasiedztwo(A, r, i, j):
    m, n = np.shape(A)
    lim_dol = min(m, i+r+1)
    lim_gora = max(0, i-r)
    lim_prawo = min(n, j+r+1)
    lim_lewo = max(0, j-r)
    return A[lim_gora:lim_dol, lim_lewo:lim_prawo]

def maksima_lokalne(A):
    maxima = []
    m, n = np.shape(A)
    for i in range(m):
        for j in range(n):
            sasiedzi = sasiedztwo(A, 1, i, j)
            if A[i,j] >= np.max(sasiedzi):
                maxima.append([i, j])
    return maxima

def czy_jednomodalna(A):
    return len(maksima_lokalne(A)) == 1

if __name__ == '__main__':
    ## WYWOŁANIA ZADANIE 1
    '''lista generatorow:
        - gen_liczby
        - gen_alfabet
        - gen_AB
    '''
    # test(gen_AB)
    # test(gen_liczby)
    # test(gen_alfabet)

    ## WYWOŁANIA ZADANIE 2
    # test2(math.atan)

    ## WYWOŁANIE ZADANIE 3
    A = np.matrix('1,2,3,4; 5,6,5,6; 2,2,3,4')
    # print(czy_jednomodalna(A))