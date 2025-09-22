/**
 * ByThePong - Classe Paddle JavaScript
 * Mantém encapsulamento e POO equivalente à versão Python
 */

class Paddle {
    /**
     * Construtor da classe Paddle
     * @param {number} x - Posição X inicial
     * @param {number} y - Posição Y inicial
     * @param {number} width - Largura da raquete
     * @param {number} height - Altura da raquete
     * @param {number} speed - Velocidade de movimento
     */
    constructor(x, y, width = 15, height = 100, speed = 7) {
        // Atributos privados
        this._x = x;
        this._y = y;
        this._width = width;
        this._height = height;
        this._speed = speed;
        
        // Configurações de renderização
        this._color = '#ffffff';
        this._glowColor = 'rgba(255, 255, 255, 0.5)';
    }
    
    /**
     * Getter para posição X
     * @returns {number} Posição X atual
     */
    get x() {
        return this._x;
    }
    
    /**
     * Setter para posição X
     * @param {number} value - Nova posição X
     */
    set x(value) {
        this._x = value;
    }
    
    /**
     * Getter para posição Y
     * @returns {number} Posição Y atual
     */
    get y() {
        return this._y;
    }
    
    /**
     * Setter para posição Y
     * @param {number} value - Nova posição Y
     */
    set y(value) {
        this._y = value;
    }
    
    /**
     * Getter para largura
     * @returns {number} Largura da raquete
     */
    get width() {
        return this._width;
    }
    
    /**
     * Getter para altura
     * @returns {number} Altura da raquete
     */
    get height() {
        return this._height;
    }
    
    /**
     * Getter para velocidade
     * @returns {number} Velocidade de movimento
     */
    get speed() {
        return this._speed;
    }
    
    /**
     * Setter para velocidade
     * @param {number} value - Nova velocidade
     */
    set speed(value) {
        this._speed = Math.max(0, value);
    }
    
    /**
     * Getter para cor
     * @returns {string} Cor da raquete
     */
    get color() {
        return this._color;
    }
    
    /**
     * Setter para cor
     * @param {string} value - Nova cor
     */
    set color(value) {
        this._color = value;
    }
    
    /**
     * Move a raquete para cima
     * @param {number} screenHeight - Altura da tela para limitação
     */
    moveUp(screenHeight) {
        this._y = Math.max(0, this._y - this._speed);
    }
    
    /**
     * Move a raquete para baixo
     * @param {number} screenHeight - Altura da tela para limitação
     */
    moveDown(screenHeight) {
        this._y = Math.min(screenHeight - this._height, this._y + this._speed);
    }
    
    /**
     * Define nova posição da raquete
     * @param {number} x - Nova posição X
     * @param {number} y - Nova posição Y
     */
    setPosition(x, y) {
        this._x = x;
        this._y = y;
    }
    
    /**
     * Retorna o centro Y da raquete
     * @returns {number} Posição Y do centro
     */
    centerY() {
        return this._y + this._height / 2;
    }
    
    /**
     * Retorna o centro X da raquete
     * @returns {number} Posição X do centro
     */
    centerX() {
        return this._x + this._width / 2;
    }
    
    /**
     * Retorna retângulo de colisão da raquete
     * @returns {Object} Retângulo com x, y, width, height
     */
    getRect() {
        return {
            x: this._x,
            y: this._y,
            width: this._width,
            height: this._height,
            centerX: this.centerX(),
            centerY: this.centerY(),
            left: this._x,
            right: this._x + this._width,
            top: this._y,
            bottom: this._y + this._height
        };
    }
    
    /**
     * Verifica colisão com outro retângulo
     * @param {Object} rect - Retângulo com x, y, width, height
     * @returns {boolean} True se há colisão
     */
    collidesWithRect(rect) {
        const paddleRect = this.getRect();
        
        return (paddleRect.x < rect.x + rect.width &&
                paddleRect.x + paddleRect.width > rect.x &&
                paddleRect.y < rect.y + rect.height &&
                paddleRect.y + paddleRect.height > rect.y);
    }
    
