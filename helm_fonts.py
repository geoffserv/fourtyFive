import pygame
# Fonts used throughout the project

font = {}


def init_fonts():
    # Don't call this until after pygame.init() in the master module.
    # On Mac OS, this initialization is very slow and takes several seconds.
    global font
    font = {'small_bold': pygame.font.SysFont('courier', 24, bold=True),
            'medium': pygame.font.SysFont('courier', 32),
            'medium_bold': pygame.font.SysFont('courier', 32, bold=True),
            'x_large': pygame.font.SysFont('courier', 80)}
