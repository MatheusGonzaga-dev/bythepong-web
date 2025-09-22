#!/usr/bin/env python3
"""
ByThePong Web - Script de execução simplificado
Executa o servidor web Flask com configurações otimizadas
"""

import sys
import webbrowser
import threading
import time
from app import app, socketio

def open_browser():
    """Abre o navegador automaticamente após o servidor iniciar"""
    time.sleep(2)  # Aguarda o servidor inicializar
    webbrowser.open('http://localhost:5000')

def main():
    """Função principal de execução"""
    print("🚀 Iniciando ByThePong Web...")
    print("=" * 50)
    print("🎮 Jogo: ByThePong - Versão Web")
    print("🐍 Backend: Python Flask + SocketIO")
    print("🌐 Frontend: HTML5 Canvas + JavaScript")
    print("💻 Servidor: http://localhost:5000")
    print("=" * 50)
    
    # Abre navegador em thread separada
    if '--no-browser' not in sys.argv:
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
    
    try:
        # Inicia servidor Flask-SocketIO
        socketio.run(
            app, 
            debug=False,  # Mude para True se quiser debug
            host='0.0.0.0', 
            port=5000,
            allow_unsafe_werkzeug=True  # Para desenvolvimento
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário.")
        print("👋 Obrigado por jogar ByThePong!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        print("\n🔧 Dicas de solução:")
        print("   • Verifique se a porta 5000 está livre")
        print("   • Execute: pip install -r requirements.txt")
        print("   • Tente executar: python app.py")
        sys.exit(1)

if __name__ == "__main__":
    main()