    /**
     * Verifica colisão com um ponto circular (como uma bola)
     * @param {number} x - Posição X do ponto
     * @param {number} y - Posição Y do ponto
     * @param {number} radius - Raio do círculo
     * @returns {boolean} True se há colisão
     */
    collidesWithCircle(x, y, radius) {
        const rect = this.getRect();
        
        // Encontra o ponto mais próximo da raquete ao centro do círculo
        const closestX = Math.max(rect.x, Math.min(x, rect.x + rect.width));
        const closestY = Math.max(rect.y, Math.min(y, rect.y + rect.height));
        
        // Calcula distância do centro do círculo ao ponto mais próximo
        const distanceX = x - closestX;
        const distanceY = y - closestY;
        const distanceSquared = distanceX * distanceX + distanceY * distanceY;
        
        return distanceSquared < (radius * radius);
    }
    
    /**
     * Move a raquete em direção a um alvo (usado para IA)
     * @param {number} targetY - Posição Y do alvo
     * @param {number} screenHeight - Altura da tela
     * @param {number} difficulty - Nível de dificuldade (0-1)
     */
    moveTowardsTarget(targetY, screenHeight, difficulty = 1.0) {
        const paddleCenter = this.centerY();
        const difference = targetY - paddleCenter;
        
        // Aplica fator de dificuldade (chance de movimento)
        if (Math.random() > difficulty) {
            return; // Às vezes não move (baseado na dificuldade)
        }
        
        // Move apenas se a diferença for significativa
        if (Math.abs(difference) > 5) {
            if (difference > 0) {
                this.moveDown(screenHeight);
            } else {
                this.moveUp(screenHeight);
            }
        }
    }
    
    /**
     * Desenha a raquete no canvas
     * @param {CanvasRenderingContext2D} ctx - Contexto do canvas
     * @param {boolean} withGlow - Se deve desenhar com brilho
     */
    draw(ctx, withGlow = true) {
        ctx.save();
        
        // Desenha brilho se ativado
        if (withGlow) {
            ctx.shadowColor = this._glowColor;
            ctx.shadowBlur = 10;
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 0;
        }
        
        // Desenha a raquete
        ctx.fillStyle = this._color;
        ctx.fillRect(this._x, this._y, this._width, this._height);
        
        // Adiciona gradiente para efeito 3D
        const gradient = ctx.createLinearGradient(
            this._x, 
            this._y, 
            this._x + this._width, 
            this._y
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.3)');
        gradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.1)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.2)');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(this._x, this._y, this._width, this._height);
        
        ctx.restore();
    }
    
    /**
     * Desenha efeitos de movimento da raquete
     * @param {CanvasRenderingContext2D} ctx - Contexto do canvas
     * @param {number} direction - Direção do movimento (-1 para cima, 1 para baixo, 0 parado)
     */
    drawMovementEffect(ctx, direction) {
        if (direction === 0) return;
        
        ctx.save();
        ctx.globalAlpha = 0.3;
        
        const trailCount = 3;
        const trailSpacing = 5;
        
        for (let i = 0; i < trailCount; i++) {
            const offsetY = direction * trailSpacing * (i + 1);
            const alpha = (trailCount - i) / trailCount * 0.3;
            
            ctx.globalAlpha = alpha;
            ctx.fillStyle = this._color;
            ctx.fillRect(
                this._x, 
                this._y + offsetY, 
                this._width, 
                this._height
            );
        }
        
        ctx.restore();
    }
    
    /**
     * Retorna uma representação em string da raquete
     * @returns {string} Informações da raquete
     */
    toString() {
        return `Paddle(x=${this._x}, y=${this._y}, w=${this._width}, h=${this._height})`;
    }
    
    /**
     * Retorna dados serializados da raquete
     * @returns {Object} Dados da raquete
     */
    toJSON() {
        return {
            x: this._x,
            y: this._y,
            width: this._width,
            height: this._height,
            speed: this._speed,
            color: this._color
        };
    }
    
    /**
     * Cria uma raquete a partir de dados serializados
     * @param {Object} data - Dados da raquete
     * @returns {Paddle} Nova instância de Paddle
     */
    static fromJSON(data) {
        const paddle = new Paddle(
            data.x, 
            data.y, 
            data.width, 
            data.height, 
            data.speed
        );
        if (data.color) {
            paddle._color = data.color;
        }
        return paddle;
    }
}

// Torna a classe disponível globalmente
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Paddle;
} else {
    window.Paddle = Paddle;
}

