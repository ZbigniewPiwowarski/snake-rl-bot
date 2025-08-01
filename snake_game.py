import pygame
import random
import sys
from datetime import datetime

# Importy z naszych modułów
from agents.random_agent import RandomAgent
from utils.save_load import ModelManager
from utils.visualization import GameRenderer

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
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Snake Game - Human/Agent Mode")
        self.clock = pygame.time.Clock()
        
        # Inicjalizacja komponentów
        self.agent = RandomAgent()
        self.model_manager = ModelManager()
        self.renderer = GameRenderer(self.screen, WINDOW_SIZE, GRID_SIZE, self)
        
        self.reset_game()
    
    def reset_game(self):
        """Resetuje grę do stanu początkowego"""
        # Wąż zaczyna w środku
        self.snake = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = [1, 0]  # Początkowo idzie w prawo
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.current_game_steps = 0
        self.max_steps_per_game = 1000  # Maksymalna liczba kroków na grę
        
        # Zachowaj licznik gier jeśli agent już grał
        if not hasattr(self, 'games_played'):
            self.games_played = 0
        if not hasattr(self, 'total_restarts'):
            self.total_restarts = 0
        
        # Zachowaj automatyczne tryby
        if not hasattr(self, 'auto_agent'):
            self.auto_agent = False
        if not hasattr(self, 'auto_restart'):
            self.auto_restart = False
        
        # Tryby gry - zachowaj auto_agent
        if self.auto_agent:
            self.human_mode = False
            self.agent_mode = True
            print(f"DEBUG RESET: auto_agent={self.auto_agent}, ustawiam agent_mode=True")
        else:
            self.human_mode = True
            self.agent_mode = False
            print(f"DEBUG RESET: auto_agent={self.auto_agent}, ustawiam agent_mode=False")
        
        self.paused = False
        
        # System zapisywania
        self.save_interval = 50  # Zapisz co 50 gier
    
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
                # Zapisz przed wyjściem
                if self.agent_mode:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    emergency_filename = f"emergency_save_{timestamp}.pkl"
                    self.model_manager.save_model(self.agent, self.games_played, 
                                               getattr(self, 'best_score', 0), emergency_filename, 
                                               getattr(self, 'total_restarts', 0))
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Zapisz przed wyjściem
                    if self.agent_mode:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        emergency_filename = f"emergency_save_{timestamp}.pkl"
                        self.model_manager.save_model(self.agent, self.games_played, 
                                                   getattr(self, 'best_score', 0), emergency_filename, 
                                                   getattr(self, 'total_restarts', 0))
                    return False
                elif event.key == pygame.K_r and self.game_over:  # Restart
                    self.total_restarts += 1
                    self.reset_game()
                elif event.key == pygame.K_h:  # Tryb człowiek
                    self.human_mode = True
                    self.agent_mode = False
                    print("Tryb: Człowiek")
                elif event.key == pygame.K_a:  # Tryb agent
                    self.human_mode = False
                    self.agent_mode = True
                    print("Tryb: Agent")
                elif event.key == pygame.K_p:  # Pauza
                    self.paused = not self.paused
                    print("Pauza" if self.paused else "Wznów")
                elif event.key == pygame.K_s:  # Zapisz
                    if self.agent_mode:
                        self.model_manager.save_model(self.agent, self.games_played, 
                                                   getattr(self, 'best_score', 0), 
                                                   total_restarts=getattr(self, 'total_restarts', 0))
                elif event.key == pygame.K_l:  # Wczytaj
                    if self.agent_mode:
                        latest_model = self.model_manager.get_latest_model()
                        if latest_model:
                            model_data = self.model_manager.load_model(latest_model)
                            if model_data:
                                self.agent = model_data['agent']
                                self.games_played = model_data.get('games_played', 0)
                                self.best_score = model_data.get('best_score', 0)
                elif event.key == pygame.K_t:  # Pokaż raport TXT
                    if self.agent_mode:
                        self.model_manager.print_model_summary()
                elif event.key == pygame.K_v:  # Lista raportów
                    if self.agent_mode:
                        self.model_manager.list_all_reports()
                elif event.key == pygame.K_c:  # Czyszczenie starych plików
                    if self.agent_mode:
                        usage = self.model_manager.get_disk_usage()
                        print(f"Użycie dysku: {usage['file_count']} plików, {usage['total_size_mb']} MB")
                        self.model_manager.cleanup_old_files(keep_last=5)
                elif event.key == pygame.K_1:  # Auto agent ON
                    self.auto_agent = True
                    self.agent_mode = True
                    self.human_mode = False
                    print("Auto agent: WŁĄCZONY")
                    print(f"DEBUG: auto_agent={self.auto_agent}, agent_mode={self.agent_mode}")
                elif event.key == pygame.K_2:  # Auto agent OFF
                    self.auto_agent = False
                    self.agent_mode = False
                    self.human_mode = True
                    print("Auto agent: WYŁĄCZONY")
                elif event.key == pygame.K_3:  # Auto restart ON
                    self.auto_restart = True
                    print("Auto restart: WŁĄCZONY")
                    print(f"DEBUG: auto_restart={self.auto_restart}")
                elif event.key == pygame.K_4:  # Auto restart OFF
                    self.auto_restart = False
                    print("Auto restart: WYŁĄCZONY")
                elif not self.game_over and not self.paused and self.human_mode:
                    # Sterowanie człowiekiem
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
        if self.game_over or self.paused:
            return
        
        # Sterowanie agentem
        if self.agent_mode:
            action = self.agent.get_action(self.snake, self.food, self.direction)
            old_snake = self.snake.copy()
            old_food = self.food
            old_direction = self.direction.copy()
            
            self.direction = self.agent.action_to_direction(action)
            self.current_game_steps += 1
        
        # Nowa pozycja głowy węża
        new_head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )
        
        # Sprawdzenie kolizji ze ścianą
        if (new_head[0] < 0 or new_head[0] >= GRID_COUNT or 
            new_head[1] < 0 or new_head[1] >= GRID_COUNT):
            self.game_over = True
            if self.agent_mode:
                # Rejestruj ruch (śmierć)
                self.agent.record_move(old_snake, old_food, old_direction, action, -1, None, old_food, True)
                self.games_played += 1
                # Zapisz co save_interval gier
                if self.games_played % self.save_interval == 0:
                    self.model_manager.save_model(self.agent, self.games_played, 
                                               getattr(self, 'best_score', 0), 
                                               total_restarts=getattr(self, 'total_restarts', 0))
                # Automatyczny restart
                if self.auto_restart:
                    self.total_restarts += 1
                    print(f"DEBUG: Auto restart! total_restarts={self.total_restarts}")
                    self.reset_game()
            return
        
        # Sprawdzenie kolizji z własnym ciałem
        if new_head in self.snake:
            self.game_over = True
            if self.agent_mode:
                # Rejestruj ruch (śmierć)
                self.agent.record_move(old_snake, old_food, old_direction, action, -1, None, old_food, True)
                self.games_played += 1
                if self.games_played % self.save_interval == 0:
                    self.model_manager.save_model(self.agent, self.games_played, 
                                               getattr(self, 'best_score', 0), 
                                               total_restarts=getattr(self, 'total_restarts', 0))
                # Automatyczny restart
                if self.auto_restart:
                    self.total_restarts += 1
                    print(f"DEBUG: Auto restart! total_restarts={self.total_restarts}")
                    self.reset_game()
            return
        
        # Sprawdzenie maksymalnej liczby kroków
        if self.agent_mode and self.current_game_steps >= self.max_steps_per_game:
            self.game_over = True
            if self.agent_mode:
                # Rejestruj ruch (timeout)
                self.agent.record_move(old_snake, old_food, old_direction, action, 0, None, old_food, True)
                self.games_played += 1
                if self.games_played % self.save_interval == 0:
                    self.model_manager.save_model(self.agent, self.games_played, 
                                               getattr(self, 'best_score', 0), 
                                               total_restarts=getattr(self, 'total_restarts', 0))
                # Automatyczny restart
                if self.auto_restart:
                    self.total_restarts += 1
                    print(f"DEBUG: Auto restart! total_restarts={self.total_restarts}")
                    self.reset_game()
            return
        
        # Dodanie nowej głowy
        self.snake.insert(0, new_head)
        
        # Sprawdzenie czy wąż zjadł jedzenie
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
            if self.agent_mode:
                # Rejestruj ruch (sukces - zjadł jedzenie)
                self.agent.record_move(old_snake, old_food, old_direction, action, 1, self.snake, self.food, False)
                self.current_game_steps = 0  # Reset kroków po zjedzeniu
        else:
            # Usunięcie ogona jeśli nie zjadł jedzenia
            self.snake.pop()
            if self.agent_mode:
                # Rejestruj ruch (neutralny)
                self.agent.record_move(old_snake, old_food, old_direction, action, 0, self.snake, self.food, False)
    
    def draw(self):
        """Rysuje grę używając renderera"""
        mode = "Agent" if self.agent_mode else "Human"
        games_played = self.games_played if self.agent_mode else None
        current_steps = self.current_game_steps if self.agent_mode else None
        
        self.renderer.render_frame(
            snake=self.snake,
            food=self.food,
            score=self.score,
            mode=mode,
            games_played=games_played,
            current_steps=current_steps,
            paused=self.paused,
            game_over=self.game_over
        )
    
    def run(self):
        """Główna pętla gry"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            
            # Różne prędkości dla różnych trybów
            if self.agent_mode:
                self.clock.tick(20)  # Szybsze dla agenta
            else:
                self.clock.tick(10)  # Wolniejsze dla człowieka
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 