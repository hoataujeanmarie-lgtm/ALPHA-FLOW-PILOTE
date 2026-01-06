from flask import Flask, render_template_string, request

app = Flask(__name__)

# Le contenu qui va apparaître quand on clique
PACKAGING = {
    "titre": "PACK LIBÉRATION TPE",
    "accroche": "Gagnez 5h par semaine ou vous ne payez rien.",
    "script": "Salut, je teste un système pour simplifier la gestion des artisans. Je peux te montrer comment gagner 1h de paperasse par jour gratuitement ?",
    "prix": "1 Unité Alpha (1 000 €)"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ALPHA-FLOW | Stratégie</title>
    <style>
        body { font-family: sans-serif; background: #0b0e14; color: #e0e0e0; text-align: center; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: #161b22; padding: 30px; border-radius: 20px; border: 1px solid #30363d; }
        h1 { color: #00ff88; }
        .btn-main { display: inline-block; background: #00ff88; color: #0b0e14; padding: 15px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; margin-top: 20px; border: none; cursor: pointer; }
        .resultat { margin-top: 30px; padding: 20px; border: 1px dashed #00ff88; background: #1c2128; display: {% if affiche %} block {% else %} none {% endif %}; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ALPHA-FLOW PILOTE</h1>
        <p>Domaine : Formation Organisationnelle</p>
        
        <form method="POST">
            <button type="submit" name="generate" class="btn-main">GÉNÉRER LE PACKAGING DE VENTE</button>
        </form>

        <div class="resultat">
            <h2 style="color: #00ff88;">{{ pack.titre }}</h2>
            <p><strong>Promesse :</strong> {{ pack.accroche }}</p>
            <p><strong>Script WhatsApp :</strong> <em>{{ pack.script }}</em></p>
            <p><strong>Objectif :</strong> {{ pack.prix }}</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    affiche = False
    if request.method == 'POST':
        affiche = True
    return render_template_string(HTML_TEMPLATE, pack=PACKAGING, affiche=affiche)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
