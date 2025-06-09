import pygame
import sys
import time
from imgs import *
from rato import *

class ConfiguracaoJogo:
    """Centraliza todas as configurações do jogo"""
    def __init__(self):
        self.FPS = 60
        self.TAMANHO_CELULA = 40
        self.VELOCIDADE_EXPLORACAO = 2  # frames por atualização
        self.VELOCIDADE_CAMINHO = 8
        self.VELOCIDADE_PLAYER = 15
        
        # Cores
        self.COR_EXPLORACAO = (255, 120, 120)
        self.COR_CAMINHO_FINAL = (120, 255, 120)
        self.COR_FUNDO = (40, 40, 40)
        self.COR_TEXTO = (255, 255, 255)
        self.COR_DESTAQUE = (255, 255, 100)

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.finished = False

class JogoLabirinto:
    def __init__(self, arquivo_labirinto):
        pygame.init()
        
        self.config = ConfiguracaoJogo()
        self.clock = pygame.time.Clock()
        
        try:
            # Carrega e valida o labirinto
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
        
        # Configurações da tela com tamanho dinâmico
        self.largura_tela = self.num_colunas * self.config.TAMANHO_CELULA
        self.altura_tela = self.num_linhas * self.config.TAMANHO_CELULA + 100  # Espaço para UI
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption("Ratinho no Labirinto - BFS Pathfinding")
        
        self.largura_celula = self.config.TAMANHO_CELULA
        self.altura_celula = self.config.TAMANHO_CELULA
        
        # Posições importantes
        self.posicao_inicial = encontrar_posicao_inicial(self.labirinto)
        self.posicao_saida = encontrar_posicao_saida(self.labirinto)
        
        # Player com tratamento de erro
        try:
            player_image = pygame.image.load('person/frame-1.png')
            player_image = self.redimensionar_imagem(player_image, self.largura_celula, self.altura_celula)
        except pygame.error:
            # Fallback: usar a imagem do sistema de imgs.py
            player_image = self.redimensionar_imagem(imagen_P_Lado, self.largura_celula, self.altura_celula)
        
        self.player = Player(
            self.posicao_inicial[0] * self.largura_celula,
            self.posicao_inicial[1] * self.altura_celula,
            player_image
        )
        
        self.reiniciar_busca()
        
    def reiniciar_busca(self):
        """Reinicia a busca e animações"""
        print("Executando busca BFS...")
        resultado = bfs_menor_caminho(self.labirinto, self.posicao_inicial, self.posicao_saida)
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
        
        # Imprime estatísticas
        if self.estatisticas:
            print(f"Busca concluída em {self.estatisticas['tempo_execucao']:.4f}s")
            print(f"Nós visitados: {self.estatisticas['nos_visitados']}")
            
            if self.caminho_encontrado:
                print(f"✓ Caminho encontrado! Tamanho: {self.estatisticas['tamanho_caminho']}")
                print(f"Eficiência: {self.estatisticas['eficiencia']:.2%}")
            else:
                print(f"✗ Nenhum caminho encontrado para a saída!")
                print(f"O labirinto pode estar bloqueado ou não ter conexão entre início e fim.")

    def redimensionar_imagem(self, imagem, largura, altura):
        return pygame.transform.scale(imagem, (largura, altura))
    
    def desenhar_labirinto(self):
        """Desenha o labirinto base"""
        for i in range(len(self.labirinto)):
            for j in range(len(self.labirinto[0])):
                x_pixel = j * self.largura_celula
                y_pixel = i * self.altura_celula
                
                if self.labirinto[i][j] == 0:
                    imagem_redimensionada = self.redimensionar_imagem(
                        imagem_chao, self.largura_celula, self.altura_celula
                    )
                    self.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
                elif self.labirinto[i][j] == 1:
                    imagem_redimensionada = self.redimensionar_imagem(
                        imagen_arvore, self.largura_celula, self.altura_celula
                    )
                    self.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
                elif self.labirinto[i][j] == 'e':
                    imagem_redimensionada = self.redimensionar_imagem(
                        imagem_casa, self.largura_celula, self.altura_celula
                    )
                    self.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
                elif self.labirinto[i][j] == 'm':
                    imagem_redimensionada = self.redimensionar_imagem(
                        imagem_chao, self.largura_celula, self.altura_celula
                    )
                    self.tela.blit(imagem_redimensionada, (x_pixel, y_pixel))
    
    def desenhar_caminhos_explorados(self):
        """Desenha os caminhos explorados com transparência"""
        for i in range(min(self.indice_exploracao, len(self.caminhos_explorados))):
            x, y = self.caminhos_explorados[i]
            if (x, y) not in self.caminho_final:
                # Criar surface com transparência
                superficie = pygame.Surface((self.largura_celula, self.altura_celula))
                superficie.set_alpha(128)  # 50% transparente
                
                # Cor diferente se não encontrou caminho
                cor = self.config.COR_EXPLORACAO if self.caminho_encontrado else (255, 180, 180)
                superficie.fill(cor)
                self.tela.blit(superficie, (x * self.largura_celula, y * self.altura_celula))
    
    def desenhar_caminho_final(self):
        """Desenha o caminho final (menor caminho)"""
        if self.caminho_encontrado:
            for i in range(min(self.indice_caminho, len(self.caminho_final))):
                x, y = self.caminho_final[i]
                pygame.draw.rect(
                    self.tela, self.config.COR_CAMINHO_FINAL,
                    (x * self.largura_celula, y * self.altura_celula,
                     self.largura_celula, self.altura_celula)
                )
    
    def desenhar_ui(self):
        """Desenha a interface do usuário"""
        y_offset = self.num_linhas * self.altura_celula + 10
        
        # Fundo da UI
        pygame.draw.rect(self.tela, (20, 20, 20), 
                        (0, y_offset - 5, self.largura_tela, 95))
        
        font_pequena = pygame.font.Font(None, 24)
        font_media = pygame.font.Font(None, 32)
        
        # Status atual
        if not self.caminho_encontrado:
            if self.pausado:
                status = "❌ CAMINHO NÃO ENCONTRADO - Pressione ESPAÇO para ver exploração"
                cor = (255, 100, 100)  # Vermelho para erro
            elif self.mostrar_exploracao:
                status = f"Explorando (sem saída)... {self.indice_exploracao}/{len(self.caminhos_explorados)}"
                cor = (255, 150, 150)
            else:
                status = "❌ Rato não conseguiu encontrar a saída! Pressione R para tentar outro labirinto"
                cor = (255, 100, 100)
        elif self.pausado:
            status = "PAUSADO - Pressione ESPAÇO para iniciar"
            cor = self.config.COR_DESTAQUE
        elif self.mostrar_exploracao:
            status = f"Explorando... {self.indice_exploracao}/{len(self.caminhos_explorados)}"
            cor = self.config.COR_EXPLORACAO
        elif self.mostrar_caminho_final:
            status = f"Menor caminho: {self.indice_caminho}/{len(self.caminho_final)} passos"
            cor = self.config.COR_CAMINHO_FINAL
        elif self.mover_player and not self.player.finished:
            status = f"Rato se movendo... {self.indice_player}/{len(self.caminho_final)}"
            cor = self.config.COR_TEXTO
        elif self.player.finished:
            status = "✓ Saída encontrada! Pressione R para reiniciar"
            cor = self.config.COR_CAMINHO_FINAL
        else:
            status = "Pronto"
            cor = self.config.COR_TEXTO
        
        texto_status = font_media.render(status, True, cor)
        self.tela.blit(texto_status, (10, y_offset))
        
        # Estatísticas
        if self.estatisticas:
            if self.caminho_encontrado:
                stats = [
                    f"Nós visitados: {self.estatisticas['nos_visitados']}",
                    f"Tempo: {self.estatisticas['tempo_execucao']:.3f}s",
                    f"Eficiência: {self.estatisticas['eficiencia']:.1%}"
                ]
            else:
                stats = [
                    f"Nós explorados: {self.estatisticas['nos_visitados']}",
                    f"Tempo: {self.estatisticas['tempo_execucao']:.3f}s",
                    f"Status: Sem caminho disponível"
                ]
            
            for i, stat in enumerate(stats):
                cor_stat = self.config.COR_TEXTO if self.caminho_encontrado else (255, 180, 180)
                texto = font_pequena.render(stat, True, cor_stat)
                self.tela.blit(texto, (10, y_offset + 35 + i * 20))
        
        # Controles
        if not self.caminho_encontrado:
            controles = "Sem saída! Controles: ESPAÇO=Ver busca | R=Novo labirinto | Q=Sair"
        else:
            controles = "Controles: ESPAÇO=Iniciar/Pausar | R=Reiniciar | Q=Sair | +/-=Velocidade"
        
        texto_controles = font_pequena.render(controles, True, (200, 200, 200))
        self.tela.blit(texto_controles, (10, self.altura_tela - 25))

    def atualizar_player(self):
        """Move o player pelo caminho final"""
        if self.indice_player < len(self.caminho_final):
            x, y = self.caminho_final[self.indice_player]
            self.player.rect.x = x * self.largura_celula
            self.player.rect.y = y * self.altura_celula
    
    def executar(self):
        running = True
        contador_frames = 0
        
        print("\n=== CONTROLES ===")
        print("ESPAÇO: Iniciar/Pausar animação")
        print("R: Reiniciar busca")
        print("Q: Sair do jogo")
        print("+/-: Ajustar velocidade")
        print("==================\n")
        
        while running:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.pausado:
                            if self.caminho_encontrado:
                                self.mostrar_exploracao = True
                            else:
                                # Se não encontrou caminho, apenas mostra a exploração
                                self.mostrar_exploracao = True
                                self.mostrar_caminho_final = False
                                self.mover_player = False
                            self.pausado = False
                        else:
                            self.pausado = True
                    elif event.key == pygame.K_r:
                        self.reiniciar_busca()
                    elif event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        # Aumentar velocidade
                        self.config.VELOCIDADE_EXPLORACAO = max(1, self.config.VELOCIDADE_EXPLORACAO - 1)
                        self.config.VELOCIDADE_CAMINHO = max(2, self.config.VELOCIDADE_CAMINHO - 2)
                        print(f"Velocidade aumentada: {self.config.VELOCIDADE_EXPLORACAO}")
                    elif event.key == pygame.K_MINUS:
                        # Diminuir velocidade
                        self.config.VELOCIDADE_EXPLORACAO += 1
                        self.config.VELOCIDADE_CAMINHO += 2
                        print(f"Velocidade diminuída: {self.config.VELOCIDADE_EXPLORACAO}")
            
            if not self.pausado:
                contador_frames += 1
                
                # Fase 1: Mostrar exploração
                if self.mostrar_exploracao and contador_frames % self.config.VELOCIDADE_EXPLORACAO == 0:
                    self.indice_exploracao += 1
                    if self.indice_exploracao >= len(self.caminhos_explorados):
                        self.mostrar_exploracao = False
                        if self.caminho_encontrado:
                            self.mostrar_caminho_final = True
                        else:
                            # Se não encontrou caminho, para aqui e volta ao estado pausado
                            self.pausado = True
                        contador_frames = 0
                
                # Fase 2: Mostrar caminho final (só se encontrou caminho)
                elif self.mostrar_caminho_final and self.caminho_encontrado and contador_frames % self.config.VELOCIDADE_CAMINHO == 0:
                    self.indice_caminho += 1
                    if self.indice_caminho >= len(self.caminho_final):
                        self.mostrar_caminho_final = False
                        self.mover_player = True
                        contador_frames = 0
                
                # Fase 3: Mover player (só se encontrou caminho)
                elif self.mover_player and self.caminho_encontrado and contador_frames % self.config.VELOCIDADE_PLAYER == 0:
                    self.indice_player += 1
                    if self.indice_player >= len(self.caminho_final):
                        self.player.finished = True
            
            # Desenhar tudo
            self.tela.fill(self.config.COR_FUNDO)
            self.desenhar_labirinto()
            self.desenhar_caminhos_explorados()
            self.desenhar_caminho_final()
            
            # Só mostra o player se encontrou caminho e está na fase de movimento
            if self.mover_player and self.caminho_encontrado:
                self.atualizar_player()
                self.tela.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
            
            self.desenhar_ui()
            
            pygame.display.flip()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()
        sys.exit()

# Execução do jogo
if __name__ == "__main__":
    import sys
    
    # Permite escolher o labirinto via argumento
    arquivo_labirinto = sys.argv[1] if len(sys.argv) > 1 else "labirintos/labirinto.txt"
    
    try:
        jogo = JogoLabirinto(arquivo_labirinto)
        jogo.executar()
    except Exception as e:
        print(f"Erro fatal: {e}")
        input("Pressione Enter para sair...")



