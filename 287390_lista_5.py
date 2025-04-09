def zadanie_1():
    def koduj(napis, klucz=1):
        stripped = list(napis)
        zakodowane = []
        for i in napis:
            c = i
            n = ord(c) - ord('a')
            n += klucz
            print(n)
            m = chr(ord('a') + n)
            print(m)
            zakodowane.append(m)
        print(zakodowane)
    koduj('dzien dobry', 0)



if __name__ == '__main__':
    zadanie_1()