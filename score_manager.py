"""
Classe ScoreManager - Gerencia pontuação e ranking do jogo ByThePong
Implementa encapsulamento com atributos privados e métodos públicos
"""

import json
import os
from typing import List, Dict, Tuple
from player import Player

class ScoreManager:
    def __init__(self, ranking_file: str = "ranking.json"):
        """
        Inicializa o gerenciador de pontuação
        
        Args:
            ranking_file (str): Nome do arquivo para salvar o ranking
        """
        self.__ranking_file = ranking_file
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
    
    def add_score(self, player_name: str, score: int):
        """
        Adiciona uma pontuação ao ranking
        
        Args:
            player_name (str): Nome do jogador
            score (int): Pontuação alcançada
        """
        # Adiciona nova pontuação
        new_entry = {"name": player_name, "score": score}
        self.__ranking.append(new_entry)
        
        # Ordena por pontuação (maior primeiro)
        self.__ranking.sort(key=lambda x: x["score"], reverse=True)
        
        # Mantém apenas os top 10
        if len(self.__ranking) > self.__max_ranking_size:
            self.__ranking = self.__ranking[:self.__max_ranking_size]
        
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
            return self.__ranking[0]["score"]
        return 0
    
    def get_player_best_score(self, player_name: str) -> int:
        """
        Retorna a melhor pontuação de um jogador específico
        
        Args:
            player_name (str): Nome do jogador
            
        Returns:
            int: Melhor pontuação do jogador ou 0 se não encontrado
        """
        for entry in self.__ranking:
            if entry["name"] == player_name:
                return entry["score"]
        return 0
    
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
            display += f"{medal} {entry['name']}: {entry['score']} pontos\n"
        
        return display
