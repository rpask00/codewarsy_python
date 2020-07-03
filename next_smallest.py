def next_smaller(n):
  s = list(map(int, str(n)))
  # The first loop looks for the right-most digit that has a higher digit in the left part of the number.
  for i in range(1, len(s)+1):
    a = s[-i]
    if any([j > a for j in s[:-i]]):
      # When found, this digit is 'a'.
      # Next step is to find the index of the first digit higher than 'a', when parsing from 'a' towards left.
      k = [c for c, d in enumerate(s[:-i]) if d > a][-1]
      # Taking care next line of the cases resulting on solutions with '0' as first digit
      if a == 0 and k == 0:
        break
      # Then we can build the answer as follow :
      # first the head of our number until one digit before j,
      # then a,
      # then the rest of the right part digits less 'a', sorted inverse
      return ''.join(map(str, s[:k]+[a]+sorted(s[k:-i]+s[-i:][1:])[::-1]))
  return -1


print(next_smaller(135))
print(next_smaller(907))
print(next_smaller(531))
print(next_smaller(2071))
print(next_smaller(414))
print(next_smaller(123456798))
print(next_smaller(123456789))
print(next_smaller(1234567908))
print(next_smaller(2626147538312233456678))
print('done')
