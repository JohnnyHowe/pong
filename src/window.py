import math
import pygame
from .clock import clock

class _Window:

    game_size = (16, 9)
    window_size = [1280, 720]
    _draw_buffer = None
    _screen = None
    camera_rotation_rads = 0 # radians anticlockwise -> for screen to rotate clockwise this must be positive
    camera_position = (0, 0)
    game_display_scale = 0.9

    def __init__(self):
        pygame.display.set_caption("Not Pong")
        pygame.font.init()
        self.set_size(self.window_size)

    def set_size(self, size):
        self.window_size = size
        self._screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        scale = self._get_game_display_scale()
        self._draw_buffer = pygame.Surface((self.game_size[0] * scale, self.game_size[1] * scale), pygame.SRCALPHA)

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

    def draw_rect(self, world_rect, color):
        rect_screen_center = self.get_screen_position((world_rect[0] + world_rect[2] / 2, world_rect[1] - world_rect[3] / 2))
        rect_screen_size = (world_rect[2] * self._get_game_display_scale(), world_rect[3] * self._get_game_display_scale())

        surface = pygame.Surface(rect_screen_size, pygame.SRCALPHA);
        surface.fill(color)
        surface = pygame.transform.rotate(surface, math.degrees(self.camera_rotation_rads))

        surface_rect = surface.get_rect()
        self._screen.blit(surface, (rect_screen_center[0] - surface_rect.width / 2, rect_screen_center[1] - surface_rect.height / 2))

    def draw_polygon(self, points, color, width=0):
        screen_points = []
        for point in points:
            screen_points.append(self.get_screen_position(point))
        pygame.draw.polygon(self._screen, color, screen_points, int(width * self._get_game_display_scale()))

    def draw_line(self, p1, p2, width, color):
        pygame.draw.line(self._screen, color, self.get_screen_position(p1), self.get_screen_position(p2), int(width * self._get_game_display_scale()))

    def draw_text(self, text, position, color=(255, 255, 255), size=1, center_aligned=True):
        my_font = pygame.font.Font("assets/FFFFORWA.TTF", int(size * self._get_game_display_scale()))
        text_surface = my_font.render(str(text), True, color)
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

    def get_screen_rect(self, world_rect):
        """ Get the world rectangle converted in to screen coordinates.
        Takes into account everything: scale, viewport offset ..."""
        game_display_scale = self._get_game_display_scale()
        return pygame.Rect((world_rect[0] + self.game_size[0] / 2) * game_display_scale,
                           (self.game_size[1] / 2 - world_rect[1]) * game_display_scale,
                           world_rect[2] * game_display_scale,
                           world_rect[3] * game_display_scale)

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

    def _get_game_display_screen_rect(self):
        """ Get the rectangle area and position of the screen that the game is displayed on."""
        game_display_offset = self._get_game_display_offset()
        game_display_scale = self._get_game_display_scale()
        game_display_size = (self.game_size[0] * game_display_scale, self.game_size[1] * game_display_scale)
        return pygame.Rect(game_display_offset[0], game_display_offset[1], game_display_size[0], game_display_size[1])
    
    def _get_game_display_scale(self):
        """ Get the scale of the game display in pixels per game unit. """
        return min(self.window_size[0] * self.game_display_scale / self.game_size[0], self.window_size[1] * self.game_display_scale / self.game_size[1])

    def get_game_display_rect_no_rotation(self):
        """ Get the area and position of the game world that is displayed on the screen. """
        return pygame.Rect(-self.game_size[0] / 2, -self.game_size[1] / 2, self.game_size[0], self.game_size[1])


# This is a singleton class, so we only need one instance of it.
window = _Window()