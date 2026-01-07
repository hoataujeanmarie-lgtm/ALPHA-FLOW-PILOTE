from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- PARAMÈTRES DE L'EMPIRE (Lois de Zoran) ---
NB_POTEAUX = 70
RENDEMENT = 0.37
PRIX_BASE = 600
MARGE_LOG_VANILLE = 0.35 # Fret, main d'oeuvre, EPIC

# --- CHARGES FIXES (Vie, Matériel, Fiscalité) ---
# Estimation mensuelle de tes dépenses réelles
FRAIS_MATERIEL = 150   # Maintenance Bobcat 331, Tracteur, Carburant
FRAIS_DEPLACEMENT = 200 # Vaiare Moorea/Tahiti tous les weekends
COURSES_VIE = 600      # Alimentation et perso
IMPOTS_ASSURANCES = 300 # Provision fiscale et assurances
CHARGES_FIXES_TOTAL = FRAIS_MATERIEL + FRAIS_DEPLACEMENT + COURSES_VIE + IMPOTS_ASSURANCES

@app.route('/', methods=['GET', 'POST'])
def home():
    alerte_cyclone = request.form.get('alerte') == 'ON'
    prix_ajuste = int(request.form.get('prix_marche', PRIX_BASE))
    
    coeff_meteo = 0.5 if alerte_cyclone else 0.85 
    
    # Rentrées Vanille (Net d'exploitation)
    net_annuel_vanille = (NB_POTEAUX * RENDEMENT * prix_ajuste * coeff_meteo * (1 - MARGE_LOG_VANILLE)) - 1500
    net_mensuel_vanille = int(max(0, net_annuel_vanille // 12))
    
    # Rentrées Immobilières
    flux_immobilier = 1050 + 18800 
    
    # CALCUL FINAL : Rentrée d'argent nette de TOUT
    total_rentrees = flux_immobilier + net_mensuel_vanille
    reste_a_vivre = total_rentrees - CHARGES_FIXES_TOTAL

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ALPHA-FLOW | Analyse Zoran</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0b1218; color: #e0e0e0; padding: 10px; }
            .container { max-width: 550px; margin: auto; }
            .card { background: #1c252e; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
            .gold { color: #ffd700; font-weight: bold; font-size: 1.8em; }
            .red { color: #ff6b6b; font-size: 0.9em; }
            .green { color: #00ff88; font-weight: bold; }
            h2 { color: #00ff88; font-size: 1.1em; border-bottom: 1px solid #333; padding-bottom: 5px; margin-top: 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #00ff88; text-align: center;">ALPHA-FLOW</h1>

            <form method="POST" class="card">
                <h2>⚙️ Variables de Terrain</h2>
                <p>Prix Vanille : <input type="number" name="prix_marche" value="{{ prix }}" style="width:60px;"> €/kg</p>
                <p>Météo : <button type="submit" name="alerte" value="{{ 'OFF' if alerte else 'ON' }}">{{ '⚠️ CYCLONE' if alerte else '✅ NORMAL' }}</button></p>
                <button type="submit" style="width:100%; margin-top:10px; cursor:pointer;">RECALCULER</button>
            </form>

            <div class="card" style="border-color: #ffd700; text-align: center;">
                <h2 style="color: #ffd700;">UNITÉS ALPHA : {{ reste // 1000 }}</h2>
                <p class="gold">{{ "{:,}".format(reste).replace(',', ' ') }} € / mois</p>
                <p style="font-size: 0.8em; color: #8b949e;">Argent disponible après toutes dépenses personnelles et pro.</p>
            </div>

            <div class="card">
                <h2>📈 Rentrées (Brut Net)</h2>
                <ul>
                    <li>Immobilier : <span class="green">19 850 €</span></li>
                    <li>Vanille (estimée) : <span class="green">{{ vanille }} €</span></li>
                </ul>
                <hr style="border:0.5px solid #333;">
                <h2>📉 Dépenses Mensuelles</h2>
                <ul>
                    <li class="red">Vie (Courses, Perso) : -600 €</li>
                    <li class="red">Logistique (Vaiare, Tracteur) : -350 €</li>
                    <li class="red">Impôts & Assurances : -300 €</li>
                </ul>
            </div>

            <div class="card">
                <h2>🛠️ État de la Flotte</h2>
                <p>• <b>Bobcat 331 :</b> Prévoir révision hydraulique.</p>
                <p>• <b>Petit Tracteur :</b> Entretien moteur avant récolte.</p>
                <p>• <b>Vaiare :</b> Rotation Moorea-Tahiti WE.</p>
            </div>

            <p style="text-align: center; font-size: 0.7em; color: #444;">PROTOCOLE OMEGA | LOI DE STRUCTURE</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE, reste=reste_a_vivre, vanille=net_mensuel_vanille, prix=prix_ajuste, alerte=alerte_cyclone)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
