from django.db import models
from django.utils import timezone

class Player(models.Model):
    """Classe para representar um jogador com encapsulamento"""
    name = models.CharField(max_length=50, unique=True)
    total_games = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    @property
    def win_rate(self):
        """Taxa de vitórias do jogador"""
        if self.total_games == 0:
            return 0
        return (self.total_wins / self.total_games) * 100
    
    def add_game_result(self, score, won):
        """Adiciona resultado de uma partida"""
        self.total_games += 1
        if won:
            self.total_wins += 1
        if score > self.best_score:
            self.best_score = score
        self.save()

class GameSession(models.Model):
    """Sessão de jogo com encapsulamento"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=[
        ('fácil', 'Fácil'),
        ('normal', 'Normal'),
        ('difícil', 'Difícil'),
        ('expert', 'Expert'),
    ])
    player_score = models.IntegerField(default=0)
    bot_score = models.IntegerField(default=0)
    game_duration = models.IntegerField(default=0)  # em segundos
    won = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.player.name} - {self.difficulty} - {self.player_score}x{self.bot_score}"
    
    @property
    def result_text(self):
        """Texto do resultado da partida"""
        if self.won:
            return "Vitória"
        elif self.player_score == self.bot_score:
            return "Empate"
        else:
            return "Derrota"

