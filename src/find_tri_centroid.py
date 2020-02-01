def centroid(input):
    f, s, t = input[0], input[1], input[2]
    x1, y1 = f[0], f[1]
    x2, y2 = s[0], s[1]
    x3, y3 = t[0], t[1]
    cx = (x1 + x2 + x3) / 3
    cy = (y1 + y2 + y3) / 3
    return (int(cx), int(cy))