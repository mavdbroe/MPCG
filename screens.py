### screens.py ###
import pygame
from config import *
from ui_components import draw_text, Button
from card_database import CARD_DATA, CARD_IMAGES


def draw_energy_circles(surface, energies, start_x, y, radius=15, padding=5):
    """Dessine les cercles de couleur pour les énergies d'un deck."""
    for i, color_name in enumerate(energies):
        color_rgb = ENERGY_COLORS.get(color_name, BLACK)
        x = start_x + i * (2 * radius + padding)
        pygame.draw.circle(surface, color_rgb, (x, y), radius)
        pygame.draw.circle(surface, DARK_GRAY, (x, y), radius, 2)


def draw_accueil_screen(surface):
    surface.fill(BLUE)
    draw_text("Pokémon TCG Pocket", 'title', WHITE, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    draw_text("Par Maxime Van den Broeck", 'subtitle', WHITE, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text("Cliquez pour commencer", 'button', GRAY, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75)


def draw_menu_screen(surface, buttons):
    surface.fill(WHITE)
    draw_text("Menu Principal", 'title', BLACK, surface, SCREEN_WIDTH / 2, 100)
    for button in buttons.values():
        button.draw(surface)


# --- Écran de sélection de deck ---
def draw_deck_selection_screen(surface, player_num, decks, buttons, validation_func):
    surface.fill(WHITE)
    draw_text(f"Joueur {player_num}, choisissez votre deck", 'title', BLACK, surface, SCREEN_WIDTH / 2, 80)

    for i in range(3):
        slot_rect = pygame.Rect(100, 150 + i * 130, SCREEN_WIDTH - 200, 110)
        pygame.draw.rect(surface, GRAY, slot_rect, border_radius=15)
        draw_text(f"Emplacement {i + 1}", 'subtitle', DARK_GRAY, surface, slot_rect.left + 150, slot_rect.top + 30)

        deck_info = decks[i]
        if deck_info is None:
            draw_text("Vide", 'default', DARK_GRAY, surface, slot_rect.left + 150, slot_rect.top + 70)
        else:
            is_valid = validation_func(deck_info)
            card_count = len(deck_info['cards'])
            draw_text(f"{card_count}/20 cartes", 'default', BLACK, surface, slot_rect.left + 150, slot_rect.top + 70)
            draw_energy_circles(surface, deck_info['energies'], slot_rect.left + 350, slot_rect.centery)

            if f'choisir_{i}' in buttons:
                buttons[f'choisir_{i}'].draw(surface)
            if not is_valid:
                draw_text("Deck invalide (Pokémon de base requis)", 'small', RED, surface, slot_rect.centerx,
                          slot_rect.bottom - 20)

    buttons['retour_menu'].draw(surface)


# --- Écran du plateau de jeu ---
def draw_game_board_screen(surface, buttons, starting_player):
    surface.fill((50, 100, 70))  # Un fond vert pour le plateau

    # Message du joueur qui commence
    draw_text(f"Joueur {starting_player} commence la partie !", 'subtitle', WHITE, surface, SCREEN_WIDTH / 2, 20)

    # --- Zones du Joueur 2 (Adversaire - en haut) ---
    # Main (face cachée)
    for i in range(5):
        pygame.draw.rect(surface, BLACK, (SCREEN_WIDTH / 2 - 125 + i * 50, 50, 45, 60), border_radius=5)
    # Banc, Deck, Défausse
    p2_bench_y = 130
    pygame.draw.rect(surface, DARK_GRAY, (20, p2_bench_y, 100, 60), border_radius=5)  # Deck
    draw_text("Deck", "small", WHITE, surface, 70, p2_bench_y + 30)
    pygame.draw.rect(surface, DARK_GRAY, (130, p2_bench_y, 100, 60), border_radius=5)  # Défausse
    draw_text("Défausse", "small", WHITE, surface, 180, p2_bench_y + 30)
    pygame.draw.circle(surface, RED, (265, p2_bench_y + 30), 15)  # Energie
    for i in range(3):
        pygame.draw.rect(surface, (150, 10, 120), (SCREEN_WIDTH / 2 - 185 + i * 125, p2_bench_y, 120, 160), 3,
                         border_radius=10)
    # Actif
    pygame.draw.rect(surface, (250, 200, 0), (SCREEN_WIDTH / 2 - 60, p2_bench_y + 170, 120, 160), 3, border_radius=10)

    # --- Zones du Joueur 1 (Vous - en bas) ---
    p1_y_offset = SCREEN_HEIGHT - 200
    # Actif
    pygame.draw.rect(surface, (250, 200, 0), (SCREEN_WIDTH / 2 - 60, p1_y_offset - 170, 120, 160), 3, border_radius=10)
    # Banc, Deck, Défausse
    for i in range(3):
        pygame.draw.rect(surface, (10, 150, 120), (SCREEN_WIDTH / 2 - 185 + i * 125, p1_y_offset, 120, 160), 3,
                         border_radius=10)
    pygame.draw.rect(surface, DARK_GRAY, (SCREEN_WIDTH - 230, p1_y_offset, 100, 60), border_radius=5)  # Défausse
    draw_text("Défausse", "small", WHITE, surface, SCREEN_WIDTH - 180, p1_y_offset + 30)
    pygame.draw.rect(surface, DARK_GRAY, (SCREEN_WIDTH - 120, p1_y_offset, 100, 60), border_radius=5)  # Deck
    draw_text("Deck", "small", WHITE, surface, SCREEN_WIDTH - 70, p1_y_offset + 30)
    pygame.draw.circle(surface, RED, (SCREEN_WIDTH - 265, p1_y_offset + 30), 15)  # Energie
    # Main
    for i in range(5):
        pygame.draw.rect(surface, GRAY, (SCREEN_WIDTH / 2 - 125 + i * 50, SCREEN_HEIGHT - 70, 45, 60), border_radius=5)

    # Bouton Abandon
    buttons['abandon'].draw(surface)


def draw_gestion_deck_screen(surface, decks, buttons):
    surface.fill(WHITE)
    draw_text("Gestion des Decks", 'title', BLACK, surface, SCREEN_WIDTH / 2, 80)
    for i in range(3):
        slot_rect = pygame.Rect(100, 150 + i * 130, SCREEN_WIDTH - 200, 110)
        pygame.draw.rect(surface, GRAY, slot_rect, border_radius=15)
        draw_text(f"Emplacement {i + 1}", 'subtitle', DARK_GRAY, surface, slot_rect.left + 150, slot_rect.top + 30)
        if decks[i] is None:
            draw_text("Vide", 'default', DARK_GRAY, surface, slot_rect.left + 150, slot_rect.top + 70)
            buttons[f'creer_{i}'].draw(surface)
        else:
            deck_info = decks[i]
            card_count = len(deck_info['cards'])
            draw_text(f"{card_count}/20 cartes", 'default', BLACK, surface, slot_rect.left + 150, slot_rect.top + 70)
            draw_energy_circles(surface, deck_info['energies'], slot_rect.left + 350, slot_rect.centery)
            buttons[f'apercu_{i}'].draw(surface)
            buttons[f'modifier_{i}'].draw(surface)
            buttons[f'supprimer_{i}'].draw(surface)
    buttons['retour'].draw(surface)


def draw_apercu_deck_screen(surface, deck_info, buttons):
    surface.fill(WHITE)
    draw_text("Aperçu du Deck", 'title', BLACK, surface, SCREEN_WIDTH / 2, 50)
    if deck_info:
        draw_energy_circles(surface, deck_info['energies'], 50, 90)
    if not deck_info or not deck_info['cards']:
        draw_text("Ce deck est vide.", 'subtitle', BLACK, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    else:
        x_start, y_start = 50, 120
        x, y = x_start, y_start
        padding = 10
        for card_name in deck_info['cards']:
            if card_name in CARD_IMAGES:
                surface.blit(CARD_IMAGES[card_name], (x, y))
            x += CARD_WIDTH + padding
            if x + CARD_WIDTH > SCREEN_WIDTH - 50:
                x = x_start
                y += CARD_HEIGHT + padding
    buttons['retour_gestion'].draw(surface)


def draw_editeur_deck_screen(surface, current_cards, current_energies, available_cards, buttons, text_input,
                             filter_buttons, save_failed):
    surface.fill(LIGHT_BLUE)
    collection_rect = pygame.Rect(20, 80, 750, SCREEN_HEIGHT - 100)
    pygame.draw.rect(surface, WHITE, collection_rect, border_radius=10)
    draw_text("Collection (clic pour ajouter)", 'small', BLACK, surface, collection_rect.centerx, 75)
    deck_rect = pygame.Rect(collection_rect.right + 20, 80, SCREEN_WIDTH - collection_rect.right - 40,
                            SCREEN_HEIGHT - 100)
    pygame.draw.rect(surface, WHITE, deck_rect, border_radius=10)
    draw_text("Énergies (1-3 requises)", 'small', BLACK, surface, deck_rect.centerx, 100)
    x, y = 790, 120
    for color_name, color_rgb in ENERGY_COLORS.items():
        btn_rect = buttons[f'energy_{color_name}'].rect
        pygame.draw.circle(surface, color_rgb, btn_rect.center, 15)
        if color_name in current_energies:
            pygame.draw.circle(surface, YELLOW, btn_rect.center, 16, 3)
        x += 35
        if x > SCREEN_WIDTH - 60:
            x = 790
            y += 35
    draw_text(f"Deck ({len(current_cards)}/20)", 'small', BLACK, surface, deck_rect.centerx, 220)
    text_input.draw(surface)
    for btn in filter_buttons.values():
        btn.draw(surface)
    x_col, y_col = collection_rect.left + 10, collection_rect.top + 50
    for i, card_name in enumerate(available_cards):
        surface.blit(CARD_IMAGES[card_name], (x_col, y_col))
        x_col += CARD_WIDTH + 5
        if x_col + CARD_WIDTH > collection_rect.right - 10:
            x_col = collection_rect.left + 10
            y_col += CARD_HEIGHT + 5
    x_deck, y_deck = deck_rect.left + 10, 240
    for i, card_name in enumerate(current_cards):
        small_img = pygame.transform.scale(CARD_IMAGES[card_name], (CARD_WIDTH * 0.7, CARD_HEIGHT * 0.7))
        surface.blit(small_img, (x_deck, y_deck))
        y_deck += 30
        if y_deck + 30 > deck_rect.bottom - 10:
            y_deck = 240
            x_deck += CARD_WIDTH * 0.7 + 5
    buttons['sauvegarder'].draw(surface)
    buttons['annuler'].draw(surface)
    if save_failed:
        draw_text("Veuillez choisir de 1 à 3 énergies.", 'small', RED, surface, SCREEN_WIDTH - 255, 80)