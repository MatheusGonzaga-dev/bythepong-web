/**
 * ByThePong - Engine principal do jogo JavaScript
 * Mantém POO e encapsulamento equivalente à versão Python
 */

class GameEngine {
    /**
     * Construtor do GameEngine
     * @param {string} canvasId - ID do elemento canvas
     */
    constructor(canvasId) {
        // Elementos DOM
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // Estado do jogo
        this.gameRunning = false;
        this.gamePaused = false;
        this.gameId = null;
        this.socket = null;
        
        // Objetos do jogo (usando classes JavaScript)
        this.player = null;
        this.bot = null;
        this.ball = null;
        this.leftPaddle = null;
        this.rightPaddle = null;
        
        // Configurações
        this.width = 800;
        this.height = 600;
        this.fps = 60;
        this.difficulty = 'normal';
        this.difficultySettings = {};
        
        // Controles
        this.keys = {};
        this.lastDirection = 0; // Para efeitos de movimento
        
        // Timers
        this.gameStartTime = 0;
        this.gameDuration = 120; // 2 minutos
        this.animationFrame = null;
        this.countdownActive = false;
        
        // UI cache e throttling
        this.ui = {
            cached: false,
            els: {},
            lastUiUpdateMs: 0,
            lastTimerUpdateMs: 0
        };
        
        // Cores e estilos
        this.colors = {
            background: '#0f0f23',
            paddle: '#ffffff',
            ball: '#ff6b6b',
            player: '#2ed573',
            bot: '#ff4757',
            text: '#ffffff',
            accent: '#00a8ff'
        };
        
        this.init();
    }
    
    /**
     * Inicializa o engine do jogo
     */
    init() {
        this.setupCanvas();
        this.setupEventListeners();
        this.setupSocket();
        this.loadGameSession();
        this.cacheUiElements();
    }
    
    /**
     * Configura o canvas e suas dimensões
     */
    setupCanvas() {
        // Ajusta canvas para responsividade
        const container = this.canvas.parentElement;
        const containerRect = container.getBoundingClientRect();
        
        // Mantém proporção 16:9 para ocupar melhor as laterais
        const aspectRatio = 16 / 9;
        // Permite até 1920px de largura
        // Usa quase toda a largura disponível (mantendo margens do layout)
        let canvasWidth = Math.min(containerRect.width - 20, 1920);
        let canvasHeight = canvasWidth / aspectRatio;
        
        if (canvasHeight > containerRect.height - 100) {
            canvasHeight = containerRect.height - 100;
            canvasWidth = canvasHeight * aspectRatio;
        }
        
        this.canvas.width = canvasWidth;
        this.canvas.height = canvasHeight;
        this.width = canvasWidth;
        this.height = canvasHeight;
        
        // Configura contexto
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
    }
    
    /**
     * Configura event listeners
     */
    setupEventListeners() {
        // Eventos de teclado
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
        document.addEventListener('keyup', (e) => this.handleKeyUp(e));
        
        // Eventos de botões
        const startBtn = document.getElementById('start-game-btn');
        const pauseBtn = document.getElementById('pause-game-btn');
        const restartBtn = document.getElementById('restart-game-btn');
        const overlayStartBtn = document.getElementById('overlay-start-btn');
        const fullscreenBtn = document.getElementById('fullscreen-btn');
        const settingsBtn = document.getElementById('game-settings-btn');
        
        if (startBtn) startBtn.addEventListener('click', () => this.startGame());
        if (pauseBtn) pauseBtn.addEventListener('click', () => this.pauseGame());
        if (restartBtn) restartBtn.addEventListener('click', () => this.restartGame());
        if (overlayStartBtn) overlayStartBtn.addEventListener('click', () => this.startGame());
        if (fullscreenBtn) fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        if (settingsBtn) settingsBtn.addEventListener('click', () => this.toggleSettings());
        
        // Eventos do modal de fim de jogo
        const playAgainBtn = document.getElementById('play-again-btn');
        const backToMenuBtn = document.getElementById('back-to-menu-btn');
        const viewRankingBtn = document.getElementById('view-ranking-btn');
        
        if (playAgainBtn) playAgainBtn.addEventListener('click', () => this.playAgain());
        if (backToMenuBtn) backToMenuBtn.addEventListener('click', () => this.backToMenu());
        if (viewRankingBtn) viewRankingBtn.addEventListener('click', () => this.viewRanking());
        
        // Redimensionamento da janela
        window.addEventListener('resize', EventUtils.debounce(() => {
            this.setupCanvas();
            this.repositionObjects();
        }, 250));
        
        // Foco na janela (para pausar/despausar)
        window.addEventListener('blur', () => {
            if (this.gameRunning && !this.gamePaused) {
                this.pauseGame();
            }
        });

        // Qualquer interação do usuário libera o áudio (exigência do navegador)
        const unlockAudio = () => {
            try { AUDIO.enable(); } catch (_) {}
            document.removeEventListener('click', unlockAudio, { capture: true });
            document.removeEventListener('keydown', unlockAudio, { capture: true });
        };
        document.addEventListener('click', unlockAudio, { capture: true, once: true });
        document.addEventListener('keydown', unlockAudio, { capture: true, once: true });
    }

