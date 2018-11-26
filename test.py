def get_square(positive_number, precision):
    def next_x(x, positive_number):
        return 1 / 2 * (x + positive_number / x)

    max_number = len(str(positive_number)) * 10 ** 2

    x = max_number

    while round(x ** 2, 10) > positive_number:
        x = next_x(x, positive_number)

    print(round(x, precision))


for i in range(10, 21):
    get_square(i, 3)