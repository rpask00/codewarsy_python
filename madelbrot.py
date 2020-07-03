import os
import pygame
import math
import cProfile
from pygame.locals import *
from numba import jit
import numpy as np


class Mandelbrot:
    def _calculate_min_max(self):
        self.x_min, self.x_max = self.center[0] - self.x_range / 2, self.center[0] + self.x_range / 2
        self.y_min, self.y_max = self.center[1] - self.y_range / 2, self.center[1] + self.y_range / 2

    def _calculate_y_range(self):
        self.y_range = self.win_height * self.x_range / self.win_width

    def __init__(self, win_dims, max_iter, threshold, center, x_range, color_algorithm, color_multiplier, palettes, current_palette):
        self.win_width, self.win_height = win_dims
        self.max_iter = max_iter
        self.threshold = threshold
        self.center = center
        self.x_range = x_range
        self._calculate_y_range()
        self.scroll_rate = 1
        self.zoom_factor = 1
        self._calculate_min_max()
        self.current_palette = current_palette
        self.color_algorithm = color_algorithm
        self.color_multiplier = color_multiplier
        self.palettes = palettes

    @staticmethod
    def _get_color(palette_colors, palette_indices, index):
        index = index % 1
        for i in range(len(palette_indices)):
            if (index >= palette_indices[i] and index <= palette_indices[i+1]):
                index_start = palette_indices[i]
                index_end = palette_indices[i+1]
                new_index = (index - index_start) / (index_end - index_start)
                color_start = palette_colors[i]
                color_end = palette_colors[i+1]
                break

        return Color(round(new_index * (color_end[0] - color_start[0]) + color_start[0]),
                     round(new_index * (color_end[1] - color_start[1]) + color_start[1]),
                     round(new_index * (color_end[2] - color_start[2]) + color_start[2]), 255)

    def cycle_current_palette(self):
        self.current_palette = (self.current_palette + 1) % len(self.palettes)
        print('Cycling to palette:', self.current_palette)

    @staticmethod
    @jit
    def _inner_calculation(x, y, max_iter, threshold_sqr):
        C = complex(x, y)
        z = 0+0j
        iter_count = 0                    # Reset iteration count for each pixel
        for _ in range(0, max_iter):
            z = z*z + C                  # f(z) = z^2 + C
            iter_count += 1
            z_mag_sqr = z.real*z.real + z.imag*z.imag
            if z_mag_sqr > threshold_sqr:
                break
        return z, iter_count

    def _get_color_index(self, abs_val, iter_count):
        temp_index = abs(iter_count - math.log(math.log(abs_val), 2))  # Smoothing
        if (self.color_algorithm == 0):
            return 1 / temp_index * self.color_multiplier  # Alg 0
        else:
            return temp_index * self.color_multiplier / 500  # Alg 1

    def draw(self, surface):
        print('Redrawing image...')
        pixel_array = pygame.PixelArray(surface)
        threshold_sqr = self.threshold * self.threshold
        x_coords = np.linspace(self.x_min, self.x_max, self.win_width)
        y_coords = np.linspace(self.y_max, self.y_min, self.win_height)
        mand = (self._inner_calculation(x, y, self.max_iter, threshold_sqr) for y in y_coords for x in x_coords)
        count = 0
        for z, iter_count in mand:
            abs_val = abs(z)
            if abs_val <= 2:
                pix_color = Color(0, 0, 0, 255)  # These are in the set
            else:
                color_index = self._get_color_index(abs_val, iter_count)
                pix_color = self._get_color(self.palettes[self.current_palette][0], self.palettes[self.current_palette][1], color_index)
            pixel_array[count % self.win_width, count // self.win_width] = pix_color
            count += 1
        del pixel_array
        print('Image redrawn')

    def _move_center(self, x_pixels, y_pixels):
        self.center[0] += x_pixels * (self.x_range / self.win_width)
        self.center[1] += y_pixels * (self.y_range / self.win_height)
        self._calculate_min_max()

    def scroll(self, x_scroll, y_scroll, surface):
        x_pixels = x_scroll * self.scroll_rate
        y_pixels = y_scroll * self.scroll_rate
        surface.scroll(x_pixels, y_pixels)
        self._move_center(-x_pixels, y_pixels)

    def increase_scroll_rate(self):
        self.scroll_rate *= 2
        print('Scroll Rate:', self.scroll_rate)

    def decrease_scroll_rate(self):
        if self.scroll_rate > 1:
            self.scroll_rate //= 2
        print('Scroll Rate:', self.scroll_rate)

    def zoom(self, surface):
        self.x_range /= self.zoom_factor
        self._calculate_y_range()
        self._calculate_min_max()
        self.draw(surface)

    def increase_zoom_factor(self):
        self.zoom_factor *= 1.1
        print('Zoom Factor:', self.zoom_factor)

    def decrease_zoom_factor(self):
        self.zoom_factor /= 1.1
        print('Zoom Factor:', self.zoom_factor)

    def print_info(self):
        print('Mandelbrot Position:')
        print('Center:', self.center)
        print('X-Min-Max:', self.x_min, self.x_max)
        print('Y-Min-Max:', self.y_min, self.y_max)
        print('Mandelbrot Variables:')
        print('Max Iterations:', self.max_iter)
        print('Threshold:', self.threshold)

    def increase_color_multiplier(self):
        self.color_multiplier *= 1.1
        print('Color Multiplier:', self.color_multiplier)

    def increase_max_iter(self):
        self.max_iter *= 2
        print('Max Iterations:', self.max_iter)

    def increase_threshold(self):
        self.threshold *= 1.1
        print('Threshold:', self.threshold)

    def decrease_color_multiplier(self):
        self.color_multiplier /= 1.1
        print('Color Multiplier:', self.color_multiplier)

    def decrease_max_iter(self):
        self.max_iter /= 2
        print('Max Iterations:', self.max_iter)

    def decrease_threshold(self):
        self.threshold /= 1.1
        print('Threshold:', self.threshold)

    def cycle_color_algorithm(self):
        self.color_algorithm = (self.color_algorithm + 1) % 2
        print('Cycling to color_algorithm:', self.color_algorithm)


# ------------------------------------------------------------------------------------------
def get_int_from_user(prompt):
    print(prompt)
    return int(input())


def keyboard_input(key, mandelbrot, surface):
    if key == pygame.K_LEFT:
        mandelbrot.scroll(1, 0, surface)
    elif key == pygame.K_RIGHT:
        mandelbrot.scroll(-1, 0, surface)
    elif key == pygame.K_UP:
        mandelbrot.scroll(0, 1, surface)
    elif key == pygame.K_DOWN:
        mandelbrot.scroll(0, -1, surface)
    elif key == pygame.K_d:
        #cProfile.runctx('mandelbrot.draw(surface)', None, locals())
        mandelbrot.draw(surface)
    elif key == pygame.K_1:
        mandelbrot.decrease_scroll_rate()
    elif key == pygame.K_2:
        mandelbrot.increase_scroll_rate()
    elif key == pygame.K_3:
        mandelbrot.decrease_color_multiplier()
    elif key == pygame.K_4:
        mandelbrot.increase_color_multiplier()
    elif key == pygame.K_5:
        mandelbrot.decrease_max_iter()
    elif key == pygame.K_6:
        mandelbrot.increase_max_iter()
    elif key == pygame.K_7:
        mandelbrot.decrease_threshold()
    elif key == pygame.K_8:
        mandelbrot.increase_threshold()
    elif key == pygame.K_9:
        mandelbrot.decrease_zoom_factor()
    elif key == pygame.K_0:
        mandelbrot.increase_zoom_factor()
    elif key == pygame.K_z:
        mandelbrot.zoom(surface)
    elif key == pygame.K_s:
        pygame.image.save(surface, 'image.png')
    elif key == pygame.K_p:
        mandelbrot.print_info()
    elif key == pygame.K_c:
        mandelbrot.cycle_current_palette()
    elif key == pygame.K_a:
        mandelbrot.cycle_color_algorithm()


def main():
    palettes = (
        (((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0)),            # RGB
         (0, 0.33, 0.66, 1)),
        (((255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 0)),       # Cotton Candy
         (0, 0.33, 0.66, 1)),
        (((255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 68, 255), (255, 0, 255), (255, 0, 0)),  # Rainbow-ish
         (0, 0.14, 0.29, 0.44, 0.59, 0.74, 0.89, 1)),
        (((255, 255, 255), (0, 0, 0), (32, 32, 32), (0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 255, 255)),  # Fire
         (0, 0.16, 0.33, 0.50, 0.67, 0.84, 1))
    )
    win_dims = 400, 400  # width, height
    pygame.init()
    surface = pygame.display.set_mode(win_dims)
    pygame.display.set_caption('Mandelbrot')
    mandelbrot = Mandelbrot(win_dims, 32, 100, [0, 0], 4, 0, 5, palettes, 2)
    mandelbrot.draw(surface)

    going = True
    while going:    # Main game loops

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN:
                keyboard_input(event.key, mandelbrot, surface)

        pygame.display.update()  # Would be better if only on scroll, zoom, draw, or color change

    pygame.quit()


main()
