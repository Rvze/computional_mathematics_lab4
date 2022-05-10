from cmath import sqrt, log, exp


def solve_minor(matrix, i, j):
    n = len(matrix)
    return [[matrix[row][col] for col in range(n) if col != j] for row in range(n) if row != i]


def solve_det(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sgn = 1
    for j in range(n):
        det += sgn * matrix[0][j] * solve_det(solve_minor(matrix, 0, j))
        sgn *= -1
    return det


def calc_s(dots, f):
    n = len(dots)
    x = [dot[0] for dot in dots]
    y = [dot[1] for dot in dots]
    return sum([(f(x[i]) - y[i]) ** 2 for i in range(n)])


def calc_stdev(coords, f):
    n = len(coords)
    return sqrt(calc_s(coords, f) / n)


def lin_appr(coords):
    data = {}
    n = len(coords)
    x = [dot[0] for dot in coords]
    y = [dot[1] for dot in coords]

    sum_x = sum(x)
    sum_x2 = sum([x[i] ** 2 for i in range(n)])
    sum_y = sum(y)
    sum_x_y = sum([x[i] * y[i] for i in range(n)])

    det = solve_det([[sum_x2, sum_x],
                     [sum_x, n]])
    det_a = solve_det([[sum_x_y, sum_x],
                       [sum_y, n]])
    det_b = solve_det([[sum_x2, sum_x_y],
                       [sum_x, sum_y]])

    try:
        a = det_a / det
        b = det_b / det
    except ZeroDivisionError:
        return None
    data["a"] = a
    data["b"] = b
    f = lambda z: a * z + b

    data['func'] = f

    data['str_func'] = "a*x + b"

    data['s'] = calc_s(coords, f)

    data['stdev'] = calc_stdev(coords, f)
    data['pirson'] = solve_coeff_pirson(coords, f)

    return data


def pow_appr(coords):
    data = {"str_func": "a*x^2"}
    n = len(coords)
    x = []
    for i in coords:
        if i[0] <= 0:
            return None
        x.append(i[0])
    y = []
    for i in coords:
        if i[1] <= 0:
            return None
        y.append(i[1])
    lin_x = [log(x[i]) for i in range(n)]
    lin_y = [log(y[i]) for i in range(n)]
    lin_result = lin_appr([(lin_x[i], lin_y[i]) for i in range(n)])

    a = exp(lin_result['b'])
    b = lin_result['a']
    data['a'] = a
    data['b'] = b

    f = lambda z: a * (z ** b)
    data['func'] = f

    data['str_func'] = "a*x^b"

    data['s'] = calc_s(coords, f)

    data['stdev'] = calc_stdev(coords, f)
    data['pirson'] = solve_coeff_pirson(coords, f)

    return data


def log_appr(coords):
    data = {}

    n = len(coords)
    x = []
    y = []
    for dot in coords:
        if dot[0] <= 0:
            return None
        x.append(dot[0])
    for dot in coords:
        if dot[1] <= 0:
            return None
        y.append(dot[1])

    lin_x = [log(x[i]) for i in range(n)]
    lin_result = lin_appr([(lin_x[i], y[i]) for i in range(n)])

    a = lin_result['a']
    b = lin_result['b']
    data['a'] = a
    data['b'] = b

    f = lambda z: a * log(z) + b
    data['func'] = f

    data['str_func'] = "a*log(x) + b"

    data['s'] = calc_s(coords, f)

    data['stdev'] = calc_stdev(coords, f)
    data['pirson'] = solve_coeff_pirson(coords, f)

    return data


def exp_appr(coords):
    data = {}

    n = len(coords)
    x = [dot[0] for dot in coords]
    y = []
    for dot in coords:
        if dot[1] <= 0:
            return None
        y.append(dot[1])

    lin_y = [log(y[i]) for i in range(n)]
    lin_result = lin_appr([(x[i], lin_y[i]) for i in range(n)])

    a = exp(lin_result['b'])
    b = lin_result['a']
    data['a'] = a
    data['b'] = b

    f = lambda z: a * exp(b * z)
    data['func'] = f

    data['str_func'] = "a*e^(b*x)"

    data['s'] = calc_s(coords, f)

    data['stdev'] = calc_stdev(coords, f)
    data['pirson'] = solve_coeff_pirson(coords, f)

    return data


def sqrt_appr(coords):
    data = {}

    n = len(coords)
    x = [dot[0] for dot in coords]
    y = [dot[1] for dot in coords]

    sx = sum(x)
    sx2 = sum([xi ** 2 for xi in x])
    sx3 = sum([xi ** 3 for xi in x])
    sx4 = sum([xi ** 4 for xi in x])
    sy = sum(y)
    sxy = sum([x[i] * y[i] for i in range(n)])
    sx2y = sum([(x[i] ** 2) * y[i] for i in range(n)])

    d = solve_det([[n, sx, sx2],
                   [sx, sx2, sx3],
                   [sx2, sx3, sx4]])
    d1 = solve_det([[sy, sx, sx2],
                    [sxy, sx2, sx3],
                    [sx2y, sx3, sx4]])
    d2 = solve_det([[n, sy, sx2],
                    [sx, sxy, sx3],
                    [sx2, sx2y, sx4]])
    d3 = solve_det([[n, sx, sy],
                    [sx, sx2, sxy],
                    [sx2, sx3, sx2y]])

    try:
        c = d1 / d
        b = d2 / d
        a = d3 / d
    except ZeroDivisionError:
        return None
    data['c'] = c
    data['b'] = b
    data['a'] = a

    f = lambda z: a * (z ** 2) + b * z + c
    data['func'] = f

    data['str_func'] = "a*x^2 + b*x + c"

    data['s'] = calc_s(coords, f)

    data['stdev'] = calc_stdev(coords, f)
    data['pirson'] = solve_coeff_pirson(coords, f)

    return data


def pol_3_appr(coords):
    data = {}

    n = len(coords)
    x = [i[0] for i in coords]
    y = [i[1] for i in coords]

    s_x = sum(x)
    s_x2 = sum([xi ** 2 for xi in x])
    s_x3 = sum([xi ** 3 for xi in x])
    s_x4 = sum([xi ** 4 for xi in x])
    s_x5 = sum([xi ** 5 for xi in x])
    s_x6 = sum([xi ** 6 for xi in x])
    s_y = sum(y)
    s_xy = sum([x[i] * y[i] for i in range(n)])
    s_x2y = sum([(x[i] ** 2) * y[i] for i in range(n)])
    s_x3y = sum([(x[i] ** 3) * y[i] for i in range(n)])

    d = solve_det([[n, s_x, s_x2, s_x3],
                   [s_x, s_x2, s_x3, s_x4],
                   [s_x2, s_x3, s_x4, s_x5],
                   [s_x3, s_x4, s_x5, s_x6]])
    d1 = solve_det([[s_y, s_x, s_x2, s_x3],
                    [s_xy, s_x2, s_x3, s_x4],
                    [s_x2y, s_x3, s_x4, s_x5],
                    [s_x3y, s_x4, s_x5, s_x6]])
    d2 = solve_det([[n, s_y, s_x2, s_x3],
                    [s_x, s_xy, s_x3, s_x4],
                    [s_x2, s_x2y, s_x4, s_x5],
                    [s_x3, s_x3y, s_x5, s_x6]])
    d3 = solve_det([[n, s_x, s_y, s_x3],
                    [s_x, s_x2, s_xy, s_x4],
                    [s_x2, s_x3, s_x2y, s_x5],
                    [s_x3, s_x4, s_x3y, s_x6]])
    d4 = solve_det([[n, s_x, s_x2, s_y],
                    [s_x, s_x2, s_x3, s_xy],
                    [s_x2, s_x3, s_x4, s_x2y],
                    [s_x3, s_x4, s_x5, s_x3y]])

    try:
        a = d4 / d
        b = d3 / d
        c = d2 / d
        q = d1 / d
    except ZeroDivisionError:
        return "Деление на ноль!"

    data['a'] = a
    data['b'] = b
    data['c'] = c
    data['d'] = q

    f = lambda z: a * (z ** 3) + b * (z ** 2) + c * z + q

    data['func'] = f
    data['str_func'] = "ax**3 + bx**2 + c*x + d"
    data['s'] = calc_s(coords, f)
    data['stdev'] = calc_stdev(coords, f)
    data['pirson'] = solve_coeff_pirson(coords, f)

    return data


def solve_coeff_pirson(coords, f):
    n = len(coords)
    x = [i[0] for i in coords]
    y = [i[1] for i in coords]

    av_x = sum(x) / n
    av_y = sum(y) / n

    sum_x_y = sum([(x[i] - av_x) * ((y[i]) - av_y) for i in range(n)])
    sum_x_y_sqrt = sqrt(sum([(x[i] - av_x) ** 2 for i in range(n)]) * sum([((y[i]) - av_y) ** 2 for i in range(n)]))

    return sum_x_y / sum_x_y_sqrt
