from flask import Flask, render_template_string, request

app = Flask(__name__)

# Tes Piliers de l'Empire
PILIERS = {
    "or_vert": {
        "titre": "L'OR VERT (Vanille)",
        "info": "130 poteaux - Moorea",
        "revenu": 13000,
        "detail": "Objectif : 13 000 € / mois",
        "action": "Vérifier la pollinisation et l'humidité."
    },
    "lagon": {
        "titre": "LE LAGON (Glamping)",
        "info": "10 tentes - Vaianae",
        "revenu": 18800,
        "detail": "Objectif : 18 800 € / mois",
        "action": "Préparer le terrain pour les premières tentes."
    },
    "ecorce": {
        "titre": "L'ÉCORCE (Faa'a)",
        "info": "Appartement Airbnb",
        "revenu": 10500,
        "detail": "Objectif : 1 050 € / mois",
        "action": "Finir les travaux de peinture."
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ALPHA-FLOW | Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e0e0e0; text-align: center; padding: 10px; }
        .container { max-width: 500px; margin: auto; background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; }
        h1 { color: #00ff88; font-size: 1.5em; }
        .btn-group { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; }
        .btn { background: #21262d; color: #00ff88; padding: 15px; border-radius: 8px; border: 1px solid #30363d; cursor: pointer; font-weight: bold; text-transform: uppercase; }
        .btn-gold { border-color: #ffd700; color: #ffd700; background: #1c1c1c; }
        .resultat { margin-top: 20px; padding: 15px; border: 1px solid #00ff88; background: #0d1117; border-radius: 10px; }
        .liberte { border-color: #ffd700; color: #ffd700; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ALPHA-FLOW PILOTE</h1>
        <p style="color: #8b949e;">Propriétaire : Jean-Marie</p>

        <form method="POST" class="btn-group">
            <button type="submit" name="pilier" value="or_vert" class="btn">L'OR VERT</button>
            <button type="submit" name="pilier" value="lagon" class="btn">LE LAGON</button>
            <button type="submit" name="pilier" value="ecorce" class="btn">L'ÉCORCE</button>
            <button type="submit" name="pilier" value="liberte" class="btn btn-gold">☀️ OBJECTIF LIBERTÉ</button>
        </form>

        {% if vue == 'pilier' %}
        <div class="resultat">
            <h2 style="color: #00ff88;">{{ data.titre }}</h2>
            <p>{{ data.info }}</p>
            <p><strong>{{ data.detail }}</strong></p>
            <p style="color: #ffa657;">Étape : {{ data.action }}</p>
        </div>
        {% elif vue == 'liberte' %}
        <div class="resultat liberte">
            <h2>PROJET BOUSSOLE</h2>
            <p>Potentiel Total : <strong>{{ total }} € / mois</strong></p>
            <p>Soit <strong>{{ total // 1000 }} Unités Alpha</strong></p>
            <hr style="border: 0.5px solid #ffd700;">
            <p><em>"La liberté de Stéphanie commence ici."</em></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    vue = None
    data = None
    total_revenu = sum(p['revenu'] for p in PILIERS.values())
    
    if request.method == 'POST':
        pilier_key = request.form.get('pilier')
        if pilier_key == 'liberte':
            vue = 'liberte'
        else:
            vue = 'pilier'
            data = PILIERS.get(pilier_key)
            
    return render_template_string(HTML_TEMPLATE, vue=vue, data=data, total=total_revenu)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
