"""
Classe ScoreManager - Gerencia pontuação e ranking do jogo ByThePong
Implementa encapsulamento com atributos privados e métodos públicos
"""

import json
import os
from typing import List, Dict, Tuple, Optional
from player import Player
from player_registry import PlayerRegistry

class ScoreManager:
    def __init__(self, ranking_file: str = "ranking.json"):
        """
        Inicializa o gerenciador de pontuação
        
        Args:
            ranking_file (str): Nome do arquivo para salvar o ranking
        """
        self.__ranking_file = ranking_file
        self.__player_registry = PlayerRegistry()
        self.__ranking = self.__load_ranking()
        self.__max_ranking_size = 10
    
    def __load_ranking(self) -> List[Dict[str, int]]:
        """
        Carrega o ranking do arquivo JSON
        
        Returns:
            List[Dict[str, int]]: Lista de jogadores no ranking
        """
        if os.path.exists(self.__ranking_file):
            try:
                with open(self.__ranking_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def __save_ranking(self):
        """Salva o ranking no arquivo JSON"""
        try:
            with open(self.__ranking_file, 'w', encoding='utf-8') as f:
                json.dump(self.__ranking, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar ranking: {e}")
    
    def add_score(self, player_name: str, score: int, won: bool = False):
        """
        Adiciona uma pontuação ao ranking e atualiza estatísticas do jogador
        
        Args:
            player_name (str): Nome do jogador
            score (int): Pontuação alcançada
            won (bool): True se o jogador venceu, False caso contrário
        """
        # Registra ou atualiza jogador no registry
        if not self.__player_registry.player_exists(player_name):
            self.__player_registry.register_player(player_name)
        
        # Atualiza estatísticas do jogador
        self.__player_registry.update_player_stats(player_name, score, won)
        
        # Obtém estatísticas atualizadas do jogador
        player_stats = self.__player_registry.get_player_stats(player_name)
        
        if player_stats:
            # Remove entrada antiga do mesmo jogador (se existir)
            self.__ranking = [entry for entry in self.__ranking 
                            if entry.get("name", "").lower() != player_name.lower()]
            
            # Adiciona nova entrada com dados completos
            new_entry = {
                "name": player_stats["name"],
                "score": player_stats["best_score"],  # Usa best_score para ranking
                "total_games": player_stats.get("total_games", 0),
                "total_wins": player_stats.get("total_wins", 0),
                "best_score": player_stats.get("best_score", 0)
            }
            self.__ranking.append(new_entry)
            
            # Ordena por best_score (maior primeiro)
            self.__ranking.sort(key=lambda x: x.get("best_score", 0), reverse=True)
            
            # Mantém apenas os top 10
            if len(self.__ranking) > self.__max_ranking_size:
                self.__ranking = self.__ranking[:self.__max_ranking_size]
            
            # Adiciona posição a cada entrada
            for i, entry in enumerate(self.__ranking, 1):
                entry["position"] = i
            
            # Salva no arquivo
            self.__save_ranking()
    
    def get_ranking(self) -> List[Dict[str, int]]:
        """
        Retorna o ranking atual
        
        Returns:
            List[Dict[str, int]]: Lista ordenada do ranking
        """
        return self.__ranking.copy()
    
    def get_top_score(self) -> int:
        """
        Retorna a maior pontuação do ranking
        
        Returns:
            int: Maior pontuação ou 0 se não houver ranking
        """
        if self.__ranking:
            return self.__ranking[0].get("best_score", self.__ranking[0].get("score", 0))
        return 0
    
    def get_player_best_score(self, player_name: str) -> int:
        """
        Retorna a melhor pontuação de um jogador específico
        
        Args:
            player_name (str): Nome do jogador
            
        Returns:
            int: Melhor pontuação do jogador ou 0 se não encontrado
        """
        player_stats = self.__player_registry.get_player_stats(player_name)
        if player_stats:
            return player_stats.get("best_score", 0)
        return 0
    
    def get_player_stats(self, player_name: str) -> Optional[Dict]:
        """
        Retorna as estatísticas completas de um jogador
        
        Args:
            player_name (str): Nome do jogador
            
        Returns:
            Optional[Dict]: Estatísticas do jogador ou None se não encontrado
        """
        return self.__player_registry.get_player_stats(player_name)
    
    def clear_ranking(self):
        """Limpa todo o ranking"""
        self.__ranking = []
        self.__save_ranking()
    
    def get_ranking_display(self) -> str:
        """
        Retorna uma string formatada do ranking para exibição
        
        Returns:
            str: Ranking formatado
        """
        if not self.__ranking:
            return "Nenhuma pontuação registrada ainda!"
        
        display = "🏆 RANKING TOP 10 🏆\n"
        display += "=" * 30 + "\n"
        
        for i, entry in enumerate(self.__ranking, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
            best_score = entry.get("best_score", entry.get("score", 0))
            total_games = entry.get("total_games", 0)
            total_wins = entry.get("total_wins", 0)
            display += f"{medal} {entry['name']}: {best_score} pts | Jogos: {total_games} | Vitórias: {total_wins}\n"
        
        return display
