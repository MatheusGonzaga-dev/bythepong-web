/**
 * ByThePong - Funções utilitárias JavaScript
 * Funções auxiliares para o funcionamento da aplicação web
 */

/**
 * Sistema de notificações
 */
class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.init();
    }
    
    init() {
        // Cria container de notificações se não existir
        this.container = document.getElementById('notification');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'notification';
            this.container.className = 'notification';
            this.container.innerHTML = `
                <span class="notification-text"></span>
                <button class="notification-close">&times;</button>
            `;
            document.body.appendChild(this.container);
        }
        
        // Adiciona event listener para fechar notificação
        const closeBtn = this.container.querySelector('.notification-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hide());
        }
    }
    
    show(message, type = 'info', duration = 5000) {
        const textElement = this.container.querySelector('.notification-text');
        if (textElement) {
            textElement.textContent = message;
        }
        
        // Remove classes anteriores
        this.container.className = 'notification show';
        
        // Adiciona classe do tipo
        if (type) {
            this.container.classList.add(type);
        }
        
        // Auto-hide após duração especificada
        if (duration > 0) {
            setTimeout(() => this.hide(), duration);
        }
    }
    
    hide() {
        this.container.classList.remove('show');
    }
    
    success(message, duration = 5000) {
        this.show(message, 'success', duration);
    }
    
    error(message, duration = 7000) {
        this.show(message, 'error', duration);
    }
    
    warning(message, duration = 6000) {
        this.show(message, 'warning', duration);
    }
}

// Instância global do sistema de notificações
const notifications = new NotificationSystem();

/**
 * Mostra uma notificação
 * @param {string} message - Mensagem a ser exibida
 * @param {string} type - Tipo da notificação (success, error, warning, info)
 * @param {number} duration - Duração em milissegundos
 */
function showNotification(message, type = 'info', duration = 5000) {
    notifications.show(message, type, duration);
}

/**
 * Utilitários de API
 */
class ApiUtils {
    static async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }
    
    static async get(url) {
        return this.request(url, { method: 'GET' });
    }
    
    static async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    static async put(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    static async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
}

/**
 * Utilitários de localStorage
 */
class StorageUtils {
    static get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return defaultValue;
        }
    }
    
    static set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Error writing to localStorage:', error);
            return false;
        }
    }
    
    static remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Error removing from localStorage:', error);
            return false;
        }
    }
    
    static clear() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('Error clearing localStorage:', error);
            return false;
        }
    }
}

/**
 * Utilitários de animação
 */
class AnimationUtils {
    static easeInOut(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }
    
    static easeIn(t) {
        return t * t;
    }
    
    static easeOut(t) {
        return t * (2 - t);
    }
    
    static linear(t) {
        return t;
    }
    
    static animate(from, to, duration, callback, easing = this.easeInOut) {
        const startTime = performance.now();
        const difference = to - from;
        
        function step(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easing(progress);
            const value = from + difference * easedProgress;
            
            callback(value, progress);
            
            if (progress < 1) {
                requestAnimationFrame(step);
            }
        }
        
        requestAnimationFrame(step);
    }
}

/**
 * Utilitários matemáticos
 */
class MathUtils {
    static clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }
    
    static lerp(start, end, t) {
        return start + (end - start) * t;
    }
    
    static distance(x1, y1, x2, y2) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    static angle(x1, y1, x2, y2) {
        return Math.atan2(y2 - y1, x2 - x1);
    }
    
    static randomBetween(min, max) {
        return Math.random() * (max - min) + min;
    }
    
    static randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    static degToRad(degrees) {
        return degrees * Math.PI / 180;
    }
    
    static radToDeg(radians) {
        return radians * 180 / Math.PI;
    }
}

/**
 * Utilitários de validação
 */
class ValidationUtils {
    static isValidPlayerName(name) {
        return typeof name === 'string' && 
               name.trim().length > 0 && 
               name.trim().length <= 20 &&
               /^[a-zA-ZÀ-ÿ0-9\s]+$/.test(name.trim());
    }
    
    static isValidDifficulty(difficulty) {
        const validDifficulties = ['fácil', 'normal', 'difícil', 'expert'];
        return validDifficulties.includes(difficulty);
    }
    
    static sanitizePlayerName(name) {
        if (typeof name !== 'string') return '';
        return name.trim().substring(0, 20);
    }
}

/**
 * Utilitários de formatação
 */
