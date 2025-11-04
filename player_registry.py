"""
Classe PlayerRegistry - Gerencia cadastro de jogadores persistente em arquivo local
Implementa encapsulamento com atributos privados e métodos públicos
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List

class PlayerRegistry:
    def __init__(self, players_file: str = "players.json"):
        """
        Inicializa o registro de jogadores
        
        Args:
            players_file (str): Nome do arquivo para salvar os jogadores
        """
        self.__players_file = players_file
        self.__players = self.__load_players()
    
    def __load_players(self) -> Dict[str, Dict]:
        """
        Carrega os jogadores do arquivo JSON
        
        Returns:
            Dict[str, Dict]: Dicionário com nome do jogador como chave e dados como valor
        """
        if os.path.exists(self.__players_file):
            try:
                with open(self.__players_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Converte lista para dicionário se necessário (compatibilidade)
                    if isinstance(data, list):
                        players_dict = {}
                        for player in data:
                            if isinstance(player, dict) and 'name' in player:
                                players_dict[player['name'].lower()] = player
                        return players_dict
                    elif isinstance(data, dict) and 'players' in data:
                        players_dict = {}
                        for player in data['players']:
                            if isinstance(player, dict) and 'name' in player:
                                players_dict[player['name'].lower()] = player
                        return players_dict
                    elif isinstance(data, dict):
                        # Já está no formato de dicionário
                        return data
            except (json.JSONDecodeError, FileNotFoundError, KeyError):
                return {}
        return {}
    
    def __save_players(self):
        """Salva os jogadores no arquivo JSON"""
        try:
            # Salva no formato com chave "players" para organização
            data = {"players": list(self.__players.values())}
            with open(self.__players_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar jogadores: {e}")
    
    def register_player(self, name: str) -> bool:
        """
        Registra um novo jogador ou retorna False se já existe
        
        Args:
            name (str): Nome do jogador
            
        Returns:
            bool: True se jogador foi registrado, False se já existe
        """
        name_lower = name.strip().lower()
        name_proper = name.strip()
        
        if not name_proper:
            raise ValueError("Nome do jogador não pode estar vazio")
        
        if name_lower in self.__players:
            return False
        
        now = datetime.now().isoformat()
        self.__players[name_lower] = {
            "name": name_proper,
            "total_games": 0,
            "total_wins": 0,
            "best_score": 0,
            "created_at": now,
            "last_played": now
        }
        
        self.__save_players()
        return True
    
    def get_player(self, name: str) -> Optional[Dict]:
        """
        Retorna os dados de um jogador
        
        Args:
            name (str): Nome do jogador
            
        Returns:
            Optional[Dict]: Dados do jogador ou None se não encontrado
        """
        name_lower = name.strip().lower()
        return self.__players.get(name_lower)
    
    def player_exists(self, name: str) -> bool:
        """
        Verifica se um jogador já está cadastrado
        
        Args:
            name (str): Nome do jogador
            
        Returns:
            bool: True se jogador existe, False caso contrário
        """
        name_lower = name.strip().lower()
        return name_lower in self.__players
    
    def update_player_stats(self, name: str, score: int, won: bool = False):
        """
        Atualiza as estatísticas de um jogador após uma partida
        
        Args:
            name (str): Nome do jogador
            score (int): Pontuação alcançada na partida
            won (bool): True se o jogador venceu, False caso contrário
        """
        name_lower = name.strip().lower()
        
        if name_lower not in self.__players:
            # Se jogador não existe, registra automaticamente
            self.register_player(name)
        
        player = self.__players[name_lower]
        player["total_games"] = player.get("total_games", 0) + 1
        
        if won:
            player["total_wins"] = player.get("total_wins", 0) + 1
        
        # Atualiza melhor pontuação se necessário
        current_best = player.get("best_score", 0)
        if score > current_best:
            player["best_score"] = score
        
        # Atualiza última vez que jogou
        player["last_played"] = datetime.now().isoformat()
        
        self.__save_players()
    
    def get_all_players(self) -> List[Dict]:
        """
        Retorna todos os jogadores cadastrados
        
        Returns:
            List[Dict]: Lista com todos os jogadores
        """
        return list(self.__players.values())
    
    def get_player_stats(self, name: str) -> Optional[Dict]:
        """
        Retorna as estatísticas completas de um jogador
        
        Args:
            name (str): Nome do jogador
            
        Returns:
            Optional[Dict]: Estatísticas do jogador ou None se não encontrado
        """
        return self.get_player(name)
    
    def get_top_players_by_best_score(self, limit: int = 10) -> List[Dict]:
        """
        Retorna os melhores jogadores ordenados por best_score
        
        Args:
            limit (int): Número máximo de jogadores a retornar
            
        Returns:
            List[Dict]: Lista de jogadores ordenados por best_score
        """
        players = list(self.__players.values())
        players.sort(key=lambda x: x.get("best_score", 0), reverse=True)
        return players[:limit]

