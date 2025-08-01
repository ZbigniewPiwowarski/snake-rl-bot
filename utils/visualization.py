import pygame

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

class GameRenderer:
    """Zarządza wizualizacją gry"""
    
    def __init__(self, screen, window_size, grid_size, game=None):
        self.screen = screen
        self.window_size = window_size
        self.grid_size = grid_size
        self.grid_count = window_size // grid_size
        self.game = game  # Referencja do gry
    
    def draw_snake(self, snake, is_agent=False):
        """Rysuje węża"""
        for i, segment in enumerate(snake):
            if is_agent:
                color = YELLOW if i == 0 else PURPLE  # Agent: żółta głowa, fioletowe ciało
            else:
                color = GREEN if i == 0 else BLUE  # Człowiek: zielona głowa, niebieskie ciało
            pygame.draw.rect(self.screen, color, 
                           (segment[0] * self.grid_size, segment[1] * self.grid_size, 
                            self.grid_size - 1, self.grid_size - 1))
    
    def draw_food(self, food):
        """Rysuje jedzenie"""
        pygame.draw.rect(self.screen, RED,
                        (food[0] * self.grid_size, food[1] * self.grid_size,
                         self.grid_size - 1, self.grid_size - 1))
    
    def draw_grid(self):
        """Rysuje siatkę"""
        for x in range(0, self.window_size, self.grid_size):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, self.window_size))
        for y in range(0, self.window_size, self.grid_size):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (self.window_size, y))
    
    def draw_info(self, score, mode, games_played=None, current_steps=None):
        """Rysuje informacje o grze"""
        font = pygame.font.Font(None, 24)
        
        # Punktacja
        score_text = font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Tryb gry
        mode_text = font.render(f"Mode: {mode}", True, WHITE)
        self.screen.blit(mode_text, (10, 35))
        
        # Informacje o agencie
        if self.game and self.game.agent_mode:
            games_text = font.render(f"Games: {games_played}", True, WHITE)
            self.screen.blit(games_text, (10, 60))
            
            steps_text = font.render(f"Steps: {current_steps}", True, WHITE)
            self.screen.blit(steps_text, (10, 85))
            
            # Status automatycznych trybów
            auto_status = []
            if hasattr(self.game, 'auto_agent') and self.game.auto_agent:
                auto_status.append("Auto Agent: ON")
            if hasattr(self.game, 'auto_restart') and self.game.auto_restart:
                auto_status.append("Auto Restart: ON")
            
            if auto_status:
                auto_text = font.render(" | ".join(auto_status), True, (255, 255, 0))
                self.screen.blit(auto_text, (10, 110))
    
    def draw_pause(self):
        """Rysuje informację o pauzie"""
        font = pygame.font.Font(None, 24)
        pause_text = font.render("PAUSED", True, YELLOW)
        text_rect = pause_text.get_rect(center=(self.window_size // 2, 50))
        self.screen.blit(pause_text, text_rect)
    
    def draw_game_over(self):
        """Rysuje komunikat o końcu gry"""
        font = pygame.font.Font(None, 24)
        game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
        text_rect = game_over_text.get_rect(center=(self.window_size // 2, self.window_size // 2))
        self.screen.blit(game_over_text, text_rect)
    
    def draw_instructions(self):
        """Rysuje instrukcje"""
        font = pygame.font.Font(None, 24)
        instructions = [
            "H - Human mode",
            "A - Agent mode", 
            "1 - Auto agent ON",
            "2 - Auto agent OFF",
            "3 - Auto restart ON",
            "4 - Auto restart OFF",
            "P - Pause/Resume",
            "S - Save model",
            "L - Load model",
            "T - Show TXT report",
            "V - List reports",
            "C - Clean old files",
            "R - Restart",
            "ESC - Exit"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = font.render(instruction, True, (100, 100, 100))
            self.screen.blit(inst_text, (self.window_size - 200, 10 + i * 20))
    
    def render_frame(self, snake, food, score, mode, games_played=None, 
                    current_steps=None, paused=False, game_over=False):
        """Renderuje całą klatkę gry"""
        self.screen.fill(BLACK)
        
        # Rysowanie elementów gry
        self.draw_snake(snake, mode == "Agent")
        self.draw_food(food)
        self.draw_grid()
        
        # Rysowanie informacji
        self.draw_info(score, mode, games_played, current_steps)
        
        # Rysowanie stanów specjalnych
        if paused:
            self.draw_pause()
        if game_over:
            self.draw_game_over()
        
        # Rysowanie instrukcji
        self.draw_instructions()
        
        pygame.display.flip() 