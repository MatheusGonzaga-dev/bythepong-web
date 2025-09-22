# ByThePong Web 🏓

Uma versão web completa do jogo ByThePong, mantendo todos os conceitos de Programação Orientada a Objetos e encapsulamento da versão desktop.

## 🌟 Características da Versão Web

### Backend (Python + Flask)
- **API REST** completa para gerenciamento de jogos
- **WebSocket** para comunicação em tempo real
- **Sessões de jogo** persistentes
- **Todas as classes Python** originais mantidas com encapsulamento
- **Sistema de ranking** web-based

### Frontend (HTML5 + JavaScript)
- **Canvas HTML5** para renderização do jogo
- **Classes JavaScript** equivalentes às Python (POO completa)
- **Interface responsiva** que se adapta a qualquer dispositivo
- **Design moderno** com animações e efeitos visuais
- **Controles intuitivos** (teclado e touch)

### Tecnologias Utilizadas
- **Backend**: Flask, Flask-SocketIO, Python 3.7+
- **Frontend**: HTML5 Canvas, JavaScript ES6+, CSS3, WebSocket
- **UI**: Font Awesome, Google Fonts, CSS Grid/Flexbox
- **Comunicação**: REST API + WebSocket para tempo real

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Instalação e Execução

1. **Clone o repositório** (se ainda não tiver):
```bash
git clone <seu-repositorio>
cd bythepong
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Execute o servidor web**:
```bash
python app.py
```

4. **Acesse no navegador**:
```
http://localhost:5000
```

### Execução em Produção

Para executar em produção, você pode usar Gunicorn:

```bash
pip install gunicorn
gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:5000
```

## 🎮 Como Jogar na Web

### Menu Principal
1. **Digite seu nome** no campo de entrada
2. **Escolha a dificuldade** (Fácil, Normal, Difícil, Expert)
3. **Clique em "Iniciar Jogo"** ou pressione Enter

### Durante o Jogo
- **W** ou **↑**: Mover raquete para cima
- **S** ou **↓**: Mover raquete para baixo
- **Espaço**: Pausar/Continuar
- **ESC**: Voltar ao menu
- **F11**: Tela cheia (funciona na versão desktop)

### Recursos Web Exclusivos
- **Responsividade**: Joga em desktop, tablet ou celular
- **Tempo real**: Sincronização via WebSocket
- **Notificações**: Feedback visual para ações
- **Ranking online**: Pontuações salvas no servidor
- **Reconexão automática**: Se perder conexão, reconecta automaticamente

## 🏗️ Arquitetura Web

### Backend - Estrutura de Classes

```
app.py (Flask Application)
├── WebGameManager
│   ├── create_game_session()
│   ├── get_game_state()
│   ├── update_paddle_position()
│   └── manage_sessions()
│
├── Player (classe original mantida)
├── Ball (classe original mantida)
├── Paddle (classe original mantida)
└── ScoreManager (classe original mantida)
```

### Frontend - Estrutura de Classes JavaScript

```
static/js/
├── game.js (GameEngine)
│   ├── GameEngine.init()
│   ├── GameEngine.startGameLoop()
│   ├── GameEngine.handleInput()
│   └── GameEngine.render()
│
├── player.js (classe Player em JS)
├── ball.js (classe Ball em JS)
├── paddle.js (classe Paddle em JS)
└── utils.js (utilitários)
```

### API Endpoints

#### REST API
- `GET /` - Página principal
- `GET /game` - Página do jogo
- `POST /api/create_game` - Criar nova sessão
- `GET /api/game_state/<id>` - Estado do jogo
- `POST /api/start_game/<id>` - Iniciar jogo
- `GET /api/ranking` - Obter ranking

#### WebSocket Events
- `connect` - Conectar ao servidor
- `join_game` - Entrar em sessão de jogo
- `paddle_move` - Movimento da raquete
- `game_update` - Atualização do estado

## 📱 Compatibilidade

### Navegadores Suportados
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### Dispositivos
- ✅ **Desktop**: Controles via teclado
- ✅ **Tablet**: Interface touch otimizada
- ✅ **Mobile**: Layout responsivo adaptado

### Recursos Modernos
- ✅ **WebSocket**: Comunicação bidirecional
- ✅ **Canvas API**: Renderização 2D acelerada
- ✅ **CSS Grid/Flexbox**: Layout moderno
- ✅ **ES6+ JavaScript**: Classes, async/await, etc.
- ✅ **LocalStorage**: Persistência local
- ✅ **ResponsiveDesign**: Adaptação automática

## 🔧 Configuração e Customização

### Variáveis de Ambiente
```bash
export FLASK_ENV=development  # Para desenvolvimento
export FLASK_DEBUG=True       # Para debug
```

### Configurações do Jogo
Edite `app.py` para alterar:
- Duração das partidas
- Configurações de dificuldade
- Porta do servidor
- Configurações de WebSocket

### Customização Visual
Edite `static/css/style.css` para alterar:
- Cores e temas
- Animações
- Layout responsivo
- Efeitos visuais

## 🐛 Solução de Problemas

### Problemas Comuns

**Erro: "Port already in use"**
```bash
# Mata processo na porta 5000
sudo kill -9 $(sudo lsof -t -i:5000)
```

**Erro: "Module not found"**
```bash
# Reinstala dependências
pip install -r requirements.txt --force-reinstall
```

**Problemas de WebSocket**
- Verifique se o firewall não está bloqueando
- Confirme se está usando HTTP (não HTTPS) localmente
- Reinicie o servidor

**Canvas não carrega**
- Verifique se o navegador suporta Canvas
- Desative extensões que possam interferir
- Teste em modo incógnito

## 📊 Performance

### Otimizações Implementadas
- **Debounce** em eventos de redimensionamento
- **RequestAnimationFrame** para animações suaves
- **Canvas otimizado** para renderização eficiente
- **WebSocket throttling** para reduzir tráfego
- **CSS transitions** com aceleração por hardware

### Métricas Esperadas
- **FPS**: 60fps constantes
- **Latência WebSocket**: < 50ms
- **Tempo de carregamento**: < 2 segundos
- **Responsividade**: Instantânea

## 🤝 Contribuição

### Estrutura para Novos Recursos
1. **Backend**: Adicione endpoints em `app.py`
2. **Frontend**: Crie componentes em `static/js/`
3. **Estilos**: Adicione CSS em `static/css/`
4. **Templates**: Modifique `templates/`

### Padrões de Código
- **Python**: PEP 8, docstrings completas
- **JavaScript**: ES6+, comentários JSDoc
- **CSS**: BEM methodology, variáveis CSS
- **HTML**: Semântico, acessível

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como demonstração de conceitos de Programação Orientada a Objetos aplicados tanto no backend (Python) quanto no frontend (JavaScript).

---

**🚀 Divirta-se jogando ByThePong na web!** 

Para dúvidas ou sugestões, consulte a documentação ou abra uma issue no repositório.

