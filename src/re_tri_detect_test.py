triangles = []
first, second = [-2.050228310502283, 1108.9497716894978], [-2.053714285714286, 1096.6777142857143]

m1 = first[0]
b1 = first[1]
m2 = second[0]
b2 = second[1]
if (m1 == m2):
    triangles = None

else:
    x = (b2-b1)/(m1-m2)
    y = m1*x +b1
    if (x < 0):
        triangles = None
    elif (y < 0):
        triangles = None
    else:
        triangles = (int(x), int(y))
if triangles[0] <= 640 and triangles[1] <= 480:
    print("intersection in image")
    print(triangles)
    print(first, second)
else:
    print("not in image")
    print(first, second)


