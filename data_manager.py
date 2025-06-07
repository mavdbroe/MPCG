### data_manager.py ###
import json
import os
from config import DECK_FILE

def load_decks():
    """Charge les decks depuis un fichier JSON s'il existe."""
    if os.path.exists(DECK_FILE):
        try:
            with open(DECK_FILE, 'r') as f:
                decks_data = json.load(f)
                # S'assurer que c'est une liste de 3 éléments
                if isinstance(decks_data, list) and len(decks_data) == 3:
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