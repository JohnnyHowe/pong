class _UserConfig:
    _data = {
        "game_paddle_speed_effect_on_ball": 0.5,
        "juice_screen_movement_from_paddle_lerp_speed": 8,
        "juice_screen_movement_from_paddle_max_vertical": 0.3,
        "juice_screen_movement_from_paddle_max_rotation_degrees": 2
    }

    def __init__(self):
        pass

    def get(self, key):
        return self._data[key]

user_config = _UserConfig()