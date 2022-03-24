import copy
import math
import time

import arcade
from abc import ABC, abstractmethod

import rotatix

class ROTATIX_OBJECT:
    def __init__(self, rotatix_sketch=None):
        self.rotatix_sketch = None
        self.iteration = 0

        self.width = 0
        self.height = 0

        self.padding = 10

        self.init(rotatix_sketch=rotatix_sketch)

        self.coordinates = []
        self.drawing = []

    def init(self, rotatix_sketch=None):
        self.rotatix_sketch = rotatix_sketch

        self.set_rotatix_sketch(rotatix_sketch=rotatix_sketch)

        self.iteration = 0

    def set_rotatix_sketch(self, rotatix_sketch=None):
        if self.rotatix_sketch:
            del self.rotatix_sketch
        self.rotatix_sketch = rotatix_sketch

        size = rotatix_sketch.rasterize_size()

        self.width = size[0]
        self.height = size[1]

    def reset(self):
        self.iteration = 0

    def update(self, delta=0, mousex=150, mousey=150):
        self.iteration = self.iteration + 1

        current_coordinates = self.get_arm_coordinates()
        rectified_coordinates = []
        for i in current_coordinates:
            rectified_coordinates.append(i)
        self.coordinates = tuple(rectified_coordinates)

        if self.iteration < self.rotatix_sketch.sides:
            coordinate_element = rectified_coordinates[-1:][0][2][1]
            self.drawing.append(coordinate_element)
    def get_drawable_elements(self):
        return tuple(self.coordinates), self.drawing
    def get_arm_coordinates(self):
        iteration = self.iteration

        point = 0, 0
        coordinates = self.rotatix_sketch.rasterize(x=0, y=0, iteration=iteration)

        result = []
        for color_in, color_out, x, y in coordinates:
            current_coordinates = x, y
            result.append((color_in, color_out, (point, current_coordinates)))
            point = current_coordinates
        return tuple(result)


class Rotatix_Sketch_Entity:
    def __init__(self, rotatix_object: ROTATIX_OBJECT = None, mousex=0, mousey=0):
        self.enable_arms = True
        self.iteration = 0

        self.active = False

        self.x = mousex
        self.y = mousey

        self.rotatix_sketch = copy.copy(rotatix_object.rotatix_sketch)

        self.rotatix_drawing_coordinates = []

        self.draw_border = True

        for coords in rotatix_object.drawing:
            coords = coords[0], coords[1]
            self.rotatix_drawing_coordinates.append(coords)

    def update(self, new=False):

        if new:
            rotatix_sketch : rotatix.Rotatix_Sketch = self.rotatix_sketch

            self.rotatix_drawing_coordinates.clear()

            for iteration in range(0, rotatix_sketch.sides):
                current_point = rotatix_sketch.rasterize(iteration=iteration, x=0, y=0)[-1:][0][2][1]
                self.rotatix_drawing_coordinates.append(current_point)

        self.iteration = self.iteration + 1

    def render(self, centerx=0, centery=0):
        last_coordinate = None


        for current_coordinate in self.rotatix_drawing_coordinates:
            current_coordinate = (current_coordinate[0] + self.x + centerx, current_coordinate[1] + self.y + centery)
            if last_coordinate:
                arcade.draw_lines(point_list=(last_coordinate, current_coordinate), line_width=2, color=(0, 0, 0))
            last_coordinate = current_coordinate

        if self.enable_arms:
            current_arm_set = self.rotatix_sketch.rasterize(iteration=self.iteration, x=self.x+centerx, y=self.y+centery)

            point = self.x + centerx, self.y + centery
            for color_in, color_out, x, y in current_arm_set:
                arcade.draw_lines(point_list=(point, (x,y)), color=color_in, line_width=3)
                point = x,y
        if self.draw_border:
            dimensions = self.rotatix_sketch.rasterize_size()
            arcade.draw_rectangle_outline(center_x=self.x + centerx, center_y=self.y + centery, border_width=3, width=dimensions[0]*2, height=dimensions[1]*2, color=((127,127,127),(255,0,0))[self.active])
    def toggle_arms(self):
        self.enable_arms = not self.enable_arms
        return self.enable_arms


