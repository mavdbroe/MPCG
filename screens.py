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

    # --- Définition des dimensions et positions ---
    slot_w, slot_h = 80, 110
    hand_w, hand_h = 80, 110
    gap = 15

    # --- Zones du Joueur 1 (Vous - en bas) ---
    p1_hand_y = SCREEN_HEIGHT - hand_h - gap
    p1_bench_y = p1_hand_y - slot_h - gap
    p1_active_y = p1_bench_y - slot_h - gap

    # Main
    num_hand_cards = 5
    hand_total_width = (num_hand_cards * hand_w) + ((num_hand_cards - 1) * 10)
    hand_start_x = (SCREEN_WIDTH - hand_total_width) / 2
    for i in range(num_hand_cards):
        pygame.draw.rect(surface, GRAY, (hand_start_x + i * (hand_w + 10), p1_hand_y, hand_w, hand_h), border_radius=8)
        pygame.draw.rect(surface, DARK_GRAY, (hand_start_x + i * (hand_w + 10), p1_hand_y, hand_w, hand_h), 2,
                         border_radius=8)

    # Banc
    bench_total_width = (3 * slot_w) + (2 * gap)
    bench_start_x = (SCREEN_WIDTH - bench_total_width) / 2
    for i in range(3):
        pygame.draw.rect(surface, (10, 150, 120), (bench_start_x + i * (slot_w + gap), p1_bench_y, slot_w, slot_h), 3,
                         border_radius=10)

    # Actif
    pygame.draw.rect(surface, (250, 200, 0), (SCREEN_WIDTH / 2 - slot_w / 2, p1_active_y, slot_w, slot_h), 3,
                     border_radius=10)

    # Deck, Défausse, Énergie
    deck_area_y = p1_bench_y + (slot_h - 60) / 2
    pygame.draw.rect(surface, DARK_GRAY, (SCREEN_WIDTH - 230, p1_bench_y, 80, 110), border_radius=5)
    draw_text("Deck", "small", WHITE, surface, SCREEN_WIDTH - 190, p1_bench_y + 50)
    pygame.draw.rect(surface, DARK_GRAY, (SCREEN_WIDTH - 120, p1_bench_y, 80, 110), border_radius=5)
    draw_text("Défausse", "small", WHITE, surface, SCREEN_WIDTH - 80, p1_bench_y + 50)
    pygame.draw.circle(surface, RED, (SCREEN_WIDTH - 135, p1_hand_y + hand_h / 2 ), 15)  # Energie

    # --- Zones du Joueur 2 (Adversaire - en haut) ---
    p2_hand_y = gap
    p2_bench_y = p2_hand_y + hand_h + gap
    p2_active_y = p2_bench_y + slot_h + gap

    # Main (plus grande)
    for i in range(num_hand_cards):
        pygame.draw.rect(surface, BLACK, (hand_start_x + i * (hand_w + 10), p2_hand_y, hand_w, hand_h), border_radius=8)

    # Banc (plus petit)
    for i in range(3):
        pygame.draw.rect(surface, (150, 10, 120), (bench_start_x + i * (slot_w + gap), p2_bench_y, slot_w, slot_h), 3,
                         border_radius=10)

    # Actif (plus petit)
    pygame.draw.rect(surface, (250, 200, 0), (SCREEN_WIDTH / 2 - slot_w / 2, p2_active_y, slot_w, slot_h), 3,
                     border_radius=10)

    # Deck, Défausse, Énergie
    deck_area_y_p2 = p2_bench_y + (slot_h - 60) / 2
    pygame.draw.rect(surface, DARK_GRAY, (40, p2_bench_y, 80, 110), border_radius=5)
    draw_text("Défausse", "small", WHITE, surface, 80, p2_bench_y + 50)
    pygame.draw.rect(surface, DARK_GRAY, (150, p2_bench_y, 80, 110), border_radius=5)
    draw_text("Deck", "small", WHITE, surface, 190, p2_bench_y + 50)
    pygame.draw.circle(surface, RED, (135, p2_hand_y + hand_h / 2), 15)  # Energie

    # Message et bouton
    draw_text(f"Joueur {starting_player} commence la partie !", 'subtitle', WHITE, surface, SCREEN_WIDTH / 2, 20)
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