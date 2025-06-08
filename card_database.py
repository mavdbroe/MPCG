### card_database.py ###
import os
import pygame
from config import IMAGE_DIR, FONTS, BLACK, GRAY, CARD_WIDTH, CARD_HEIGHT, RED


def get_image_path(filename):
    """Retourne le chemin complet vers une image."""
    return os.path.join(IMAGE_DIR, filename)


def generate_placeholder_image(name, path):
    """Génère une image de remplacement si le fichier n'est pas trouvé."""
    if not os.path.exists(path):
        print(f"Image '{os.path.basename(path)}' non trouvée. Création d'un substitut.")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        placeholder_surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        placeholder_surf.fill(GRAY)
        pygame.draw.rect(placeholder_surf, BLACK, placeholder_surf.get_rect(), 2)

        if 'small' not in FONTS:
            FONTS['small'] = pygame.font.Font(None, 18)

        text_surf = FONTS['small'].render(name, True, BLACK)
        text_rect = text_surf.get_rect(center=(CARD_WIDTH / 2, CARD_HEIGHT / 2))
        placeholder_surf.blit(text_surf, text_rect)
        pygame.image.save(placeholder_surf, path)


CARD_DATA = {
    "Pikachu": {"type": "Pokémon",
                "pokemon_type": "Foudre",
                "hp": 60,
                "stage": 0,
                "is_EX": False,
                "ability": None,
                "attacks": [{"name": "Vive-Attaque", "cost": ["Incolore"], "damage": 10},
                            {"name": "Éclair", "cost": ["Foudre", "Incolore"], "damage": 20}],
                "weakness": {"type": "Combat", "value": "x2"}, "resistance": {},
                "retreat_cost": 1, "image": get_image_path("Pikachu.png")},
    "Bulbizarre": {"type": "Pokémon", "pokemon_type": "Plante", "hp": 70, "stage": 0, "is_EX": False,
                   "ability": {"name": "Peau Dure", "text": "Ce Pokémon subit 10 dégâts de moins."},
                   "attacks": [{"name": "Fouet Lianes", "cost": ["Plante", "Incolore"], "damage": 20}],
                   "weakness": {"type": "Feu", "value": "x2"}, "resistance": {}, "retreat_cost": 1,
                   "image": get_image_path("Bulbizarre.png")},
    "Salamèche": {"type": "Pokémon", "pokemon_type": "Feu", "hp": 60, "stage": 0, "is_EX": False, "ability": None,
                  "attacks": [{"name": "Griffe", "cost": ["Incolore"], "damage": 10},
                              {"name": "Flammèche", "cost": ["Feu", "Incolore"], "damage": 20}],
                  "weakness": {"type": "Eau", "value": "x2"}, "resistance": {}, "retreat_cost": 1,
                  "image": get_image_path("Salameche.png")},
    "Carapuce": {"type": "Pokémon", "pokemon_type": "Eau", "hp": 60, "stage": 0, "is_EX": False, "ability": None,
                 "attacks": [{"name": "Pistolet à O", "cost": ["Eau"], "damage": 10}],
                 "weakness": {"type": "Plante", "value": "x2"}, "resistance": {}, "retreat_cost": 1,
                 "image": get_image_path("Carapuce.png")},
    "Potion": {"type": "Dresseur", "trainer_type": "Objet", "text": "Soignez 30 dégâts à 1 de vos Pokémon.",
               "image": get_image_path("Potion.png")},
    "Professeur Keteleeria": {"type": "Dresseur", "trainer_type": "Supporter",
                              "text": "Défaussez votre main et piochez 7 cartes.",
                              "image": get_image_path("Keteleeria.png")},
}

CARD_IMAGES = {}


def load_card_images():
    """Charge toutes les images de cartes en mémoire."""
    for name, data in CARD_DATA.items():
        path = data['image']
        generate_placeholder_image(name, path)
        try:
            image = pygame.image.load(path).convert_alpha()
            CARD_IMAGES[name] = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        except pygame.error as e:
            print(f"Impossible de charger l'image {path}: {e}")
            error_surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            error_surf.fill(RED)
            CARD_IMAGES[name] = error_surf