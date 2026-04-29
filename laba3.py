import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class Dota2App:
    def __init__(self, root):
        self.root = root
        self.root.title("База данных Dota 2")
        self.root.geometry("800x600")

        self.conn = psycopg2.connect(
            dbname='dota2_tournaments',
            user='postgres',
            password='7526',
            host='localhost',
            port='5432'
        )
        self.cursor = self.conn.cursor()

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)

        notebook.add(tab1, text='Добавить команду')
        notebook.add(tab2, text='Добавить игрока')
        notebook.add(tab3, text='Добавить матч')
        notebook.add(tab4, text='Поиск')

        self.setup_team_tab(tab1)
        self.setup_player_tab(tab2)
        self.setup_match_tab(tab3)
        self.setup_search_tab(tab4)

    def setup_team_tab(self, parent):
        frame = tk.Frame(parent, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Название команды:").grid(row=0, column=0, sticky='w', pady=5)
        self.team_name = tk.Entry(frame, width=30)
        self.team_name.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Страна:").grid(row=1, column=0, sticky='w', pady=5)
        self.team_country = tk.Entry(frame, width=30)
        self.team_country.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Год основания:").grid(row=2, column=0, sticky='w', pady=5)
        self.team_year = tk.Entry(frame, width=30)
        self.team_year.grid(row=2, column=1, pady=5)

        tk.Button(frame, text="Добавить", command=self.add_team,
                 bg='green', fg='black', width=20).grid(row=3, column=0, columnspan=2, pady=15)

        self.team_result = tk.Text(frame, height=10, width=50)
        self.team_result.grid(row=4, column=0, columnspan=2)

    def add_team(self):
        name = self.team_name.get()
        country = self.team_country.get()
        year = self.team_year.get()

        query = "INSERT INTO teams (team_name, country, founding_year) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (name, country, int(year) if year else None))
        self.conn.commit()

        self.team_name.delete(0, tk.END)
        self.team_country.delete(0, tk.END)
        self.team_year.delete(0, tk.END)

        self.show_teams()
        messagebox.showinfo("Успех", f"Команда '{name}' добавлена!")

    def show_teams(self):
        self.team_result.delete(1.0, tk.END)

        self.cursor.execute("SELECT team_id, team_name, country FROM teams ORDER BY team_id DESC LIMIT 5")
        teams = self.cursor.fetchall()

        self.team_result.insert(tk.END, "ID  | Название\n")
        self.team_result.insert(tk.END, "=" * 40 + "\n")

        for team in teams:
            self.team_result.insert(tk.END, f"{team[0]:<4}| {team[1]}\n")

    def setup_player_tab(self, parent):
        frame = tk.Frame(parent, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Никнейм:").grid(row=0, column=0, sticky='w', pady=5)
        self.player_nick = tk.Entry(frame, width=30)
        self.player_nick.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Настоящее имя:").grid(row=1, column=0, sticky='w', pady=5)
        self.player_name = tk.Entry(frame, width=30)
        self.player_name.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="ID команды:").grid(row=2, column=0, sticky='w', pady=5)
        self.player_team = tk.Entry(frame, width=30)
        self.player_team.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Позиция:").grid(row=3, column=0, sticky='w', pady=5)
        self.player_pos = ttk.Combobox(frame, values=['Carry', 'Mid', 'Offlane', 'Support'], width=28)
        self.player_pos.grid(row=3, column=1, pady=5)

        tk.Button(frame, text="Добавить", command=self.add_player,
                 bg='blue', fg='white', width=20).grid(row=4, column=0, columnspan=2, pady=15)

        self.player_result = tk.Text(frame, height=10, width=50)
        self.player_result.grid(row=5, column=0, columnspan=2)

    def add_player(self):
        nick = self.player_nick.get()
        name = self.player_name.get()
        team_id = self.player_team.get()
        position = self.player_pos.get()

        query = "INSERT INTO players (nickname, real_name, team_id, position) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (nick, name, int(team_id) if team_id else None, position))
        self.conn.commit()

        self.player_nick.delete(0, tk.END)
        self.player_name.delete(0, tk.END)
        self.player_team.delete(0, tk.END)
        self.player_pos.set('')

        self.show_players()
        messagebox.showinfo("Успех", f"Игрок '{nick}' добавлен!")

    def show_players(self):
        self.player_result.delete(1.0, tk.END)

        self.cursor.execute("""
            SELECT p.player_id, p.nickname, t.team_name 
            FROM players p 
            LEFT JOIN teams t ON p.team_id = t.team_id 
            ORDER BY p.player_id DESC LIMIT 5
        """)
        players = self.cursor.fetchall()

        self.player_result.insert(tk.END, "ID  | Никнейм     | Команда\n")
        self.player_result.insert(tk.END, "=" * 45 + "\n")

        for p in players:
            self.player_result.insert(tk.END, f"{p[0]:<4}| {p[1]:<12}| {p[2] or 'N/A'}\n")

    def setup_match_tab(self, parent):
        frame = tk.Frame(parent, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="ID турнира:").grid(row=0, column=0, sticky='w', pady=5)
        self.match_tournament = tk.Entry(frame, width=30)
        self.match_tournament.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="ID команды 1:").grid(row=1, column=0, sticky='w', pady=5)
        self.match_team1 = tk.Entry(frame, width=30)
        self.match_team1.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="ID команды 2:").grid(row=2, column=0, sticky='w', pady=5)
        self.match_team2 = tk.Entry(frame, width=30)
        self.match_team2.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="ID победителя:").grid(row=3, column=0, sticky='w', pady=5)
        self.match_winner = tk.Entry(frame, width=30)
        self.match_winner.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Дата (YYYY-MM-DD):").grid(row=4, column=0, sticky='w', pady=5)
        self.match_date = tk.Entry(frame, width=30)
        self.match_date.grid(row=4, column=1, pady=5)

        tk.Button(frame, text="Добавить", command=self.add_match,
                 bg='purple', fg='white', width=20).grid(row=5, column=0, columnspan=2, pady=15)

        self.match_result = tk.Text(frame, height=8, width=50)
        self.match_result.grid(row=6, column=0, columnspan=2)

    def add_match(self):
        t_id = self.match_tournament.get()
        t1 = self.match_team1.get()
        t2 = self.match_team2.get()
        winner = self.match_winner.get()
        date = self.match_date.get()

        query = "INSERT INTO matches (tournament_id, team1_id, team2_id, winner_id, match_date) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (int(t_id), int(t1), int(t2), int(winner), date or None))
        self.conn.commit()

        self.match_tournament.delete(0, tk.END)
        self.match_team1.delete(0, tk.END)
        self.match_team2.delete(0, tk.END)
        self.match_winner.delete(0, tk.END)
        self.match_date.delete(0, tk.END)

        self.show_matches()
        messagebox.showinfo("Успех", "Матч добавлен!")

    def show_matches(self):
        self.match_result.delete(1.0, tk.END)

        self.cursor.execute("""
            SELECT m.match_id, t1.team_name, t2.team_name, w.team_name
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            JOIN teams w ON m.winner_id = w.team_id
            ORDER BY m.match_id DESC LIMIT 5
        """)
        matches = self.cursor.fetchall()

        self.match_result.insert(tk.END, "ID  | Матч | Победитель\n")
        self.match_result.insert(tk.END, "=" * 50 + "\n")

        for m in matches:
            self.match_result.insert(tk.END, f"{m[0]:<4}| {m[1]} vs {m[2]} | {m[3]}\n")

    def setup_search_tab(self, parent):
        frame = tk.Frame(parent, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Выберите запрос:", font=('Arial', 12, 'bold')).pack(pady=10)

        self.search_var = tk.StringVar(value='teams')

        queries = [
            ('Все команды', 'teams'),
            ('Все игроки', 'players'),
            ('Все матчи', 'matches'),
            ('Игроки с командами', 'players_teams'),
            ('Статистика команд', 'team_stats')
        ]

        for text, value in queries:
            tk.Radiobutton(frame, text=text, variable=self.search_var, value=value).pack(anchor='w')

        tk.Button(frame, text="Выполнить поиск", command=self.execute_search,
                 bg='orange', fg='white', width=20).pack(pady=15)

        self.search_result = tk.Text(frame, height=15, width=70, font=('Courier', 9))
        self.search_result.pack()

    def execute_search(self):
        search_type = self.search_var.get()

        queries = {
            'teams': "SELECT team_id, team_name, country, founding_year FROM teams",
            'players': "SELECT player_id, nickname, real_name, position FROM players",
            'matches': "SELECT match_id, team1_id, team2_id, winner_id, match_date FROM matches",
            'players_teams': """
                SELECT p.nickname, p.real_name, t.team_name, p.position
                FROM players p
                LEFT JOIN teams t ON p.team_id = t.team_id
                ORDER BY t.team_name
            """,
            'team_stats': """
                SELECT t.team_name, COUNT(p.player_id) as players_count
                FROM teams t
                LEFT JOIN players p ON t.team_id = p.team_id
                GROUP BY t.team_name
                ORDER BY players_count DESC
            """
        }

        query = queries[search_type]
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        self.search_result.delete(1.0, tk.END)

        headers = [desc[0] for desc in self.cursor.description]
        header_line = " | ".join(f"{h:15}" for h in headers)
        self.search_result.insert(tk.END, header_line + "\n")
        self.search_result.insert(tk.END, "=" * len(header_line) + "\n")

        # Данные
        for row in results:
            row_line = " | ".join(f"{str(val) if val else 'N/A':15}" for val in row)
            self.search_result.insert(tk.END, row_line + "\n")

        self.search_result.insert(tk.END, f"\nНайдено: {len(results)} записей\n")

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = Dota2App(root)
    root.mainloop()