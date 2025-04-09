from random import seed, randrange, setstate, getstate, shuffle
from time import perf_counter
from itertools import repeat
import gc

def sortowanie_bąbelkowe(lista, relacja=lambda x, y: x <= y):
    n = len(lista)
    dalej = True
    i = 0
    while dalej:
        dalej = False
        for j in range(n - 1 - i):
            if not relacja(lista[j], lista[j + 1]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                dalej = True
        i += 1


def sortowanie_wstawianie(lista, relacja=lambda x, y: x <= y):
    for i in range(1, len(lista)):
        li = lista[i]
        j = i
        while j > 0 and not relacja(lista[j - 1], li):
            lista[j] = lista[j - 1]
            j -= 1
        lista[j] = li


def sortowanie_wybieranie(lista, relacja=lambda x, y: x <= y):
    n = len(lista)
    for i in range(n - 1):
        j = i
        for k in range(i + 1, n):
            if not relacja(lista[j], lista[k]):
                j = k
        if j != i:
            lista[i], lista[j] = lista[j], lista[i]


def sortowanie_scalanie(lista, relacja=lambda x, y: x <= y):
    def scal(lista1, lista2):
        wynik = []
        n1 = len(lista1)
        n2 = len(lista2)
        i1 = 0
        i2 = 0
        while i1 < n1 and i2 < n2:
            if relacja(lista1[i1], lista2[i2]):
                wynik.append(lista1[i1])
                i1 += 1
            else:
                wynik.append(lista2[i2])
                i2 += 1
        return wynik + lista1[i1:] + lista2[i2:]

    n = len(lista)
    if n <= 1:
        return lista.copy()
    k = n // 2
    l1, l2 = lista[:k], lista[k:]
    l1 = sortowanie_scalanie(l1)
    l2 = sortowanie_scalanie(l2)
    return scal(l1, l2)

def zmierz_raz_sortowanie(algorytm, lista, min_time=0.2):
    czas = 0
    ile_teraz = 1
    stan_gc = gc.isenabled()
    gc.disable()
    while czas < min_time:
        kopie_list = [lista.copy() for _ in repeat(None, ile_teraz)]
        if ile_teraz == 1:
            start = perf_counter()
            algorytm(kopie_list.pop())
            stop = perf_counter()
        else:
            iterator = repeat(None, ile_teraz)
            start = perf_counter()
            for _ in iterator:
                algorytm(kopie_list.pop())
            stop = perf_counter()
        czas = stop - start
        ile_teraz *= 2
    if stan_gc:
        gc.enable()
    return czas / ile_teraz


def zmierz_min_sortowanie(algorytm, lista, serie_min=5, min_time=0.2):
    pomiary = []
    generator = getstate()
    seed()
    my_seed = randrange(1000)
    for _ in repeat(None, serie_min):
        seed(my_seed)
        pomiary.append(zmierz_raz_sortowanie(algorytm, lista, min_time=min_time))
    setstate(generator)
    return min(pomiary)


def zmierz_sortowanie(algorytm, lista, serie_median=10, serie_min=5, min_time=0.2):
    pomiary = []
    lista = lista.copy()
    for _ in repeat(None, serie_median):
        shuffle(lista)
        pomiary.append(zmierz_min_sortowanie(algorytm, lista, serie_min=serie_min, min_time=min_time))
    pomiary.sort()
    if serie_median % 2 == 0:
        return (pomiary[serie_median // 2 - 1] + pomiary[serie_median // 2]) / 2
    else:
        return pomiary[serie_median // 2]