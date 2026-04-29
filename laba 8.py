import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import folium

objects = [
    {"name": "Битцевский лес",    "lat": 55.6254670740427,  "lon": 37.56014895645482, "type": "Парк",          "area_ha": 2200, "year": 1994},
    {"name": "Концертный зал BASE","lat": 55.70971814245301, "lon": 37.5952817480515,  "type": "Культура",      "area_ha": 1,    "year": 2012},
    {"name": "Живописный мост",   "lat": 55.77621080718898, "lon": 37.44340936712159, "type": "Достопримечательность", "area_ha": 0, "year": 2007},
    {"name": "Профсоюзная улица", "lat": 55.63341723656918, "lon": 37.519767373462486,"type": "Транспорт",     "area_ha": 0,    "year": 1960},
]
df = pd.DataFrame(objects)

m = folium.Map(location=[55.72, 37.52], tiles='openstreetmap', zoom_start=11)

folium.CircleMarker(
    location=[55.6254670740427, 37.56014895645482],
    radius=30, color='green', fill=True, fill_color='green', fill_opacity=0.4,
    popup='Битцевский лес', tooltip='Битцевский лес'
).add_to(m)

folium.Marker(
    location=[55.70971814245301, 37.5952817480515],
    popup='Концертный зал BASE',
    tooltip='Концертный зал BASE',
    icon=folium.Icon(color='blue', icon='music', prefix='fa')
).add_to(m)

folium.Marker(
    location=[55.77621080718898, 37.44340936712159],
    popup='Живописный мост',
    tooltip='Живописный мост',
    icon=folium.Icon(color='red', icon='camera', prefix='fa')
).add_to(m)

folium.PolyLine(
    locations=[
        [55.638, 37.519], [55.635, 37.519], [55.633, 37.520], [55.630, 37.520]
    ],
    color='orange', weight=5,
    popup='Профсоюзная улица',
    tooltip='Профсоюзная улица'
).add_to(m)

m.save('map.html')

fig_bar = px.bar(df, x='name', y='area_ha', color='type',
                 title='Площадь объектов (га)',
                 labels={'name': 'Объект', 'area_ha': 'Площадь (га)', 'type': 'Тип'})
fig_bar.update_layout(xaxis_tickangle=-15)

fig_pie = px.pie(df, names='type', title='Типы объектов',
                 color_discrete_sequence=px.colors.qualitative.Set2)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('ГИС-система: объекты Москвы', style={'textAlign': 'center', 'fontFamily': 'Arial'}),

    html.H3('Карта объектов', style={'fontFamily': 'Arial'}),
    html.Iframe(
        srcDoc=open('map.html', 'r', encoding='utf-8').read(),
        style={'width': '100%', 'height': '500px', 'border': 'none'}
    ),

    html.H3('Таблица объектов', style={'fontFamily': 'Arial', 'marginTop': '20px'}),
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {'name': 'Название',    'id': 'name'},
            {'name': 'Тип',         'id': 'type'},
            {'name': 'Год',         'id': 'year'},
            {'name': 'Площадь (га)','id': 'area_ha'},
        ],
        style_cell={'fontFamily': 'Arial', 'textAlign': 'left', 'padding': '8px'},
        style_header={'backgroundColor': '#2c7fb8', 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#f0f4f8'}],
        page_size=10
    ),

    html.H3('Статистика', style={'fontFamily': 'Arial', 'marginTop': '20px'}),
    html.Div([
        html.Div(dcc.Graph(figure=fig_bar), style={'width': '60%'}),
        html.Div(dcc.Graph(figure=fig_pie), style={'width': '38%'}),
    ], style={'display': 'flex', 'gap': '2%'}),

], style={'maxWidth': '1100px', 'margin': 'auto', 'padding': '20px', 'fontFamily': 'Arial'})


app.run(debug=True)