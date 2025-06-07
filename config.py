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

# --- Polices (initialisées dans main.py) ---
FONTS = {}

# --- Cartes ---
CARD_WIDTH = 100
CARD_HEIGHT = 140