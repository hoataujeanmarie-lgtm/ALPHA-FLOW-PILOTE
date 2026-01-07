from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- DONNÉES DE STRUCTURE ---
REVENUS_PASSIFS = 1050 + 18800 # Faa'a + Moorea Campsite
CHARGES_VIE_ET_FIXES = 1250    # Courses, Vaiare, Assurances, Impôts
DEPENSES_MATERIEL_MOY = 150    # Bobcat, Tracteur, Outillage

@app.route('/', methods=['GET', 'POST'])
def home():
    # Variables de terrain
    prix_marche = int(request.form.get('prix_marche', 600))
    etat_matériel = request.form.get('etat_matériel', 'OK')
    alerte_cyclone = request.form.get('alerte') == 'ON'

    # --- ALGORITHME DE RENDEMENT ---
    # Si le Bobcat est en panne, le rendement vanille baisse de 20% (retard maintenance)
    coeff_matos = 0.8 if etat_matériel == 'PANNE' else 1.0
    coeff_meteo = 0.5 if alerte_cyclone else 0.85
    
    production_vanille = (70 * 0.37) * coeff_meteo * coeff_matos
    net_vanille_mensuel = int(((production_vanille * prix_marche) * 0.65 - 1500) // 12)
    
    # CALCUL DE SURVIE (Le score Insubmersible)
    total_rentrees = REVENUS_PASSIFS + net_vanille_mensuel
    cash_flow_libre = total_rentrees - CHARGES_VIE_ET_FIXES - DEPENSES_MATERIEL_MOY
    
    # Loi de Zoran : Ratio Indépendance (Revenus Passifs / Charges de vie)
    ratio_survie = round(REVENUS_PASSIFS / (CHARGES_VIE_ET_FIXES + DEPENSES_MATERIEL_MOY), 1)

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ALPHA-FLOW EXPERT</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0b1218; color: #e0e0e0; padding: 10px; }
            .container { max-width: 500px; margin: auto; }
            .card { background: #1c252e; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
            .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
            .gold { color: #ffd700; font-weight: bold; font-size: 1.4em; }
            .insubmersible { border: 2px solid #00ff88; text-align: center; }
            .warning { color: #ff6b6b; font-weight: bold; }
            select, input { background: #0b1218; color: #fff; border: 1px solid #444; padding: 5px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #00ff88; text-align:center;">ALPHA-FLOW EXPERT</h1>

            <form method="POST" class="card">
                <h2>🛰️ État du Système</h2>
                <div class="stat-grid">
                    <div>Prix Vanille: <input type="number" name="prix_marche" value="{{ prix }}" style="width:60px;"></div>
                    <div>Matériel: 
                        <select name="etat_matériel">
                            <option value="OK" {% if matos == 'OK' %}selected{% endif %}>Opérationnel</option>
                            <option value="PANNE" {% if matos == 'PANNE' %}selected{% endif %}>Bobcat/Tract. HS</option>
                        </select>
                    </div>
                </div>
                <button type="submit" style="width:100%; margin-top:10px; background:#238636; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">Lancer l'Analyse</button>
            </form>

            <div class="card insubmersible">
                <p>SCORE D'INDÉPENDANCE</p>
                <div class="gold" style="font-size: 2.5em;">x {{ ratio }}</div>
                <p>Tes revenus passifs couvrent <b>{{ ratio }} fois</b> ton train de vie.</p>
            </div>

            <div class="card">
                <h2>💸 Cash-Flow Libre (Net-Net)</h2>
                <p class="gold">{{ "{:,}".format(cash).replace(',', ' ') }} € / mois</p>
                <p style="font-size: 0.8em; color: #8b949e;">C'est l'argent qui reste après avoir tout payé (nourriture, matériel, impôts, Vaiare).</p>
                {% if matos == 'PANNE' %}<p class="warning">⚠️ Production Vanille impactée par panne matériel.</p>{% endif %}
            </div>

            <div class="card">
                <h2>🧭 Boussole Unités Alpha</h2>
                <p class="gold">{{ cash // 1000 }} Unités Alpha réelles</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE, prix=prix_marche, matos=etat_matériel, cash=cash_flow_libre, ratio=ratio_survie)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
