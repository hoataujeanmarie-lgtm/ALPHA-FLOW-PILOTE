from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>ALPHA-FLOW : Générateur d'Unités</title>
            <style>
                body { font-family: sans-serif; text-align: center; background: #1a1a1a; color: white; padding: 50px; }
                .card { background: #2d2d2d; border: 2px solid #00ff88; border-radius: 15px; padding: 20px; max-width: 500px; margin: auto; }
                h1 { color: #00ff88; }
                .btn { background: #00ff88; color: black; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>ALPHA-FLOW PILOTE</h1>
                <p><strong>STATUT :</strong> OPERATIONNEL</p>
                <hr>
                <h3>PROCHAINE OPPORTUNITE DETECTEE :</h3>
                <p><i>Domaine : Formation Organisationnelle</i></p>
                <p>Cible : TPE locales en manque de structure</p>
                <p><b>Objectif : 1 Unité Alpha (1 000 &euro;)</b></p>
                <br>
                <a href="#" class="btn">GENERER LE PACKAGING DE VENTE</a>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
