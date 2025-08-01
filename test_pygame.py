import pygame
import sys

# Inicjalizacja pygame
pygame.init()

# Tworzenie okna
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Test Pygame")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Główna pętla
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Wypełnienie ekranu
    screen.fill(WHITE)
    
    # Rysowanie czerwonego kwadratu
    pygame.draw.rect(screen, RED, (150, 100, 100, 100))
    
    # Aktualizacja ekranu
    pygame.display.flip()

pygame.quit()
sys.exit() 