import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import psycopg2

connection = psycopg2.connect(
    user="postgres",
    password="7526",
    host="localhost",
    port="5432",
    database="dota2_tournaments"
)

cursor = connection.cursor()

barplot = [
    ["birth_year", "nickname"],              # 0. год рождения игроков
    ["duration_minutes", "tournament_id"],   # 1. длительность матчей по турнирам
    ["total_prize_money", "team_name"],      # 2. призовые команд
    ["kills", "deaths"],                     # 3. K/D игроков в матчах
    ["kills", "assists"],                    # 4. K/A игроков в матчах
    ["avg_duration", "tournament_name"],     # 5. средняя длительность турниров
    ["players_count", "team_name"],          # 6. количество игроков в командах
    ["matches_count", "team_name"],          # 7. число матчей по командам
    ["age_2021", "nickname"],                # 8. возраст игроков на 2021
    ["wins", "team_name"],                   # 9. количество побед команд
]

query = [
    "SELECT nickname, birth_year FROM players WHERE birth_year IS NOT NULL ORDER BY birth_year",
    "SELECT duration_minutes, tournament_id FROM matches ORDER BY duration_minutes",
    "SELECT team_name, total_prize_money FROM teams ORDER BY total_prize_money DESC",
    "SELECT kills, deaths FROM player_statistics ORDER BY kills DESC",
    "SELECT kills, assists FROM player_statistics ORDER BY kills DESC",
    """
    SELECT t.tournament_name,
           (SELECT AVG(m.duration_minutes)
            FROM matches m
            WHERE m.tournament_id = t.tournament_id) AS avg_duration
    FROM tournaments t
    ORDER BY avg_duration DESC
    """,
    """
    SELECT t.team_name,
           (SELECT COUNT(*)
            FROM players p
            WHERE p.team_id = t.team_id) AS players_count
    FROM teams t
    ORDER BY players_count DESC
    """,
    """
    SELECT t.team_name,
           (SELECT COUNT(*)
            FROM matches m
            WHERE m.team1_id = t.team_id OR m.team2_id = t.team_id) AS matches_count
    FROM teams t
    ORDER BY matches_count DESC
    """,
    """
    SELECT nickname,
           2021 - birth_year AS age_2021
    FROM players
    WHERE birth_year IS NOT NULL
    ORDER BY age_2021
    """,
    """
    SELECT t.team_name,
           (SELECT COUNT(*)
            FROM matches m
            WHERE m.winner_id = t.team_id) AS wins
    FROM teams t
    ORDER BY wins DESC
    """
]

print("Выбери номер запроса:")
for num, q in enumerate(query):
    print(f"{num} -> {barplot[num]}")

i = int(input("Введите номер от 0 до 9: "))
dataframe1 = pd.read_sql(query[i], connection)

print(dataframe1.head())

sb.set_theme(style="darkgrid")
plt.figure(figsize=(10, 5))

if i in [3, 4]:
    sb.scatterplot(x=barplot[i][1], y=barplot[i][0], data=dataframe1)
elif i in [0, 1, 2, 5, 6, 7, 8, 9]:
    sb.barplot(x=barplot[i][1], y=barplot[i][0], data=dataframe1)

plt.title(f"График по запросу №{i}")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

connection.close()