def divide(a, b):
    return a / b


def get_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)


def find_item(items, target):
    for i in range(len(items)):
        if items[i] == target:
            return i
    return None


print(divide(10, 0))
print(get_average([]))
print(find_item([1, 2, 3], 5))
