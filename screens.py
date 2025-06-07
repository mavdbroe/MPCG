### screens.py ###
import pygame
from config import *
from ui_components import draw_text, Button
from card_database import CARD_DATA, CARD_IMAGES


def draw_accueil_screen(surface):
    surface.fill(BLUE)
    draw_text("Pokémon TCG Pocket", 'title', WHITE, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    draw_text("Par Votre Nom", 'subtitle', WHITE, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # MODIFIEZ ICI
    draw_text("Cliquez pour commencer", 'button', GRAY, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.75)


def draw_menu_screen(surface, buttons):
    surface.fill(WHITE)
    draw_text("Menu Principal", 'title', BLACK, surface, SCREEN_WIDTH / 2, 100)
    for button in buttons.values():
        button.draw(surface)


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
            card_count = len(decks[i])
            draw_text(f"{card_count}/20 cartes", 'default', BLACK, surface, slot_rect.left + 150, slot_rect.top + 70)
            buttons[f'apercu_{i}'].draw(surface)
            buttons[f'modifier_{i}'].draw(surface)
            buttons[f'supprimer_{i}'].draw(surface)

    buttons['retour'].draw(surface)


def draw_apercu_deck_screen(surface, deck_content, buttons):
    surface.fill(WHITE)
    draw_text("Aperçu du Deck", 'title', BLACK, surface, SCREEN_WIDTH / 2, 50)

    if not deck_content:
        draw_text("Ce deck est vide.", 'subtitle', BLACK, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    else:
        x_start, y_start = 50, 120
        x, y = x_start, y_start
        padding = 10
        for card_name in deck_content:
            if card_name in CARD_IMAGES:
                surface.blit(CARD_IMAGES[card_name], (x, y))
            x += CARD_WIDTH + padding
            if x + CARD_WIDTH > SCREEN_WIDTH - 50:
                x = x_start
                y += CARD_HEIGHT + padding

    buttons['retour_gestion'].draw(surface)


def draw_editeur_deck_screen(surface, current_deck, available_cards, buttons, text_input, filter_buttons):
    surface.fill(LIGHT_BLUE)

    # Zone de la collection (à gauche)
    collection_rect = pygame.Rect(20, 80, 750, SCREEN_HEIGHT - 100)
    pygame.draw.rect(surface, WHITE, collection_rect, border_radius=10)
    draw_text("Collection (clic pour ajouter)", 'small', BLACK, surface, collection_rect.centerx, 50)

    # Zone du deck (à droite)
    deck_rect = pygame.Rect(collection_rect.right + 20, 80, SCREEN_WIDTH - collection_rect.right - 40,
                            SCREEN_HEIGHT - 100)
    pygame.draw.rect(surface, WHITE, deck_rect, border_radius=10)
    draw_text(f"Deck ({len(current_deck)}/20) (clic pour retirer)", 'small', BLACK, surface, deck_rect.centerx, 50)

    # Filtres
    text_input.draw(surface)
    for btn in filter_buttons.values():
        btn.draw(surface)

    # Affichage des cartes disponibles (la logique de création des boutons est maintenant dans main.py)
    x, y = collection_rect.left + 10, collection_rect.top + 50
    for i, card_name in enumerate(available_cards):
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        surface.blit(CARD_IMAGES[card_name], card_rect.topleft)
        x += CARD_WIDTH + 5
        if x + CARD_WIDTH > collection_rect.right - 10:
            x = collection_rect.left + 10
            y += CARD_HEIGHT + 5

    # Affichage des cartes du deck (la logique de création des boutons est maintenant dans main.py)
    x, y = deck_rect.left + 10, deck_rect.top + 10
    for i, card_name in enumerate(current_deck):
        card_rect = pygame.Rect(x, y, CARD_WIDTH * 0.7, CARD_HEIGHT * 0.7)
        small_img = pygame.transform.scale(CARD_IMAGES[card_name], (card_rect.width, card_rect.height))
        surface.blit(small_img, card_rect.topleft)
        y += 30
        if y + 30 > deck_rect.bottom - 10:
            y = deck_rect.top + 10
            x += card_rect.width + 5

    # Boutons Sauvegarder et Annuler
    buttons['sauvegarder'].draw(surface)
    buttons['annuler'].draw(surface)