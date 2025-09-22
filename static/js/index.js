/**
 * ByThePong - Script da página inicial
 * Gerencia o menu principal e configuração do jogo
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const gameForm = document.getElementById('game-form');
    const playerNameInput = document.getElementById('player-name');
    const difficultyOptions = document.querySelectorAll('input[name="difficulty"]');
    const startButton = document.querySelector('.btn-start');
    
    // Estado da aplicação
    let isSubmitting = false;
    
    // Inicialização
    init();
    
    function init() {
        setupEventListeners();
        loadSavedData();
        validateForm();
        animateHeroElements();
    }
    
    function setupEventListeners() {
        // Formulário de configuração do jogo
        gameForm.addEventListener('submit', handleGameStart);
        
        // Validação em tempo real do nome
        playerNameInput.addEventListener('input', handleNameInput);
        playerNameInput.addEventListener('blur', validatePlayerName);
        
        // Mudança de dificuldade
        difficultyOptions.forEach(option => {
            option.addEventListener('change', handleDifficultyChange);
        });
        
        // Teclas de atalho
        document.addEventListener('keydown', handleKeyboardShortcuts);
        
        // Animações de hover nos cards de característica
        setupFeatureCardAnimations();
    }
    
    function handleGameStart(event) {
        event.preventDefault();
        
        if (isSubmitting) return;
        
        const formData = new FormData(gameForm);
        const playerName = formData.get('player_name');
        const difficulty = formData.get('difficulty');
        
        // Validação final
        if (!validateGameData(playerName, difficulty)) {
            return;
        }
        
        // Inicia o jogo
        startGame(playerName, difficulty);
    }
    
    function handleNameInput(event) {
        const input = event.target;
        const value = input.value;
        
        // Remove caracteres inválidos em tempo real
        const sanitized = value.replace(/[^a-zA-ZÀ-ÿ0-9\s]/g, '');
        
        if (sanitized !== value) {
            input.value = sanitized;
            showInputFeedback(input, 'Apenas letras, números e espaços são permitidos', 'warning');
        } else {
            clearInputFeedback(input);
        }
        
        validateForm();
    }
    
    function handleDifficultyChange(event) {
        const difficulty = event.target.value;
        
        // Salva a escolha
        StorageUtils.set('preferredDifficulty', difficulty);
        
        // Animação visual
        animateDifficultySelection(event.target);
        
        // Atualiza descrição
        updateDifficultyDescription(difficulty);
        
        validateForm();
    }
    
    function handleKeyboardShortcuts(event) {
        // Enter para iniciar jogo (se válido)
        if (event.key === 'Enter' && !event.target.matches('input, textarea, select')) {
            event.preventDefault();
            if (isFormValid()) {
                gameForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape para limpar formulário
        if (event.key === 'Escape') {
            clearForm();
        }
        
        // Números para seleção rápida de dificuldade
        if (event.key >= '1' && event.key <= '4') {
            const index = parseInt(event.key) - 1;
            if (difficultyOptions[index]) {
                difficultyOptions[index].checked = true;
                difficultyOptions[index].dispatchEvent(new Event('change'));
            }
        }
    }
    
    function validateGameData(playerName, difficulty) {
        // Valida nome do jogador
        if (!ValidationUtils.isValidPlayerName(playerName)) {
            showNotification('Por favor, digite um nome válido (1-20 caracteres)', 'error');
            playerNameInput.focus();
            return false;
        }
        
        // Valida dificuldade
        if (!ValidationUtils.isValidDifficulty(difficulty)) {
            showNotification('Por favor, selecione uma dificuldade válida', 'error');
            return false;
        }
        
        return true;
    }
    
    function validatePlayerName() {
        const name = playerNameInput.value.trim();
        
        if (name.length === 0) {
            showInputFeedback(playerNameInput, 'Nome é obrigatório', 'error');
            return false;
        }
        
        if (name.length > 20) {
            showInputFeedback(playerNameInput, 'Nome muito longo (máximo 20 caracteres)', 'error');
            return false;
        }
        
        if (!ValidationUtils.isValidPlayerName(name)) {
            showInputFeedback(playerNameInput, 'Nome contém caracteres inválidos', 'error');
            return false;
        }
        
        showInputFeedback(playerNameInput, 'Nome válido!', 'success');
        return true;
    }
    
    function validateForm() {
        const isValid = isFormValid();
        
        startButton.disabled = !isValid;
        startButton.classList.toggle('disabled', !isValid);
        
        return isValid;
    }
    
    function isFormValid() {
        const name = playerNameInput.value.trim();
        const difficulty = document.querySelector('input[name="difficulty"]:checked');
        
        return ValidationUtils.isValidPlayerName(name) && 
               difficulty && 
               ValidationUtils.isValidDifficulty(difficulty.value);
    }
    
    async function startGame(playerName, difficulty) {
        isSubmitting = true;
        startButton.disabled = true;
        
        // Mostra loading
        showGameStartAnimation();
        
        try {
            // Salva dados localmente
            StorageUtils.set('lastPlayerName', playerName);
            StorageUtils.set('preferredDifficulty', difficulty);
            
            // Cria sessão de jogo no servidor
            const response = await ApiUtils.post('/api/create_game', {
                player_name: playerName,
                difficulty: difficulty
            });
            
            if (response.success) {
                showNotification('Jogo criado com sucesso! Redirecionando...', 'success');
                
                // Redireciona para a página do jogo após animação
                setTimeout(() => {
                    window.location.href = '/game';
                }, 800);
            } else {
                throw new Error(response.error || 'Erro ao criar jogo');
            }
            
        } catch (error) {
            console.error('Erro ao iniciar jogo:', error);
            showNotification('Erro ao conectar com o servidor. Tente novamente.', 'error');
            hideGameStartAnimation();
            isSubmitting = false;
            startButton.disabled = false;
        }
    }
    
    function showGameStartAnimation() {
        startButton.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            Iniciando...
        `;
        startButton.classList.add('loading');
        
        // Adiciona overlay com animação
        const overlay = document.createElement('div');
        overlay.className = 'game-start-overlay';
        overlay.innerHTML = `
            <div class="start-animation">
                <i class="fas fa-table-tennis spinning"></i>
                <h3>Preparando o jogo...</h3>
                <p>Configurando raquetes e bola</p>
            </div>
        `;
        document.body.appendChild(overlay);
        
        // Animação de entrada
        setTimeout(() => overlay.classList.add('show'), 10);
    }
    
    function hideGameStartAnimation() {
        startButton.innerHTML = `
            <i class="fas fa-play"></i>
            Iniciar Jogo
        `;
        startButton.classList.remove('loading');
        
        // Remove overlay
        const overlay = document.querySelector('.game-start-overlay');
        if (overlay) {
            overlay.classList.remove('show');
            setTimeout(() => overlay.remove(), 300);
        }
    }
    
    function loadSavedData() {
        // Carrega último nome usado
        const lastPlayerName = StorageUtils.get('lastPlayerName');
        if (lastPlayerName) {
            playerNameInput.value = lastPlayerName;
        }
        
        // Carrega dificuldade preferida
        const preferredDifficulty = StorageUtils.get('preferredDifficulty', 'normal');
        const difficultyInput = document.querySelector(`input[value="${preferredDifficulty}"]`);
        if (difficultyInput) {
            difficultyInput.checked = true;
            updateDifficultyDescription(preferredDifficulty);
        }
        
        // Valida formulário
        validateForm();
    }
    
    function clearForm() {
        playerNameInput.value = '';
        document.querySelector('input[value="normal"]').checked = true;
        clearInputFeedback(playerNameInput);
        updateDifficultyDescription('normal');
        validateForm();
    }
    
    function showInputFeedback(input, message, type) {
        let feedback = input.parentNode.querySelector('.input-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'input-feedback';
            input.parentNode.appendChild(feedback);
        }
        
        feedback.textContent = message;
        feedback.className = `input-feedback ${type}`;
        feedback.style.display = 'block';
    }
    
    function clearInputFeedback(input) {
        const feedback = input.parentNode.querySelector('.input-feedback');
        if (feedback) {
            feedback.style.display = 'none';
        }
    }
    
    function animateDifficultySelection(selectedInput) {
        // Remove animação anterior
        difficultyOptions.forEach(option => {
            option.parentNode.classList.remove('selected-animation');
        });
        
        // Adiciona animação ao selecionado
        selectedInput.parentNode.classList.add('selected-animation');
        
        // Remove após animação
        setTimeout(() => {
            selectedInput.parentNode.classList.remove('selected-animation');
        }, 600);
    }
    
    function updateDifficultyDescription(difficulty) {
        const descriptions = {
            'fácil': 'Perfeito para iniciantes - IA lenta e bola mais devagar',
            'normal': 'Equilibrado e divertido - bom para todos os níveis',
            'difícil': 'Para jogadores experientes - IA rápida e bola veloz',
            'expert': 'Apenas para os melhores - desafio extremo!'
        };
        
        // Atualiza descrição se existe elemento para isso
        const descElement = document.querySelector('.difficulty-description');
        if (descElement) {
            descElement.textContent = descriptions[difficulty] || descriptions.normal;
        }
    }
    
    function animateHeroElements() {
        // Anima título com efeito de typing
        const heroTitle = document.querySelector('.hero-title');
        if (heroTitle) {
            heroTitle.style.opacity = '0';
            setTimeout(() => {
                heroTitle.style.opacity = '1';
                heroTitle.style.animation = 'fadeInUp 1s ease';
            }, 500);
        }
        
        // Anima preview do pong
        const pongPreview = document.querySelector('.pong-preview');
        if (pongPreview) {
            setTimeout(() => {
                pongPreview.style.animation = 'slideInRight 1s ease';
            }, 800);
        }
    }
    
    function setupFeatureCardAnimations() {
        const featureCards = document.querySelectorAll('.feature-card');
        
        featureCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            
            // Adiciona hover effect
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    }
    
    // Auto-focus no campo de nome quando a página carrega
    setTimeout(() => {
        if (playerNameInput && !playerNameInput.value) {
            playerNameInput.focus();
        }
    }, 1000);
});

