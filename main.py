### main.py ###

import pygame
import sys
import random
from config import *
from card_database import CARD_DATA, load_card_images
from data_manager import load_decks, save_decks
from ui_components import Button, TextInputBox
import screens

# --- Initialisation ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon TCG Pocket")
clock = pygame.time.Clock()

# --- Polices ---
FONTS['default'] = pygame.font.Font(None, 32)
FONTS['small'] = pygame.font.Font(None, 18)
FONTS['title'] = pygame.font.Font(None, 74)
FONTS['subtitle'] = pygame.font.Font(None, 42)
FONTS['button'] = pygame.font.Font(None, 36)

# --- Chargement des données ---
load_card_images()
decks = load_decks()

# --- Variables d'état ---
game_state = "accueil"
buttons = {}

# --- Variables pour l'éditeur de deck ---
active_deck_index = -1
current_deck_cards = []
current_deck_energies = []
name_filter_input = TextInputBox(25, 10, 200, 40, font_name='default')
filter_type = "Tous"
available_cards_in_editor = list(CARD_DATA.keys())
last_save_attempt_failed = False

# --- Variables pour la partie ---
player1_deck = None
player2_deck = None
starting_player = None


def is_deck_valid(deck_info):
    """Vérifie si un deck contient au moins un Pokémon de base (stage 0)."""
    if not deck_info or not deck_info['cards']:
        return False
    for card_name in deck_info['cards']:
        card_data = CARD_DATA.get(card_name)
        if card_data and card_data['type'] == 'Pokémon' and card_data.get('stage') == 0:
            return True
    return False


def apply_filters():
    global available_cards_in_editor
    name_query = name_filter_input.text.lower()
    filtered_list = []
    for name, data in CARD_DATA.items():
        if name_query and name_query not in name.lower():
            continue
        if filter_type != "Tous" and data['type'] != filter_type:
            continue
        filtered_list.append(name)
    available_cards_in_editor = sorted(filtered_list)


def setup_buttons_for_state(state):
    """Crée les boutons nécessaires pour un état de jeu donné."""
    buttons.clear()
    if state == "menu":
        buttons['gerer_deck'] = Button(SCREEN_WIDTH / 2 - 200, 250, 400, 80, "Gérer les Decks")
        buttons['lancer_partie'] = Button(SCREEN_WIDTH / 2 - 200, 350, 400, 80, "Lancer une partie", color=GREEN)

    elif state == "gestion_deck":
        buttons['retour'] = Button(20, 20, 150, 60, "Retour", color=RED)
        for i in range(3):
            if decks[i] is None:
                buttons[f'creer_{i}'] = Button(SCREEN_WIDTH - 280, 175 + i * 130, 150, 60, "Créer", color=GREEN)
            else:
                buttons[f'apercu_{i}'] = Button(SCREEN_WIDTH - 600, 175 + i * 130, 150, 60, "Aperçu", color=BLUE)
                buttons[f'modifier_{i}'] = Button(SCREEN_WIDTH - 440, 175 + i * 130, 150, 60, "Modifier", color=YELLOW)
                buttons[f'supprimer_{i}'] = Button(SCREEN_WIDTH - 280, 175 + i * 130, 150, 60, "Supprimer", color=RED)

    elif state == "apercu_deck":
        buttons['retour_gestion'] = Button(20, 20, 150, 60, "Retour", color=RED)

    # --- Boutons pour la sélection de deck ---
    elif state in ["deck_selection_p1", "deck_selection_p2"]:
        buttons['retour_menu'] = Button(20, 20, 150, 60, "Retour Menu", color=RED)
        for i in range(3):
            if decks[i] is not None:
                is_valid = is_deck_valid(decks[i])
                color = GREEN if is_valid else DARK_GRAY
                buttons[f'choisir_{i}'] = Button(SCREEN_WIDTH - 280, 175 + i * 130, 150, 60, "Choisir", color=color)

    elif state == "editeur_deck":
        buttons['sauvegarder'] = Button(SCREEN_WIDTH - 170, 10, 150, 60, "Sauvegarder", color=GREEN)
        buttons['annuler'] = Button(SCREEN_WIDTH - 340, 10, 150, 60, "Annuler", color=RED)
        buttons['filter_tous'] = Button(250, 10, 100, 40, "Tous")
        buttons['filter_pokemon'] = Button(360, 10, 100, 40, "Pokémon")
        buttons['filter_dresseur'] = Button(470, 10, 120, 40, "Dresseur")
        x, y = 790, 120
        for color_name in ENERGY_COLORS:
            buttons[f'energy_{color_name}'] = Button(x, y, 30, 30, '')
            x += 35
            if x > SCREEN_WIDTH - 60:
                x = 790
                y += 35

    # --- Boutons pour le plateau de jeu ---
    elif state == "game_board":
        buttons['abandon'] = Button(20, SCREEN_HEIGHT - 80, 150, 60, "Abandon", color=RED)


