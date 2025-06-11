"""
RATINHO NO LABIRINTO - Algoritmos de Pathfinding
Ponto de entrada único do projeto
Autor: Sistema de Demonstração Educacional
"""
import sys
import os
from utils import verificar_dependencias, debug_print

def main():
    """Função principal para inicializar o jogo"""
    print("🐭 RATINHO NO LABIRINTO - Sistema de Pathfinding")
    print("=" * 55)
    print("🎓 Demonstração educacional de algoritmos de busca")
    print("=" * 55)
    
    # Verificar dependências críticas
    if not verificar_dependencias():
        input("❌ Dependências não encontradas. Pressione Enter para sair...")
        return
    
    print("🎮 Inicializando sistema...")
    
    # Verificar se foi passado argumento de linha de comando (modo direto)
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
            print("🎨 Tentando abrir seletor gráfico...")
            
            try:
                from tela_inicial import TelaInicial
                tela_inicial = TelaInicial()
                arquivo_selecionado = tela_inicial.executar()
                
                if not arquivo_selecionado:
                    print("👋 Jogo cancelado pelo usuário.")
                    return
                
                arquivo_labirinto = arquivo_selecionado
                
            except Exception as e:
                print(f"❌ Erro na tela inicial: {e}")
                print("📝 Usando modo de compatibilidade...")
                arquivo_labirinto = _modo_compatibilidade()
                if not arquivo_labirinto:
                    return
        
        print(f"🚀 Iniciando jogo diretamente com: {os.path.basename(arquivo_labirinto)}")
    
    else:
        # Modo normal - sempre mostrar tela inicial gráfica
        print("🎨 Abrindo seletor de labirintos...")
        
        try:
            from tela_inicial import TelaInicial
            print("✅ Módulo tela_inicial importado")
            
            tela_inicial = TelaInicial()
            print("✅ TelaInicial criada")
            
            arquivo_labirinto = tela_inicial.executar()
            print(f"✅ Tela inicial retornou: {arquivo_labirinto}")
            
            if not arquivo_labirinto:
                print("👋 Jogo cancelado pelo usuário.")
                return
                
            print(f"✅ Labirinto selecionado: {os.path.basename(arquivo_labirinto)}")
            
        except ImportError as e:
            print(f"❌ Erro ao importar tela_inicial: {e}")
            print("🔄 Tentando modo de compatibilidade...")
            arquivo_labirinto = _modo_compatibilidade()
            if not arquivo_labirinto:
                return
                
        except Exception as e:
            print(f"❌ Erro na tela inicial: {e}")
            import traceback
            traceback.print_exc()
            print("🔄 Tentando modo de compatibilidade...")
            
            arquivo_labirinto = _modo_compatibilidade()
            if not arquivo_labirinto:
                return
    
    print(f"\n🚀 Carregando jogo...")
    print("⏳ Aguarde a janela maximizar...")
    
    try:
        from jogo import JogoLabirinto
        print("✅ Módulo jogo importado")
        
        jogo = JogoLabirinto(arquivo_labirinto)
        print("✅ JogoLabirinto criado")
        
        jogo.executar()
        
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        print("\n🔧 Informações para debug:")
        print(f"   - Arquivo: {arquivo_labirinto}")
        print(f"   - Existe: {os.path.exists(arquivo_labirinto) if 'arquivo_labirinto' in locals() else 'N/A'}")
        print(f"   - Diretório atual: {os.getcwd()}")
        
        input("\n📝 Pressione Enter para sair...")

def _modo_compatibilidade():
    """Modo de compatibilidade com menu texto se a interface gráfica falhar"""
    print("\n" + "="*50)
    print("🐭 RATINHO NO LABIRINTO - MODO COMPATIBILIDADE")
    print("="*50)
    
    pasta_labirintos = "labirintos"
    labirintos = []
    
    if os.path.exists(pasta_labirintos):
        for arquivo in sorted(os.listdir(pasta_labirintos)):
            if arquivo.endswith('.txt'):
                caminho_completo = os.path.join(pasta_labirintos, arquivo)
                labirintos.append((arquivo, caminho_completo))
    
    if not labirintos:
        print("❌ Nenhum labirinto encontrado na pasta 'labirintos/'")
        return None
    
    print("Labirintos disponíveis:")
    print("-" * 30)
    
    for i, (nome, caminho) in enumerate(labirintos, 1):
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
            return None
        
        indice = int(escolha) - 1
        if 0 <= indice < len(labirintos):
            nome, caminho = labirintos[indice]
            print(f"✅ Selecionado: {nome}")
            return caminho
        else:
            print("❌ Número inválido!")
            return _modo_compatibilidade()
            
    except (ValueError, KeyboardInterrupt):
        print("\n👋 Operação cancelada.")
        return None

if __name__ == "__main__":
    main()



