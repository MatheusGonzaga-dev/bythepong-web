<!-- fad330ca-33d0-4b70-9ddc-b5836b054be7 da469988-cbb7-40ca-9ce5-cb930304f9a1 -->
# Sistema de Cadastro de Jogadores e Ranking

## Objetivo

Criar sistema de cadastro de jogadores persistente em arquivo local (`players.json`) e melhorar o ranking para ser organizado e correto, evitando múltiplas entradas do mesmo jogador.

## Arquivos que serão modificados/criados

### 1. Novo arquivo: `player_registry.py`

- Classe `PlayerRegistry` para gerenciar cadastro de jogadores
- Salva em `players.json` com estrutura:
  ```json
  {
    "players": [
      {
        "name": "nome",
        "total_games": 0,
        "total_wins": 0,
        "best_score": 0,
        "created_at": "timestamp",
        "last_played": "timestamp"
      }
    ]
  }
  ```

- Métodos: `register_player()`, `get_player()`, `update_player_stats()`, `get_all_players()`

### 2. Modificar `score_manager.py`

- Integrar com `PlayerRegistry`
- Modificar `add_score()` para:
  - Registrar jogador se não existir
  - Atualizar estatísticas (total_games, total_wins, best_score)
  - Manter apenas uma entrada por jogador no ranking (atualizar se score for melhor)
- Adicionar método `get_player_stats()` para retornar estatísticas completas

### 3. Modificar `menu.py`

- Na tela de entrada de nome, verificar se jogador já existe
- Se novo jogador, cadastrar automaticamente
- Mostrar mensagem de boas-vindas para novos jogadores
- Mostrar estatísticas do jogador existente (opcional)

### 4. Modificar `game.py`

- Garantir que ao final do jogo, o jogador seja registrado e estatísticas atualizadas
- Considerar vitória/derrota para atualizar `total_wins`

### 5. Melhorar `ranking.json`

- Estrutura melhorada com dados do jogador:
  ```json
  [
    {
      "name": "nome",
      "score": 10,
      "total_games": 5,
      "total_wins": 3,
      "best_score": 10,
      "position": 1
    }
  ]
  ```


## Fluxo de funcionamento

1. **Primeira vez jogando:**

   - Jogador digita nome no menu
   - Sistema verifica se existe em `players.json`
   - Se não existe, cria novo registro
   - Inicia jogo

2. **Jogador existente:**

   - Sistema carrega dados do jogador
   - Mostra estatísticas (opcional)
   - Inicia jogo

3. **Ao finalizar partida:**

   - Atualiza `total_games` (+1)
   - Se venceu, atualiza `total_wins` (+1)
   - Se score > `best_score`, atualiza `best_score`
   - Atualiza `last_played`
   - Adiciona ao ranking (se for top 10) ou atualiza posição existente

4. **Ranking:**

   - Ordenado por `best_score` (melhor pontuação)
   - Máximo 10 jogadores
   - Cada jogador aparece apenas uma vez
   - Mostra posição, nome, best_score, total_games, total_wins

## Implementação

### Fase 1: Criar PlayerRegistry

- Criar classe com métodos de CRUD para jogadores
- Salvar/carregar de `players.json`
- Validação de dados

### Fase 2: Integrar com ScoreManager

- Modificar `add_score()` para usar `PlayerRegistry`
- Atualizar lógica de ranking para evitar duplicatas
- Incluir estatísticas no ranking

### Fase 3: Integrar no Menu

- Verificar/cadastrar jogador na entrada de nome
- Mostrar mensagem de boas-vindas (opcional)

### Fase 4: Integrar no Game

- Atualizar estatísticas ao finalizar partida
- Passar informação de vitória/derrota

### Fase 5: Melhorar exibição do ranking

- Mostrar mais informações na tela de ranking
- Formatação melhorada

## Benefícios

- Cadastro persistente de jogadores
- Ranking organizado sem duplicatas
- Histórico de jogos por jogador
- Estatísticas completas (vitórias, melhor score, etc.)
- Tudo salvo em arquivos locais (sem banco de dados)

### To-dos

- [ ] Adicionar prev_x/prev_y e getters em ball.py
- [ ] Aplicar colisão swept para raquete esquerda em game.py
- [ ] Aplicar colisão swept para raquete direita em game.py
- [ ] Adicionar correção anti-stuck pós-colisão em game.py
- [ ] Testar manualmente em normal/difícil/expert