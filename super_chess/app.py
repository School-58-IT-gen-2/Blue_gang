for i in range(100_000 + 1):
    x = i / 100_000
    if round(int(20 * x + 23), 3) == round(20 + 23 * x, 3):
        print(x)