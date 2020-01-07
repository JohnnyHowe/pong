import random
import slowEngine
from slowEngine.geometery import *


class Game:
    def __init__(self):
        self.engine = slowEngine.Engine()
        self.engine.set_window(Vector(400, 400))

        self.player_dist = 5
        self.board = slowEngine.physics.BoxObject(Rect(0, 0, 1, 1) * self.player_dist * 2)

        self.p0 = None
        self.p1 = None
        self.set_players()

        self.ball = None
        self.set_ball()

        self.launching_player = 0
        self.in_play = False

        self.top_wall = None
        self.low_wall = None
        self.set_y_walls()
        self.wall_colliders = [self.top_wall.collider, self.low_wall.collider]

        self.left_wall = None
        self.right_wall = None
        self.set_x_walls()
        self.reset_colliders = [self.left_wall.collider, self.right_wall.collider]

        self.left_cover = None
        self.right_cover = None
        self.set_x_covers()

    def set_ball(self):
        self.ball = slowEngine.physics.BoxObject(Rect(0, 0, 0.5, 0.5))
        self.ball.mass = 0
        self.ball.max_velocity = 5
        self.ball.collider = slowEngine.physics.BoxCollider(self.ball, bounce=1)

    def new_wall(self, rect):
        wall = slowEngine.physics.BoxObject(rect)
        wall.collider = slowEngine.physics.BoxCollider(wall)
        wall.collider.bounce = 0
        wall.mass = float("inf")
        return wall

    def set_y_walls(self):
        wall_width = 0.1
        self.top_wall = self.new_wall(Rect(0, self.player_dist, self.player_dist * 2, wall_width))
        self.low_wall = self.new_wall(Rect(0, -self.player_dist, self.player_dist * 2, wall_width))

    def set_x_walls(self):
        wall_width = 0.1
        self.right_wall = self.new_wall(Rect(self.player_dist + self.ball.rect.w * 2, 0, wall_width, self.player_dist * 2))
        self.left_wall = self.new_wall(Rect(-(self.player_dist + self.ball.rect.w * 2), 0, wall_width, self.player_dist * 2))

    def set_x_covers(self):
        wall_width = 2
        self.right_cover = self.new_wall(Rect(self.player_dist + wall_width / 2, 0, wall_width, self.player_dist * 2))
        self.left_cover = self.new_wall(Rect(-(self.player_dist + wall_width / 2), 0, wall_width, self.player_dist * 2))

    def set_players(self):
        width = 0.5
        self.p0 = slowEngine.physics.BoxObject(Rect(-self.player_dist + width / 2, 0, width, 2))
        self.p0.controller = slowEngine.controllers.KeyBoardControllerSmooth(self.p0, {"w": Vector(0, 1), "s": Vector(0, -1)})
        self.p0.collider = slowEngine.physics.BoxCollider(self.p0)
        self.p0.collider.bounce = 0
        self.p0.max_velocity = 10
        self.p1 = slowEngine.physics.BoxObject(Rect(self.player_dist - width / 2, 0, width, 2))
        self.p1.controller = slowEngine.controllers.KeyBoardControllerSmooth(self.p1, {"UPARROW": Vector(0, 1), "DOWNARROW": Vector(0, -1)})
        self.p1.collider = slowEngine.physics.BoxCollider(self.p1)
        self.p1.collider.bounce = 0
        self.p1.max_velocity = 10

    def display(self):
        self.engine.window.fill((150, 150, 150))
        self.show_all()
        self.engine.window.update_display()

    def show_all(self):
        self.board.show_block(self.engine, (230, 230, 230))

        self.p0.show_block(self.engine, (50, 50, 50))
        self.p1.show_block(self.engine, (50, 50, 50))

        self.ball.show_circle(self.engine, (5, 200, 0))

        self.left_cover.show_block(self.engine, (150, 150, 150))
        self.right_cover.show_block(self.engine, (150, 150, 150))

    def update(self):
        self.engine.update()
        self.p0.update(self.engine)
        self.p1.update(self.engine)
        if not self.in_play:
            self.run()
        else:
            self.play_phase()
        self.p0.collider.run_collisions(self.wall_colliders)
        self.p1.collider.run_collisions(self.wall_colliders)

    def launch_phase(self):
        if self.launching_player == 0:
            self.ball_follow_player(self.p0, 1)
        else:
            self.ball_follow_player(self.p1, -1)
        self.launch()

    def play_phase(self):
        self.ball.update(self.engine)
        if self.ball.collider.is_collided_with(self.reset_colliders):
            self.reset()

        effect = 0.5
        if self.ball.collider.is_collided_with([self.p0.collider]):
            self.ball.velocity += self.p0.velocity * effect
        if self.ball.collider.is_collided_with([self.p1.collider]):
            self.ball.velocity += self.p1.velocity * effect

        self.restrict_ball_angle()
        self.ball.collider.run_collisions(self.wall_colliders + [self.p0.collider, self.p1.collider])

    def run(self):
        if not self.in_play:
            self.launch_phase()
        else:
            self.play_phase()

    def ball_follow_player(self, player, side):
        self.ball.rect.x = player.rect.x + (player.rect.w / 2 + self.ball.rect.w / 2) * side
        self.ball.rect.y = player.rect.y

    def launch(self):
        if (self.engine.keyboard.is_pressed("d") and self.launching_player == 0 or
                self.engine.keyboard.is_pressed("LEFTARROW") and self.launching_player == 1):
            velocity = Vector(random.randint(3, 10), random.randint(-4, 4)) + [self.p0.velocity, self.p1.velocity][self.launching_player]
            scale = self.ball.max_velocity / velocity.length()
            velocity *= scale
            self.ball.velocity = velocity
            self.in_play = True

    def reset(self):
        self.launching_player = abs(self.launching_player - 1)
        self.in_play = False

    def restrict_ball_angle(self):
        if abs(self.ball.velocity.y) / abs(self.ball.velocity.x) > 1:
            self.ball.velocity.x /= abs(self.ball.velocity.x)
            self.ball.velocity.y /= abs(self.ball.velocity.y)
        scale = self.ball.max_velocity / self.ball.velocity.length()
        self.ball.velocity *= scale


def main():
    game = Game()

    while True:
        game.update()
        game.display()


if __name__ == "__main__":
    main()
