from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- CONFIGURATION EXPERT L'OR VERT ---
NB_POTEAUX = 130
RENDEMENT_VERT_PAR_POTEAU = 1.5 # kg
RATIO_TRANSFORMATION = 0.25 # 4kg vert -> 1kg préparé
PRIX_AU_KG_PREPARE = 600 # Prix Luxe en Euro (approx 71,000 FCFP)

def calcul_vanille():
    total_vert = NB_POTEAUX * RENDEMENT_VERT_PAR_POTEAU
    total_prepare = total_vert * RATIO_TRANSFORMATION
    revenu_annuel = total_prepare * PRIX_AU_KG_PREPARE
    return int(revenu_annuel / 12) # Revenu mensuel

PILIERS = {
    "or_vert": {
        "titre": "L'OR VERT (Vanille)",
        "info": f"{NB_POTEAUX} poteaux en production",
        "revenu": calcul_vanille(),
        "detail": f"Récolte estimée : {int(NB_POTEAUX * 1.5 * 0.25)} kg préparés / an",
        "action": "Priorité : Maîtrise de l'humidité et pollinisation manuelle."
    },
    "lagon": {"titre": "LE LAGON (Glamping)", "info": "10 tentes - Moorea", "revenu": 18800, "detail": "Objectif : 18 800 € / mois", "action": "Planification des plateformes."},
    "ecorce": {"titre": "L'ÉCORCE (Faa'a)", "info": "Appartement Airbnb", "revenu": 1050, "detail": "Objectif : 1 050 € / mois", "action": "Peinture et décoration."}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ALPHA-FLOW | Expert</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e0e0e0; text-align: center; padding: 10px; }
        .container { max-width: 500px; margin: auto; background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; }
        h1 { color: #00ff88; }
        .btn-group { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; }
        .btn { background: #21262d; color: #00ff88; padding: 15px; border-radius: 8px; border: 1px solid #30363d; cursor: pointer; font-weight: bold; }
        .btn-gold { border-color: #ffd700; color: #ffd700; }
        .resultat { margin-top: 20px; padding: 15px; border: 1px solid #00ff88; background: #0d1117; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ALPHA-FLOW PILOTE</h1>
        <form method="POST" class="btn-group">
            <button type="submit" name="pilier" value="or_vert" class="btn">L'OR VERT (Expert)</button>
            <button type="submit" name="pilier" value="lagon" class="btn">LE LAGON</button>
            <button type="submit" name="pilier" value="ecorce" class="btn">L'ÉCORCE</button>
            <button type="submit" name="pilier" value="liberte" class="btn btn-gold">☀️ OBJECTIF LIBERTÉ</button>
        </form>

        {% if vue == 'pilier' %}
        <div class="resultat">
            <h2 style="color: #00ff88;">{{ data.titre }}</h2>
            <p>{{ data.info }}</p>
            <p><strong>Revenu estimé : {{ "{:,}".format(data.revenu).replace(',', ' ') }} € / mois</strong></p>
            <p style="font-size: 0.9em; color: #8b949e;">{{ data.detail }}</p>
            <p style="color: #ffa657;"><strong>Action :</strong> {{ data.action }}</p>
        </div>
        {% elif vue == 'liberte' %}
        <div class="resultat" style="border-color: #ffd700;">
            <h2 style="color: #ffd700;">PROJET BOUSSOLE</h2>
            <p>Potentiel Total : <strong>{{ "{:,}".format(total).replace(',', ' ') }} € / mois</strong></p>
            <p>Indicateur : <strong>{{ total // 1000 }} Unités Alpha</strong></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    vue, data = None, None
    total_revenu = sum(p['revenu'] for p in PILIERS.values())
    if request.method == 'POST':
        key = request.form.get('pilier')
        if key == 'liberte': vue = 'liberte'
        else: vue, data = 'pilier', PILIERS.get(key)
    return render_template_string(HTML_TEMPLATE, vue=vue, data=data, total=total_revenu)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
