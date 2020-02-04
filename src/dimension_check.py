def in_img(input, h, w):
    f, s, t = input

    point_1_in_img = f if f[0] <= w  and f[1] <= h else None
    point_2_in_img = s if s[0] <= w and s[1] <= h else None
    point_3_in_img = t if t[0] <= w and t[1] <= h else None

    return point_1_in_img, point_2_in_img, point_3_in_img
