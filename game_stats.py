class GameStats():
    def __init__(self,settings):
        self.settings = settings
        set.game_active = True
        self.reset_stats()
    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
