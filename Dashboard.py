# Charger les données depuis le CSV
def load_data():
    try:
        df = pd.read_csv("scraping_data.csv", sep=";")
        df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Heure"])
        df["Prix"] = pd.to_numeric(df["Prix"], errors="coerce")
        return df
    except Exception as e:
        print("Erreur de chargement:", e)
        return pd.DataFrame(columns=["Date", "Heure", "Prix", "DateTime"])

# Créer l'app Dash
app = Dash(__name__)
app.title = "Suivi Prix WTI - Dashboard"

app.layout = html.Div([
    html.H1("Prix du pétrole WTI 📈", style={"textAlign": "center"}),

    dcc.Interval(id="interval", interval=5*60*1000, n_intervals=0),  # refresh toutes les 5 minutes

    dcc.Graph(id="graphique"),

    html.H2("Données récentes"),
    html.Div(id="tableau"),

    html.H2("Rapport du jour (20h)"),
    html.Div(id="rapport")
])

# Callback pour mettre à jour le graphique et les données
@app.callback(
    [   
        dcc.Output("graphique", "figure"),
        dcc.Output("tableau", "children"),
        dcc.Output("rapport", "children")
    ],
    [dcc.Input("interval", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()

    if df.empty:
        return {}, "Aucune donnée disponible.", "Aucune donnée pour le rapport."

    # Graph
    fig = px.line(df, x="DateTime", y="Prix", title="Évolution du prix du WTI", markers=True)

    # Tableau HTML
    table = html.Table([
        html.Tr([html.Th(col) for col in ["Date", "Heure", "Prix"]])
    ] + [
        html.Tr([html.Td(df.iloc[i][col]) for col in ["Date", "Heure", "Prix"]])
        for i in range(len(df)-1, max(len(df)-11, -1), -1)
    ])

    # Rapport quotidien si après 20h
    now = datetime.datetime.now()
    rapport = "Le rapport sera disponible à 20h."
    if now.hour >= 20 and not df.empty:
        df_today = df[df["Date"] == now.strftime("%Y-%m-%d")]
        if not df_today.empty:
            open_price = df_today["Prix"].iloc[0]
            close_price = df_today["Prix"].iloc[-1]
            min_price = df_today["Prix"].min()
            max_price = df_today["Prix"].max()
            mean_price = df_today["Prix"].mean()
            evolution = ((close_price - open_price) / open_price) * 100

            rapport = html.Ul([
                html.Li(f"Prix d'ouverture : {open_price:.2f}"),
                html.Li(f"Prix de clôture : {close_price:.2f}"),
                html.Li(f"Évolution : {evolution:.2f} %"),
                html.Li(f"Min : {min_price:.2f}"),
                html.Li(f"Max : {max_price:.2f}"),
                html.Li(f"Moyenne : {mean_price:.2f}")
            ])

    return fig, table, rapport

# Lancer le serveur
if __name__ == "__main__":
    app.run_server(debug=True)
