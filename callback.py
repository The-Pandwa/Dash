from dash import Dash, html, dcc, Output, Input, State
import pandas as pd
import plotly.express as px

# Initialiser l'application Dash
app = Dash(__name__)

# Charger les données à partir du lien fourni
df = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv', on_bad_lines="skip")

# Extraire la liste unique des auteurs
auteurs = df['authors'].unique()

# Callback pour mettre à jour le graphique dynamiquement
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('user-choice', 'value'),
     Input('input-pages', 'value')]
)
def update_graph(selected_author, max_pages):
    # Filtrer les données en fonction des entrées utilisateur
    filtered_df = df.copy()
    if selected_author:
        filtered_df = filtered_df[filtered_df['authors'] == selected_author]
    if max_pages is not None:
        filtered_df = filtered_df[filtered_df['  num_pages'] <= max_pages]

    # Créer un graphique en barres avec les données filtrées
    fig = px.bar(
        filtered_df,
        x='title',
        y='  num_pages',
        title='Nombre de pages par livre',
        labels={'  num_pages': 'Nombre de pages', 'title': 'Titre'}
    )
    return fig

# Layout de l'application
app.layout = html.Div([
    # Titre principal
    html.H1("Bibliothèque de Livres"),

    # Graphique
    dcc.Graph(
        id='bar-chart'  # Graphique dynamique
    ),

    # Sélecteur d'auteur
    html.Label('Sélectionnez un auteur :'),
    dcc.Dropdown(
        id='user-choice',
        options=[{'label': auteur, 'value': auteur} for auteur in auteurs],
        placeholder="Sélectionnez un auteur"
    ),

    # Entrée pour le nombre maximal de pages
    html.Label('Nombre maximal de pages :'),
    dcc.Slider(
        min=df['  num_pages'].min(),
        max=df['  num_pages'].max(),
        step=200,
        value=500,  # Valeur initiale
        id='input-pages'
    ),
])

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
