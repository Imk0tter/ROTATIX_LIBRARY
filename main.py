from rotatix_util import *

import rotatix

# entry point
sides = 50
rotations = (1.5, 3, 7)

print("Sides: " + str(sides))
print("Rotations: " + str(rotations))
print("")
result = sides_and_rotations_to_degrees_per_radian_and_degrees(sides, *rotations)

print("degrees_per_radian: " + str(result[0]))
print("degrees_per_iteration: " + str(result[1]))
radians_per_iteration = degrees_per_radian_and_degrees_per_iteration_to_radians_per_iteration(result[0], *result[1])
print("radians_per_iteration: " + str(radians_per_iteration))
print("")

result = rectify_degrees_per_radian_and_degrees_per_iteration(result[0], *result[1])
print("     degrees_per_radian_rectified: " + str(result[0]))
print("     degrees_per_iteration_rectified: " + str(result[1]))
radians_per_iteration = degrees_per_radian_and_degrees_per_iteration_to_radians_per_iteration(result[0], *result[1])
print("     radians_per_iteration_rectified: " + str(radians_per_iteration))
print("")

degrees_per_radian = 7.977641522481254
degrees_per_iteration = (1.25, 2, 4, 6)

print("DEGREES_PER_RADIAN: " + str(degrees_per_radian))
print("DEGREES_PER_ITERATION: " + str(degrees_per_iteration))

result = rectify_degrees_per_radian_and_degrees_per_iteration(degrees_per_radian, *degrees_per_iteration)
radians_per_iteration = degrees_per_radian_and_degrees_per_iteration_to_radians_per_iteration(result[0], *result[1])

print("DEGREES_PER_RADIAN_RECTIFIED: " + str(result[0]))

print("GCD: " + str(gcd(result[0] * (math.pi * 2), 1)))
print("SIDES: " + str(result[0] * (math.pi * 2)))

print("DEGREES_PER_ITERATION_RECTIFIED: " + str(result[1]))
print("RADIANS_PER_ITERATION_RECTIFIED: " + str(radians_per_iteration))
print("")
sides = 123
rotations = (1, 2, 44, 7, 3)
lengths = (25, 50, 100, 25, 30)

rotatix_sketch = rotatix.Rotatix_Sketch(sides=sides, rotations=rotations, lengths=lengths)

#application = rotatix_application.Application.GetApplication(rotatix_sketch=rotatix_sketch)

#application.start()

#print("Exited!")

#print("SUM: 10000 = " + str(sum(range(10001))))
#print("SUM: 10000 = " + str(10000 / 2 * 10001))

import rotatix_game

rotatix_arcade = rotatix_game.Rotatix_Arcade(rotatix_sketch = rotatix_sketch)
rotatix_arcade.run()