class FormatUtils {
    static formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    
    static formatScore(score) {
        return score.toString().padStart(2, '0');
    }
    
    static formatPlayerName(name, maxLength = 15) {
        if (name.length <= maxLength) return name;
        return name.substring(0, maxLength - 3) + '...';
    }
    
    static getDifficultyEmoji(difficulty) {
        const emojis = {
            'fácil': '🟢',
            'normal': '🟡',
            'difícil': '🟠',
            'expert': '🔴'
        };
        return emojis[difficulty] || '⚪';
    }
    
    static getDifficultyColor(difficulty) {
        const colors = {
            'fácil': '#2ed573',
            'normal': '#ffa502',
            'difícil': '#ff6b6b',
            'expert': '#ff4757'
        };
        return colors[difficulty] || '#6c6c6c';
    }
}

/**
 * Utilitários de eventos
 */
class EventUtils {
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    static throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    static once(func) {
        let called = false;
        return function executedFunction(...args) {
            if (!called) {
                called = true;
                return func.apply(this, args);
            }
        };
    }
}

/**
 * Utilitários de dispositivo
 */
class DeviceUtils {
    static isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    static isTablet() {
        return /iPad|Android|Tablet/i.test(navigator.userAgent) && !this.isMobile();
    }
    
    static isDesktop() {
        return !this.isMobile() && !this.isTablet();
    }
    
    static getTouchSupport() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    }
    
    static getScreenSize() {
        return {
            width: window.innerWidth,
            height: window.innerHeight
        };
    }
}

/**
 * ThemeManager - gerencia temas visuais (neon, retrô, minimal)
 */
class ThemeManager {
    constructor() {
        this.current = StorageUtils.get('theme', 'neon');
        this.themes = ['neon', 'retro', 'minimal'];
        this.apply(this.current);
    }

    apply(theme) {
        if (!this.themes.includes(theme)) theme = 'neon';
        document.documentElement.setAttribute('data-theme', theme);
        StorageUtils.set('theme', theme);
    }

    next() {
        const idx = this.themes.indexOf(this.current);
        this.current = this.themes[(idx + 1) % this.themes.length];
        this.apply(this.current);
        return this.current;
    }
}

/**
 * AudioManager - gerencia SFX e BGM com volume/mute
 */
class AudioManager {
    constructor() {
        this.muted = StorageUtils.get('audio_muted', false);
        this.volume = StorageUtils.get('audio_volume', 0.6);
        
        // WebAudio precisa de gesto do usuário para iniciar em muitos navegadores
        this.ctx = null; // adiado até habilitar
        this.initialized = false;
    }

    // Cria/retoma o AudioContext quando houver gesto do usuário
    enable() {
        if (this.muted) return false;
        if (!this.ctx) {
            const Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return false;
            this.ctx = new Ctx();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume?.();
        }
        this.initialized = true;
        return true;
    }

    setMuted(m) {
        this.muted = !!m;
        StorageUtils.set('audio_muted', this.muted);
    }

    setVolume(v) {
        this.volume = MathUtils.clamp(v, 0, 1);
        StorageUtils.set('audio_volume', this.volume);
    }

    beep(freq = 440, duration = 0.15, type = 'sine', gainMul = 1) {
        if (this.muted) return;
        // Garante contexto ativo
        if (!this.enable()) return;
        const o = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        o.type = type;
        o.frequency.value = freq;
        g.gain.value = this.volume * 0.3 * gainMul;
        o.connect(g); g.connect(this.ctx.destination);
        o.start();
        o.stop(this.ctx.currentTime + duration);
    }

    // Atalhos
    sfxHit() { this.beep(600, 0.05, 'square', 1); }
    sfxScore() { this.beep(320, 0.2, 'sawtooth', 1.2); }
    sfxCountdownTick() { this.beep(700, 0.08, 'square', 0.8); }
    sfxCountdownGo() { this.beep(900, 0.18, 'triangle', 1.3); }
}

// Exporta todas as utilitários para o escopo global
window.showNotification = showNotification;
window.ApiUtils = ApiUtils;
window.StorageUtils = StorageUtils;
window.AnimationUtils = AnimationUtils;
window.MathUtils = MathUtils;
window.ValidationUtils = ValidationUtils;
window.FormatUtils = FormatUtils;
window.EventUtils = EventUtils;
window.DeviceUtils = DeviceUtils;
window.ThemeManager = ThemeManager;
window.AudioManager = AudioManager;

