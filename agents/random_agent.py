import random
from datetime import datetime

class RandomAgent:
    """Prosty losowy agent"""
    def __init__(self):
        self.name = "Random Agent"
        self.agent_type = "Losowy (nie uczy się)"
        
        # Inicjalizacja list do zbierania danych
        if not hasattr(self, 'movement_history'):
            self.movement_history = []
        if not hasattr(self, 'successful_patterns'):
            self.successful_patterns = []
        if not hasattr(self, 'failed_patterns'):
            self.failed_patterns = []
        self.stats = {
            'total_moves': 0,
            'successful_moves': 0,
            'collision_moves': 0
        }
    
    def record_move(self, snake, food, direction, action, reward, new_snake, new_food, game_over):
        """Zapisuje szczegółowe dane o ruchu"""
        move_data = {
            'timestamp': datetime.now().isoformat(),
            'snake_head': snake[0],
            'snake_body': snake[1:],
            'food_position': food,
            'direction': direction,
            'action': action,
            'reward': reward,
            'new_snake_head': new_snake[0] if new_snake else None,
            'food_eaten': len(new_snake) > len(snake) if new_snake else False,
            'game_over': game_over,
            'game_score': len(snake) - 1
        }
        
        self.movement_history.append(move_data)
        
        # Analiza wzorców
        if reward > 0:  # Sukces
            self.successful_patterns.append({
                'snake_head': snake[0],
                'food_position': food,
                'action': action,
                'direction': direction
            })
        elif reward < 0:  # Porażka
            self.failed_patterns.append({
                'snake_head': snake[0],
                'food_position': food,
                'action': action,
                'direction': direction
            })
    
    def get_detailed_stats(self):
        """Zwraca szczegółowe statystyki"""
        if not self.movement_history:
            return {}
        
        # Analiza ostatnich 100 ruchów
        recent_moves = self.movement_history[-100:]
        
        # Najczęstsze akcje
        actions = [move['action'] for move in recent_moves]
        action_counts = {}
        for action in actions:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        # Najlepsze wzorce (gdy zjadł jedzenie)
        successful_moves = [move for move in recent_moves if move['reward'] > 0]
        
        return {
            'total_moves_recorded': len(self.movement_history),
            'recent_moves': len(recent_moves),
            'action_distribution': action_counts,
            'successful_moves_count': len(successful_moves),
            'successful_patterns_count': len(self.successful_patterns),
            'failed_patterns_count': len(self.failed_patterns),
            'average_score': sum(move['game_score'] for move in recent_moves) / len(recent_moves) if recent_moves else 0
        }
    
    def get_action(self, snake, food, direction):
        """Zwraca losowy kierunek (0=góra, 1=dół, 2=lewo, 3=prawo)"""
        possible_actions = [0, 1, 2, 3]  # góra, dół, lewo, prawo
        
        # Usuń przeciwny kierunek (nie można iść w przeciwnym kierunku)
        if direction == [0, -1]:  # idzie w górę
            possible_actions.remove(1)  # nie może iść w dół
        elif direction == [0, 1]:  # idzie w dół
            possible_actions.remove(0)  # nie może iść w górę
        elif direction == [-1, 0]:  # idzie w lewo
            possible_actions.remove(3)  # nie może iść w prawo
        elif direction == [1, 0]:  # idzie w prawo
            possible_actions.remove(2)  # nie może iść w lewo
        
        self.stats['total_moves'] += 1
        return random.choice(possible_actions)
    
    def action_to_direction(self, action):
        """Konwertuje akcję (0-3) na kierunek [x, y]"""
        if action == 0: return [0, -1]  # góra
        elif action == 1: return [0, 1]   # dół
        elif action == 2: return [-1, 0]  # lewo
        elif action == 3: return [1, 0]   # prawo
        return [1, 0]  # domyślnie prawo
    
    def get_stats(self):
        """Zwraca statystyki agenta"""
        return {
            'nazwa': self.name,
            'wszystkie_ruchy': self.stats['total_moves'],
            'udane_ruchy': self.stats['successful_moves'],
            'kolizje': self.stats['collision_moves'],
            'typ_agenta': self.agent_type
        }
    
    def record_successful_move(self):
        """Zapisuje udany ruch"""
        self.stats['successful_moves'] += 1
    
    def record_collision(self):
        """Zapisuje kolizję"""
        self.stats['collision_moves'] += 1 