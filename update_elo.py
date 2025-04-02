import pandas as pd
import logging
from game import Game
from player import Player
import time

logging.basicConfig(
    filename='/workspace/log.txt',  # Path to your log file
    level=logging.DEBUG,           # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    filemode='a'  # 'a' means append to the log file (use 'w' to overwrite the file)
)

logging.info("Starting the program")

class Elo_Updater:
    def __init__(self):
        self.game_filename = "workspace/data/games.csv"
        self.elo_filename = "workspace/data/elos.csv"
        self.elo_ratings = None
        self.default_elo = 1500
        self.players: list[Player] = []
        self.games: list[Game] = []

    def get_players_from_database(self):
        try:
            elos = pd.read_csv(self.elo_filename, sep=',', header=0,
                               names=['player', 'elo'])
            for index, row in elos.iterrows():
                self.players.append(Player(row['player'], row['elo']))

            for player in self.players:
                logging.log(logging.DEBUG, player)

        except FileNotFoundError:
            self.elo_ratings = None
            logging.log(
                logging.DEBUG, "No elo file found at " + self.elo_filename)

    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        player = Player(name, self.default_elo)
        self.players.append(player)
        self.write_elo_file()
        return player

    def get_games_from_database(self):
        try:
            self.games_df = pd.read_csv(self.game_filename, sep=',', header=0,
                                        names=['ID',
                                               'Team1_Player1',
                                               'Team1_Player2',
                                               'Team2_Player1',
                                               'Team2_Player2',
                                               'Team1_Score',
                                               'Team2_Score'])
            for index, row in self.games_df.iterrows():
                identifier = row['ID']
                team1_player1 = self.get_player(row['Team1_Player1'])
                team1_player2 = self.get_player(row['Team1_Player2'])
                team2_player1 = self.get_player(row['Team2_Player1'])
                team2_player2 = self.get_player(row['Team2_Player2'])
                score = (row['Team1_Score'], row['Team2_Score'])
                logging.log(logging.DEBUG, "Game " + str(identifier)
                            + " " + str(team1_player1)
                            + " " + str(team1_player2)
                            + " " + str(team2_player1)
                            + " " + str(team2_player2)
                            + " " + str(score))
                game = Game(identifier,
                            [team1_player1, team1_player2],
                            [team2_player1, team2_player2],
                            score)
                logging.log(logging.DEBUG, game)
                self.games.append(game)
        except FileNotFoundError:
            logging.log(
                logging.ERROR, "No game file found at " + self.game_filename)

    def _calculate_combined_rating(self, team):
        return sum([player.elo for player in team]) / len(team)

    def _calculate_expeted_score(self, combined_rating_1, combined_rating_2):
        return 1 / (1 + 10 ** ((combined_rating_2 - combined_rating_1) / 400))

    def update_elo(self, game: Game):
        K = 40
        logging.log(logging.DEBUG, "Updating elo for game " + str(game))
        combined_rating_1 = self._calculate_combined_rating(game.team1)
        combined_rating_2 = self._calculate_combined_rating(game.team2)

        winner = game.team1 if game.score[0] > game.score[1] else game.team2
        loser = game.team1 if game.score[0] < game.score[1] else game.team2

        expected_score = self._calculate_expeted_score(combined_rating_1,
                                                       combined_rating_2)
        for player in winner:
            player.elo += K * (1 - expected_score)

        for player in loser:
            player.elo += K * (0 - expected_score)

        logging.log(logging.DEBUG, "Updated elo for game " + str(game))
        # print new elos
        for player in self.players:
            logging.log(logging.DEBUG, player)

    def write_elo_file(self):
        # construct a pandas dataframe with name, elo
        data = {'player': [player.name for player in self.players],
                'elo': [player.elo for player in self.players]}
        df = pd.DataFrame(data)
        df.to_csv(self.elo_filename, index=False)

    def update_games_history(self):
        try:
            hist_games = pd.read_csv('workspace/data/games_history.csv',
                                     sep=',', header=0,
                                     names=['ID',
                                            'Team1_Player1',
                                            'Team1_Player2',
                                            'Team2_Player1',
                                            'Team2_Player2',
                                            'Team1_Score',
                                            'Team2_Score'])
        except FileNotFoundError:
            pass

        hist_games = pd.concat((hist_games, self.games_df))
        hist_games.to_csv('workspace/data/games_history.csv', index=False)


if __name__ == "__main__":
    updater = Elo_Updater()
    logging.info("Updating elo ratings")
    updater.get_players_from_database()
    updater.get_games_from_database()
    for game in updater.games:
        updater.update_elo(game)
    updater.write_elo_file()
    updater.update_games_history()
