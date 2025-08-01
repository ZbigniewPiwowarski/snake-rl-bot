import pickle
import os
from datetime import datetime

class ModelManager:
    """Zarządza zapisywaniem i wczytywaniem modeli agentów"""
    
    def __init__(self, models_dir="models"):
        self.models_dir = models_dir
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
    
    def save_model(self, agent, games_played, best_score=0, filename=None, total_restarts=0):
        """Zapisuje model agenta"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snake_model_{games_played}_{timestamp}.pkl"
        
        filepath = os.path.join(self.models_dir, filename)
        model_data = {
            'agent': agent,
            'games_played': games_played,
            'best_score': best_score,
            'total_restarts': total_restarts,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Zapis w formacie .pkl
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            print(f"Model zapisany: {filepath}")
            
            # Zapis w formacie .txt (czytelny)
            txt_filename = filename.replace('.pkl', '.txt')
            txt_filepath = os.path.join(self.models_dir, txt_filename)
            self._save_txt_report(model_data, txt_filepath)
            
            return True
        except Exception as e:
            print(f"Błąd zapisywania: {e}")
            return False
    
    def _save_txt_report(self, model_data, filepath):
        """Zapisuje raport w formacie TXT"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=== RAPORT AGENTA SNAKE ===\n")
                f.write(f"Data zapisu: {model_data['timestamp']}\n")
                f.write(f"Typ agenta: {model_data['agent'].__class__.__name__}\n")
                f.write(f"Liczba rozegranych gier: {model_data['games_played']}\n")
                f.write(f"Najlepszy wynik: {model_data['best_score']} punktów\n")
                f.write(f"Liczba restartów: {model_data.get('total_restarts', 0)}\n")
                
                # Dodatkowe informacje o agencie
                if hasattr(model_data['agent'], 'name'):
                    f.write(f"Nazwa agenta: {model_data['agent'].name}\n")
                
                # Statystyki (jeśli dostępne)
                if hasattr(model_data['agent'], 'get_stats'):
                    stats = model_data['agent'].get_stats()
                    f.write("\n=== STATYSTYKI ===\n")
                    for key, value in stats.items():
                        f.write(f"{key}: {value}\n")
                
                # Szczegółowe statystyki ruchów
                if hasattr(model_data['agent'], 'get_detailed_stats'):
                    detailed_stats = model_data['agent'].get_detailed_stats()
                    if detailed_stats:
                        f.write("\n=== SZCZEGÓŁOWE STATYSTYKI RUCHÓW ===\n")
                        f.write(f"Zarejestrowane ruchy: {detailed_stats.get('total_moves_recorded', 0)}\n")
                        f.write(f"Ostatnie ruchy (analiza): {detailed_stats.get('recent_moves', 0)}\n")
                        f.write(f"Udane ruchy: {detailed_stats.get('successful_moves_count', 0)}\n")
                        f.write(f"Wzorce sukcesu: {detailed_stats.get('successful_patterns_count', 0)}\n")
                        f.write(f"Wzorce porażki: {detailed_stats.get('failed_patterns_count', 0)}\n")
                        f.write(f"Średni wynik: {detailed_stats.get('average_score', 0):.2f}\n")
                        
                        # Rozkład akcji
                        action_dist = detailed_stats.get('action_distribution', {})
                        if action_dist:
                            f.write("\nRozkład akcji (ostatnie 100 ruchów):\n")
                            for action, count in action_dist.items():
                                action_names = {0: 'góra', 1: 'dół', 2: 'lewo', 3: 'prawo'}
                                f.write(f"  {action_names.get(action, action)}: {count}\n")
                
                f.write("\n=== INFORMACJE TECHNICZNE ===\n")
                f.write(f"Plik .pkl: {filepath.replace('.txt', '.pkl')}\n")
                f.write(f"Plik .txt: {filepath}\n")
                
            print(f"Raport TXT zapisany: {filepath}")
        except Exception as e:
            print(f"Błąd zapisywania raportu TXT: {e}")
    
    def load_model(self, filename):
        """Wczytuje model agenta"""
        filepath = os.path.join(self.models_dir, filename)
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            print(f"Model wczytany: {filepath}")
            return model_data
        except Exception as e:
            print(f"Błąd wczytywania: {e}")
            return None
    
    def get_latest_model(self):
        """Zwraca nazwę najnowszego modelu"""
        files = [f for f in os.listdir(self.models_dir) if f.endswith('.pkl')]
        if files:
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(self.models_dir, x)))
            return latest_file
        return None
    
    def list_models(self):
        """Listuje wszystkie dostępne modele"""
        files = [f for f in os.listdir(self.models_dir) if f.endswith('.pkl')]
        return sorted(files, key=lambda x: os.path.getctime(os.path.join(self.models_dir, x)), reverse=True)
    
    def print_model_summary(self, filename=None):
        """Wyświetla podsumowanie modelu w konsoli"""
        if filename is None:
            filename = self.get_latest_model()
        
        if filename:
            txt_filename = filename.replace('.pkl', '.txt')
            txt_filepath = os.path.join(self.models_dir, txt_filename)
            
            if os.path.exists(txt_filepath):
                print(f"\n=== PODSUMOWANIE MODELU: {filename} ===")
                with open(txt_filepath, 'r', encoding='utf-8') as f:
                    print(f.read())
            else:
                print(f"Nie znaleziono raportu TXT dla: {filename}")
        else:
            print("Brak dostępnych modeli")
    
    def list_all_reports(self):
        """Listuje wszystkie raporty TXT"""
        txt_files = [f for f in os.listdir(self.models_dir) if f.endswith('.txt')]
        if txt_files:
            print("\n=== DOSTĘPNE RAPORTY ===")
            for txt_file in sorted(txt_files, reverse=True):
                filepath = os.path.join(self.models_dir, txt_file)
                creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
                print(f"📄 {txt_file} (utworzony: {creation_time.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print("Brak dostępnych raportów TXT") 
    
    def cleanup_old_files(self, keep_last=10):
        """Usuwa stare pliki, zostawia tylko ostatnie keep_last"""
        pkl_files = [f for f in os.listdir(self.models_dir) if f.endswith('.pkl')]
        txt_files = [f for f in os.listdir(self.models_dir) if f.endswith('.txt')]
        
        # Sortuj po dacie utworzenia (najnowsze pierwsze)
        pkl_files.sort(key=lambda x: os.path.getctime(os.path.join(self.models_dir, x)), reverse=True)
        txt_files.sort(key=lambda x: os.path.getctime(os.path.join(self.models_dir, x)), reverse=True)
        
        # Usuń stare pliki
        for old_file in pkl_files[keep_last:]:
            filepath = os.path.join(self.models_dir, old_file)
            os.remove(filepath)
            print(f"Usunięto stary plik: {old_file}")
        
        for old_file in txt_files[keep_last:]:
            filepath = os.path.join(self.models_dir, old_file)
            os.remove(filepath)
            print(f"Usunięto stary plik: {old_file}")
        
        print(f"Zachowano ostatnie {keep_last} plików")
    
    def get_disk_usage(self):
        """Zwraca informacje o użyciu dysku"""
        total_size = 0
        file_count = 0
        
        for filename in os.listdir(self.models_dir):
            filepath = os.path.join(self.models_dir, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
                file_count += 1
        
        return {
            'file_count': file_count,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'average_size_kb': round(total_size / file_count / 1024, 2) if file_count > 0 else 0
        } 