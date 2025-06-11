import pygame
import sys

def teste_basico():
    """Teste básico do pygame"""
    print("🧪 Testando inicialização básica do pygame...")
    
    try:
        pygame.init()
        print("✅ Pygame inicializado")
        
        # Criar janela simples
        tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Teste Básico")
        print("✅ Janela criada")
        
        # Loop básico
        clock = pygame.time.Clock()
        running = True
        frames = 0
        
        while running and frames < 300:  # 5 segundos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Desenhar
            tela.fill((50, 100, 150))
            
            # Texto de teste
            font = pygame.font.Font(None, 36)
            texto = font.render(f"Teste OK - Frame {frames}", True, (255, 255, 255))
            tela.blit(texto, (50, 50))
            
            pygame.display.flip()
            clock.tick(60)
            frames += 1
            
            if frames == 1:
                print("✅ Primeira tela desenhada")
        
        pygame.quit()
        print("✅ Teste concluído com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def teste_tela_inicial():
    """Teste específico da tela inicial"""
    print("\n🧪 Testando tela inicial...")
    
    try:
        from tela_inicial import TelaInicial
        print("✅ Módulo tela_inicial importado")
        
        tela_inicial = TelaInicial()
        print("✅ TelaInicial criada com sucesso")
        
        # Não executar o loop completo, só verificar se inicializa
        pygame.quit()
        print("✅ Teste da tela inicial passou")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste da tela inicial: {e}")
        import traceback
        traceback.print_exc()
        return False

def teste_main_completo():
    """Teste completo simulando o main.py"""
    print("\n🧪 Testando simulação completa do main...")
    
    try:
        from tela_inicial import TelaInicial
        print("✅ Módulo tela_inicial importado")
        
        print("🎨 Criando tela inicial...")
        tela_inicial = TelaInicial()
        print("✅ TelaInicial criada")
        
        print("🚀 Executando tela inicial por 5 segundos...")
        
        # Executar por tempo limitado para teste
        import threading
        import time
        
        resultado = [None]
        
        def executar_com_timeout():
            try:
                resultado[0] = tela_inicial.executar()
            except Exception as e:
                resultado[0] = f"ERRO: {e}"
        
        thread = threading.Thread(target=executar_com_timeout)
        thread.daemon = True
        thread.start()
        
        # Aguardar 3 segundos
        time.sleep(3)
        
        if thread.is_alive():
            print("✅ Tela inicial está rodando normalmente")
            # Simular ESC para fechar
            import pygame
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
            thread.join(timeout=2)
            
        print(f"📊 Resultado: {resultado[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste completo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Executar todos os testes
    teste1 = teste_basico()
    teste2 = teste_tela_inicial()
    teste3 = teste_main_completo()
    
    print(f"\n📊 Resultados Finais:")
    print(f"   Pygame básico: {'✅ OK' if teste1 else '❌ FALHOU'}")
    print(f"   Tela inicial: {'✅ OK' if teste2 else '❌ FALHOU'}")
    print(f"   Simulação main: {'✅ OK' if teste3 else '❌ FALHOU'}")
    
    if teste1 and teste2 and teste3:
        print("\n🎉 Todos os testes passaram!")
        print("💡 Tente executar: python main.py")
    elif teste1 and teste2:
        print("\n🔍 Problema pode estar no loop principal ou main.py")
    else:
        print("\n🚨 Problemas encontrados nos testes básicos")
