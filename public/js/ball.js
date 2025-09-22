/**
 * ByThePong - Classe Ball JavaScript
 * Mantém encapsulamento e POO equivalente à versão Python
 */

class Ball {
    /**
     * Construtor da classe Ball
     * @param {number} x - Posição inicial X
     * @param {number} y - Posição inicial Y
     * @param {number} radius - Raio da bola
     * @param {number} initialSpeed - Velocidade inicial
     */
    constructor(x, y, radius = 10, initialSpeed = 5) {
        // Atributos privados
        this._x = x;
        this._y = y;
        this._radius = radius;
        this._speed = initialSpeed;
        this._initialSpeed = initialSpeed;
        
        // Calcula ângulo inicial aleatório
        this._angle = (Math.random() - 0.5) * Math.PI / 2; // -45° a +45°
        this._dx = this._speed * Math.cos(this._angle);
        this._dy = this._speed * Math.sin(this._angle);
        
        // Configurações de física
        this._maxSpeed = 12;
        this._speedIncrease = 1.05;
        this._minSpeed = 2;
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
     * Getter para o raio
     * @returns {number} Raio da bola
     */
    get radius() {
        return this._radius;
    }
    
    /**
     * Getter para a velocidade
     * @returns {number} Velocidade atual
     */
    get speed() {
        return this._speed;
    }
    
    /**
     * Getter para direção X
     * @returns {number} Velocidade em X
     */
    get dx() {
        return this._dx;
    }
    
    /**
     * Getter para direção Y
     * @returns {number} Velocidade em Y
     */
    get dy() {
        return this._dy;
    }
    
    /**
     * Move a bola baseado na velocidade atual
     */
    move() {
        this._x += this._dx;
        this._y += this._dy;
    }
    
    /**
     * Inverte a direção horizontal (rebate em X)
     */
    bounceX() {
        this._dx = -this._dx;
    }
    
    /**
     * Inverte a direção vertical (rebate em Y)
     */
    bounceY() {
        this._dy = -this._dy;
    }
    
    /**
     * Rebate a bola na raquete com cálculo de ângulo
     * @param {number} paddleY - Posição Y da raquete
     * @param {number} paddleHeight - Altura da raquete
     */
    bouncePaddle(paddleY, paddleHeight) {
        // Calcula onde a bola bateu na raquete (de -1 a 1)
        const relativeIntersectY = (this._y - (paddleY + paddleHeight / 2)) / (paddleHeight / 2);
        
        // Calcula novo ângulo baseado na posição de impacto
        const angle = relativeIntersectY * Math.PI / 4; // Máximo de 45°
        
        // Aumenta velocidade gradualmente
        this._speed = Math.min(this._speed * this._speedIncrease, this._maxSpeed);
        
        // Inverte direção horizontal e aplica novo ângulo
        this._dx = -this._dx;
        this._dy = this._speed * Math.sin(angle);
        
        // Garante velocidade mínima
        if (Math.abs(this._dx) < this._minSpeed) {
            this._dx = this._dx > 0 ? this._minSpeed : -this._minSpeed;
        }
    }
    
    /**
     * Reseta a bola para posição inicial
     * @param {number} x - Nova posição X
     * @param {number} y - Nova posição Y
     */
    reset(x, y) {
        this._x = x;
        this._y = y;
        this._speed = this._initialSpeed;
        
        // Novo ângulo aleatório
        this._angle = (Math.random() - 0.5) * Math.PI / 2;
        this._dx = this._speed * Math.cos(this._angle);
        this._dy = this._speed * Math.sin(this._angle);
        
        // Direção horizontal aleatória
        if (Math.random() < 0.5) {
            this._dx = -this._dx;
        }
    }
    
    /**
     * Retorna retângulo de colisão da bola
     * @returns {Object} Retângulo com x, y, width, height
     */
    getRect() {
        return {
            x: this._x - this._radius,
            y: this._y - this._radius,
            width: this._radius * 2,
            height: this._radius * 2,
            centerX: this._x,
            centerY: this._y,
            radius: this._radius
        };
    }
    
    /**
     * Verifica colisão com retângulo
     * @param {Object} rect - Retângulo com x, y, width, height
     * @returns {boolean} True se há colisão
     */
    collidesWithRect(rect) {
        const ballRect = this.getRect();
        
        // Verifica se há sobreposição
        return (ballRect.x < rect.x + rect.width &&
                ballRect.x + ballRect.width > rect.x &&
                ballRect.y < rect.y + rect.height &&
                ballRect.y + ballRect.height > rect.y);
    }
    
    /**
     * Desenha a bola no canvas
     * @param {CanvasRenderingContext2D} ctx - Contexto do canvas
     * @param {string} color - Cor da bola
     */
    draw(ctx, color = '#ffffff') {
        ctx.save();
        
        // Desenha bola com brilho
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(this._x, this._y, this._radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Adiciona brilho
        const gradient = ctx.createRadialGradient(
            this._x - this._radius / 3, 
            this._y - this._radius / 3, 
            0,
            this._x, 
            this._y, 
            this._radius
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.8)');
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this._x, this._y, this._radius, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
    
    /**
     * Retorna uma representação em string da bola
     * @returns {string} Informações da bola
     */
    toString() {
        return `Ball(x=${this._x.toFixed(1)}, y=${this._y.toFixed(1)}, speed=${this._speed.toFixed(1)})`;
    }
    
    /**
     * Retorna dados serializados da bola
     * @returns {Object} Dados da bola
     */
    toJSON() {
        return {
            x: this._x,
            y: this._y,
            radius: this._radius,
            speed: this._speed,
            dx: this._dx,
            dy: this._dy
        };
    }
    
    /**
     * Cria uma bola a partir de dados serializados
     * @param {Object} data - Dados da bola
     * @returns {Ball} Nova instância de Ball
     */
    static fromJSON(data) {
        const ball = new Ball(data.x, data.y, data.radius, data.speed);
        // Só aplica dx/dy se presentes; caso contrário mantém valores calculados
        if (typeof data.dx === 'number') ball._dx = data.dx;
        if (typeof data.dy === 'number') ball._dy = data.dy;
        return ball;
    }
}

// Torna a classe disponível globalmente
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Ball;
} else {
    window.Ball = Ball;
}
