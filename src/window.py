import math
import pygame
from pygame import gfxdraw
from .clock import clock
from .game_configuration import *

class _Window:

    game_size = (16, 9)
    window_size = [1280, 720]
    _draw_buffer = None
    _screen = None
    camera_rotation_rads = 0 # radians anticlockwise -> for screen to rotate clockwise this must be positive
    camera_position = (0, 0)
    game_display_scale = 0.9

    windowed_size = (1280, 720)

    def __init__(self):
        pygame.display.set_caption("Not Pong")
        pygame.font.init()
        self.force_set_size(self.window_size)
        if GAME_START_FULLSCREEN: self.toggle_fullscreen()

    def set_size(self, new_size):
        is_fullscreen = self._screen.get_flags() & pygame.FULLSCREEN == pygame.FULLSCREEN
        if (not is_fullscreen): self.force_set_size(new_size)

    def force_set_size(self, new_size):
        self.window_size = new_size
        self._screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.refresh_draw_buffer()

    def refresh_draw_buffer(self):
        scale = self._get_game_display_scale()
        self._draw_buffer = pygame.Surface((self.game_size[0] * scale, self.game_size[1] * scale), pygame.SRCALPHA)

    def toggle_fullscreen(self):
        is_fullscreen = self._screen.get_flags() & pygame.FULLSCREEN == pygame.FULLSCREEN
        if (is_fullscreen):
            self.force_set_size(self.windowed_size)
        else:
            self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.window_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            self.refresh_draw_buffer()
        
    def update(self):
        pygame.display.flip()

    def draw_fps(self):
        self.draw_text("FPS: " + str(int(clock.smoothed_fps)), (-self.game_size[0] / 2, self.game_size[1] / 2), size=0.5, center_aligned=False)

    def fill_undefined_area(self, color=(255, 255, 255)):
        self._screen.fill(color)
        self.draw_rect((-self.game_size[0] / 2, self.game_size[1] / 2, self.game_size[0], self.game_size[1]), (0, 0, 0))

    def fill_game_area(self, color=(255, 255, 255)):
        x = (self.game_size[0]) / 2
        y = (self.game_size[1]) / 2
        self.draw_polygon([(x, y), (x, -y), (-x, -y), (-x, y)], color, 0)

    # =============================================================================================
    # Client draw methods
    # =============================================================================================

    def draw_square(self, center_position, size, color, rotation_rads=0):
        self.draw_rect((center_position[0] - size / 2, center_position[1] + size / 2, size, size), color, rotation_rads)

    def draw_rect(self, world_rect, color, rotation_rads=0):
        if (world_rect[2] == 0 or world_rect[3] == 0): return
        points = [(world_rect[0], world_rect[1]), (world_rect[0] + world_rect[2], world_rect[1]), (world_rect[0] + world_rect[2], world_rect[1] - world_rect[3]), (world_rect[0], world_rect[1] - world_rect[3])]
        center = (world_rect[0] + world_rect[2] / 2, world_rect[1] - world_rect[3] / 2)
        self.draw_polygon(self.rotate_points(center, points, rotation_rads), color, 0)

    def rotate_points(self, origin, points, angle_rads):
        if (angle_rads == 0): return points
        rotated_points = []
        for point in points:
            rotated_points.append(self.rotate_point(origin, point, angle_rads))
        return rotated_points

    def rotate_point(self, origin, point, angle_rads):
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(-angle_rads) * (px - ox) - math.sin(-angle_rads) * (py - oy)
        qy = oy + math.sin(-angle_rads) * (px - ox) + math.cos(-angle_rads) * (py - oy)
        return qx, qy

    def draw_polygon(self, points, color, width=0):
        screen_points = []
        for point in points:
            screen_points.append(self.get_screen_position(point))
        if GAME_ANTIALIASING:
            gfxdraw.aapolygon(self._screen, screen_points, color)
            gfxdraw.filled_polygon(self._screen, screen_points, color)
        else:
            pygame.draw.polygon(self._screen, color, screen_points, int(width * self._get_game_display_scale()))

    def draw_text(self, text, position, color=(255, 255, 255), size=1, center_aligned=True, rotation_rads=0):
        my_font = pygame.font.Font("assets/FFFFORWA.TTF", int(size * self._get_game_display_scale()))
        text_surface = my_font.render(str(text), GAME_ANTIALIASING, color)
        if (rotation_rads != 0): text_surface = pygame.transform.rotate(text_surface, math.degrees(rotation_rads))
        text_surface = pygame.transform.rotate(text_surface, math.degrees(self.camera_rotation_rads))

        draw_position = self.get_screen_position(position)
        if center_aligned:
            text_rect = text_surface.get_rect()
            screen_center = self.get_screen_position(position)
            draw_position = (screen_center[0] - text_rect.width / 2, screen_center[1] - text_rect.height / 2)

        self._screen.blit(text_surface, draw_position)

    # =============================================================================================
    # Position conversion methods and helpers
    # =============================================================================================

    def get_screen_position(self, world_position):
        """ Get the world position converted in to screen coordinates.
        Takes into account everything: scale, viewport offset ..."""
        world_position_translated = self._get_world_position_with_camera_offset(world_position)
        world_position_translated = (world_position_translated[0] + self.game_size[0] / 2, self.game_size[1] / 2 -  world_position_translated[1])
        game_display_scale = self._get_game_display_scale()
        game_display_offset = (self.window_size[0] / 2 - self.game_size[0] * game_display_scale / 2, self.window_size[1] / 2 - self.game_size[1] * game_display_scale / 2)
        return world_position_translated[0] * game_display_scale + game_display_offset[0], world_position_translated[1] * game_display_scale + game_display_offset[1]

    def _get_world_position_with_camera_offset(self, world_position):
        # return world_position
        translated = (world_position[0] - self.camera_position[0], world_position[1] - self.camera_position[1])
        rotated = (translated[0] * math.cos(self.camera_rotation_rads) - translated[1] * math.sin(self.camera_rotation_rads),
                   translated[0] * math.sin(self.camera_rotation_rads) + translated[1] * math.cos(self.camera_rotation_rads))
        return rotated

    def _get_game_display_scale(self):
        """ Get the scale of the game display in pixels per game unit. """
        return min(self.window_size[0] * self.game_display_scale / self.game_size[0], self.window_size[1] * self.game_display_scale / self.game_size[1])

    def get_game_display_rect_no_rotation(self):
        """ Get the area and position of the game world that is displayed on the screen. """
        return pygame.Rect(-self.game_size[0] / 2, -self.game_size[1] / 2, self.game_size[0], self.game_size[1])


# This is a singleton class, so we only need one instance of it.
window = _Window()