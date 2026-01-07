from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- CONFIGURATION DES SERVICES (REVENUS VIRTUELS) ---
PRIX_HEURE_CONSEIL = 125 # Env 15.000 FCFP
PRIX_DOSSIER_STRAT = 500 # Env 60.000 FCFP (Analyse de projet tiers)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Suivi des missions en cours (Virtuel)
    missions_conseil = int(request.form.get('missions', 0))
    dossiers_strat = int(request.form.get('dossiers', 0))
    
    # Calcul du CA immatériel généré
    ca_virtuel = (missions_conseil * PRIX_HEURE_CONSEIL) + (dossiers_strat * PRIX_DOSSIER_STRAT)
    
    # Tes revenus passifs physiques restent en fond de sécurité
    revenus_fondation = 1050 + 18800
    total_dispo = revenus_fondation + ca_virtuel

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ALPHA-FLOW | Business Unit</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e0e0e0; padding: 15px; }
            .container { max-width: 500px; margin: auto; }
            .card { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
            .cash-target { border: 2px solid #00ff88; text-align: center; }
            .gold { color: #ffd700; font-weight: bold; font-size: 2em; }
            input { background: #0d1117; color: white; border: 1px solid #30363d; padding: 10px; width: 60px; border-radius: 5px; }
            .btn { background: #238636; color: white; padding: 12px; border: none; border-radius: 6px; width: 100%; cursor: pointer; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #00ff88; text-align:center;">ALPHA-CASH GENERATOR</h1>

            <div class="card cash-target">
                <p>CASH IMMÉDIAT DISPONIBLE</p>
                <div class="gold">{{ total }} €</div>
                <p style="font-size: 0.8em;">(Passif + Services de Conseil)</p>
            </div>

            <form method="POST" class="card">
                <h2>🖋️ Vente d'Expertise (Conseil)</h2>
                <p>Heures de Conseil vendues : <input type="number" name="missions" value="{{ missions }}"></p>
                <p>Dossiers Stratégiques livrés : <input type="number" name="dossiers" value="{{ dossiers }}"></p>
                <button type="submit" class="btn">ACTUALISER LES RENTRÉES</button>
            </form>

            <div class="card">
                <h2>📈 Analyse de Performance</h2>
                <p>CA Services : <span style="color: #00ff88;">+ {{ ca }} €</span></p>
                <p>Marge nette : 100% (Zéro coût physique)</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE, total=total_dispo, ca=ca_virtuel, missions=missions_conseil, dossiers=dossiers_strat)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
