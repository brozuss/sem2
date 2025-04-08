_N_DLA_SITA = 2
_WYNIK_SITA = [2]
_SITO = [None, None, 2]
def sito_eratostenesa_cache(N):
    global _N_DLA_SITA
    global _WYNIK_SITA
    global _SITO
    if N == _N_DLA_SITA:
        return _WYNIK_SITA.copy()
    elif N < _N_DLA_SITA:
        return [x for x in _WYNIK_SITA if x<=N]
    _SITO += list(range(_N_DLA_SITA+1, N+1))
    for p in _SITO:
        if p is None:
            continue
        if p*p > N:
            break
        for x in range(max(p, (_N_DLA_SITA//p+1))*p, N+1, p):
            _SITO[x] = None
    _WYNIK_SITA = [x for x in _SITO if x is not None]
    _N_DLA_SITA = N
    return _WYNIK_SITA.copy()



def przyjaciele(n):
    sito_eratostenesa_cache(n)

przyjaciele(1000)