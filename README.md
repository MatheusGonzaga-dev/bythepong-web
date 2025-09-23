# ByThePong - Versão Web com Django

## 🎮 Sobre o Projeto

ByThePong é uma versão web do clássico jogo Pong, desenvolvido com **Programação Orientada a Objetos** usando Django. O projeto demonstra conceitos de encapsulamento, herança e polimorfismo através de classes bem estruturadas.

## 🏗️ Arquitetura POO

### Classes Principais

#### `Ball` (game_logic.py)
- **Encapsulamento**: Atributos privados com `__`
- **Propriedades**: Getters para acesso controlado
- **Métodos**: `move()`, `bounce_wall()`, `bounce_paddle()`, `reset()`

#### `Paddle` (game_logic.py)
- **Encapsulamento**: Posição e dimensões privadas
- **Métodos**: `move_up()`, `move_down()`, `set_position()`

#### `Game` (game_logic.py)
- **Encapsulamento**: Estado do jogo privado
- **Lógica de negócio**: Colisões, pontuação, fim de jogo
- **Configuração**: Dificuldades dinâmicas

#### `Player` (models.py)
- **Modelo Django**: Persistência no banco
- **Métodos**: `add_game_result()`, propriedade `win_rate`

#### `GameSession` (models.py)
- **Modelo Django**: Histórico de partidas
- **Relacionamentos**: ForeignKey com Player

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Django 4.2+

### Instalação
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

### Acessar o Jogo
- **URL**: http://127.0.0.1:8000/
- **Menu**: Configuração de nome e dificuldade
- **Jogo**: Canvas HTML5 com controles por teclado
- **Ranking**: Sistema de pontuação persistente

## 🎯 Funcionalidades

### Sistema de Jogo
- ✅ **4 Níveis de Dificuldade**: Fácil, Normal, Difícil, Expert
- ✅ **IA Inteligente**: Bot com comportamento adaptativo
- ✅ **Controles**: W/S ou ↑/↓ para mover raquete
- ✅ **Tempo Limite**: Partidas de 2 minutos
- ✅ **Condições de Vitória**: Primeiro a 3 pontos ou maior pontuação no tempo

### Sistema de Ranking
- ✅ **Persistência**: Banco de dados SQLite
- ✅ **Estatísticas**: Melhor pontuação, taxa de vitórias
- ✅ **Histórico**: Partidas recentes com detalhes
- ✅ **Classificação**: Ranking por melhor pontuação

### Interface Web
- ✅ **Design Responsivo**: Funciona em desktop e mobile
- ✅ **Templates Django**: Separação de lógica e apresentação
- ✅ **API REST**: Endpoints para comunicação em tempo real
- ✅ **Estilização CSS**: Interface moderna e intuitiva

## 🔧 Estrutura do Projeto

```
bythepong/
├── bythepong_web/          # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── game/                   # App principal
│   ├── models.py          # Modelos de dados
│   ├── views.py           # Views e API
│   ├── urls.py            # URLs do app
│   └── game_logic.py      # Classes POO do jogo
├── templates/             # Templates HTML
│   └── game/
│       ├── index.html     # Menu principal
│       ├── game.html      # Página do jogo
│       └── ranking.html   # Ranking
└── requirements.txt       # Dependências
```

## 🎓 Conceitos POO Demonstrados

### Encapsulamento
- Atributos privados com `__` (ex: `self.__x`, `self.__y`)
- Propriedades públicas para acesso controlado
- Métodos privados para lógica interna

### Abstração
- Classes com responsabilidades bem definidas
- Interfaces claras entre componentes
- Separação de lógica de negócio e apresentação

### Herança
- Modelos Django herdam de `models.Model`
- Reutilização de funcionalidades base

### Polimorfismo
- Métodos com comportamentos diferentes por contexto
- Tratamento uniforme de objetos diferentes

## 🏆 Sistema de Pontuação

### Critérios de Vitória
1. **Primeiro a 3 pontos** (vitória imediata)
2. **Maior pontuação em 2 minutos** (vitória por tempo)
3. **Empate** (mesma pontuação no tempo limite)

### Ranking
- Ordenado por **melhor pontuação**
- Desempate por **taxa de vitórias**
- Histórico completo de partidas

## 🎮 Controles

- **W** ou **↑**: Mover raquete para cima
- **S** ou **↓**: Mover raquete para baixo
- **ESPAÇO**: Iniciar/pausar jogo
- **Navegação**: Links no header para menu e ranking

## 📱 Responsividade

O jogo é totalmente responsivo e funciona em:
- 🖥️ **Desktop**: Experiência completa
- 📱 **Mobile**: Interface adaptada
- 📟 **Tablet**: Controles otimizados

## 🔮 Tecnologias Utilizadas

- **Backend**: Django 4.2+ (Python)
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Banco**: SQLite (desenvolvimento)
- **Canvas**: HTML5 Canvas para renderização
- **API**: REST com JSON

## 📝 Licença

Projeto acadêmico desenvolvido para demonstração de conceitos de POO.

---

**Desenvolvido com ❤️ usando Django e Programação Orientada a Objetos**