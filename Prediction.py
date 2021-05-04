class Prediction:
    def __init__(self, goals_home, goals_guest):
        self.goals_home = goals_home
        self.goals_guest = goals_guest

    def __repr__(self):
        if self.goals_home is None or self.goals_guest is None:
            return "none"

        return self.goals_home + ":" + self.goals_guest