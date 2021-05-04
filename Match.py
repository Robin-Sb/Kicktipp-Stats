# representation of the games in objects
class Match:
    def __init__(self, home_team, guest_team, goals_home, goals_guest, predictions):
        self.home_team = home_team
        self.guest_team = guest_team
        self.goals_home = goals_home
        self.goals_guest = goals_guest
        self.predictions = predictions

    def __repr__(self):
        if self.goals_home == None or self.goals_guest == None:
            return "none"
        return self.home_team + " " + str(self.goals_home) + ":" + str(self.goals_guest) + " " + self.guest_team + str(self.predictions)