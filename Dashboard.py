import pandas as pd
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import datetime

# Charger les données depuis le CSV
def load_data():
    try:
        df = pd.read_csv("scraping_data.csv", sep=";", names=["DateTime", "Prix"])
        df["DateTime"] = pd.to_datetime(df["DateTime"], dayfirst=True)
        df["Date"] = df["DateTime"].dt.strftime("%Y-%m-%d")
        df["Heure"] = df["DateTime"].dt.strftime("%H:%M:%S")
        df["Prix"] = pd.to_numeric(df["Prix"], errors="coerce")
        df = df.dropna(subset=["Prix"])
        return df
    except Exception as e:
        print("Erreur de chargement:", e)
        return pd.DataFrame(columns=["DateTime", "Date", "Heure", "Prix"])

# Créer l'app Dash
app = Dash(__name__)
app.title = "Suivi Prix WTI - Dashboard"

# Ajouter du CSS externe pour améliorer le style
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

# Mise en page du dashboard
app.layout = html.Div([
    html.H1("🛢️ Prix du pétrole WTI 📈📉", style={"textAlign": "center", "color": "#333"}),

    dcc.Interval(id="interval", interval=5*60*1000, n_intervals=0),

    dcc.Graph(id="graphique", style={"height": "500px"}),

    html.H2("📊 Données récentes", style={"textAlign": "center", "marginTop": "20px"}),
    dash_table.DataTable(
        id="tableau",
        columns=[
            {"name": "Date", "id": "Date"},
            {"name": "Heure", "id": "Heure"},
            {"name": "Prix", "id": "Prix"}
        ],
        style_table={"overflowX": "auto", "margin": "0 auto", "width": "80%"},
        style_cell={"textAlign": "center", "padding": "10px"},
        style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#f9f9f9"}
        ],
        page_size=10
    ),

    html.H2("📅 Rapport du jour :", style={"textAlign": "center", "marginTop": "20px"}),
    html.Div(id="rapport", style={"textAlign": "center", "marginBottom": "20px"})
], style={"padding": "20px", "fontFamily": "Arial, sans-serif"})

# Callback pour mettre à jour le dashboard
@app.callback(
    [
        Output("graphique", "figure"),
        Output("tableau", "data"),
        Output("rapport", "children")
    ],
    [Input("interval", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()

    if df.empty:
        return {}, [], "Aucune donnée disponible."

    fig = px.line(
        df,
        x="DateTime",
        y="Prix",
        title="Évolution du prix du WTI",
        markers=True,
        template="plotly_white"
    )
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center"},
        xaxis_title="Date et Heure",
        yaxis_title="Prix (USD)",
        font=dict(size=14),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    fig.update_traces(line_color="#1f77b4", marker=dict(size=8))

    recent_data = df[["Date", "Heure", "Prix"]].tail(10).iloc[::-1].to_dict("records")

    now = datetime.datetime.now()
    df_today = df[df["Date"] == now.strftime("%Y-%m-%d")]

    if not df_today.empty and now.hour >= 20:
        open_price = df_today["Prix"].iloc[0]
        close_price = df_today["Prix"].iloc[-1]
        min_price = df_today["Prix"].min()
        max_price = df_today["Prix"].max()
        mean_price = df_today["Prix"].mean()
        volatility = df_today["Prix"].std()
        evolution = ((close_price - open_price) / open_price) * 100

        rapport = html.Ul([
            html.Li(f"📈 Prix d'ouverture : {open_price:.2f} USD", style={"color": "#333"}),
            html.Li(f"📉 Prix de clôture : {close_price:.2f} USD", style={"color": "#333"}),
            html.Li(f"📊 Évolution : {evolution:.2f} %", style={"color": "green" if evolution >= 0 else "red"}),
            html.Li(f"🔻 Min : {min_price:.2f} USD", style={"color": "#333"}),
            html.Li(f"🔺 Max : {max_price:.2f} USD", style={"color": "#333"}),
            html.Li(f"📐 Moyenne : {mean_price:.2f} USD", style={"color": "#333"}),
            html.Li(f"🔀 Volatilité : {volatility:.4f}", style={"color": "#333"})
        ], style={"listStyleType": "none", "padding": "0"})
    else:
        rapport = "Le rapport du jour sera disponible à partir de 20h."

    return fig, recent_data, rapport

# Lancer le serveur
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
