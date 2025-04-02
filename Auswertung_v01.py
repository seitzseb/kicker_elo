Matthias = 1000
Johannes = 1000
Daniel = 1000
Martin = 1000


def calculate_elo(player_rating, opponent_rating, score, k_factor=32):
    """
    Berechnet die neue Elo-Zahl basierend auf dem Ergebnis eines Spiels.
    
    :param player_rating: Aktuelle Elo-Zahl des Spielers
    :param opponent_rating: Aktuelle Elo-Zahl des Gegners
    :param score: Tatsächliches Ergebnis (1 = Sieg, 0.5 = Remis, 0 = Niederlage)
    :param k_factor: K-Faktor zur Anpassung der Elo-Zahl
    :return: Neue Elo-Zahl des Spielers
    """
    expected_score = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))
    new_rating = player_rating + k_factor * (score - expected_score)
    return round(new_rating, 2)

def read_file(filename):
    try:
        elo_ratings = {}  # Speichert die Elo-Zahlen der Spieler
        default_elo = 1000  # Standardwert für neue Spieler

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    break  # Beende das Lesen bei einer leeren Zeile
                
                matches = line.split(';')  # Trenne die Matches
                for match in matches:
                    pairs = match.split(',')  # Trenne die einzelnen Paarungen
                    game_results = []

                    for pair in pairs:
                        if '=' not in pair:
                            continue  # Falls das Format nicht stimmt, überspringen
                        
                        teams, result = pair.split('=')  # Trenne Teams und Ergebnis
                        result = int(result)
                        players = teams.split('+')  # Trenne die Spieler, falls ein "+" vorhanden ist
                        game_results.append((players, result))
                    
                    # Bestimme Sieger und Verlierer
                    max_score = max(result for _, result in game_results)
                    winners = [players for players, result in game_results if result == max_score]
                    losers = [players for players, result in game_results if result < max_score]
                    
                    for players in winners + losers:
                        for player in players:
                            if player not in elo_ratings:
                                elo_ratings[player] = default_elo  # Setze Standardwert, falls Spieler neu ist
                    
                    # Berechne und aktualisiere Elo-Zahlen
                    for winners_team in winners:
                        for losers_team in losers:
                            winner_elo = sum(elo_ratings[player] for player in winners_team) / len(winners_team)
                            loser_elo = sum(elo_ratings[player] for player in losers_team) / len(losers_team)
                            
                            new_winner_elo = calculate_elo(winner_elo, loser_elo, 1)
                            new_loser_elo = calculate_elo(loser_elo, winner_elo, 0)
                            
                            for player in winners_team:
                                elo_ratings[player] = new_winner_elo
                            for player in losers_team:
                                elo_ratings[player] = new_loser_elo
        
        # Ausgabe der aktuellen Elo-Werte
        for player, rating in elo_ratings.items():
            print(f"{player}: {rating}")
    except FileNotFoundError:
        print("Datei nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


# Beispielaufruf
filename = "D:\Kicker-Elo-Wertung\ergebnisse_v01.txt"  # Ersetze mit dem tatsächlichen Dateinamen
read_file(filename)