class Rotatix_Arcade(arcade.Window):
    def __init__(self, rotatix_sketch=None):
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768

        self.SCREEN_TITLE = "Rotatix V2.0"

        self.BACKGROUND_COLOR = (255, 255, 255)

        super().__init__(width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT, title=self.SCREEN_TITLE)
        arcade.set_background_color(color=self.BACKGROUND_COLOR)

        self.running = True

        self.rotatix_object = ROTATIX_OBJECT(rotatix_sketch=rotatix_sketch)

        self.mousex = 0
        self.mousey = 0

        self.centerx = 0
        self.centery = 0

        self.last_coordinates = []

        self.sketch_entities : Rotatix_Sketch_Entity = []

        self.active_sketch = None

        self.last_click = 0
        self.last_button = 0

        self.activate_menu = 0

    def on_mouse_press(self, x, y, button, modifiers):
        did_last_click = False
        current_click = time.time_ns()

        if self.last_button == button:
            if current_click - self.last_click < 200000000:
                if button == arcade.MOUSE_BUTTON_RIGHT:
                    self.activate_menu = not self.activate_menu
                else:
                    pass
                did_last_click = True

        self.last_click = current_click
        self.last_button = button

        if not did_last_click:
            if button == arcade.MOUSE_BUTTON_RIGHT:
                best_x = 0
                best_y = 0
                best_length = 10000000000
                if self.active_sketch:
                    if self.active_sketch.active:
                        self.active_sketch.active = False

                self.active_sketch = None
                best_found = False

                for sketch in self.sketch_entities:
                    #sketch_size = (sketch.rotatix_sketch.rasterize_size()[0] ^ 2 * 2) ^ (2 ^ -1)
                    sketch_size = sketch.rotatix_sketch.rasterize_size()[0] + 20
                    offset_x = abs(x - sketch.x)
                    offset_y = abs(y - sketch.y)

                    offset_length = abs(((offset_x ^ 2) + (offset_y ^ 2)) ^ (2 ^ -1))

                    print ("OFFSET LENGTH!: " + str(offset_length) + ", BEST LENGTH: " + str(best_length) + ", SKETCH_SIZE: " + str(sketch_size))

                    if ((offset_length < best_length) or (not self.active_sketch)) and (offset_length <= sketch_size):
                        best_found = True
                        self.active_sketch = sketch
                        best_x = offset_x
                        best_y = offset_y
                        best_length = offset_length
                if self.active_sketch and best_found:
                    self.active_sketch.active = True
                else:
                    self.active_sketch = None

            elif button == arcade.MOUSE_BUTTON_LEFT:
                if self.active_sketch:
                    self.active_sketch.active = False
                new_sketch = Rotatix_Sketch_Entity(rotatix_object=self.rotatix_object, mousex=x-self.centerx, mousey=y-self.centery)
                new_sketch.active = True

                self.active_sketch = new_sketch

                self.sketch_entities.append(new_sketch)

            elif button == arcade.MOUSE_BUTTON_MIDDLE:
                if self.active_sketch:
                    self.active_sketch.toggle_arms()
    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        pass

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        if buttons & arcade.MOUSE_BUTTON_MIDDLE:
                self.centerx = self.centerx + dx
                self.centery = self.centery + dy
        if buttons & arcade.MOUSE_BUTTON_RIGHT:
            if self.active_sketch:
                self.active_sketch.x =  self.active_sketch.x + dx
                self.active_sketch.y = self.active_sketch.y + dy

    def on_mouse_motion(self, x=0, y=0,dx =0, dy=0, **kwargs):
        self.mousex = x
        self.mousey = y

    def on_update(self, delta_time=0):
        self.rotatix_object.update(mousex=self.mousex, mousey=self.mousey)
        for sketch_entity in self.sketch_entities:
            sketch_entity.update()
    def on_draw(self):
        arcade.start_render()

        drawable_elements = self.rotatix_object.get_drawable_elements()

        arm_lines = drawable_elements[0]
        drawing_lines = drawable_elements[1]

        colors = []

        for color_in, color_out, coordinates in arm_lines:
            coordinates = ((coordinates[0][0] + self.mousex, coordinates[0][1] + self.mousey), (coordinates[1][0] + self.mousex, coordinates[1][1] + self.mousey))
            arcade.draw_lines(color=color_in, point_list=coordinates, line_width=3)
            colors.append((color_in, color_out))

        i = 0
        last_coordinates = None

        for coordinates in drawing_lines:
            coordinates = coordinates[0] + self.mousex, coordinates[1] + self.mousey
            current_colors = colors[i % len(colors)]
            if last_coordinates:
                arcade.draw_lines(color=current_colors[0], point_list=(last_coordinates, coordinates), line_width=1)
            i = i + 1
            last_coordinates = coordinates
        dimensions = self.rotatix_object.rotatix_sketch.rasterize_size()
        arcade.draw_rectangle_outline(center_x=self.mousex, center_y=self.mousey,width = dimensions[0] * 2,height=dimensions[1] * 2, color=(0, 0, 0), border_width=3)

        for sketch_entity in self.sketch_entities:
            sketch_entity.render(centerx=self.centerx, centery=self.centery)

        arcade.finish_render()

