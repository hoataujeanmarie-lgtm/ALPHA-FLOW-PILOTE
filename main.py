from flask import Flask, render_template_string, request

app = Flask(__name__)

# Tes données réelles (Le Cerveau de ton site)
PILIERS = {
    "or_vert": {
        "titre": "L'OR VERT (Vanille)",
        "info": "500 m² - 130 poteaux",
        "calcul": "Objectif : 13 000 € / mois (13 Unités Alpha)",
        "action": "Vérifier l'humidité des serres et la pousse."
    },
    "lagon": {
        "titre": "LE LAGON (Glamping)",
        "info": "Moorea - 10 tentes Luxe",
        "calcul": "Objectif : 18 800 € / mois (18,8 Unités Alpha)",
        "action": "Lancer le script de réservation 'Eco-Luxury'."
    },
    "ecorce": {
        "titre": "L'ÉCORCE (Faa'a)",
        "info": "Appartement en rénovation",
        "calcul": "Objectif : 1 050 € net / mois (1 Unité Alpha)",
        "action": "Finaliser les finitions pour mise sur Airbnb."
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ALPHA-FLOW | Cockpit Personnel</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e0e0e0; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: #161b22; padding: 30px; border-radius: 20px; border: 1px solid #30363d; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { color: #00ff88; letter-spacing: 2px; }
        .btn-group { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
        .btn-pilier { background: #21262d; color: #00ff88; padding: 15px; border-radius: 10px; border: 1px solid #30363d; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .btn-pilier:hover { background: #30363d; border-color: #00ff88; }
        .resultat { margin-top: 30px; padding: 20px; border: 1px solid #00ff88; background: #0d1117; border-radius: 10px; display: {% if pilier %} block {% else %} none {% endif %}; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ALPHA-FLOW PILOTE</h1>
        <p style="color: #8b949e;">Statut : OMEGA STATUS - Jean-Marie</p>
        
        <form method="POST" class="btn-group">
            <button type="submit" name="pilier" value="or_vert" class="btn-pilier">L'OR VERT (Moore'a)</button>
            <button type="submit" name="pilier" value="lagon" class="btn-pilier">LE LAGON (Glamping)</button>
            <button type="submit" name="pilier" value="ecorce" class="btn-pilier">L'ÉCORCE (Faa'a)</button>
        </form>

        {% if pilier %}
        <div class="resultat">
            <h2 style="color: #00ff88;">{{ pilier.titre }}</h2>
            <p><strong>Détails :</strong> {{ pilier.info }}</p>
            <p style="font-size: 1.2em;"><strong>Finances :</strong> {{ pilier.calcul }}</p>
            <hr style="border: 0.5px solid #30363d; margin: 15px 0;">
            <p style="color: #ffa657;"><strong>PROCHAINE ÉTAPE :</strong> {{ pilier.action }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_pilier = None
    if request.method == 'POST':
        pilier_key = request.form.get('pilier')
        selected_pilier = PILIERS.get(pilier_key)
    return render_template_string(HTML_TEMPLATE, pilier=selected_pilier)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