# --- Boucle principale ---
setup_buttons_for_state(game_state)
running = True
while running:
    events = pygame.event.get()

    # --- Mise à jour des boutons de cartes dynamiques ---
    if game_state == "editeur_deck":
        keys_to_remove = [k for k in buttons if k.startswith('collection_') or k.startswith('deck_')]
        for k in keys_to_remove:
            del buttons[k]

        # Boutons pour la collection
        x_col, y_col = 20 + 10, 80 + 50
        for i, card_name in enumerate(available_cards_in_editor):
            buttons[f'collection_{card_name}_{i}'] = Button(x_col, y_col, CARD_WIDTH, CARD_HEIGHT, '')
            x_col += CARD_WIDTH + 5
            if x_col + CARD_WIDTH > 20 + 750 - 10:
                x_col = 20 + 10
                y_col += CARD_HEIGHT + 5

        # Boutons pour le deck
        x_deck, y_deck = 790 + 10, 240
        for i, card_name in enumerate(current_deck_cards):
            card_rect = pygame.Rect(x_deck, y_deck, CARD_WIDTH * 0.7, CARD_HEIGHT * 0.7)
            buttons[f'deck_{card_name}_{i}'] = Button(x_deck, y_deck, card_rect.width, card_rect.height, '')
            y_deck += 30
            if y_deck + 30 > 80 + SCREEN_HEIGHT - 100 - 10:
                y_deck = 240
                x_deck += card_rect.width + 5

    # --- Gestion des événements ---
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if game_state == "editeur_deck":
            name_filter_input.handle_event(event)
            if event.type == pygame.KEYDOWN and name_filter_input.active:
                apply_filters()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            state_changed = False
            last_save_attempt_failed = False

            if game_state == "accueil":
                game_state = "menu"
                state_changed = True

            elif game_state == "menu":
                if buttons['gerer_deck'].is_clicked(event):
                    game_state = "gestion_deck"
                    state_changed = True
                elif 'lancer_partie' in buttons and buttons['lancer_partie'].is_clicked(event):
                    player1_deck = None
                    player2_deck = None
                    game_state = "deck_selection_p1"
                    state_changed = True

            # --- Logique de sélection de deck ---
            elif game_state in ["deck_selection_p1", "deck_selection_p2"]:
                if buttons['retour_menu'].is_clicked(event):
                    game_state = "menu"
                    state_changed = True
                else:
                    for i in range(3):
                        if f'choisir_{i}' in buttons and buttons[f'choisir_{i}'].is_clicked(event):
                            if is_deck_valid(decks[i]):
                                if game_state == "deck_selection_p1":
                                    player1_deck = decks[i]
                                    game_state = "deck_selection_p2"
                                    state_changed = True
                                    break
                                elif game_state == "deck_selection_p2":
                                    player2_deck = decks[i]
                                    starting_player = random.choice([1, 2])
                                    game_state = "game_board"
                                    state_changed = True
                                    break

            # --- NOUVEAU : Logique du plateau de jeu ---
            elif game_state == "game_board":
                if buttons['abandon'].is_clicked(event):
                    game_state = "menu"
                    state_changed = True

            elif game_state == "gestion_deck":
                if buttons['retour'].is_clicked(event):
                    game_state = "menu"
                    state_changed = True
                else:
                    for i in range(3):
                        if decks[i] is None:
                            if f'creer_{i}' in buttons and buttons[f'creer_{i}'].is_clicked(event):
                                active_deck_index = i
                                current_deck_cards = []
                                current_deck_energies = []
                                game_state = "editeur_deck"
                                state_changed = True
                                break
                        else:
                            if f'apercu_{i}' in buttons and buttons[f'apercu_{i}'].is_clicked(event):
                                active_deck_index = i
                                game_state = "apercu_deck"
                                state_changed = True
                                break
                            if f'modifier_{i}' in buttons and buttons[f'modifier_{i}'].is_clicked(event):
                                active_deck_index = i
                                current_deck_cards = list(decks[i]['cards'])
                                current_deck_energies = list(decks[i]['energies'])
                                game_state = "editeur_deck"
                                state_changed = True
                                break
                            if f'supprimer_{i}' in buttons and buttons[f'supprimer_{i}'].is_clicked(event):
                                decks[i] = None
                                save_decks(decks)
                                setup_buttons_for_state(game_state)
                                break

            elif game_state == "apercu_deck":
                if buttons['retour_gestion'].is_clicked(event):
                    game_state = "gestion_deck"
                    state_changed = True

            elif game_state == "editeur_deck":
                if buttons['sauvegarder'].is_clicked(event):
                    if 1 <= len(current_deck_energies) <= 3:
                        decks[active_deck_index] = {"cards": list(current_deck_cards),
                                                    "energies": list(current_deck_energies)}
                        save_decks(decks)
                        game_state = "gestion_deck"
                        state_changed = True
                    else:
                        last_save_attempt_failed = True
                elif buttons['annuler'].is_clicked(event):
                    game_state = "gestion_deck"
                    state_changed = True
                elif buttons['filter_tous'].is_clicked(event):
                    filter_type = "Tous"
                    apply_filters()
                elif buttons['filter_pokemon'].is_clicked(event):
                    filter_type = "Pokémon"
                    apply_filters()
                elif buttons['filter_dresseur'].is_clicked(event):
                    filter_type = "Dresseur"
                    apply_filters()

                if not state_changed:
                    # Gestion des clics sur les couleurs d'énergie
                    for color_name in ENERGY_COLORS:
                        if f'energy_{color_name}' in buttons and buttons[f'energy_{color_name}'].is_clicked(event):
                            if color_name in current_deck_energies:
                                current_deck_energies.remove(color_name)
                            elif len(current_deck_energies) < 3:
                                current_deck_energies.append(color_name)

                    # Clic sur une carte de la collection pour l'ajouter
                    for key, btn in list(buttons.items()):
                        if key.startswith("collection_") and btn.is_clicked(event):
                            if len(current_deck_cards) < 20:
                                card_name = key.split('_')[1]
                                current_deck_cards.append(card_name)

                    # Clic sur une carte du deck pour la retirer
                    for key, btn in list(buttons.items()):
                        if key.startswith("deck_") and btn.is_clicked(event):
                            card_index_in_deck = int(key.split('_')[2])
                            del current_deck_cards[card_index_in_deck]
                            break

            if state_changed:
                setup_buttons_for_state(game_state)
                break

    # --- Mise à jour du survol ---
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons.values():
        button.check_hover(mouse_pos)

    # --- Dessin ---
    screen.fill(BLACK)
    if game_state == "accueil":
        screens.draw_accueil_screen(screen)
    elif game_state == "menu":
        screens.draw_menu_screen(screen, buttons)
    elif game_state == "deck_selection_p1":
        screens.draw_deck_selection_screen(screen, 1, decks, buttons, is_deck_valid)
    elif game_state == "deck_selection_p2":
        screens.draw_deck_selection_screen(screen, 2, decks, buttons, is_deck_valid)
    elif game_state == "game_board":
        screens.draw_game_board_screen(screen, buttons, starting_player)
    elif game_state == "gestion_deck":
        screens.draw_gestion_deck_screen(screen, decks, buttons)
    elif game_state == "apercu_deck":
        screens.draw_apercu_deck_screen(screen, decks[active_deck_index], buttons)
    elif game_state == "editeur_deck":
        filter_btns = {k: v for k, v in buttons.items() if k.startswith('filter_')}
        screens.draw_editeur_deck_screen(screen, current_deck_cards, current_deck_energies, available_cards_in_editor,
                                         buttons, name_filter_input, filter_btns, last_save_attempt_failed)

    pygame.display.flip()
    clock.tick(60)

# --- Fin ---
pygame.quit()
sys.exit()