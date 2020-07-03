def find_position(num):
    for i in range(1, len(num)//2):
        top = num[:-i]
        prefix = num[-i:]

        word = prefix + top

        prefix = int(prefix)
        while int(word) <= int(num):
            word = str(prefix) + top
            prefix += 1

            f_word = word
            word = word + str(int(word)+1)

            if word.count(num):
                print(f_word)
                return calcutale_index(int(f_word)) + word.index(num)


# print(find_position('53635'))
# 1234567891011 12

def calcutale_index(n):
    i = 1
    index = 0
    first_n = n
    while n:
        n_str = str(n)
        div = 10**i
        if div > n:
            index += n * i
            n -= n % div
            return index

        index += div * i
        n -= div

        i += 1

    return index


# print(calcutale_index(99))
print(find_position('949225100'))
