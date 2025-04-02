import matplotlib.pyplot as plt
import gc
from time import perf_counter
from itertools import repeat

def dzielniki(n):
    dzielniki_set = {1}
    for i in range(2, int(n*0.5 +1)):
        if n % i == 0:
            dzielniki_set.add(i)
            dzielniki_set.add(n // i)
    return sorted(dzielniki_set)

def zadanie_1():
    def czy_doskonala(n):
        if n < 2:
            return None
        dzielniki_lista = dzielniki(n)
        suma_dzielnikow = sum(dzielniki_lista)

        if suma_dzielnikow == n:
            return n

    def doskonale_list(n):
        doskonale = []
        for i in range(n):
            if czy_doskonala(i):
                doskonale.append(i)

        return doskonale

    print(doskonale_list(100))


def zadanie_2():
    def przyjaciele(n):
        pary = []
        sprawdzone = set()

        for a in range(2, n + 1):
            if a in sprawdzone:
                continue

            b = sum(dzielniki(a))
            if b != a and sum(dzielniki(b)) == a:
                pary.append((a, b))
                sprawdzone.add(a)
                sprawdzone.add(b)

        return pary

    print(przyjaciele(10_000))

def zadanie_3():
    def sito_Sundarama(n):
            k = (n - 2) // 2
            sito = [True for _ in range(k + 1)]

            for i in range(1, k + 1):
                for j in range(1, k + 1):
                    mark = i + j + 2 * i * j
                    if mark <= k:
                        sito[mark] = False

            prime  = [2]
            for i in range(1, k + 1):
                if sito[i]:
                    prime.append(2*i + 1)

            # print(sito)
            # print(len(sito))
            # print(prime)


    def sito_Sundarama2(n):
        """Ograniczamy zakres (1), przez co możemy pozbyć się (2), główną różnicą będzie (1) - wykonamy zdecydowanie mniej iteracji"""

        k = (n - 2) // 2
        sito = [True for _ in range(k + 1)]

        for i in range(1, k):
            j_max = (k - i) // (2*i + 1)        #(1)
            for j in range(1, j_max + 1):           #(1)
                mark = i + j + 2 * i * j
                sito[mark] = False
                # if mark <= k:                 (2)
                #     sito[mark] = False        (2)

        prime = [2]
        for i in range(1, k):
            if sito[i]:
                prime.append(2 * i + 1)

    def sito_erastotenes(N):
        if N < 2:
            return []

        kandydaci = list(range(N))
        kandydaci[0] = None
        kandydaci[1] = None
        for x in kandydaci:
            if x is None:
                continue
            if x * x >= N:
                break
            for y in range(x * x, N, x):
                kandydaci[y] = None
        return [x for x in kandydaci if x is not None]


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

    def test():
        # dlugosc list do testow
        list_lengths = [10, 100, 1000, 10000]

        ## wyniki
        ###liczby
        results = { sito_Sundarama: [],
                    sito_Sundarama2: [],
                    sito_erastotenes: [],
                   }
        for func in results:
            for length in list_lengths:
                czas = zmierz_raz(func(length))
                results[func].append(czas)
        print(results)

        ## plot
        plt.figure(figsize=(10, 6))
        for func, czasy in results.items():
            func_name = func.__name__

            plt.plot(list_lengths, czasy, label=func_name, marker='o')

        plt.autoscale(enable=True, axis='y')
        plt.xlabel('Długość listy')
        plt.ylabel('Czas wykonania (s)')
        plt.title(f'Czas szukania liczb pierwszych zależnie od sposobu')
        plt.legend()
        plt.grid(True)
        plt.xscale('log')

        plt.show()

    test()


if __name__ == '__main__':
    zadanie_1()
    # zadanie_2()
    # zadanie_3()