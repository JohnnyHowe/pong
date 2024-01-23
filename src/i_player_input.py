class IPlayerInput:
    def get_movement(self):
        """ Returns a value between -1 and 1.
        1 = max speed up, -1 = max speed down"""
        raise NotImplemented()