# Arquitetura do ByThePong

## Diagrama de Classes

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Player      │    │      Ball       │    │     Paddle      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - __name: str   │    │ - __x: int      │    │ - __x: int      │
│ - __score: int  │    │ - __y: int      │    │ - __y: int      │
├─────────────────┤    │ - __radius: int │    │ - __width: int  │
│ + name: str     │    │ - __speed: float│    │ - __height: int │
│ + score: int    │    │ - __angle: float│    │ - __speed: int  │
│ + add_point()   │    │ - __dx: float   │    ├─────────────────┤
│ + reset_score() │    │ - __dy: float   │    │ + x: int        │
└─────────────────┘    ├─────────────────┤    │ + y: int        │
                       │ + x: int        │    │ + width: int    │
                       │ + y: int        │    │ + height: int   │
                       │ + radius: int   │    │ + speed: int    │
                       │ + speed: float  │    │ + move_up()     │
                       │ + move()        │    │ + move_down()   │
                       │ + bounce_x()    │    │ + set_position()│
                       │ + bounce_y()    │    │ + get_rect()    │
                       │ + bounce_paddle()│   │ + center_y()    │
                       │ + reset()       │    └─────────────────┘
                       │ + get_rect()    │
                       └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  ScoreManager   │    │      Game       │    │      Menu       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - __ranking_file│    │ - __width: int  │    │ - __width: int  │
│ - __ranking: [] │    │ - __height: int │    │ - __height: int │
│ - __max_size: 10│    │ - __screen      │    │ - __screen      │
├─────────────────┤    │ - __player      │    │ - __colors      │
│ + add_score()   │    │ - __ball        │    │ - __fonts       │
│ + get_ranking() │    │ - __left_paddle │    │ - __current_screen│
│ + get_top_score()│   │ - __right_paddle│    │ - __player_name │
│ + get_player_best()│ │ - __score_manager│   │ - __input_active│
│ + clear_ranking()│   │ - __game_running│    │ - __score_manager│
│ + get_ranking_display()│ - __clock      │    │ - __start_game_callback│
└─────────────────┘    │ - __fps: int    │    ├─────────────────┤
                       ├─────────────────┤    │ + set_start_game_callback()│
                       │ + width: int    │    │ + update()       │
                       │ + height: int   │    │ + handle_events()│
                       │ + player: Player│    │ + quit()         │
                       │ + score_manager │    └─────────────────┘
                       │ + set_player_name()│
                       │ + start_game()  │
                       │ + stop_game()   │
                       │ + update()      │
                       │ + handle_events()│
                       │ + quit()        │
                       └─────────────────┘
```

## Fluxo do Programa

```
main.py
    ↓
Menu (menu.py)
    ↓ (callback)
Game (game.py)
    ↓ (usa)
Player + Ball + Paddle + ScoreManager
    ↓ (volta para)
Menu
```

## Princípios de Encapsulamento Aplicados

### 1. Atributos Privados
- Todos os atributos internos usam prefixo `__`
- Acesso controlado através de propriedades

### 2. Propriedades (Getters/Setters)
- `@property` para leitura
- `@property.setter` para escrita com validação

### 3. Métodos Públicos
- Interface clara e bem definida
- Métodos privados para lógica interna

### 4. Validação de Dados
- Setters validam entrada
- Tratamento de erros adequado

## Responsabilidades de Cada Classe

### Player
- Gerencia nome e pontuação do jogador
- Validação de dados de entrada
- Operações de pontuação

### Ball
- Física e movimento da bola
- Cálculos de colisão e rebote
- Controle de velocidade e ângulo

### Paddle
- Movimento das raquetes
- Limites de tela
- Geometria para colisão

### ScoreManager
- Persistência de dados
- Ranking ordenado
- Interface de consulta

### Game
- Coordenação geral do jogo
- Loop principal
- Gerenciamento de eventos

### Menu
- Interface de usuário
- Navegação entre telas
- Entrada de dados

## Padrões de Design Utilizados

1. **Encapsulamento**: Dados privados com interface pública
2. **Separação de Responsabilidades**: Cada classe tem uma função específica
3. **Callback Pattern**: Menu chama jogo através de callback
4. **Property Pattern**: Acesso controlado a atributos
5. **Singleton Pattern**: ScoreManager gerencia estado global
