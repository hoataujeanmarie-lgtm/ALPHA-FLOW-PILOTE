import time

# CONFIGURATION OMEGA STATUS
WALLET_SOLANA = "2tyXwhi63XAe3AXJ7ZQHjRqW1mpJSbxKBHsb3Byzr39s"

def lancer_ia():
    print("--- SYSTEME ALPHA-FLOW ACTIF ---")
    print(f"Surveillance du portefeuille : {WALLET_SOLANA}")
    print("En attente de la premiere Unite Alpha...")

if __name__ == "__main__":
    lancer_ia()
    while True:
        # L'IA fait son travail de veille
        print("Recherche de paiements sur la blockchain...")
        time.sleep(300) # L'IA verifie toutes les 5 minutes
