import pygame
import random
import sys

# Inicjalizacja pygame
pygame.init()

# Stałe gry
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset_game()
    
    def reset_game(self):
        """Resetuje grę do stanu początkowego"""
        # Wąż zaczyna w środku
        self.snake = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = [1, 0]  # Początkowo idzie w prawo
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
    
    def generate_food(self):
        """Generuje nowe jedzenie w losowym miejscu"""
        while True:
            food = (random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1))
            if food not in self.snake:
                return food
    
    def handle_events(self):
        """Obsługuje zdarzenia klawiatury"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif not self.game_over:
                    # Zmiana kierunku (nie można iść w przeciwnym kierunku)
                    if event.key == pygame.K_UP and self.direction != [0, 1]:
                        self.direction = [0, -1]
                    elif event.key == pygame.K_DOWN and self.direction != [0, -1]:
                        self.direction = [0, 1]
                    elif event.key == pygame.K_LEFT and self.direction != [1, 0]:
                        self.direction = [-1, 0]
                    elif event.key == pygame.K_RIGHT and self.direction != [-1, 0]:
                        self.direction = [1, 0]
        return True
    
    def update(self):
        """Aktualizuje stan gry"""
        if self.game_over:
            return
        
        # Nowa pozycja głowy węża
        new_head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )
        
        # Sprawdzenie kolizji ze ścianą
        if (new_head[0] < 0 or new_head[0] >= GRID_COUNT or 
            new_head[1] < 0 or new_head[1] >= GRID_COUNT):
            self.game_over = True
            return
        
        # Sprawdzenie kolizji z własnym ciałem
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Dodanie nowej głowy
        self.snake.insert(0, new_head)
        
        # Sprawdzenie czy wąż zjadł jedzenie
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            # Usunięcie ogona jeśli nie zjadł jedzenia
            self.snake.pop()
    
    def draw(self):
        """Rysuje grę"""
        self.screen.fill(BLACK)
        
        # Rysowanie węża
        for i, segment in enumerate(self.snake):
            color = GREEN if i == 0 else BLUE  # Głowa zielona, reszta niebieska
            pygame.draw.rect(self.screen, color, 
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                            GRID_SIZE - 1, GRID_SIZE - 1))
        
        # Rysowanie jedzenia
        pygame.draw.rect(self.screen, RED,
                        (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE,
                         GRID_SIZE - 1, GRID_SIZE - 1))
        
        # Rysowanie siatki (opcjonalne)
        for x in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, WINDOW_SIZE))
        for y in range(0, WINDOW_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (WINDOW_SIZE, y))
        
        # Wyświetlanie punktacji
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Komunikat o końcu gry
        if self.game_over:
            game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Główna pętla gry"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 