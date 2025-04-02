from player import Player


class Game:
    def __init__(self, identifier, team1, team2, score):
        self.identifier: int = identifier
        self.team1: list[Player] = team1
        self.team2: list[Player] = team2
        self.score: tuple[int, int] = score

    def __str__(self):
        # catch if any player is None
        if None in self.team1 or None in self.team2:
            raise ValueError("One of the players in the game is None")
        
        return f"{self.team1[0].name} ({self.team1[0].elo:.1f}) and {self.team1[1].name} ({self.team1[1].elo:.1f})vs \
            {self.team2[0].name} ({self.team2[0].elo:.1f}) and {self.team2[1].name}({self.team2[1].elo:.1f}) ({self.score})"
