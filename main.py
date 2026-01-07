from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- CONFIGURATION SÉCURITÉ & RISQUES ---
NB_POTEAUX_ACTUELS = 70
NB_POTEAUX_CIBLE = 130
PRIX_KG_VANILLE = 600
RENDEMENT_THEORIQUE = 0.37 # kg/poteau/an

# Facteurs de protection (Loi de Structure)
COEFF_RISQUE = 0.15 # 15% de perte estimée (Vol, Maladie, Aléas)
MARGE_LOGISTIQUE = 0.35
FRAIS_FIXES_EPIC = 1500

def calcul_net_securise(nb_poteaux):
    # Production brute moins les pertes de 15%
    production_reelle = (nb_poteaux * RENDEMENT_THEORIQUE) * (1 - COEFF_RISQUE)
    brut_annuel = production_reelle * PRIX_KG_VANILLE
    net_annuel = (brut_annuel * (1 - MARGE_LOGISTIQUE)) - FRAIS_FIXES_EPIC
    return int(max(0, net_annuel))

@app.route('/', methods=['GET', 'POST'])
def home():
    vue = None
    net_actuel = calcul_net_securise(NB_POTEAUX_ACTUELS)
    net_cible = calcul_net_securise(NB_POTEAUX_CIBLE)
    # Flux mensuels constants (Faa'a + Glamping)
    flux_mensuel = 1050 + 18800

    if request.method == 'POST':
        vue = request.form.get('vue')

    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ALPHA-FLOW | Sécurité</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e0e0e0; text-align: center; padding: 10px; }
            .container { max-width: 500px; margin: auto; background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; }
            .btn-group { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; }
            .btn { background: #21262d; color: #00ff88; padding: 15px; border-radius: 8px; border: 1px solid #30363d; cursor: pointer; font-weight: bold; }
            .card { margin-top: 20px; padding: 15px; border: 1px solid #ff6b6b; background: #0d1117; border-radius: 10px; text-align: left; }
            .badge-safe { background: #00ff88; color: #000; padding: 2px 8px; border-radius: 5px; font-size: 0.7em; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #00ff88;">ALPHA-FLOW</h1>
            <p>Stratégie : <b>3 Serres Compartimentées</b> <span class="badge-safe">SÉCURISÉ</span></p>

            <form method="POST" class="btn-group">
                <button type="submit" name="vue" value="risque" class="btn">L'OR VERT (Analyse Risque)</button>
                <button type="submit" name="vue" value="liberte" class="btn" style="border-color:#ffd700; color:#ffd700;">☀️ OBJECTIF LIBERTÉ</button>
            </form>

            {% if vue == 'risque' %}
            <div class="card">
                <h3 style="color: #ff6b6b; margin-top:0;">Gestion du Risque (λ)</h3>
                <p>• Compartimentation : 3 blocs séparés.</p>
                <p>• Marge de sécurité incluse : -15% (Vol/Maladie).</p>
                <hr style="border: 0.5px solid #333;">
                <p><b>Net Annuel Sécurisé (70 pot.) :</b> {{ net_actuel }} €</p>
                <p style="color: #00ff88;"><b>Net Annuel Cible (130 pot.) :</b> {{ net_cible }} €</p>
            </div>
            {% elif vue == 'liberte' %}
            <div class="card" style="border-color: #ffd700;">
                <h3 style="color: #ffd700; margin-top:0;">UNITÉS ALPHA RÉELLES</h3>
                <p>Basé sur revenus nets APRES risque et charges :</p>
                <p><b>Aujourd'hui : {{ (flux_mensuel + (net_actuel // 12)) }} €/mois</b></p>
                <p style="color: #00ff88; font-size: 1.2em;"><b>Objectif 2026 : {{ (flux_mensuel + (net_cible // 12)) }} €/mois</b></p>
                <hr style="border: 0.5px solid #ffd700;">
                <p>Sécurité Stéphanie : <b>{{ (flux_mensuel + (net_cible // 12)) // 1000 }} Unités Alpha</b></p>
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE, vue=vue, net_actuel=net_actuel, net_cible=net_cible, flux_mensuel=flux_mensuel)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
