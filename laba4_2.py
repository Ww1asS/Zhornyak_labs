from dash import Dash, dcc, html, Input, Output
import pandas as pd
import psycopg2
import plotly.express as px
import seaborn as sb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

connection = psycopg2.connect(user='postgres', password='7526', host='localhost', port='5432', database='dota2_tournaments')
df_teams = pd.read_sql('SELECT * FROM teams', connection)
df_matches = pd.read_sql('SELECT * FROM matches', connection)
df_stats = pd.read_sql('SELECT * FROM player_statistics', connection)
df_tournaments = pd.read_sql('SELECT * FROM tournaments', connection)
connection.close()

wins_df = pd.DataFrame({'team_name': df_teams['team_name'], 'wins': [len(df_matches[df_matches['winner_id'] == i]) for i in df_teams['team_id']]})

app = Dash(__name__)
app.layout = html.Div([
    html.H1('Анализ Dota 2'),
    dcc.Dropdown(id='graph', options=[
        {'label': 'Plotly: Призовые команд', 'value': 'money'},
        {'label': 'Plotly: Длительность матчей', 'value': 'time'},
        {'label': 'Plotly: Kills vs Deaths', 'value': 'kd'},
        {'label': 'Plotly: Победы команд', 'value': 'wins'},
        {'label': 'Seaborn: Распределение kills', 'value': 'sk'},
        {'label': 'Seaborn: Призовые команд', 'value': 'sm'},
        {'label': 'Seaborn: Kills vs Assists', 'value': 'ska'},
        {'label': 'Seaborn: Призовой фонд у турниров', 'value': 'priz'}
    ],
        value='money', clearable=False),
    dcc.Graph(id='plotly-out'),
    html.Img(id='seaborn-out', style={'width': '100%', 'maxWidth': '900px'})
])

@app.callback(Output('plotly-out', 'figure'), Output('seaborn-out', 'src'), Input('graph', 'value'))
def update(g):
    if g == 'money':
        return px.bar(df_teams, x='team_name', y='total_prize_money', title='Призовые команд'), ''
    if g == 'time':
        return px.line(df_matches, x='duration_minutes', title='Длительность матчей'), ''
    if g == 'kd':
        return px.pie(df_stats, values='kills', names='player_id', title='Kills vs Deaths'), ''
    if g == 'wins':
        return px.bar(wins_df, x='team_name', y='wins', title='Победы команд'), ''

    fig, ax = plt.subplots(figsize=(10, 5))
    if g == 'sk':
        sb.histplot(df_stats['kills'], bins=20, kde=True, ax=ax)
        ax.set_title('Распределение kills')
    elif g == 'sm':
        sb.barplot(data=df_teams, x='team_name', y='total_prize_money', ax=ax)
        ax.set_title('Призовые команд')
        ax.tick_params(axis='x', rotation=45)
    elif g == 'priz':
        sb.barplot(data=df_tournaments, x='tournament_id', y='prize_pool')
    else:
        sb.scatterplot(data=df_stats, x='kills', y='assists', ax=ax)
        ax.set_title('Kills vs Assists')

    buf = io.BytesIO(); plt.tight_layout(); fig.savefig(buf, format='png', bbox_inches='tight'); plt.close(fig)
    img = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
    return {}, img


app.run(debug=True)