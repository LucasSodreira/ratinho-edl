import pygame
import sys
from config import ConfiguracaoJogo
from player import GerenciadorPlayer
from interface import GerenciadorInterface
from rato import *
from pathfinding import GerenciadorPathfinding

# Novos módulos organizados
from eventos import GerenciadorEventos
from animacoes import GerenciadorAnimacoes
from renderizacao import GerenciadorRenderizacao
from estado_jogo import GerenciadorEstadoJogo
from tela import GerenciadorTela

class JogoLabirinto:
    def __init__(self, arquivo_labirinto):
        pygame.init()
        
        # Configurações básicas
        self.config = ConfiguracaoJogo()
        self.clock = pygame.time.Clock()
        
        # Carregar e validar labirinto
        self._carregar_labirinto(arquivo_labirinto)
        
        # Inicializar gerenciadores especializados
        self._inicializar_gerenciadores()
        
        # Configurar tela e componentes visuais
        self.gerenciador_tela.inicializar_tela_maximizada()
        
        self.player_manager = GerenciadorPlayer(
            self.posicao_inicial, self.tamanho_celula, self.offset_x, self.offset_y
        )
          # Executar primeira busca
        self.gerenciador_estado.executar_busca()
    
    def _carregar_labirinto(self, arquivo_labirinto):
        """Carrega e valida o arquivo do labirinto"""
        try:
            self.labirinto = criar_labirinto(arquivo_labirinto)
            validacao = validar_labirinto(self.labirinto)
            
            if not validacao["valido"]:
                raise ValueError(f"Labirinto inválido: {validacao['erro']}")
            
            self.info_labirinto = validacao
            print(f"Labirinto carregado: {validacao['altura']}x{validacao['largura']}")
            
            # Calcular estatísticas do labirinto
            total_celulas = validacao['altura'] * validacao['largura']
            paredes = sum(linha.count(1) for linha in self.labirinto)
            caminhos_livres = sum(linha.count(0) for linha in self.labirinto)
            print(f"Paredes: {paredes}, Caminhos livres: {caminhos_livres}")
            
        except Exception as e:
            print(f"Erro ao carregar labirinto: {e}")
            pygame.quit()
            sys.exit(1)
        
        self.num_linhas = len(self.labirinto)
        self.num_colunas = len(self.labirinto[0])
        
        # Posições importantes
        self.posicao_inicial = encontrar_posicao_inicial(self.labirinto)
        self.posicao_saida = encontrar_posicao_saida(self.labirinto)
    
    def _inicializar_gerenciadores(self):
        """Inicializa todos os gerenciadores especializados"""
        # Gerenciadores principais
        self.interface = GerenciadorInterface(self.config)
        self.pathfinder = GerenciadorPathfinding()
        
        # Gerenciadores organizados
        self.gerenciador_eventos = GerenciadorEventos(self)
        self.gerenciador_animacoes = GerenciadorAnimacoes(self)
        self.gerenciador_renderizacao = GerenciadorRenderizacao(self)
        self.gerenciador_estado = GerenciadorEstadoJogo(self)
        self.gerenciador_tela = GerenciadorTela(self)
    
    # Métodos delegados para manter compatibilidade
    def reiniciar_busca(self, algoritmo="a_star"):
        """Reinicia a busca com algoritmo especificado"""
        self.gerenciador_estado.executar_busca(algoritmo)
    
    def comparar_algoritmos(self):
        """Compara todos os algoritmos disponíveis"""
        self.gerenciador_estado.comparar_todos_algoritmos()
    
    def alternar_fullscreen(self):
        """Alterna entre modo janela e fullscreen"""
        self.gerenciador_tela.alternar_fullscreen()
    
    def redimensionar_janela(self, nova_largura, nova_altura):
        """Lida com redimensionamento da janela"""
        self.gerenciador_tela.redimensionar_janela(nova_largura, nova_altura)
    
    def obter_estado_jogo(self):
        """Retorna o estado atual do jogo para a interface"""
        return self.gerenciador_estado.obter_estado_completo()
    
    # Propriedades para acesso direto aos atributos da tela
    @property
    def fullscreen(self):
        return self.gerenciador_tela.fullscreen
    
    @fullscreen.setter 
    def fullscreen(self, value):
        self.gerenciador_tela.fullscreen = value
    
    def executar(self):
        """Loop principal do jogo"""
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
        
        running = True
        
        while running:
            # Processar eventos
            running = self.gerenciador_eventos.processar_eventos()
            if not running:
                break
            
            # Atualizar animações
            self.gerenciador_animacoes.atualizar()
            
            # Renderizar frame completo
            self.gerenciador_renderizacao.renderizar_frame_completo()
            
            pygame.display.flip()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()
        sys.exit()
