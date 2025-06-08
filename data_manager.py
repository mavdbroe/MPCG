### data_manager.py ###
import json
import os
from config import DECK_FILE

def load_decks():
    """Charge les decks depuis un fichier JSON et valide leur structure."""
    if os.path.exists(DECK_FILE):
        try:
            with open(DECK_FILE, 'r') as f:
                decks_data = json.load(f)
                if isinstance(decks_data, list) and len(decks_data) == 3:
                    # Vérification de la structure de chaque deck non-vide
                    for deck in decks_data:
                        if deck is not None:
                            if not isinstance(deck, dict) or 'cards' not in deck or 'energies' not in deck:
                                print(f"Avertissement: Structure de deck invalide dans {DECK_FILE}. Réinitialisation.")
                                return [None, None, None]
                    return decks_data
                else:
                    return [None, None, None]
        except (json.JSONDecodeError, TypeError):
            print(f"Avertissement: Le fichier {DECK_FILE} est corrompu. Il sera réinitialisé.")
            return [None, None, None]
    return [None, None, None]

def save_decks(decks):
    """Sauvegarde l'état actuel des decks dans un fichier JSON."""
    with open(DECK_FILE, 'w') as f:
        json.dump(decks, f, indent=4)