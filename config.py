### config.py ###
import os

# --- Chemins ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGE_DIR = os.path.join(ASSETS_DIR, "images")
DECK_FILE = "decks.json"

# --- Fenêtre ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# --- Couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 100, 200)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 223, 0)

# --- Couleurs d'Énergie ---
ENERGY_COLORS = {
    'rouge': (220, 20, 60),
    'jaune': (255, 215, 0),
    'bleu': (70, 130, 180),
    'mauve': (153, 50, 204),
    'vert': (60, 179, 113),
    'orange': (255, 140, 0),
    'pourpre': (139, 0, 139),
    'gris': (128, 128, 128),
    'rose': (255, 105, 180),
    'noir': (30, 30, 30)
}

# --- Polices (initialisées dans main.py) ---
FONTS = {}

# --- Cartes ---
CARD_WIDTH = 100
CARD_HEIGHT = 140