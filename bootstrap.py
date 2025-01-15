from dash import Dash, html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Créer l'application Dash avec Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Charger les données
df = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv', on_bad_lines="skip")

# Extraire la liste unique des auteurs
auteurs = df['authors'].unique()

# Layout de l'application
app.layout = dbc.Container([
    # Barre de navigation
    dbc.NavbarSimple(
        brand="Exploration de données",
        brand_href="#",
        color="primary",
        dark=True
    ),

    # Onglets
    dbc.Tabs([
        # Onglet Dataset
        dbc.Tab(
            dbc.Container([
                html.H3("Voici le Dataset"),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{"name": col, "id": col} for col in df.columns],
                    page_size=10,
                    style_table={'overflowX': 'auto'}
                )
            ], fluid=True),
            label="Dataset"
        ),
        
        # Onglet Graph
        dbc.Tab(
            dbc.Container([
                html.H3("Graphique des livres"),

                # Graphique dynamique
                dcc.Graph(
                    id='bar-chart'
                ),

                # Sélecteur d'auteur
                html.Div([
                    html.Label('Sélectionnez un auteur :'),
                    dcc.Dropdown(
                        id='user-choice',
                        options=[{'label': auteur, 'value': auteur} for auteur in auteurs],
                        placeholder="Sélectionnez un auteur"
                    )
                ], style={'margin-bottom': '20px'}),

                # Slider pour le nombre maximal de pages
                html.Div([
                    html.Label('Nombre maximal de pages :'),
                    dcc.Slider(
                        min=df['  num_pages'].min(), 
                        max=df['  num_pages'].max(), 
                        step=200, 
                        value=500,  # Valeur initiale
                        id='input-pages'
                    )
                ], style={'margin-bottom': '20px'})
            ], fluid=True),
            label="Graph"
        )
    ])
], fluid=True)

# Callback pour mettre à jour le graphique dynamiquement
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('user-choice', 'value'),
     Input('input-pages', 'value')]
)
def update_graph(selected_author, max_pages):
    # Filtrer les données
    filtered_df = df.copy()
    if selected_author:
        filtered_df = filtered_df[filtered_df['authors'] == selected_author]
    if max_pages is not None:
        filtered_df = filtered_df[filtered_df['  num_pages'] <= max_pages]

    # Créer un graphique en barres
    fig = px.bar(
        filtered_df,
        x='title',
        y='  num_pages',
        title='Nombre de pages par livre',
        labels={'  num_pages': 'Nombre de pages', 'title': 'Titre'}
    )
    return fig

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
