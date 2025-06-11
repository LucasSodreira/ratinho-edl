"""
Launcher alternativo para forçar a tela inicial
"""
import sys
import os

def main():
    print("🚀 LAUNCHER - Ratinho no Labirinto")
    print("=" * 40)
    
    try:
        # Forçar importação e execução direta
        print("📦 Importando módulos...")
        
        from tela_inicial import TelaInicial
        print("✅ TelaInicial importada")
        
        print("🎨 Criando tela inicial...")
        tela = TelaInicial()
        print("✅ Tela criada")
        
        print("▶️ Executando tela inicial...")
        print("   (A janela deve aparecer agora)")
        
        arquivo_selecionado = tela.executar()
        
        if arquivo_selecionado:
            print(f"✅ Arquivo selecionado: {arquivo_selecionado}")
            
            # Iniciar jogo
            print("🎮 Iniciando jogo...")
            from jogo import JogoLabirinto
            
            jogo = JogoLabirinto(arquivo_selecionado)
            jogo.executar()
            
        else:
            print("👋 Nenhum arquivo selecionado")
            
    except Exception as e:
        print(f"💥 Erro: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
