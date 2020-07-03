def countOnes(left, right):
    # Your code here!
    arr = []
    for i in range(left, right+1):
        arr.append("{0:b}".format(i))
    return sum([a.count('1') for a in arr])


print(countOnes(12, 29))