    toggleFullscreen() {
        const elem = this.canvas.parentElement;
        if (!document.fullscreenElement) {
            elem.requestFullscreen?.();
        } else {
            document.exitFullscreen?.();
        }
    }

    toggleSettings() {
        const settingsPanel = document.getElementById('settings-panel');
        if (settingsPanel) {
            settingsPanel.classList.toggle('show');
        }
    }

    cacheUiElements() {
        if (this.ui.cached) return;
        this.ui.els = {
            playerScoreEl: document.getElementById('player-score'),
            botScoreEl: document.getElementById('bot-score'),
            playerNameEl: document.getElementById('player-name'),
            difficultyBadge: document.getElementById('difficulty-badge'),
            timerEl: document.getElementById('game-timer'),
            startBtn: document.getElementById('start-game-btn'),
            pauseBtn: document.getElementById('pause-game-btn')
        };
        this.ui.cached = true;
    }
    
    /**
     * Configura conexão WebSocket
     */
    setupSocket() {
        // Garante que o cliente Socket.IO está disponível
        if (typeof io === 'undefined') {
            console.warn('Socket.IO client não encontrado. Continuando sem tempo real.');
            this.updateConnectionStatus('disconnected');
            this.socket = null;
            return;
        }

        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Conectado ao servidor');
            this.updateConnectionStatus('connected');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Desconectado do servidor');
            this.updateConnectionStatus('disconnected');
        });
        
        this.socket.on('game_update', (data) => {
            this.updateGameState(data);
        });
        
        this.socket.on('game_joined', (data) => {
            console.log('Entrou no jogo:', data.game_id);
        });
    }
    
    /**
     * Carrega sessão de jogo do servidor
     */
    async loadGameSession() {
        try {
            // Mostra loading
            this.showLoadingModal();
            
            // Sempre cria nova sessão ao chegar na página do jogo
            let gameId = null;

                // Cria nova sessão
                const playerName = StorageUtils.get('lastPlayerName', 'Jogador');
                const difficulty = StorageUtils.get('preferredDifficulty', 'normal');
                
                const response = await ApiUtils.post('/api/create_game', {
                    player_name: playerName,
                    difficulty: difficulty
                });
                
                if (response.success) {
                    gameId = response.game_id;
                } else {
                    throw new Error('Erro ao criar sessão de jogo');
                }
            
            // Carrega estado do jogo
            await this.loadGameState(gameId);
            
            // Entra na sala do jogo
            this.socket.emit('join_game', { game_id: gameId });
            
            this.hideLoadingModal();
            this.showGameOverlay('Pronto para Jogar?', 'Pressione INICIAR ou ESPAÇO para começar');
            
        } catch (error) {
            console.error('Erro ao carregar jogo:', error);
            this.hideLoadingModal();
            showNotification('Erro ao conectar com o servidor', 'error');
        }
    }
    
    /**
     * Carrega estado do jogo do servidor
     */
    async loadGameState(gameId) {
        try {
            const gameState = await ApiUtils.get(`/api/game_state/${gameId}`);
            this.updateGameFromServer(gameState);
            this.gameId = gameId;
        } catch (error) {
            console.error('Erro ao carregar estado do jogo:', error);
            throw error;
        }
    }
    
    /**
     * Atualiza objetos do jogo com dados do servidor
     */
    updateGameFromServer(gameState) {
        this.difficulty = gameState.difficulty;
        this.difficultySettings = this.getDifficultySettings(this.difficulty);
        
        // Cria objetos do jogo
        this.player = new Player(gameState.player.name);
        this.player._score = gameState.player.score;
        
        this.bot = new Player(gameState.bot.name);
        this.bot._score = gameState.bot.score;
        
        this.ball = Ball.fromJSON(gameState.ball);
        this.leftPaddle = Paddle.fromJSON(gameState.left_paddle);
        this.rightPaddle = Paddle.fromJSON(gameState.right_paddle);
        
        // Atualiza UI
        this.updateUI();
        
        // Ajusta dimensões se necessário
        if (gameState.width && gameState.height) {
            this.repositionObjects();
        }
    }
    
    /**
     * Reposiciona objetos após redimensionamento
     */
    repositionObjects() {
        if (!this.ball || !this.leftPaddle || !this.rightPaddle) return;
        
        // Reposiciona paddles proporcionalmente
        const leftPaddleY = (this.leftPaddle.y / 600) * this.height;
        const rightPaddleY = (this.rightPaddle.y / 600) * this.height;
        
        this.leftPaddle.setPosition(50, leftPaddleY);
        this.rightPaddle.setPosition(this.width - 65, rightPaddleY);
        
        // Reposiciona bola proporcionalmente
        const ballX = (this.ball.x / 800) * this.width;
        const ballY = (this.ball.y / 600) * this.height;
        
        this.ball.x = ballX;
        this.ball.y = ballY;
    }
    
    /**
     * Configurações de dificuldade
     */
    getDifficultySettings(difficulty) {
        const settings = {
            'fácil': {
                aiDifficulty: 0.3,
                ballSpeed: 3,
                aiSpeed: 4,
                description: 'Perfeito para iniciantes'
            },
            'normal': {
                aiDifficulty: 0.6,
                ballSpeed: 5,
                aiSpeed: 6,
                description: 'Equilibrado e divertido'
            },
            'difícil': {
                aiDifficulty: 0.8,
                ballSpeed: 7,
                aiSpeed: 8,
                description: 'Para jogadores experientes'
            },
            'expert': {
                aiDifficulty: 0.95,
                ballSpeed: 9,
                aiSpeed: 10,
                description: 'Apenas para os melhores!'
            }
        };
        
        return settings[difficulty] || settings['normal'];
    }
    
    /**
     * Manipula teclas pressionadas
     */
    handleKeyDown(event) {
        this.keys[event.code] = true;
        
        // Atalhos específicos
        switch (event.code) {
            case 'Space':
                event.preventDefault();
                if (!this.gameRunning) {
                    this.startGame();
                } else {
                    this.pauseGame();
                }
                break;
            case 'ArrowUp':
            case 'ArrowDown':
                // Evita scroll da página em algumas plataformas
                event.preventDefault();
                break;
                
            case 'Escape':
                event.preventDefault();
                if (this.gameRunning) {
                    this.pauseGame();
                } else {
                    this.backToMenu();
                }
                break;
                
            case 'KeyR':
                if (event.ctrlKey) {
                    event.preventDefault();
                    this.restartGame();
                }
                break;
        }
    }
    
    /**
     * Manipula teclas soltas
     */
    handleKeyUp(event) {
        this.keys[event.code] = false;
    }
    
    /**
     * Processa entrada do usuário
     */
    handleInput() {
        if (!this.gameRunning || this.gamePaused || !this.leftPaddle) return;
        
        // Movimento simples e direto
        const upPressed = this.keys['KeyW'] || this.keys['ArrowUp'];
        const downPressed = this.keys['KeyS'] || this.keys['ArrowDown'];
        
        if (upPressed && !downPressed) {
            this.leftPaddle.moveUp(this.height);
            this.lastDirection = -1;
        } else if (downPressed && !upPressed) {
            this.leftPaddle.moveDown(this.height);
            this.lastDirection = 1;
        } else {
            this.lastDirection = 0;
        }
    }
    
    /**
     * Inicia o jogo
     */
    async startGame() {
        if (!this.gameId) return;
        
        try {
            await ApiUtils.post(`/api/start_game/${this.gameId}`);
            
            this.gameRunning = true;
            this.gamePaused = false;
            this.gameStartTime = Date.now();

            // Centraliza a bola e inicia contagem regressiva
            if (this.ball) {
                this.ball.reset(this.width / 2, this.height / 2);
            }

            this.countdownActive = true;
            await this.runCountdown(3); // 3,2,1
            this.countdownActive = false;

            this.hideGameOverlay();
            this.updateButtons();
            this.startGameLoop();
            
            showNotification('Jogo iniciado! Use W/S ou ↑/↓ para mover', 'success', 3000);
            
        } catch (error) {
            console.error('Erro ao iniciar jogo:', error);
            showNotification('Erro ao iniciar jogo', 'error');
        }
    }

    /**
     * Executa contagem regressiva 3-2-1 antes do início
     */
    async runCountdown(seconds = 3) {
        const overlay = document.getElementById('game-overlay');
        const titleEl = document.getElementById('overlay-title');
        const messageEl = document.getElementById('overlay-message');

        if (overlay && titleEl) {
            overlay.classList.remove('hidden');
            messageEl.textContent = '';
            for (let s = seconds; s > 0; s -= 1) {
                titleEl.textContent = String(s);
                if (window.AUDIO) window.AUDIO.sfxCountdownTick();
                await new Promise(res => setTimeout(res, 900));
            }
            titleEl.textContent = 'Go!';
            if (window.AUDIO) window.AUDIO.sfxCountdownGo();
            await new Promise(res => setTimeout(res, 500));
        }
    }
    
    /**
     * Pausa/despausa o jogo
     */
    pauseGame() {
        if (!this.gameRunning) return;
        
        this.gamePaused = !this.gamePaused;
        
        if (this.gamePaused) {
            this.showGameOverlay('Jogo Pausado', 'Pressione ESPAÇO para continuar');
            showNotification('Jogo pausado', 'warning');
        } else {
            this.hideGameOverlay();
            showNotification('Jogo retomado', 'success');
        }
        
        this.updateButtons();
    }
    
    /**
     * Reinicia o jogo
     */
    async restartGame() {
        this.stopGame();
        
        try {
            // Remove sessão atual
            StorageUtils.remove('currentGameId');
            
            // Recarrega página para nova sessão
            window.location.reload();
            
        } catch (error) {
            console.error('Erro ao reiniciar jogo:', error);
            showNotification('Erro ao reiniciar jogo', 'error');
        }
    }
    
    /**
     * Para o jogo
     */
    stopGame() {
        this.gameRunning = false;
        this.gamePaused = false;
        
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }
        
        this.updateButtons();
    }
    
    /**
     * Loop principal do jogo
     */
    startGameLoop() {
        const gameLoop = () => {
            if (!this.gameRunning) return;
            
            if (!this.gamePaused) {
                this.handleInput();
                this.updateGame();
                this.checkCollisions();
                this.updateAI();
            }
            
            this.render();
            this.animationFrame = requestAnimationFrame(gameLoop);
        };
        
        gameLoop();
    }
    
    /**
     * Atualiza lógica do jogo
     */
    updateGame() {
        if (!this.ball) return;
        // Durante a contagem regressiva, não mover a bola
        if (this.countdownActive) return;
        
        // Move a bola
        this.ball.move();
        
        // Atualiza timer
        this.updateTimer();
    }
    
    /**
     * Verifica colisões
     */
    checkCollisions() {
        if (!this.ball || !this.leftPaddle || !this.rightPaddle) return;
        
        const ballRect = this.ball.getRect();
        
        // Colisão com paredes superior e inferior
        if (ballRect.centerY <= this.ball.radius) {
            this.ball.bounceY();
            this.ball.y = this.ball.radius + 1;
        }
        
        if (ballRect.centerY >= this.height - this.ball.radius) {
            this.ball.bounceY();
            this.ball.y = this.height - this.ball.radius - 1;
        }
        
        // Colisão com paddles
        const leftPaddleRect = this.leftPaddle.getRect();
        const rightPaddleRect = this.rightPaddle.getRect();
        
        // Paddle esquerdo
        if (this.ball.collidesWithRect(leftPaddleRect) && this.ball.dx < 0) {
            this.ball.bouncePaddle(leftPaddleRect.y, leftPaddleRect.height);
            this.ball.x = leftPaddleRect.right + this.ball.radius + 2;
            this.playPaddleHitEffect();
        }
        
        // Paddle direito
        if (this.ball.collidesWithRect(rightPaddleRect) && this.ball.dx > 0) {
            this.ball.bouncePaddle(rightPaddleRect.y, rightPaddleRect.height);
            this.ball.x = rightPaddleRect.left - this.ball.radius - 2;
            this.playPaddleHitEffect();
        }
        
        // Pontuação
        if (ballRect.centerX < 0) {
            this.bot.addPoint();
            this.resetBall();
            this.showScoreEffect('Bot pontuou!', this.colors.bot);
            if (window.AUDIO) window.AUDIO.sfxScore();
        }
        
        if (ballRect.centerX > this.width) {
            this.player.addPoint();
            this.resetBall();
            this.showScoreEffect('Você pontuou!', this.colors.player);
            if (window.AUDIO) window.AUDIO.sfxScore();
        }
        
        // Verifica fim de jogo
        this.checkGameEnd();
    }
    
    /**
     * Atualiza IA do paddle direito
     */
    updateAI() {
        if (!this.rightPaddle || !this.ball) return;
        
        // IA simples que segue a bola
        const targetY = this.ball.y;
        this.rightPaddle.moveTowardsTarget(
            targetY, 
            this.height, 
            this.difficultySettings.aiDifficulty
        );
    }
    
    /**
     * Reseta a bola para o centro
     */
    resetBall() {
        if (!this.ball) return;
        
        this.ball.reset(this.width / 2, this.height / 2);
        this.updateUI();
    }
    
    /**
     * Verifica condições de fim de jogo
     */
    checkGameEnd() {
        const maxScore = 3;
        const timeUp = this.getRemainingTime() <= 0;
        
        if (this.player.score >= maxScore || this.bot.score >= maxScore || timeUp) {
            this.endGame();
        }
    }
    
    /**
     * Finaliza o jogo
     */
    endGame() {
        this.stopGame();
        
        let winner = 'Empate';
        let isVictory = false;
        
        if (this.player.score > this.bot.score) {
            winner = 'Vitória';
            isVictory = true;
        } else if (this.bot.score > this.player.score) {
            winner = 'Derrota';
            isVictory = false;
        }
        
        this.showGameOverModal(winner, isVictory);
    }
    
    /**
     * Renderiza o jogo
     */
    render() {
        // Limpa canvas
        this.ctx.fillStyle = this.colors.background;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Desenha linha central
        this.drawCenterLine();
        
        // Desenha objetos
        if (this.leftPaddle) {
            this.leftPaddle.color = this.colors.player;
            this.leftPaddle.draw(this.ctx, true);
        }
        
        if (this.rightPaddle) {
            this.rightPaddle.color = this.colors.bot;
            this.rightPaddle.draw(this.ctx, true);
        }
        
        if (this.ball) {
            this.ball.draw(this.ctx, this.colors.ball);
        }
        
        // Desenha placar
        this.drawScore();
        
        // Desenha informações de debug (se necessário)
        if (window.DEBUG_MODE) {
            this.drawDebugInfo();
        }
    }
    
    /**
     * Desenha linha central
     */
    drawCenterLine() {
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        this.ctx.lineWidth = 2;
        this.ctx.setLineDash([10, 10]);
        
        this.ctx.beginPath();
        this.ctx.moveTo(this.width / 2, 0);
        this.ctx.lineTo(this.width / 2, this.height);
        this.ctx.stroke();
        
        this.ctx.setLineDash([]);
    }
    
    /**
     * Desenha placar
     */
    drawScore() {
        if (!this.player || !this.bot) return;
        
        const fontSize = Math.max(24, this.width / 20);
        this.ctx.font = `bold ${fontSize}px Orbitron, monospace`;
        
        // Pontuação do jogador
        this.ctx.fillStyle = this.colors.player;
        this.ctx.fillText(
            this.player.score.toString(),
            this.width / 2 - fontSize * 1.5,
            fontSize * 1.5
        );
        
        // Separador
        this.ctx.fillStyle = this.colors.text;
        this.ctx.fillText(
            '×',
            this.width / 2,
            fontSize * 1.5
        );
        
        // Pontuação do bot
        this.ctx.fillStyle = this.colors.bot;
        this.ctx.fillText(
            this.bot.score.toString(),
            this.width / 2 + fontSize * 1.5,
            fontSize * 1.5
        );
    }
    
    /**
     * Atualiza interface do usuário
     */
    updateUI() {
        // Throttle: no máx 10x por segundo
        const now = performance.now();
        if (now - this.ui.lastUiUpdateMs < 100) return;
        this.ui.lastUiUpdateMs = now;
        this.cacheUiElements();
        const { playerScoreEl, botScoreEl, playerNameEl, difficultyBadge } = this.ui.els;
        if (playerScoreEl && this.player) playerScoreEl.textContent = this.player.score;
        if (botScoreEl && this.bot) botScoreEl.textContent = this.bot.score;
        if (playerNameEl && this.player) playerNameEl.textContent = this.player.name;
        if (difficultyBadge) {
            difficultyBadge.textContent = this.difficulty.charAt(0).toUpperCase() + this.difficulty.slice(1);
            difficultyBadge.style.backgroundColor = FormatUtils.getDifficultyColor(this.difficulty);
        }
    }
    
    /**
     * Atualiza timer do jogo
     */
    updateTimer() {
        // Throttle: 4x por segundo
        const now = performance.now();
        if (now - this.ui.lastTimerUpdateMs < 250) return;
        this.ui.lastTimerUpdateMs = now;
        this.cacheUiElements();
        const timerEl = this.ui.els.timerEl;
        if (!timerEl) return;
        const remaining = this.getRemainingTime();
        timerEl.textContent = FormatUtils.formatTime(remaining);
        if (remaining <= 30) {
            timerEl.style.color = this.colors.accent;
            timerEl.style.animation = 'pulse 1s infinite';
        }
    }
    
    /**
     * Obtém tempo restante em segundos
     */
    getRemainingTime() {
        if (!this.gameStartTime) return this.gameDuration;
        
        const elapsed = (Date.now() - this.gameStartTime) / 1000;
        return Math.max(0, this.gameDuration - elapsed);
    }
    
    /**
     * Atualiza botões de controle
     */
    updateButtons() {
        this.cacheUiElements();
        const { startBtn, pauseBtn } = this.ui.els;
        if (startBtn && pauseBtn) {
            if (this.gameRunning) {
                startBtn.style.display = 'none';
                pauseBtn.style.display = 'inline-flex';
                pauseBtn.innerHTML = this.gamePaused ? 
                    '<i class="fas fa-play"></i> Continuar' : 
                    '<i class="fas fa-pause"></i> Pausar';
            } else {
                startBtn.style.display = 'inline-flex';
                pauseBtn.style.display = 'none';
            }
        }
    }
    
    /**
     * Mostra modal de loading
     */
    showLoadingModal() {
        const modal = document.getElementById('loading-game-modal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }
    
    /**
     * Esconde modal de loading
     */
    hideLoadingModal() {
        const modal = document.getElementById('loading-game-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }
    
    /**
     * Mostra overlay do jogo
     */
    showGameOverlay(title, message) {
        const overlay = document.getElementById('game-overlay');
        const titleEl = document.getElementById('overlay-title');
        const messageEl = document.getElementById('overlay-message');
        
        if (overlay) {
            if (titleEl) titleEl.textContent = title;
            if (messageEl) messageEl.textContent = message;
            overlay.classList.remove('hidden');
        }
    }
    
    /**
     * Esconde overlay do jogo
     */
    hideGameOverlay() {
        const overlay = document.getElementById('game-overlay');
        if (overlay) {
            overlay.classList.add('hidden');
        }
    }
    
    /**
     * Mostra modal de fim de jogo
     */
    showGameOverModal(result, isVictory) {
        const modal = document.getElementById('game-over-modal');
        const title = document.getElementById('game-over-title');
        const resultMessage = document.getElementById('result-message');
        const finalPlayerScore = document.getElementById('final-player-score');
        const finalBotScore = document.getElementById('final-bot-score');
        
        if (modal) {
            modal.style.display = 'flex';
            
            if (title) {
                title.textContent = result;
                title.className = `game-over-header ${isVictory ? 'victory' : 'defeat'}`;
            }
            
            if (resultMessage) {
                let message = '';
                if (isVictory) {
                    message = `Parabéns ${this.player.name}! Você venceu!`;
                } else if (result === 'Empate') {
                    message = 'Jogo empatado! Que partida emocionante!';
                } else {
                    message = `Que pena ${this.player.name}! O Bot venceu!`;
                }
                
                resultMessage.textContent = message;
                resultMessage.className = `result-message ${isVictory ? 'victory' : result === 'Empate' ? 'draw' : 'defeat'}`;
            }
            
            if (finalPlayerScore) finalPlayerScore.textContent = this.player.score;
            if (finalBotScore) finalBotScore.textContent = this.bot.score;
        }
    }
    
    /**
     * Mostra efeito de pontuação
     */
    showScoreEffect(text, color) {
        showNotification(text, 'success', 2000);
        
        // Efeito visual adicional no canvas
        // (implementar animação de pontuação se desejado)
    }
    
    /**
     * Efeito sonoro/visual de rebote
     */
    playPaddleHitEffect() {
        // Efeito sonoro discreto
        if (window.AUDIO) window.AUDIO.sfxHit();
    }
    
    /**
     * Atualiza status de conexão
     */
    updateConnectionStatus(status) {
        const statusEl = document.getElementById('connection-status');
        const iconEl = document.getElementById('connection-icon');
        const textEl = document.getElementById('connection-text');
        
        if (statusEl && iconEl && textEl) {
            statusEl.className = `connection-status ${status}`;
            iconEl.className = `fas fa-wifi ${status}`;
            
            const statusTexts = {
                connected: 'Conectado',
                disconnected: 'Desconectado',
                reconnecting: 'Reconectando...'
            };
            
            textEl.textContent = statusTexts[status] || 'Desconhecido';
        }
    }
    
    /**
     * Joga novamente
     */
    playAgain() {
        document.getElementById('game-over-modal').style.display = 'none';
        this.restartGame();
    }
    
    /**
     * Volta ao menu principal
     */
    backToMenu() {
        StorageUtils.remove('currentGameId');
        window.location.href = '/';
    }
    
    /**
     * Visualiza ranking
     */
    viewRanking() {
        showRanking(); // Função global definida em base.html
    }
    
    /**
     * Atualiza estado do jogo via WebSocket
     */
    updateGameState(gameState) {
        // Atualiza objetos locais com dados do servidor
        if (gameState && this.ball && this.leftPaddle && this.rightPaddle) {
            // Sincroniza posições (suavizado para evitar jitter)
            this.ball.x = gameState.ball.x;
            this.ball.y = gameState.ball.y;
            
            this.rightPaddle.y = gameState.right_paddle.y;
            
            // Atualiza pontuação
            if (this.player) this.player._score = gameState.player.score;
            if (this.bot) this.bot._score = gameState.bot.score;
            
            this.updateUI();
        }
    }
    
    /**
     * Desenha informações de debug
     */
    drawDebugInfo() {
        const fontSize = 12;
        this.ctx.font = `${fontSize}px monospace`;
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        
        const debugInfo = [
            `FPS: ${this.fps}`,
            `Ball: (${Math.round(this.ball?.x || 0)}, ${Math.round(this.ball?.y || 0)})`,
            `Speed: ${Math.round(this.ball?.speed || 0)}`,
            `Difficulty: ${this.difficulty}`,
            `Running: ${this.gameRunning}`,
            `Paused: ${this.gamePaused}`
        ];
        
        debugInfo.forEach((info, index) => {
            this.ctx.fillText(info, 10, 20 + index * 15);
        });
    }
}

// Inicializa o jogo quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Cria instância global do jogo
    window.game = new GameEngine('game-canvas');
    
    // Debug mode (ativar via console: window.DEBUG_MODE = true)
    window.DEBUG_MODE = false;
    
    console.log('ByThePong Web Game carregado!');
});
