import prettytable
import math


class Element:
    def __init__(self, power, coefficient):
        self.power = power
        self.coefficient = coefficient

    def multiply(self, other):
        result = Element(0, 0)
        result.power = self.power + other.power
        result.coefficient = self.coefficient * other.coefficient

        return result

    def add(self, other):
        if self.power != other.power:
            return None
        else:
            self.coefficient += other.coefficient
            return self

    def take_integral(self):
        self.power += 1
        self.coefficient /= self.power

    def __str__(self):
        return str(self.coefficient) + "x^" + str(self.power)


def contains_power(array, value):
    for elem in array:
        if elem.power == value.power:
            return elem
    return None


def add_similar(array):
    result = []
    for elem in array:
        addition_elem = contains_power(result, elem)
        if addition_elem is not None:
            addition_elem.add(elem)
        else:
            result.append(elem)

    return result


def find_coefficients_for_power_of_2(array):
    result = []
    for elem1 in array:
        for elem2 in array:
            result.append(elem1.multiply(elem2))
    result = add_similar(result)

    return result


def take_integral(array):
    for elem in array:
        elem.take_integral()


def find_coefficients_for_level(level):
    if level < 1:
        return None

    array = [Element(3, 1/3)]
    for i in range(1, level):
        array = find_coefficients_for_power_of_2(array)
        array.append(Element(2, 1))
        take_integral(array)
    return array


def main():
    min_level = 3
    max_level = 10

    min_x = 0
    steps = 200

    h = 1e-2

    coefficients = []

    for i in range(min_level, max_level):
        coefficients.append(find_coefficients_for_level(i))

    current_x = min_x
    x = []

    explicit_current = 0
    non_explicit_current = 0

    linar = [[] for c in coefficients]

    explicit = []
    non_explicit = []

    for i in range(steps):
        x.append(current_x)
        for i in range(len(coefficients)):
            value = 0
            for elem in coefficients[i]:
                value += elem.coefficient * current_x**elem.power
            linar[i].append(value)

        explicit.append(explicit_current)
        non_explicit.append(non_explicit_current)

        explicit_current += h * (current_x**2 + explicit_current**2)
        current_x += h

        if non_explicit_current is not None:
            D = 1 - 4 * h * (non_explicit_current + h * current_x**2)
            if D < 0:
                non_explicit_current = None
            else:
                non_explicit_current = 1 - math.sqrt(D)
                non_explicit_current /= 2 * h

    table = prettytable.PrettyTable()
    table.add_column("x", x)
    for i in range(len(linar)):
        table.add_column("Линар " + str(i + min_level) + "-ое", linar[i])
    table.add_column("Лом. явный", explicit)
    table.add_column("Лом. неявный", non_explicit)

    table.float_format = "6.5"

    print(table)


if __name__ == "__main__":
    main()