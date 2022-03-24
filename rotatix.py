import rotatix_util

import math

class Rotatix_Arm:
    def __init__(self, child=None, rotations=1, length=50, color_in=[0, 0, 0], color_out=[0, 0, 0], draw=True, **kwargs):
        self.child = child
        self.length = length
        self.rotations = rotations
        self.color_in = color_in
        self.color_out = color_out
        self.draw = draw
    def rasterize(self, iteration=1, x=0, y=0, degrees_per_radian=1, **kwargs):
        current_x = (math.sin(((self.rotations / degrees_per_radian * iteration)) % (math.pi * 2)) * self.length) + x
        current_y = (math.cos(((self.rotations / degrees_per_radian * iteration)) % (math.pi * 2)) * self.length) + y

        return self.draw, self.color_in, self.color_out, current_x, current_y


class Rotatix_Sketch:
    def __str__(self):
        return "Sides: " + str(self.sides) + ", Rotations: " + str(self.rotations) + ", Lengths: " + str(self.lengths) + ", Degrees per radian: " + str(self.degrees_per_radian)

    def __init__(self, x=0, y=0, sides=360, rotations=(1), lengths=(100), **kwargs):
        self.sides = sides
        self.degrees_per_radian = rotatix_util.sides_to_degrees_per_radian(self.sides)

        self.rotations = rotations
        self.lengths = lengths

        self.arm = None

        self.arm_count = 0
        for x, y in zip(rotations, lengths):
            self.arm_count + self.arm_count + 1
            if self.arm_count == len(rotations) - 1:
                draw = True
            else:
                draw = False
            self.add_arm(Rotatix_Arm(length=(50,y)[y > 0], rotations=x, draw=draw))

    def rasterize_size(self):

        temp_arm = self.arm

        total_length = 0
        while temp_arm != None:
            total_length = total_length + temp_arm.length
            temp_arm = temp_arm.child
        return total_length, total_length

    def rasterize(self, iteration, x=0, y=0):
        temp_arm = self.arm

        result = []

        temp_arms = []
        while temp_arm != None:
            current_rasterization = temp_arm.rasterize(degrees_per_radian=self.degrees_per_radian, iteration=iteration, x=x, y=y)

            color_in = current_rasterization[1]
            color_out = current_rasterization[2]

            x = current_rasterization[3]
            y = current_rasterization[4]

            result.append(current_rasterization)
            temp_arm = temp_arm.child
        return tuple(result)

    def get_sides(self):
        return self.sides

    def add_arm(self, arm):
        temp_arm = self.arm

        if temp_arm == None:
            self.arm = arm
        else:
            while temp_arm != None:
                if temp_arm.child == None:
                    temp_arm.child = arm
                    break
                else:
                    temp_arm = temp_arm.child
        self.arm_count = self.arm_count + 1
    def remove_arm(self, position = 0):
        temp_arm = self.arm
        previous_arm = None
        for x in range(1, position):
            previous_arm = temp_arm
            temp_arm = temp_arm.child
        if previous_arm != None:
            previous_arm.child = temp_arm
        else:
            self.arm = temp_arm
        self.arm_count = self.arm_count - 1


# Testing
sides = 42
rotations = (1,3,5,2,1)
lengths=(50,25,100,50,25)

temp_sketch = Rotatix_Sketch(x=150, y=150, sides=42, rotations=rotations, lengths=lengths)

print("Sides: " + str(sides))
print("Rotations: " + str(rotations))
print("Lengths: " + str(lengths))
print("Degrees Per Radian: " + str(rotatix_util.sides_to_degrees_per_radian(sides)))
print("Size: " + str(temp_sketch.rasterize_size()))
print("")

print("=== PRINTING ITERATIONS ===")
for i in range(0, sides + 1):
    print("ITERATION: " + str(i))
    result = temp_sketch.rasterize(i)
    arm_number = 1
    for r in result:
        print("ARM_NUMBER: " + str(arm_number))
        print("COLOR_IN: " + str(r[0]))
        print("COLOR_OUT: " + str(r[1]))
        print("X: " + str(r[2]))
        print("Y: " + str(r[3]))
        arm_number = arm_number + 1
    print ("")

