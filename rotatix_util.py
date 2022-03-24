import math

def sides_and_rotations_to_unknown(sides, *rotations):
    degree_list = []
    for x in range(0, len(rotations)):
        degree_list.append((((math.pi * 2) * sides) / rotations[x]))
    return tuple(degree_list)

def sides_and_rotations_to_degrees(sides, *rotations):
    degree_list = []
    for x in range(0, len(rotations)):
        degree_list.append(sides / (360 / rotations[x]))
    return tuple(degree_list)

def gcd(*numbers):
    a = numbers[0]
    if len(numbers) <= 1:
        return a
    b = numbers[1]
    current = a % b
    next_numbers = []
    next_numbers.extend(numbers[2:])

    if current != 0:
        return gcd(b, current, *tuple(next_numbers))
    return gcd(b, *tuple(next_numbers))


def lcm(*numbers):
    if len(numbers) > 1:
        temp = list(numbers[2:])
        return lcm(numbers[0] * numbers[1] / gcd(numbers[0], numbers[1]), *tuple(temp))
    return numbers[0]

def sides_to_degrees_per_radian(degrees_per_rotation):
        return degrees_per_rotation / (math.pi * 2)

def sides_and_rotations_to_degrees_per_radian_and_degrees(degrees_per_rotation, *rotations):
    degrees_per_radian = sides_to_degrees_per_radian(degrees_per_rotation)
    degrees = []
    for x in range(0, len(rotations)):
        degrees.append(rotations[x])
    return (degrees_per_radian, tuple(degrees))

def degrees_per_radian_and_degrees_per_iteration_to_radians_per_iteration(degrees_per_radian, *degrees_per_iteration):
    radians_per_iteration = []

    for x in range(0, len(degrees_per_iteration)):
        radians_per_iteration.append(degrees_per_iteration[x] / degrees_per_radian)
    return tuple(radians_per_iteration)

def rectify_degrees_per_radian_and_degrees_per_iteration(degrees_per_radian, *degrees_per_iteration):
    divider = gcd(*degrees_per_iteration)

    degrees_per_radian /= divider
    degrees_per_iteration_ = []
    for x in range(0, len(degrees_per_iteration)):
        degrees_per_iteration_.append(math.trunc(degrees_per_iteration[x] / divider))

    return (degrees_per_radian, tuple(degrees_per_iteration_))
