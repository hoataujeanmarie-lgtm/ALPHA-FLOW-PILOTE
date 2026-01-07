from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- DONNÉES DE BASE ---
NB_POTEAUX = 70
RENDEMENT = 0.37
PRIX_MARCHE_BASE = 600 
MARGE_LOGISTIQUE = 0.35

@app.route('/', methods=['GET', 'POST'])
def home():
    # --- LOGIQUE DE CALCUL ---
    alerte_cyclone = request.form.get('alerte') == 'ON'
    prix_ajuste = int(request.form.get('prix_marche', PRIX_MARCHE_BASE))
    
    coeff_meteo = 0.5 if alerte_cyclone else 0.85
    net_annuel = (NB_POTEAUX * RENDEMENT * prix_ajuste * coeff_meteo * (1 - MARGE_LOGISTIQUE)) - 1500
    net_mensuel = int(max(0, net_annuel // 12))
    total_mensuel = 1050 + 18800 + net_mensuel

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ALPHA-FLOW | Dashboard Total</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0b1218; color: #e0e0e0; padding: 10px; }
            .container { max-width: 550px; margin: auto; }
            .card { background: #1c252e; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
            .alerte-card { border: 2px solid {% if alerte %} #ff4b2b {% else %} #00ff88 {% endif %}; }
            .btn { background: #21262d; color: #00ff88; padding: 10px; border-radius: 5px; border: 1px solid #30363d; cursor: pointer; width: 100%; margin-top: 10px; font-weight: bold;}
            .input-prix { background: #0b1218; color: #ffd700; border: 1px solid #30363d; width: 60px; padding: 5px; border-radius: 4px; }
            .gold { color: #ffd700; font-size: 1.5em; font-weight: bold; }
            h2 { color: #00ff88; border-bottom: 1px solid #333; padding-bottom: 5px; margin-top: 0; }
            h3 { margin-top: 0; }
            ul { padding-left: 20px; color: #8b949e; font-size: 0.9em; }
            li { margin-bottom: 8px; }
            .badge { background: #30363d; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; color: #ffd700; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #00ff88; text-align: center;">ALPHA-FLOW</h1>
            
            <form method="POST">
                <div class="card alerte-card">
                    <h3>🛠️ Paramètres & Risques</h3>
                    <p>Prix Marché : <input type="number" name="prix_marche" value="{{ prix }}" class="input-prix"> €/kg</p>
                    <p>Alerte Cyclone : 
                       <button type="submit" name="alerte" value="{{ 'OFF' if alerte else 'ON' }}" 
                               style="background: {{ '#ff4b2b' if alerte else '#21262d' }}; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                               {{ 'DÉSACTIVER' if alerte else 'ACTIVER' }}
                       </button>
                    </p>
                    <button type="submit" class="btn">ACTUALISER LES UNITÉS ALPHA</button>
                </div>
            </form>

            <div class="card" style="border-color: #ffd700; text-align: center;">
                <h2 style="color: #ffd700;">SOLVABILITÉ : {{ total // 1000 }} UNITÉS</h2>
                <p class="gold">{{ total }} € / mois</p>
                <p style="font-size: 0.8em; color: #8b949e;">(Après charges, logistique et risques)</p>
            </div>

            <div class="card">
                <h2>🌿 Production (L'Or Vert)</h2>
                <ul>
                    <li><b>Pollinisation :</b> Mariage des fleurs (Prévu Mai-Août).</li>
                    <li><b>Maintenance :</b> Vérification humidité et structure des 70 poteaux.</li>
                    <li><b>Santé :</b> Traitement escargots et champignons (hebdomadaire).</li>
                </ul>
            </div>

            <div class="card">
                <h2>🚢 Logistique & Dépenses</h2>
                <ul>
                    <li><b>Fret :</b> Budget Moorea-Tahiti (Marchandises/Matériel).</li>
                    <li><b>Institutionnel :</b> Cotisation Agricole + Label EPIC Vanille.</li>
                    <li><b>Main d'oeuvre :</b> Ponctuelle pour les gros travaux de serre.</li>
                </ul>
            </div>

            <div class="card">
                <h2>📅 Calendrier</h2>
                <ul>
                    <li><span class="badge">JAN</span> Suivi chantier Faa'a (Peinture).</li>
                    <li><span class="badge">JUIN</span> Récolte et préparation 1ère tranche Vanille.</li>
                    <li><span class="badge">MI-2026</span> Extension : +60 poteaux (3 serres 100m²).</li>
                </ul>
            </div>

        </div>
    </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE, 
                                 total=total_mensuel, 
                                 net_m=net_mensuel, 
                                 prix=prix_ajuste, 
                                 alerte=alerte_cyclone)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
