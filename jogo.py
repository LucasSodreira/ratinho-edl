import pygame
import sys
from config import ConfiguracaoJogo
from player import GerenciadorPlayer
from interface import GerenciadorInterface
from imgs import *
from rato import *
# Importar classes específicas para funcionalidades avançadas
from labirinto import GerenciadorLabirinto
from pathfinding import GerenciadorPathfinding

class JogoLabirinto:
    def __init__(self, arquivo_labirinto):
        pygame.init()
        
        self.config = ConfiguracaoJogo()
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        
        # Obter informações da tela
        info_tela = pygame.display.Info()
        self.resolucao_nativa = (info_tela.current_w, info_tela.current_h)
        
        # Carregar e validar labirinto
        self._carregar_labirinto(arquivo_labirinto)
        
        # Inicializar componentes
        self.interface = GerenciadorInterface(self.config)
        self.pathfinder = GerenciadorPathfinding()
        self.inicializar_tela()
        self.player_manager = GerenciadorPlayer(
            self.posicao_inicial, self.tamanho_celula, self.offset_x, self.offset_y
        )
        
        self.reiniciar_busca()
    
    def _carregar_labirinto(self, arquivo_labirinto):
        """Carrega e valida o arquivo do labirinto"""
        try:
            self.labirinto = criar_labirinto(arquivo_labirinto)
            validacao = validar_labirinto(self.labirinto)
            
            if not validacao["valido"]:
                raise ValueError(f"Labirinto inválido: {validacao['erro']}")
            
            self.info_labirinto = validacao
            print(f"Labirinto carregado: {validacao['dimensoes'][0]}x{validacao['dimensoes'][1]}")
            print(f"Paredes: {validacao['paredes']}, Caminhos livres: {validacao['caminhos_livres']}")
            
        except Exception as e:
            print(f"Erro ao carregar labirinto: {e}")
            pygame.quit()
            sys.exit(1)
        
        self.num_linhas = len(self.labirinto)
        self.num_colunas = len(self.labirinto[0])
        
        # Posições importantes
        self.posicao_inicial = encontrar_posicao_inicial(self.labirinto)
        self.posicao_saida = encontrar_posicao_saida(self.labirinto)
    
    def inicializar_tela(self):
        """Inicializa a tela em modo maximizado usando API do Windows"""
        import os
        
        # Configurar variável de ambiente do SDL para centralizar
        os.environ['SDL_WINDOW_CENTERED'] = '1'
        
        # Primeiro criar uma janela pequena
        self.tela = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Ratinho no Labirinto - BFS Pathfinding")
        
        # Aguardar um pouco para garantir que a janela foi criada
        pygame.time.wait(100)
        
        # Usar API do Windows para maximizar
        try:
            import ctypes
            import ctypes.wintypes
            
            # Obter handle da janela do pygame
            hwnd = pygame.display.get_wm_info()["window"]
            
            # Constantes do Windows para maximização
            SW_MAXIMIZE = 3
            SW_RESTORE = 9
            
            # Primeiro restaurar para garantir que não está minimizada
            ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
            pygame.time.wait(50)
            
            # Depois maximizar
            ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
            pygame.time.wait(100)
            
            # Forçar atualização da tela
            pygame.display.flip()
            
            print("Janela maximizada com sucesso usando API do Windows")
            
        except (ImportError, KeyError, AttributeError, OSError) as e:
            # Fallback: usar tamanho manual se API falhar
            print(f"API do Windows falhou ({e}), usando tamanho manual")
            largura_maxima = int(self.resolucao_nativa[0] * 0.95)
            altura_maxima = int(self.resolucao_nativa[1] * 0.9)
            self.tela = pygame.display.set_mode((largura_maxima, altura_maxima), pygame.RESIZABLE)
        
        # Aguardar um pouco mais para garantir que as mudanças foram aplicadas
        pygame.time.wait(100)
        
        self.calcular_dimensoes_tela()
    
    def calcular_dimensoes_tela(self):
        """Calcula as dimensões adaptativas baseadas no tamanho atual da tela"""
        largura_tela, altura_tela = self.tela.get_size()
        
        # Área disponível para o labirinto (descontando UI e margens)
        largura_disponivel = largura_tela - (self.config.MARGEM_LATERAL * 2)
        altura_disponivel = altura_tela - self.config.MARGEM_UI - 20
        
        # Calcular tamanho ideal da célula baseado no espaço disponível
        tamanho_celula_largura = largura_disponivel // self.num_colunas
        tamanho_celula_altura = altura_disponivel // self.num_linhas
        
        # Usar o menor para manter proporção quadrada
        self.tamanho_celula = min(tamanho_celula_largura, tamanho_celula_altura, 80)  # Máximo 80px
        self.tamanho_celula = max(self.tamanho_celula, 20)  # Mínimo 20px
        
        # Dimensões do labirinto renderizado
        self.largura_labirinto = self.num_colunas * self.tamanho_celula
        self.altura_labirinto = self.num_linhas * self.tamanho_celula
        
        # Posição para centralizar o labirinto
        self.offset_x = (largura_tela - self.largura_labirinto) // 2
        self.offset_y = 20  # Pequena margem do topo
        
        print(f"Tela: {largura_tela}x{altura_tela}, Célula: {self.tamanho_celula}px, Offset: ({self.offset_x}, {self.offset_y})")
    
    def alternar_fullscreen(self):
        """Alterna entre modo janela e fullscreen"""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            self.tela = pygame.display.set_mode(self.resolucao_nativa, pygame.FULLSCREEN)
        else:
            # Volta para modo janela e maximiza novamente
            self.tela = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
            pygame.time.wait(50)
            
            # Maximizar novamente usando API do Windows
            try:
                import ctypes
                hwnd = pygame.display.get_wm_info()["window"]
                SW_MAXIMIZE = 3
                ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
                pygame.time.wait(100)
            except:
                # Fallback para tamanho manual
                largura_maxima = int(self.resolucao_nativa[0] * 0.95)
                altura_maxima = int(self.resolucao_nativa[1] * 0.9)
                self.tela = pygame.display.set_mode((largura_maxima, altura_maxima), pygame.RESIZABLE)
        
        self.calcular_dimensoes_tela()
        self.player_manager.atualizar_dimensoes(self.tamanho_celula, self.offset_x, self.offset_y)
    
    def redimensionar_janela(self, nova_largura, nova_altura):
        """Lida com redimensionamento da janela"""
        if not self.fullscreen:
            self.tela = pygame.display.set_mode((nova_largura, nova_altura), pygame.RESIZABLE)
            self.calcular_dimensoes_tela()
            self.player_manager.atualizar_dimensoes(self.tamanho_celula, self.offset_x, self.offset_y)

    def reiniciar_busca(self, algoritmo=None):
        """Reinicia a busca e animações com algoritmo especificado"""
        algoritmo_usado = algoritmo or "a_star"  # A* como padrão
        
        print(f"Executando busca com algoritmo: {algoritmo_usado.upper()}...")
        resultado = self.pathfinder.encontrar_caminho(
            self.labirinto, self.posicao_inicial, self.posicao_saida, algoritmo_usado
        )
        self.caminho_final, self.caminhos_explorados, self.estatisticas = resultado
        
        # Verifica se encontrou um caminho
        self.caminho_encontrado = len(self.caminho_final) > 0
        
        # Estados da animação
        self.mostrar_exploracao = False
        self.mostrar_caminho_final = False
        self.mover_player = False
        self.pausado = True
        self.indice_exploracao = 0
        self.indice_caminho = 0
        self.indice_player = 0
        
        # Reset player
        self.player_manager.resetar()
        
        # Imprime estatísticas melhoradas
        if self.estatisticas:
            print(f"Busca concluída em {self.estatisticas['tempo_execucao']:.4f}s")
            print(f"Algoritmo: {self.estatisticas.get('algoritmo', algoritmo_usado)}")
            print(f"Nós visitados: {self.estatisticas['nos_visitados']}")
            
            if self.caminho_encontrado:
                print(f"✓ Caminho encontrado! Tamanho: {self.estatisticas['tamanho_caminho']}")
                print(f"Eficiência: {self.estatisticas['eficiencia']:.2%}")
            else:
                print(f"✗ Nenhum caminho encontrado para a saída!")

    def comparar_algoritmos(self):
        """Compara todos os algoritmos disponíveis"""
        print("\n=== COMPARAÇÃO DE ALGORITMOS ===")
        resultados = self.pathfinder.comparar_algoritmos(
            self.labirinto, self.posicao_inicial, self.posicao_saida
        )
        
        for algoritmo, resultado in resultados.items():
            if "erro" in resultado:
                print(f"{algoritmo.upper()}: ERRO - {resultado['erro']}")
            else:
                print(f"{algoritmo.upper()}:")
                print(f"  Caminho: {resultado['tamanho_caminho']} passos")
                print(f"  Visitados: {resultado['nos_visitados']} nós")
                print(f"  Eficiência: {resultado['eficiencia']:.2%}")
                print(f"  Tempo: {resultado['tempo_execucao']:.4f}s")
        print("=" * 33)

    def redimensionar_imagem(self, imagem, largura, altura):
        return pygame.transform.scale(imagem, (largura, altura))
    
    def desenhar_labirinto(self):
        """Desenha o labirinto base com posicionamento centralizado"""
        for i in range(len(self.labirinto)):
            for j in range(len(self.labirinto[0])):
                x_pixel = self.offset_x + (j * self.tamanho_celula)
                y_pixel = self.offset_y + (i * self.tamanho_celula)
                
                if self.labirinto[i][j] == 0:
                    imagem_redimensionada = self.redimensionar_imagem(
                        imagem_chao, self.tamanho_celula, self.tamanho_celula
                    )
                    self.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
                elif self.labirinto[i][j] == 1:
                    imagem_redimensionada = self.redimensionar_imagem(
                        imagen_arvore, self.tamanho_celula, self.tamanho_celula
                    )
                    self.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
                elif self.labirinto[i][j] == 'e':
                    imagem_redimensionada = self.redimensionar_imagem(
                        imagem_casa, self.tamanho_celula, self.tamanho_celula
                    )
                    self.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
                elif self.labirinto[i][j] == 'm':
                    imagem_redimensionada = self.redimensionar_imagem(
                        imagem_chao, self.tamanho_celula, self.tamanho_celula
                    )
                    self.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
    
    def desenhar_caminhos_explorados(self):
        """Desenha os caminhos explorados com transparência e posicionamento centralizado"""
        for i in range(min(self.indice_exploracao, len(self.caminhos_explorados))):
            x, y = self.caminhos_explorados[i]
            if (x, y) not in self.caminho_final:
                # Criar surface com transparência
                superficie = pygame.Surface((self.tamanho_celula, self.tamanho_celula))
                superficie.set_alpha(128)  # 50% transparente
                
                # Cor diferente se não encontrou caminho
                cor = self.config.COR_EXPLORACAO if self.caminho_encontrado else (255, 180, 180)
                superficie.fill(cor)
                self.tela.blit(superficie, (
                    self.offset_x + (x * self.tamanho_celula),
                    self.offset_y + (y * self.tamanho_celula)
                ))
    
    def desenhar_caminho_final(self):
        """Desenha o caminho final (menor caminho) com posicionamento centralizado"""
        if self.caminho_encontrado:
            for i in range(min(self.indice_caminho, len(self.caminho_final))):
                x, y = self.caminho_final[i]
                pygame.draw.rect(
                    self.tela, self.config.COR_CAMINHO_FINAL,
                    (self.offset_x + (x * self.tamanho_celula),
                     self.offset_y + (y * self.tamanho_celula),
                     self.tamanho_celula, self.tamanho_celula)
                )
    
    def obter_estado_jogo(self):
        """Retorna o estado atual do jogo para a interface"""
        return {
            'caminho_encontrado': self.caminho_encontrado,
            'pausado': self.pausado,
            'mostrar_exploracao': self.mostrar_exploracao,
            'mostrar_caminho_final': self.mostrar_caminho_final,
            'mover_player': self.mover_player,
            'player_finished': self.player_manager.player.finished if self.player_manager.player else False,
            'indice_exploracao': self.indice_exploracao,
            'indice_caminho': self.indice_caminho,
            'indice_player': self.indice_player,
            'caminho_final': self.caminho_final,
            'caminhos_explorados': self.caminhos_explorados,
            'estatisticas': self.estatisticas,
            'tamanho_celula': self.tamanho_celula,
            'offset_x': self.offset_x,
            'offset_y': self.offset_y,
            'altura_labirinto': self.altura_labirinto
        }

    def atualizar_player(self):
        """Move o player pelo caminho final com posicionamento centralizado"""
        if self.indice_player < len(self.caminho_final):
            x, y = self.caminho_final[self.indice_player]
            self.player_manager.mover_para_posicao(x, y)
    
    def processar_eventos(self):
        """Processa todos os eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                self.redimensionar_janela(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.pausado:
                        if self.caminho_encontrado:
                            self.mostrar_exploracao = True
                        else:
                            self.mostrar_exploracao = True
                            self.mostrar_caminho_final = False
                            self.mover_player = False
                        self.pausado = False
                    else:
                        self.pausado = True
                elif event.key == pygame.K_r:
                    self.reiniciar_busca("a_star")  # Usar A* por padrão
                elif event.key == pygame.K_1:
                    print("Usando BFS básico...")
                    self.reiniciar_busca("bfs")
                elif event.key == pygame.K_2:
                    print("Usando BFS otimizado...")
                    self.reiniciar_busca("bfs_otimizado")
                elif event.key == pygame.K_3:
                    print("Usando A* Manhattan...")
                    self.reiniciar_busca("a_star")
                elif event.key == pygame.K_4:
                    print("Usando A* Euclidiano...")
                    self.reiniciar_busca("a_star_euclidiano")
                elif event.key == pygame.K_c:
                    self.comparar_algoritmos()
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_F11:
                    self.alternar_fullscreen()
                elif event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.config.VELOCIDADE_EXPLORACAO = max(1, self.config.VELOCIDADE_EXPLORACAO - 1)
                    self.config.VELOCIDADE_CAMINHO = max(2, self.config.VELOCIDADE_CAMINHO - 2)
                    print(f"Velocidade aumentada: {self.config.VELOCIDADE_EXPLORACAO}")
                elif event.key == pygame.K_MINUS:
                    self.config.VELOCIDADE_EXPLORACAO += 1
                    self.config.VELOCIDADE_CAMINHO += 2
                    print(f"Velocidade diminuída: {self.config.VELOCIDADE_EXPLORACAO}")
        return True
    
    def atualizar_animacoes(self, contador_frames):
        """Atualiza as animações do jogo"""
        if not self.pausado:
            # Fase 1: Mostrar exploração
            if self.mostrar_exploracao and contador_frames % self.config.VELOCIDADE_EXPLORACAO == 0:
                self.indice_exploracao += 1
                if self.indice_exploracao >= len(self.caminhos_explorados):
                    self.mostrar_exploracao = False
                    if self.caminho_encontrado:
                        self.mostrar_caminho_final = True
                    else:
                        self.pausado = True
                    return 0
            
            # Fase 2: Mostrar caminho final
            elif self.mostrar_caminho_final and self.caminho_encontrado and contador_frames % self.config.VELOCIDADE_CAMINHO == 0:
                self.indice_caminho += 1
                if self.indice_caminho >= len(self.caminho_final):
                    self.mostrar_caminho_final = False
                    self.mover_player = True
                    return 0
            
            # Fase 3: Mover player
            elif self.mover_player and self.caminho_encontrado and contador_frames % self.config.VELOCIDADE_PLAYER == 0:
                self.indice_player += 1
                if self.indice_player >= len(self.caminho_final):
                    self.player_manager.player.finished = True
        
        return contador_frames
    
    def executar(self):
        """Loop principal do jogo"""
        running = True
        contador_frames = 0
        
        print("\n=== CONTROLES APRIMORADOS ===")
        print("ESPAÇO: Iniciar/Pausar animação")
        print("R: Reiniciar com A* (padrão)")
        print("1: Usar BFS básico")
        print("2: Usar BFS otimizado") 
        print("3: Usar A* Manhattan")
        print("4: Usar A* Euclidiano")
        print("C: Comparar todos os algoritmos")
        print("F11: Alternar Fullscreen")
        print("ESC: Sair do jogo")
        print("+/-: Ajustar velocidade")
        print("==============================\n")
        
        while running:
            # Processar eventos
            running = self.processar_eventos()
            if not running:
                break
            
            # Atualizar animações
            contador_frames += 1
            contador_frames = self.atualizar_animacoes(contador_frames)
            
            # Desenhar tudo
            self.tela.fill(self.config.COR_FUNDO)
            self.desenhar_labirinto()
            self.desenhar_caminhos_explorados()
            self.desenhar_caminho_final()
            
            # Desenhar player se estiver se movendo
            if self.mover_player and self.caminho_encontrado:
                self.atualizar_player()
                self.player_manager.desenhar(self.tela)
            
            # Desenhar interface
            self.interface.desenhar_ui(self.tela, self.obter_estado_jogo())
            
            pygame.display.flip()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()
        sys.exit()
