/**
 * ByThePong - Classe Player JavaScript
 * Mantém encapsulamento e POO equivalente à versão Python
 */

class Player {
    /**
     * Construtor da classe Player
     * @param {string} name - Nome do jogador
     */
    constructor(name = "Jogador") {
        // Atributos privados usando convenção JavaScript
        this._name = "";
        this._score = 0;
        
        // Inicializa com validação
        this.name = name;
    }
    
    /**
     * Getter para o nome do jogador
     * @returns {string} Nome do jogador
     */
    get name() {
        return this._name;
    }
    
    /**
     * Setter para o nome do jogador com validação
     * @param {string} value - Novo nome do jogador
     */
    set name(value) {
        if (typeof value !== 'string' || !value.trim()) {
            throw new Error("O nome do jogador não pode ser vazio.");
        }
        this._name = value.trim();
    }
    
    /**
     * Getter para a pontuação do jogador
     * @returns {number} Pontuação atual
     */
    get score() {
        return this._score;
    }
    
    /**
     * Adiciona um ponto à pontuação do jogador
     */
    addPoint() {
        this._score++;
    }
    
    /**
     * Reseta a pontuação do jogador para zero
     */
    resetScore() {
        this._score = 0;
    }
    
    /**
     * Retorna uma representação em string do jogador
     * @returns {string} Informações do jogador
     */
    toString() {
        return `${this._name}: ${this._score} pontos`;
    }
    
    /**
     * Retorna um objeto com os dados serializados do jogador
     * @returns {Object} Dados do jogador
     */
    toJSON() {
        return {
            name: this._name,
            score: this._score
        };
    }
    
    /**
     * Cria um jogador a partir de dados serializados
     * @param {Object} data - Dados do jogador
     * @returns {Player} Nova instância de Player
     */
    static fromJSON(data) {
        const player = new Player(data.name);
        player._score = data.score || 0;
        return player;
    }
}

// Torna a classe disponível globalmente
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Player;
} else {
    window.Player = Player;
}
