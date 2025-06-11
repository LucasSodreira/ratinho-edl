import sys
import os
from jogo import JogoLabirinto

def listar_labirintos_disponiveis():
    """Lista todos os labirintos disponíveis na pasta labirintos"""
    pasta_labirintos = "labirintos"
    labirintos = []
    
    if os.path.exists(pasta_labirintos):
        for arquivo in os.listdir(pasta_labirintos):
            if arquivo.endswith('.txt'):
                caminho_completo = os.path.join(pasta_labirintos, arquivo)
                labirintos.append((arquivo, caminho_completo))
    
    return sorted(labirintos)

def mostrar_menu_labirintos():
    """Mostra menu interativo para seleção de labirintos"""
    print("\n" + "="*50)
    print("🐭 RATINHO NO LABIRINTO - SELETOR DE MAPAS")
    print("="*50)
    
    labirintos = listar_labirintos_disponiveis()
    
    if not labirintos:
        print("❌ Nenhum labirinto encontrado na pasta 'labirintos/'")
        return None
    
    print("Labirintos disponíveis:")
    print("-" * 30)
    
    for i, (nome, caminho) in enumerate(labirintos, 1):
        # Extrair informações básicas do arquivo
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                primeira_linha = f.readline().strip()
                if 'x' in primeira_linha.lower():
                    dimensoes = primeira_linha.replace('x', ' x ').split()
                    if len(dimensoes) >= 3:
                        altura, largura = dimensoes[0], dimensoes[2]
                        print(f"{i:2d}. {nome:<20} ({altura}x{largura})")
                    else:
                        print(f"{i:2d}. {nome:<20} (formato especial)")
                else:
                    print(f"{i:2d}. {nome:<20} (dimensões não detectadas)")
        except:
            print(f"{i:2d}. {nome:<20} (erro ao ler)")
    
    print("-" * 30)
    print(" 0. Sair")
    print("="*50)
    
    try:
        escolha = input("Escolha um labirinto (número): ").strip()
        
        if escolha == '0':
            print("👋 Saindo...")
            return None
        
        indice = int(escolha) - 1
        if 0 <= indice < len(labirintos):
            nome, caminho = labirintos[indice]
            print(f"✅ Selecionado: {nome}")
            return caminho
        else:
            print("❌ Número inválido!")
            return mostrar_menu_labirintos()
            
    except (ValueError, KeyboardInterrupt):
        print("\n👋 Operação cancelada.")
        return None

def main():
    """Função principal para inicializar o jogo"""
    print("🎮 Inicializando Ratinho no Labirinto...")
    
    # Verificar se foi passado argumento de linha de comando
    if len(sys.argv) > 1:
        arquivo_labirinto = sys.argv[1]
        
        # Se não tem extensão, assumir que está na pasta labirintos
        if not arquivo_labirinto.endswith('.txt'):
            arquivo_labirinto += '.txt'
        
        # Se não tem caminho, assumir que está na pasta labirintos
        if not os.path.sep in arquivo_labirinto and not arquivo_labirinto.startswith('labirintos'):
            arquivo_labirinto = os.path.join('labirintos', arquivo_labirinto)
        
        print(f"📁 Labirinto especificado via argumento: {arquivo_labirinto}")
        
        if not os.path.exists(arquivo_labirinto):
            print(f"❌ Arquivo '{arquivo_labirinto}' não encontrado!")
            print("💡 Tentando encontrar labirintos disponíveis...")
            arquivo_labirinto = mostrar_menu_labirintos()
            if not arquivo_labirinto:
                return
    else:
        # Tentar usar labirinto padrão ou mostrar menu
        arquivo_padrao = "labirintos/labirinto.txt"
        
        if os.path.exists(arquivo_padrao):
            print(f"📁 Usando labirinto padrão: {arquivo_padrao}")
            arquivo_labirinto = arquivo_padrao
        else:
            print("📁 Labirinto padrão não encontrado. Escolha um labirinto:")
            arquivo_labirinto = mostrar_menu_labirintos()
            if not arquivo_labirinto:
                return
    
    print(f"\n🚀 Carregando jogo com: {arquivo_labirinto}")
    print("⏳ Aguarde...")
    
    try:
        jogo = JogoLabirinto(arquivo_labirinto)
        jogo.executar()
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        print("\n🔧 Informações para debug:")
        print(f"   - Arquivo: {arquivo_labirinto}")
        print(f"   - Existe: {os.path.exists(arquivo_labirinto) if 'arquivo_labirinto' in locals() else 'N/A'}")
        print(f"   - Diretório atual: {os.getcwd()}")
        
        input("\n📝 Pressione Enter para sair...")

if __name__ == "__main__":
    main()



