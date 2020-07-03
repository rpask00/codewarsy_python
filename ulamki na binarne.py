def transform(dec, precision=20):
    binary = '0,'
    liczba = float(dec)
    dec = [int(d) for d in dec[2:]]

    for i in range(int(precision)):
        nextpoweroftwo = 2 ** (-(i + 1))

        if not liczba:
            return binary

        if liczba >= nextpoweroftwo:
            liczba -= nextpoweroftwo
            binary += '1'
        else:
            binary += '0'

    return binary


liczba = input('Podaj ułamek: ')
precision = input('Podaj dokładnośc (liczbe miejsc po przecinku): ')

print(transform(liczba, precision))

print(transform('0.65', 50))
