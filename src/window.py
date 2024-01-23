import pygame


class _Window:

    game_size = (16, 9)
    window_size = [1280, 720]
    _screen = None

    def __init__(self):
        pygame.display.set_caption("Not Pong")
        self.set_size(self.window_size)

    def set_size(self, size):
        self.window_size = size
        self._screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

    def draw_screen_gizmos(self):
        self.draw_grid()
        self.draw_origin_gizmo()

    def draw_grid(self, color = (50, 50, 50), line_width=0.01):
        game_display_rect = self.get_game_display_rect()

        x_start = game_display_rect.left - 1
        x_end = game_display_rect.right + 1
        x_line_count = self.game_size[0] + 2

        y_start = game_display_rect.top - 1
        y_end = game_display_rect.bottom + 1
        y_line_count = self.game_size[1] + 2

        for i in range(x_line_count):
            x = x_start + i
            self.draw_line((x, y_start), (x, y_end), color, line_width)
        for i in range(y_line_count):
            y = y_start + i
            self.draw_line((x_start, y), (x_end, y), color, line_width)

    def draw_origin_gizmo(self):
        self.draw_line((0, 0), (1, 0), (0, 150, 0))
        self.draw_line((0, 0), (0, 1), (0, 0, 150))
        self.draw_circle((0, 0), .1, (200, 200, 200))

    def fill_undefined_area(self, color=(255, 255, 255)):
        game_display_rect = self._get_game_display_screen_rect()
        self.draw_screen_rect((0, 0, game_display_rect.left, self.window_size[1]), color)
        self.draw_screen_rect((game_display_rect.right, 0, self.window_size[0] - game_display_rect.right, self.window_size[1]), color)
        self.draw_screen_rect((0, 0, self.window_size[0], game_display_rect.top), color)
        self.draw_screen_rect((0, game_display_rect.bottom, self.window_size[0], self.window_size[1] - game_display_rect.bottom), color)

    # =============================================================================================
    # Client draw methods
    # =============================================================================================

    def draw_circle(self, world_position, radius, color):
        self.draw_screen_circle(self.get_screen_position(world_position), radius * self._get_game_display_scale(), color)

    def draw_screen_circle(self, screen_position, radius, color):
        pygame.draw.circle(self._screen, color, screen_position, radius)

    def draw_rect(self, world_rect, color):
        self.draw_screen_rect(self.get_screen_rect(world_rect), color)

    def draw_screen_rect(self, screen_rect, color):
        pygame.draw.rect(self._screen, color, screen_rect)

    def draw_line(self, start, end, color, width=0.1):
        self.draw_screen_line(self.get_screen_position(start), self.get_screen_position(end), color, width * self._get_game_display_scale())

    def draw_screen_line(self, start, end, color, width=1):
        if width == 0: return 
        pygame.draw.line(self._screen, color, start, end, max(1, int(width)))

    # =============================================================================================
    # Position conversion methods and helpers
    # =============================================================================================

    def get_screen_rect(self, world_rect):
        """ Get the world rectangle converted in to screen coordinates.
        Takes into account everything: scale, viewport offset ..."""
        game_display_offset = self._get_game_display_offset()
        game_display_scale = self._get_game_display_scale()
        return pygame.Rect((world_rect[0] + self.game_size[0] / 2) * game_display_scale + game_display_offset[0],
                           (self.game_size[1] / 2 - world_rect[1]) * game_display_scale + game_display_offset[1],
                           world_rect[2] * game_display_scale,
                           world_rect[3] * game_display_scale)

    def get_screen_position(self, world_position):
        """ Get the world position converted in to screen coordinates.
        Takes into account everything: scale, viewport offset ..."""
        centered_world_position = (world_position[0] + self.game_size[0] / 2, self.game_size[1] / 2 -  world_position[1])
        game_display_offset = self._get_game_display_offset()
        game_display_scale = self._get_game_display_scale()
        return centered_world_position[0] * game_display_scale + game_display_offset[0], centered_world_position[1] * game_display_scale + game_display_offset[1]

    def _get_game_display_screen_rect(self):
        """ Get the rectangle area and position of the screen that the game is displayed on."""
        game_display_offset = self._get_game_display_offset()
        game_display_scale = self._get_game_display_scale()
        game_display_size = (self.game_size[0] * game_display_scale, self.game_size[1] * game_display_scale)
        return pygame.Rect(game_display_offset[0], game_display_offset[1], game_display_size[0], game_display_size[1])

    def _get_game_display_offset(self):
        """ Get the pixel distance from the top left corner of the window to the top left corner of the game display."""
        game_display_scale = self._get_game_display_scale()
        game_display_size = (self.game_size[0] * game_display_scale, self.game_size[1] * game_display_scale)
        game_display_offset = ((self.window_size[0] - game_display_size[0]) / 2, (self.window_size[1] - game_display_size[1]) / 2)
        return game_display_offset
    
    def _get_game_display_scale(self):
        """ Get the scale of the game display in pixels per game unit. """
        return min(self.window_size[0] / self.game_size[0], self.window_size[1] / self.game_size[1])

    def get_game_display_rect(self):
        """ Get the area and position of the game world that is displayed on the screen. """
        return pygame.Rect(-self.game_size[0] / 2, -self.game_size[1] / 2, self.game_size[0], self.game_size[1])


# This is a singleton class, so we only need one instance of it.
window = _Window()