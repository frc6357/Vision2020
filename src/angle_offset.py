def find_deg(input, w, d):
    x_val = input[0][0]

    print(x_val, "x_val")

    px = (x_val - w/2)
    print(px, "difference img width and x_val")

    px = px * 19.625/d

    return px
