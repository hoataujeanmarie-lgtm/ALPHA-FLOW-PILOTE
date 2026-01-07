from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- DONNÉES SÉCURISÉES ---
NB_POTEAUX_ACTUELS = 70
NB_POTEAUX_CIBLE = 130
PRIX_KG_VANILLE = 600
RENDEMENT_THEORIQUE = 0.37 
COEFF_RISQUE = 0.15 
MARGE_LOGISTIQUE = 0.35
FRAIS_FIXES_EPIC = 1500

def calcul_net_securise(nb_poteaux):
    production_reelle = (nb_poteaux * RENDEMENT_THEORIQUE) * (1 - COEFF_RISQUE)
    brut_annuel = production_reelle * PRIX_KG_VANILLE
    net_annuel = (brut_annuel * (1 - MARGE_LOGISTIQUE)) - FRAIS_FIXES_EPIC
    return int(max(0, net_annuel))

@app.route('/', methods=['GET', 'POST'])
def home():
    net_actuel = calcul_net_securise(NB_POTEAUX_ACTUELS)
    net_cible = calcul_net_securise(NB_POTEAUX_CIBLE)
    # Revenus Mensuels Fixes (Airbnb + Glamping)
    flux_mensuel = 1050 + 18800

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ALPHA-FLOW | Dashboard Complet</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e0e0e0; text-align: center; padding: 10px; }
            .container { max-width: 500px; margin: auto; }
            .card { background: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; text-align: left; }
            .gold-border { border-color: #ffd700; }
            .green-text { color: #00ff88; font-weight: bold; }
            .gold-text { color: #ffd700; font-weight: bold; }
            h2 { font-size: 1.1em; margin-top: 0; text-transform: uppercase; letter-spacing: 1px; }
            .unit { font-size: 0.8em; color: #8b949e; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #00ff88; margin-bottom: 20px;">ALPHA-FLOW</h1>

            <div class="card">
                <h2>🌊 Flux Mensuels (Lagon + Écorce)</h2>
                <p>Airbnb Faa'a : <span class="green-text">1 050 €</span></p>
                <p>Glamping Moorea : <span class="green-text">18 800 €</span></p>
                <p class="unit">Total Flux : {{ flux_mensuel }} € / mois</p>
            </div>

            <div class="card">
                <h2>🌿 L'OR VERT (Vanille)</h2>
                <p>Statut : {{ nb_pot }} poteaux</p>
                <p>Bénéfice Net Sécurisé : <span class="green-text">{{ net_actuel }} € / an</span></p>
                <p class="unit">Risque (λ) de 15% et charges incluses.</p>
            </div>

            <div class="card gold-border">
                <h2 class="gold-text">☀️ OBJECTIF LIBERTÉ</h2>
                <p>Revenu mensuel total : <br><span style="font-size: 1.5em;" class="gold-text">{{ total_mensuel }} €</span></p>
                <hr style="border: 0.5px solid #30363d;">
                <p>Indicateur : <span style="font-size: 1.2em;">{{ total_mensuel // 1000 }} Unités Alpha</span></p>
                <p class="unit">Priorité : Sécuriser Stéphanie (La Boussole)</p>
            </div>

            <p style="font-size: 0.8em; color: #8b949e;">Mise à jour : 07 Janvier 2026</p>
        </div>
    </body>
    </html>
    """
    total_m = flux_mensuel + (net_actuel // 12)
    return render_template_string(HTML_TEMPLATE, 
                                 net_actuel=net_actuel, 
                                 flux_mensuel=flux_mensuel, 
                                 total_mensuel=total_m,
                                 nb_pot=NB_POTEAUX_ACTUELS)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
