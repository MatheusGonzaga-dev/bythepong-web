# ByThePong 🏓

Um jogo Pong moderno desenvolvido em Python usando Programação Orientada a Objetos com encapsulamento.

## 🎮 Características

- **Interface intuitiva e bonita** com menu interativo
- **Sistema de pontuação** com contador em tempo real
- **Ranking persistente** que salva as melhores pontuações
- **IA inteligente** para o oponente
- **Encapsulamento completo** seguindo princípios de POO
- **Física realista** da bola com rebotes dinâmicos

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- pygame

### Instalação
1. Clone ou baixe este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar o jogo
```bash
python main.py
```

## 🎯 Como Jogar

1. **Menu Principal**: Escolha entre Jogar, Ver Ranking ou Sair
2. **Nome do Jogador**: Digite seu nome para personalizar a experiência
3. **Controles**:
   - **W** ou **↑**: Mover raquete para cima
   - **S** ou **↓**: Mover raquete para baixo
   - **ESPAÇO**: Iniciar/pausar o jogo
   - **ESC**: Voltar ao menu ou sair

## 🏗️ Arquitetura do Projeto

O projeto foi desenvolvido seguindo princípios de Programação Orientada a Objetos com encapsulamento:

### Classes Principais

- **`Player`**: Gerencia informações do jogador (nome, pontuação)
- **`Ball`**: Controla a física e movimento da bola
- **`Paddle`**: Representa as raquetes com movimento e colisão
- **`Game`**: Classe principal que coordena toda a lógica do jogo
- **`Menu`**: Interface de menu e entrada de dados
- **`ScoreManager`**: Gerencia pontuação e ranking persistente

### Encapsulamento

Todas as classes implementam encapsulamento adequado:
- Atributos privados (prefixo `__`)
- Propriedades públicas com getters/setters
- Métodos públicos para interação
- Validação de dados nos setters

## 📁 Estrutura de Arquivos

```
bythepong/
├── main.py              # Arquivo principal
├── game.py              # Classe principal do jogo
├── menu.py              # Interface de menu
├── player.py            # Classe do jogador
├── ball.py              # Classe da bola
├── paddle.py            # Classe das raquetes
├── score_manager.py     # Gerenciador de pontuação
├── requirements.txt     # Dependências
├── README.md           # Documentação
└── ranking.json        # Arquivo de ranking (criado automaticamente)
```

## 🎨 Recursos Visuais

- **Cores modernas** e interface limpa
- **Animações suaves** de movimento
- **Feedback visual** para interações
- **Medalhas** no ranking (🥇🥈🥉)
- **Cursor piscante** no campo de entrada

## 🏆 Sistema de Ranking

- Salva automaticamente as 10 melhores pontuações
- Persistência em arquivo JSON
- Exibição com medalhas e posições
- Busca por melhor pontuação individual

## 🔧 Personalização

Você pode facilmente modificar:
- **Dificuldade da IA**: Ajuste `__ai_difficulty` na classe `Game`
- **Velocidade do jogo**: Modifique `__fps` na classe `Game`
- **Cores**: Altere as constantes de cor em cada classe
- **Dimensões**: Ajuste `width` e `height` no construtor

## 🐛 Solução de Problemas

### Erro de pygame não encontrado
```bash
pip install pygame
```

### Problemas de performance
- Reduza o FPS na classe `Game`
- Verifique se há outros programas pesados rodando

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como trabalho de faculdade sobre Programação Orientada a Objetos.

## 👨‍💻 Desenvolvido por

Projeto desenvolvido para demonstrar conceitos de POO com encapsulamento em Python.

---

**Divirta-se jogando ByThePong! 🏓**
