class ConfiguracaoJogo:
    """Centraliza todas as configurações do jogo"""
    def __init__(self):
        self.FPS = 60
        self.TAMANHO_CELULA_BASE = 40  # Tamanho base da célula
        self.VELOCIDADE_EXPLORACAO = 2  # frames por atualização
        self.VELOCIDADE_CAMINHO = 8
        self.VELOCIDADE_PLAYER = 15
        
        # Cores
        self.COR_EXPLORACAO = (255, 120, 120)
        self.COR_CAMINHO_FINAL = (120, 255, 120)
        self.COR_FUNDO = (40, 40, 40)
        self.COR_TEXTO = (255, 255, 255)
        self.COR_DESTAQUE = (255, 255, 100)
        
        # Configurações de tela
        self.MARGEM_UI = 120  # Espaço reservado para UI
        self.MARGEM_LATERAL = 50  # Margem nas laterais
