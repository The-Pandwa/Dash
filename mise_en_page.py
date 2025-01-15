from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# Initialiser l'application Dash
app = Dash(__name__)

# Charger les données à partir du lien fourni
df = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv', on_bad_lines="skip")

# Garder seulement les 10 premiers livres
df = df.head(10)

# Créer un graphique en barres avec Plotly Express
fig = px.bar(df, x='title', y='  num_pages', title='Nombre de pages par livre')

# Extraire la liste unique des auteurs
auteurs = df['authors'].unique()

# Layout de l'application
app.layout = html.Div([
    # Titre principal
    html.H1("Bibliothèque de Livres"),
    
    # Graphique
    dcc.Graph(
        id='bar-chart',
        figure=fig  # Graphique en barres
    ),
    
    # Sélecteur d'auteur
    html.Label('Sélectionnez un auteur :'),
    dcc.Dropdown(
        id='select-auteur',
        options=[{'label': auteur, 'value': auteur} for auteur in auteurs],
        placeholder="Choisissez un auteur"
    ),
    
    # Entrée pour le nombre maximal de pages
    html.Label('Nombre maximal de pages :'),
    dcc.Input(
        id='input-pages',
        type='number',
        placeholder="Entrez un nombre"
    )
])

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
