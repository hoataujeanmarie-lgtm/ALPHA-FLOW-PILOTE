from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- CONFIGURATION DE L'EMPIRE (JEAN-MARIE) ---
NB_POTEAUX = 70
RENDEMENT_THEORIQUE = 0.37 
PRIX_BASE = 600
MARGE_LOGISTIQUE = 0.35
FRAIS_FIXES_ANNUELS = 1500

@app.route('/', methods=['GET', 'POST'])
def home():
    # --- LOGIQUE DU CALCULATEUR ---
    alerte_cyclone = request.form.get('alerte') == 'ON'
    prix_ajuste = int(request.form.get('prix_marche', PRIX_BASE))
    
    # Impact météo et risques (Loi de Structure)
    coeff_meteo = 0.5 if alerte_cyclone else 0.85 
    
    # Calcul Or Vert (Net)
    production_reelle = (NB_POTEAUX * RENDEMENT_THEORIQUE) * coeff_meteo
    brut_annuel = production_reelle * prix_ajuste
    net_annuel = (brut_annuel * (1 - MARGE_LOGISTIQUE)) - FRAIS_FIXES_ANNUELS
    net_mensuel_vanille = int(max(0, net_annuel // 12))
    
    # Autres revenus (L'Écorce + Le Lagon)
    flux_mensuel_fixe = 1050 + 18800 
    total_mensuel = flux_mensuel_fixe + net_mensuel_vanille

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ALPHA-FLOW | Dashboard Total</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0b1218; color: #e0e0e0; padding: 10px; line-height: 1.5; }
            .container { max-width: 550px; margin: auto; }
            .card { background: #1c252e; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
            .btn-update { background: #238636; color: white; padding: 10px; border-radius: 6px; border: none; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; }
            .btn-alerte { background: {{ '#da3633' if alerte else '#21262d' }}; color: white; border: 1px solid #30363d; padding: 5px 10px; border-radius: 4px; cursor: pointer; }
            .input-prix { background: #0b1218; color: #ffd700; border: 1px solid #30363d; width: 70px; padding: 5px; border-radius: 4px; text-align: center; }
            .gold { color: #ffd700; font-weight: bold; }
            .green { color: #00ff88; font-weight: bold; }
            h2 { color: #00ff88; font-size: 1.2em; border-bottom: 1px solid #333; padding-bottom: 5px; margin-top: 0; }
            ul { padding-left: 20px; color: #8b949e; font-size: 0.9em; list-style-type: square; }
            li { margin-bottom: 8px; }
            .badge { background: #30363d; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; color: #ffd700; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #00ff88; text-align: center; margin-bottom: 20px;">ALPHA-FLOW</h1>

            <form method="POST" class="card" style="border-color: {% if alerte %} #ff4b2b {% else %} #30363d {% endif %};">
                <h2>🛰️ Pilotage & Risques</h2>
                <p>Marché Vanille : <input type="number" name="prix_marche" value="{{ prix }}" class="input-prix"> €/kg</p>
                <p>État Météo : 
                   <button type="submit" name="alerte" value="{{ 'OFF' if alerte else 'ON' }}" class="btn-alerte">
                               {{ '⚠️ ALERTE CYCLONE' if alerte else '✅ CIEL DÉGAGÉ' }}
                   </button>
                </p>
                <button type="submit" class="btn-update">METTRE À JOUR LE DASHBOARD</button>
            </form>

            <div class="card" style="border-color: #ffd700; text-align: center;">
                <h2 style="color: #ffd700;">UNITÉS ALPHA : {{ total // 1000 }}</h2>
                <p class="gold" style="font-size: 1.8em; margin: 10px 0;">{{ "{:,}".format(total).replace(',', ' ') }} € / mois</p>
                <p style="font-size: 0.85em; color: #8b949e;">Revenu Net Total (Lagon + Écorce + Or Vert)</p>
            </div>

            <div class="card">
                <h2>🌿 Maintenance (Or Vert)</h2>
                <ul>
                    <li><b>Mariage des fleurs :</b> Prévu Mai-Août (70 poteaux).</li>
                    <li><b>Humidité :</b> Contrôle quotidien des brumisateurs.</li>
                    <li><b>Sanitaire :</b> Traitement escargots/champignons (Lutte Bio).</li>
                </ul>
            </div>

            <div class="card">
                <h2>🚢 Logistique & Dépenses</h2>
                <ul>
                    <li><b>Fret :</b> Liaison Moorea-Tahiti (Produits/Ventes).</li>
                    <li><b>Labels :</b> Certification EPIC Vanille + Cotisation Agri.</li>
                    <li><b>Écorce :</b> Budget finitions peinture (Février).</li>
                </ul>
            </div>

            <div class="card">
                <h2>📅 Calendrier 2026</h2>
                <ul>
                    <li><span class="badge">JAN</span> Suivi financier & Maintenance serres.</li>
                    <li><span class="badge">JUIN</span> Récolte 1 et Vente stock préparé.</li>
                    <li><span class="badge">MI-26</span> Chantier Extension (+60 poteaux).</li>
                </ul>
            </div>

            <p style="text-align: center; font-size: 0.7em; color: #444;">ID: OMEGA STATUS | Propriété Jean-Marie</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE, total=total_mensuel, prix=prix_ajuste, alerte=alerte_cyclone)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
