### ui_components.py ###
import pygame
from config import FONTS, WHITE, BLACK, BLUE, DARK_GRAY, GRAY, YELLOW


def draw_text(text, font_name, color, surface, x, y, center=True):
    """Fonction utilitaire pour dessiner du texte."""
    font = FONTS.get(font_name, FONTS['default'])
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect


class Button:
    """Classe simple pour créer et dessiner un bouton."""

    def __init__(self, x, y, width, height, text, font_name='button', color=DARK_GRAY, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_name = font_name
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        draw_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, draw_color, self.rect, border_radius=10)
        draw_text(self.text, self.font_name, WHITE, surface, self.rect.centerx, self.rect.centery)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered


class TextInputBox:
    """Classe pour une zone de saisie de texte."""

    def __init__(self, x, y, w, h, font_name='default', text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.font_name = font_name
        self.active_color = YELLOW
        self.inactive_color = GRAY
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)
        draw_text(self.text, self.font_name, BLACK, screen, self.rect.x + 5, self.rect.centery, center=False)