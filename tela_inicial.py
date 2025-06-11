import pygame
import os
import ctypes # Adicionado para correção
from typing import List, Optional, Tuple

class TelaInicial:
    """Tela inicial gráfica para seleção de labirintos"""
    
    def __init__(self):
        print("🎮 Inicializando tela inicial...")
        
        try:
            pygame.init()
            print("✅ Pygame inicializado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao inicializar pygame: {e}")
            raise
        
        # Configurar API do Windows para maximização
        self._inicializar_tela_maximizada()
          # Cores modernas com mais contraste e elegância
        self.cores = {
            'fundo': (18, 18, 28),  # Azul escuro mais elegante
            'fundo_secundario': (25, 25, 40),
            'fundo_card': (35, 35, 50),
            'card_hover': (45, 45, 65),
            'card_selecionado': (70, 130, 220),  # Azul mais vibrante
            'card_borda_selecionado': (100, 160, 255),
            'texto': (245, 245, 255),
            'texto_secundario': (180, 180, 200),
            'texto_destaque': (255, 255, 255),
            'botao': (50, 150, 100),  # Verde mais moderno
            'botao_hover': (70, 180, 120),
            'botao_sair': (220, 70, 70),  # Vermelho mais suave
            'botao_sair_hover': (240, 90, 90),
            'destaque': (255, 200, 50),  # Dourado mais suave
            'acento': (120, 200, 255),  # Azul claro para acentos
            'sucesso': (100, 220, 100),
            'aviso': (255, 180, 50),
            'erro': (255, 100, 100),
            'sombra': (0, 0, 0, 60)  # Sombra com transparência
        }
        
        # Fontes adaptativas baseadas no tamanho da tela
        self._configurar_fontes()
          # Estado
        self.labirinto_selecionado = None
        self.botao_hover = None
        self.clock = pygame.time.Clock()
        self._fullscreen_ativo = False  # Iniciar sempre em modo maximizado, não fullscreen
        
        # Carregar labirintos
        print("📁 Carregando labirintos...")
        self.labirintos = self._carregar_labirintos()
        print(f"✅ {len(self.labirintos)} labirintos carregados")
        
        if not self.labirintos:
            print("⚠️ Nenhum labirinto encontrado! Verificar pasta 'labirintos/'")
        
        # Layout
        self._calcular_layout()
        print("✅ Tela inicial configurada com sucesso")
    def _inicializar_tela_maximizada(self):
        """Inicializa a tela em modo maximizado usando API do Windows"""
        import os
        
        print("🖥️ Configurando tela...")
        
        # Configurar variável de ambiente do SDL para centralizar
        os.environ['SDL_WINDOW_CENTERED'] = '1'
        
        try:
            # Obter dimensões da tela (resolução nativa)
            user32 = ctypes.windll.user32
            self.resolucao_nativa = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
            
            # Criar janela redimensionável em tamanho menor primeiro
            self.tela = pygame.display.set_mode((800, 600), pygame.RESIZABLE, vsync=1)
            pygame.display.set_caption("Ratinho no Labirinto - Seleção")
            
            # Aguardar um pouco para a janela se estabilizar
            pygame.time.wait(50)
            
            # Maximizar usando a API do Windows
            hwnd = pygame.display.get_wm_info()["window"]
            SW_MAXIMIZE = 3
            ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
            pygame.time.wait(100)
            
            # Obter o tamanho real após maximizar
            self.largura, self.altura = self.tela.get_size()
            print(f"✅ Tela inicializada e maximizada: {self.largura}x{self.altura}")
            
        except Exception as e:
            print(f"⚠️ Erro ao maximizar ({e}), usando fallback")
            # Fallback - usar 90% da resolução da tela
            try:
                user32 = ctypes.windll.user32
                screen_w, screen_h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
                self.resolucao_nativa = (screen_w, screen_h)
                self.largura = int(screen_w * 0.9)
                self.altura = int(screen_h * 0.9)
            except:
                self.largura, self.altura = 1280, 720
                self.resolucao_nativa = (1920, 1080)
            
            self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE, vsync=1)
            pygame.display.set_caption("Ratinho no Labirinto - Seleção")
            print(f"✅ Configuração básica aplicada: {self.largura}x{self.altura}")

    def _desenhar_gradiente(self, superficie, rect, cor_inicio, cor_fim, vertical=True):
        """Desenha um gradiente em um retângulo"""
        if vertical:
            for y in range(rect.height):
                progresso = y / rect.height
                cor_interpolada = (
                    int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * progresso),
                    int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * progresso),
                    int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * progresso)
                )
                pygame.draw.line(superficie, cor_interpolada, (rect.left, rect.top + y), (rect.right, rect.top + y))
        else:
            for x in range(rect.width):
                progresso = x / rect.width
                cor_interpolada = (
                    int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * progresso),
                    int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * progresso),
                    int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * progresso)
                )
                pygame.draw.line(superficie, cor_interpolada, (rect.left + x, rect.top), (rect.left + x, rect.bottom))
    
    def _desenhar_sombra(self, superficie, rect, offset=5, blur=3, color=(0,0,0), alpha=50):
        """Desenha uma sombra suave atrás de um retângulo."""
        sombra_rect_base = rect.copy()
        
        # Desenhar múltiplas camadas para simular blur
        for i in range(blur):
            current_offset = offset + i // 2 
            sombra_rect = sombra_rect_base.move(current_offset, current_offset)
            
            # A opacidade diminui para as camadas mais externas do blur
            current_alpha = max(0, alpha - i * (alpha // (blur * 2) if blur > 0 else 0) ) # Evitar divisão por zero e ajustar progressão
            
            if current_alpha > 0:
                sombra_surface = pygame.Surface(sombra_rect.size, pygame.SRCALPHA)
                sombra_surface.fill((*color, int(current_alpha))) # Garantir que alpha é int
                superficie.blit(sombra_surface, sombra_rect.topleft)

    def _configurar_fontes(self):
        """Configura fontes adaptativas baseadas no tamanho da tela"""
        # Escalar fontes baseado na largura da tela
        escala = min(self.largura / 1000, self.altura / 700)
        escala = max(0.8, min(escala, 2.0))  # Limitar escala entre 0.8x e 2.0x
        
        self.fonte_titulo = pygame.font.Font(None, int(48 * escala))
        self.fonte_subtitulo = pygame.font.Font(None, int(32 * escala))
        self.fonte_texto = pygame.font.Font(None, int(24 * escala))
        self.fonte_pequena = pygame.font.Font(None, int(20 * escala))

    def _get_cores_card(self, hover: bool, selecionado: bool) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
        """Retorna as cores (fundo_top, fundo_bottom, borda) para um card com base no estado."""
        if selecionado:
            cor_fundo_top = self.cores.get('card_selecionado_top', self.cores.get('card_selecionado', (70, 120, 180)))
            cor_fundo_bottom = self.cores.get('card_selecionado_bottom', (max(0, cor_fundo_top[0] - 20), max(0, cor_fundo_top[1] - 20), max(0, cor_fundo_top[2] - 20)))
            borda_cor = self.cores.get('card_borda_selecionado', self.cores.get('destaque', (100, 180, 255)))
        elif hover:
            cor_fundo_top = self.cores.get('card_hover_top', self.cores.get('card_hover', (60, 80, 110)))
            cor_fundo_bottom = self.cores.get('card_hover_bottom', (max(0, cor_fundo_top[0] - 15), max(0, cor_fundo_top[1] - 15), max(0, cor_fundo_top[2] - 15)))
            borda_cor = self.cores.get('card_borda_hover', self.cores.get('acento', (80, 130, 200)))
        else:
            cor_fundo_top = self.cores.get('fundo_card_top', self.cores.get('fundo_card', (45, 55, 70)))
            cor_fundo_bottom = self.cores.get('fundo_card_bottom', (max(0, cor_fundo_top[0] - 10), max(0, cor_fundo_top[1] - 10), max(0, cor_fundo_top[2] - 10)))
            borda_cor = self.cores.get('card_borda', (60, 70, 90))
        return cor_fundo_top, cor_fundo_bottom, borda_cor

    def _carregar_labirintos(self) -> List[dict]:
        """Carrega informações de todos os labirintos disponíveis"""
        pasta_labirintos = "labirintos"
        labirintos = []
        
        print(f"📂 Verificando pasta: {pasta_labirintos}")
        
        if not os.path.exists(pasta_labirintos):
            print(f"❌ Pasta '{pasta_labirintos}' não encontrada!")
            print(f"📍 Diretório atual: {os.getcwd()}")
            print("📋 Conteúdo do diretório atual:")
            try:
                for item in os.listdir('.'):
                    print(f"   - {item}")
            except:
                print("   Erro ao listar conteúdo")
            return []
        
        print(f"✅ Pasta '{pasta_labirintos}' encontrada")
        
        try:
            arquivos = os.listdir(pasta_labirintos)
            arquivos_txt = [f for f in arquivos if f.endswith('.txt')]
            print(f"📄 Arquivos .txt encontrados: {arquivos_txt}")
            
            for arquivo in sorted(arquivos_txt):
                caminho = os.path.join(pasta_labirintos, arquivo)
                print(f"🔍 Processando: {arquivo}")
                info = self._obter_info_labirinto(caminho)
                if info:
                    labirintos.append(info)
                    print(f"   ✅ {arquivo} - {info['dimensoes']} - {info['dificuldade']}")
                else:
                    print(f"   ❌ Erro ao processar {arquivo}")
                    
        except Exception as e:
            print(f"❌ Erro ao listar arquivos: {e}")
        
        return labirintos
    
    def _obter_info_labirinto(self, caminho: str) -> Optional[dict]:
        """Extrai informações detalhadas de um labirinto"""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                primeira_linha = f.readline().strip()
                
                # Parse das dimensões
                if 'x' in primeira_linha.lower():
                    dimensoes = primeira_linha.replace('x', ' x ').split()
                    if len(dimensoes) >= 3:
                        altura = int(dimensoes[0])
                        largura = int(dimensoes[2])
                    else:
                        return None
                else:
                    return None
                
                # Contar elementos
                total_celulas = altura * largura
                paredes = 0
                caminhos = 0
                
                for _ in range(altura):
                    linha = f.readline().strip()
                    if linha:
                        paredes += linha.count('1')
                        caminhos += linha.count('0')
                
                # Determinar dificuldade
                if total_celulas <= 100:
                    dificuldade = "Fácil"
                    cor_dificuldade = (60, 180, 60)
                elif total_celulas <= 300:
                    dificuldade = "Médio"
                    cor_dificuldade = (255, 165, 0)
                else:
                    dificuldade = "Difícil"
                    cor_dificuldade = (255, 80, 80)
                
                return {
                    'nome': os.path.basename(caminho).replace('.txt', ''),
                    'caminho': caminho,
                    'dimensoes': f"{altura}x{largura}",
                    'altura': altura,
                    'largura': largura,
                    'total_celulas': total_celulas,
                    'paredes': paredes,
                    'caminhos': caminhos,
                    'dificuldade': dificuldade,
                    'cor_dificuldade': cor_dificuldade,
                    'densidade_paredes': paredes / total_celulas if total_celulas > 0 else 0
                }
        except Exception as e:
            print(f"Erro ao ler {caminho}: {e}")
            return None
    
    def _calcular_layout(self):
        """Calcula o layout dos elementos na tela de forma responsiva"""
        # Área do título (proporcional à altura)
        altura_titulo = int(self.altura * 0.17)  # 17% da altura
        self.area_titulo = pygame.Rect(0, 0, self.largura, altura_titulo)
        
        # Área dos cards de labirintos (responsiva)
        margem = max(30, int(self.largura * 0.03))  # 3% da largura como margem mínima
        
        # Calcular quantos cards cabem por linha baseado na largura da tela
        card_largura_min = 280
        cards_por_linha = max(2, min(4, (self.largura - margem * 2) // (card_largura_min + 20)))
        
        # Calcular largura real do card
        espacamento = 20
        largura_disponivel = self.largura - margem * 2 - (cards_por_linha - 1) * espacamento
        card_largura = largura_disponivel // cards_por_linha
        
        # Altura do card proporcional
        card_altura = min(200, int(self.altura * 0.25))  # Máximo 25% da altura
        
        self.cards_labirintos = []
        x_inicio = margem
        y_inicio = altura_titulo + 20
        
        for i, labirinto in enumerate(self.labirintos):
            linha = i // cards_por_linha
            coluna = i % cards_por_linha
            
            x = x_inicio + coluna * (card_largura + espacamento)
            y = y_inicio + linha * (card_altura + 20)
            
            rect = pygame.Rect(x, y, card_largura, card_altura)
            self.cards_labirintos.append((rect, labirinto))
          # Botões (responsivos) - reservar espaço para textos acima e abaixo
        botao_largura = max(180, int(self.largura * 0.15))  # 15% da largura
        botao_altura = max(40, int(self.altura * 0.06))    # 6% da altura
        
        # Reservar espaço para instruções (40px) + botões + controles (30px) + margens
        espaco_necessario = 40 + botao_altura + 30 + 40  # Total: ~150px
        y_botoes = self.altura - espaco_necessario
        
        self.botao_comecar = pygame.Rect(
            self.largura // 2 - botao_largura - 10, y_botoes, 
            botao_largura, botao_altura
        )
        
        self.botao_sair = pygame.Rect(
            self.largura // 2 + 10, y_botoes,
            botao_largura, botao_altura
        )
    def _desenhar_titulo(self):
        """Desenha o título e subtítulo com gradiente"""
        # Fundo do título com gradiente
        self._desenhar_gradiente(self.tela, self.area_titulo, 
                               self.cores['fundo'], self.cores['fundo_secundario'])
        
        # Título principal com sombra
        titulo_texto = "🐭 Ratinho no Labirinto"
        
        # Sombra do título
        titulo_sombra = self.fonte_titulo.render(titulo_texto, True, (0, 0, 0))
        titulo_sombra_rect = titulo_sombra.get_rect(center=(self.largura // 2 + 2, 42))
        self.tela.blit(titulo_sombra, titulo_sombra_rect)
        
        # Título principal
        titulo = self.fonte_titulo.render(titulo_texto, True, self.cores['destaque'])
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 40))
        self.tela.blit(titulo, titulo_rect)
        
        # Subtítulo com cor mais suave
        subtitulo = self.fonte_subtitulo.render("Escolha um labirinto para começar", True, self.cores['texto'])
        subtitulo_rect = subtitulo.get_rect(center=(self.largura // 2, 80))
        self.tela.blit(subtitulo, subtitulo_rect)
          # Linha decorativa com gradiente
        for i in range(3):
            cor_linha = (self.cores['destaque'][0] - i*30, 
                        self.cores['destaque'][1] - i*30, 
                        self.cores['destaque'][2] - i*10)
            pygame.draw.line(self.tela, cor_linha, 
                           (50, 110 + i), (self.largura - 50, 110 + i), 1)
    
    def _desenhar_card_labirinto(self, rect: pygame.Rect, labirinto: dict, hover: bool, selecionado: bool):
        """Desenha um card de labirinto com design moderno"""
        cor_fundo_top, cor_fundo_bottom, borda_cor = self._get_cores_card(hover, selecionado)

        # Sombra do card
        if hover or selecionado:
            self._desenhar_sombra(self.tela, rect, offset=4, blur=5, alpha=100, color=self.cores.get('sombra_forte', (0,0,0)))
        else:
            self._desenhar_sombra(self.tela, rect, offset=2, blur=3, alpha=60, color=self.cores.get('sombra_suave', (0,0,0)))
                
        # Cor do fundo com gradiente
        # Removida a lógica de cores daqui, pois foi movida para _get_cores_card
        # if selecionado:
        #     cor_fundo_top = self.cores['card_selecionado']
        #     cor_fundo_bottom = (cor_fundo_top[0] - 20, cor_fundo_top[1] - 20, cor_fundo_top[2] - 20)
        #     borda_cor = self.cores['card_borda_selecionado']
        # elif hover:
        #     cor_fundo_top = self.cores['card_hover']
        #     cor_fundo_bottom = (cor_fundo_top[0] - 15, cor_fundo_top[1] - 15, cor_fundo_top[2] - 15)
        #     borda_cor = self.cores['acento']
        # else:
        #     cor_fundo_top = self.cores['fundo_card']
        #     cor_fundo_bottom = (cor_fundo_top[0] - 10, cor_fundo_top[1] - 10, cor_fundo_top[2] - 10)
        #     borda_cor = (60, 60, 80)
        
        # Desenhar gradiente de fundo
        self._desenhar_gradiente(self.tela, rect, cor_fundo_top, cor_fundo_bottom)
        
        # Borda com corner radius simulado
        pygame.draw.rect(self.tela, borda_cor, rect, 2, border_radius=12)
        
        # Header do card com ícone
        header_height = 35
        header_rect = pygame.Rect(rect.x, rect.y, rect.width, header_height)
        header_cor = (cor_fundo_top[0] + 15, cor_fundo_top[1] + 15, cor_fundo_top[2] + 15)
        pygame.draw.rect(self.tela, header_cor, header_rect, border_radius=12)
        pygame.draw.rect(self.tela, header_cor, 
                        (rect.x, rect.y + header_height - 12, rect.width, 12))  # Cobrir bordas inferiores
        
        # Ícone do labirinto
        icone = "🏰" if labirinto['total_celulas'] > 500 else "🏠" if labirinto['total_celulas'] > 200 else "🎯"
        icone_surface = self.fonte_texto.render(icone, True, self.cores['destaque'])
        self.tela.blit(icone_surface, (rect.x + 10, rect.y + 8))
        
        # Nome do labirinto no header
        nome = self.fonte_texto.render(labirinto['nome'], True, self.cores['texto_destaque'])
        nome_rect = nome.get_rect(x=rect.x + 40, centery=rect.y + header_height // 2)
        self.tela.blit(nome, nome_rect)
        
        # Dimensões com ícone
        y_pos = rect.y + 50
        dim_icone = self.fonte_pequena.render("📐", True, self.cores['acento'])
        self.tela.blit(dim_icone, (rect.x + 15, y_pos))
        dimensoes = self.fonte_pequena.render(f"{labirinto['dimensoes']}", True, self.cores['texto'])
        self.tela.blit(dimensoes, (rect.x + 35, y_pos))
        
        # Dificuldade com badge colorido
        y_pos += 25
        badge_width = 80
        badge_height = 20
        badge_rect = pygame.Rect(rect.x + 15, y_pos, badge_width, badge_height)
        pygame.draw.rect(self.tela, labirinto['cor_dificuldade'], badge_rect, border_radius=10)
        
        dificuldade_texto = self.fonte_pequena.render(labirinto['dificuldade'], True, (255, 255, 255))
        dificuldade_rect = dificuldade_texto.get_rect(center=badge_rect.center)
        self.tela.blit(dificuldade_texto, dificuldade_rect)
        
        # Células totais
        y_pos += 35
        celulas_icone = self.fonte_pequena.render("🔢", True, self.cores['acento'])
        self.tela.blit(celulas_icone, (rect.x + 15, y_pos))
        total = self.fonte_pequena.render(f"{labirinto['total_celulas']} células", True, self.cores['texto_secundario'])
        self.tela.blit(total, (rect.x + 35, y_pos))
        
        # Barra de densidade melhorada
        y_pos += 30
        barra_largura = rect.width - 30
        barra_altura = 8
        barra_x = rect.x + 15
        barra_y = y_pos
        
        # Fundo da barra com bordas arredondadas
        fundo_barra_cor = self.cores.get('fundo_barra', (25, 25, 35))
        fundo_barra = pygame.Rect(barra_x, barra_y, barra_largura, barra_altura)
        pygame.draw.rect(self.tela, fundo_barra_cor, fundo_barra, border_radius=4)
        
        preenchimento_width = int(barra_largura * labirinto['densidade_paredes'])
        # Definir preenchimento_rect antes do if, mesmo que a largura seja 0, para evitar erros.
        preenchimento_rect = pygame.Rect(barra_x, barra_y, preenchimento_width, barra_altura)
        
        if preenchimento_width > 0:
            cor_barra_inicio = self.cores.get('barra_grad_inicio', (70, 150, 220)) 
            cor_barra_fim = self.cores.get('barra_grad_fim', (30, 100, 180))     
                        
            self._desenhar_gradiente(self.tela, preenchimento_rect, 
                                   cor_barra_inicio, cor_barra_fim, vertical=False)
            # Borda sutil no preenchimento
            borda_preenchimento_cor = (min(255, cor_barra_fim[0]+20), min(255, cor_barra_fim[1]+20), min(255, cor_barra_fim[2]+20))
            pygame.draw.rect(self.tela, borda_preenchimento_cor, preenchimento_rect, 1, border_radius=4)
        
        # Label da densidade
        densidade_texto = f"Complexidade: {labirinto['densidade_paredes']:.0%}"
        densidade = self.fonte_pequena.render(densidade_texto, True, self.cores['texto_secundario'])
        self.tela.blit(densidade, (barra_x, barra_y + 15))
        
        # Recomendação com ícone especial
        if labirinto['total_celulas'] > 200:
            y_pos += 40
            recomendacao_rect = pygame.Rect(rect.x + 10, y_pos, rect.width - 20, 25)
            
            rec_fundo_inicio = self.cores.get('recomendacao_fundo_inicio', (50, 70, 100))
            rec_fundo_fim = self.cores.get('recomendacao_fundo_fim', (30, 50, 80))
            self._desenhar_gradiente(self.tela, recomendacao_rect, rec_fundo_inicio, rec_fundo_fim, vertical=False)
            
            pygame.draw.rect(self.tela, self.cores.get('destaque_secundario', (70, 110, 170)), recomendacao_rect, 1, border_radius=8)
            
            estrela = self.fonte_pequena.render("⭐", True, self.cores.get('estrela_cor', self.cores['destaque']))
            self.tela.blit(estrela, (rect.x + 15, y_pos + (recomendacao_rect.height - estrela.get_height()) // 2))
            
            recomendacao_texto_cor = self.cores.get('texto_recomendacao', self.cores['texto_destaque'])
            recomendacao = self.fonte_pequena.render("Ideal para A*", True, recomendacao_texto_cor)
            self.tela.blit(recomendacao, (rect.x + 35, y_pos + (recomendacao_rect.height - recomendacao.get_height()) // 2))
        
        # Indicador de seleção animado
        if selecionado:
            # Desenhar checkmark no canto superior direito
            check_size = 25
            check_x = rect.right - check_size - 10
            check_y = rect.y + 10
            check_rect = pygame.Rect(check_x, check_y, check_size, check_size)
            
            pygame.draw.circle(self.tela, self.cores['sucesso'], check_rect.center, check_size // 2)
            pygame.draw.circle(self.tela, (255, 255, 255), check_rect.center, check_size // 2, 2)
            
            # Desenhar checkmark
            check_text = self.fonte_pequena.render("✓", True, (255, 255, 255))
            check_text_rect = check_text.get_rect(center=check_rect.center)
            self.tela.blit(check_text, check_text_rect)    
            
    def _desenhar_botao(self, rect: pygame.Rect, texto: str, cor_normal: tuple, cor_hover: tuple, hover: bool, ativo: bool = True):
        """Desenha um botão moderno com gradiente e sombra"""
        # Sombra do botão
        if ativo and hover:
            self._desenhar_sombra(self.tela, rect, offset=4, blur=3)
        elif ativo:
            self._desenhar_sombra(self.tela, rect, offset=2, blur=2)
        
        # Cor base
        if hover and ativo:
            cor_top = cor_hover
            cor_bottom = (max(0, cor_hover[0] - 30), max(0, cor_hover[1] - 30), max(0, cor_hover[2] - 30))
        elif ativo:
            cor_top = cor_normal
            cor_bottom = (max(0, cor_normal[0] - 20), max(0, cor_normal[1] - 20), max(0, cor_normal[2] - 20))
        else:
            cor_top = self.cores.get('botao_inativo_fundo_top', (60, 60, 70))
            cor_bottom = self.cores.get('botao_inativo_fundo_bottom', (40, 40, 50))
        
        # Desenhar gradiente do botão
        self._desenhar_gradiente(self.tela, rect, cor_top, cor_bottom)
        
        # Borda do botão
        borda_cor_rgb = self.cores.get('botao_borda_hover', (255, 255, 255)) if hover and ativo else self.cores.get('botao_borda', (150, 150, 150))
        pygame.draw.rect(self.tela, borda_cor_rgb, rect, 2, border_radius=8)
        
        # Texto do botão com sombra
        cor_texto = self.cores.get('texto_botao', self.cores['texto']) if ativo else self.cores.get('texto_botao_inativo', (120, 120, 120))
        
        # Sombra do texto
        texto_sombra = self.fonte_texto.render(texto, True, (0, 0, 0))
        texto_sombra_rect = texto_sombra.get_rect(center=(rect.centerx + 1, rect.centery + 1))
        self.tela.blit(texto_sombra, texto_sombra_rect)
        
        # Texto principal
        texto_surface = self.fonte_texto.render(texto, True, cor_texto)
        texto_rect = texto_surface.get_rect(center=rect.center)
        self.tela.blit(texto_surface, texto_rect)
    
    def _desenhar_info_algoritmos(self):
        """Desenha informações sobre os algoritmos na lateral de forma responsiva"""
        if not self.labirinto_selecionado: # Não mostrar se nenhum labirinto estiver selecionado
            # Opcional: Desenhar um placeholder ou instrução se nenhum labirinto estiver selecionado
            placeholder_texto = "Selecione um labirinto para ver os algoritmos."
            placeholder_surface = self.fonte_texto.render(placeholder_texto, True, self.cores['texto_secundario'])
            placeholder_rect = placeholder_surface.get_rect(centerx=self.largura - (max(250, int(self.largura * 0.25)) // 2) - 20, 
                                                          y=self.area_titulo.height + 50 + (max(200, int(self.altura * 0.35)) // 2))
            self.tela.blit(placeholder_surface, placeholder_rect)
            return
        
        # Posicionamento responsivo
        info_largura = max(250, int(self.largura * 0.25))  # 25% da largura
        info_altura = max(200, int(self.altura * 0.35))    # 35% da altura
        info_x = self.largura - info_largura - 20
        info_y = self.area_titulo.height + 50
        
        # Verificar se há espaço suficiente na lateral
        if info_x < self.largura * 0.7:  # Se não há espaço, não desenhar
            return
        
        # Fundo da área de informações
        info_rect = pygame.Rect(info_x, info_y, info_largura, info_altura)
        self._desenhar_sombra(self.tela, info_rect, offset=3, blur=4, alpha=80, color=self.cores.get('sombra_media', (0,0,0)))
        pygame.draw.rect(self.tela, self.cores['fundo_card'], info_rect, border_radius=10)
        pygame.draw.rect(self.tela, self.cores['destaque'], info_rect, 2, border_radius=10)
        
        # Título
        titulo = self.fonte_texto.render("🧠 Algoritmos Disponíveis", True, self.cores['destaque'])
        titulo_rect = titulo.get_rect(centerx=info_rect.centerx, y=info_y + 15)
        self.tela.blit(titulo, titulo_rect)
        
        # Lista de algoritmos
        algoritmos = [
            ("1 - BFS Básico", "~15-25% eficiência", (255, 120, 120)),
            ("2 - BFS Otimizado", "~30-50% eficiência", (255, 200, 120)),
            ("3 - A* Manhattan", "~80-95% eficiência ⭐", (120, 255, 120)),
            ("4 - A* Euclidiano", "~85-95% eficiência", (120, 200, 255))
        ]
        
        y_offset = 50
        espacamento_vertical = max(35, info_altura // len(algoritmos) - 20)
        
        for nome, desc, cor in algoritmos:
            if y_offset + 40 > info_altura - 40:  # Verificar se cabe
                break
                
            # Nome do algoritmo
            nome_surface = self.fonte_pequena.render(nome, True, cor)
            self.tela.blit(nome_surface, (info_x + 10, info_y + y_offset))
            
            # Descrição
            desc_surface = self.fonte_pequena.render(desc, True, self.cores['texto_secundario'])
            self.tela.blit(desc_surface, (info_x + 10, info_y + y_offset + 20))
            
            y_offset += espacamento_vertical
        
        # Dica
        if y_offset + 30 <= info_altura:
            dica = "Pressione C no jogo para comparar!"
            dica_surface = self.fonte_pequena.render(dica, True, self.cores['destaque'])
            dica_rect = dica_surface.get_rect(centerx=info_rect.centerx, y=info_y + info_altura - 30)
            self.tela.blit(dica_surface, dica_rect)

    def executar(self) -> Optional[str]:
        """Executa a tela inicial e retorna o caminho do labirinto selecionado"""
        print("🚀 Iniciando loop principal da tela inicial...")
        
        if not self.labirintos:
            print("❌ Nenhum labirinto disponível! Criando labirinto de exemplo...")
            self._criar_labirinto_exemplo()
        
        running = True
        frames = 0
        
        # Desenhar primeira tela
        try:
            self.tela.fill(self.cores['fundo'])
            self._desenhar_titulo()
            pygame.display.flip()
            print("✅ Primeira tela desenhada")
        except Exception as e:
            print(f"❌ Erro ao desenhar primeira tela: {e}")
        
        while running:
            frames += 1
            
            # Debug a cada 60 frames (1 segundo)
            if frames % 60 == 0:
                print(f"🔄 Frame {frames}, labirintos: {len(self.labirintos)}, selecionado: {self.labirinto_selecionado is not None}")
            
            # Eventos
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("👋 Usuário fechou a janela")
                        return None
                    
                    elif event.type == pygame.VIDEORESIZE:
                        print(f"🔄 Janela redimensionada para: {event.w}x{event.h}")
                        # Recalcular layout quando a janela for redimensionada
                        self.largura, self.altura = event.w, event.h
                        self._configurar_fontes()
                        self._calcular_layout()
                    
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Clique esquerdo
                            mouse_pos = event.pos
                            print(f"🖱️ Clique em: {mouse_pos}")
                            
                            # Verificar clique nos cards
                            for i, (rect, labirinto) in enumerate(self.cards_labirintos):
                                if rect.collidepoint(mouse_pos):
                                    self.labirinto_selecionado = labirinto
                                    print(f"✅ Labirinto selecionado: {labirinto['nome']}")
                                    break
                            
                            # Verificar clique nos botões
                            if hasattr(self, 'botao_comecar') and self.botao_comecar.collidepoint(mouse_pos) and self.labirinto_selecionado:
                                print(f"🚀 Iniciando jogo com: {self.labirinto_selecionado['nome']}")
                                return self.labirinto_selecionado['caminho']
                            
                            if hasattr(self, 'botao_sair') and self.botao_sair.collidepoint(mouse_pos):
                                print("👋 Botão sair pressionado")
                                return None
                    
                    elif event.type == pygame.KEYDOWN:
                        print(f"⌨️ Tecla pressionada: {pygame.key.name(event.key)}")
                        
                        if event.key == pygame.K_ESCAPE:
                            print("👋 ESC pressionado")
                            return None
                        elif event.key == pygame.K_RETURN and self.labirinto_selecionado:
                            print(f"🚀 Enter pressionado, iniciando: {self.labirinto_selecionado['nome']}")
                            return self.labirinto_selecionado['caminho']
                        elif event.key == pygame.K_F11:
                            print("🖥️ F11 pressionado - alternando fullscreen")
                            self._alternar_fullscreen()
                        elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                            # Seleção rápida por número
                            indice = event.key - pygame.K_1
                            if indice < len(self.labirintos):
                                self.labirinto_selecionado = self.labirintos[indice]
                                print(f"🔢 Seleção rápida: {self.labirinto_selecionado['nome']}")
                
            except Exception as e:
                print(f"❌ Erro no processamento de eventos: {e}")
            
            # Atualizar hover
            try:
                mouse_pos = pygame.mouse.get_pos()
                self.botao_hover = None
                
                if hasattr(self, 'botao_comecar') and self.botao_comecar.collidepoint(mouse_pos):
                    self.botao_hover = 'comecar'
                elif hasattr(self, 'botao_sair') and self.botao_sair.collidepoint(mouse_pos):
                    self.botao_hover = 'sair'
            except:
                pass
            
            # Desenhar tudo
            try:
                self.tela.fill(self.cores['fundo'])
                
                # Título
                self._desenhar_titulo()
                
                # Cards dos labirintos
                if hasattr(self, 'cards_labirintos'):
                    for rect, labirinto in self.cards_labirintos:
                        hover = rect.collidepoint(mouse_pos) if 'mouse_pos' in locals() else False
                        selecionado = self.labirinto_selecionado == labirinto
                        self._desenhar_card_labirinto(rect, labirinto, hover, selecionado)
                
                # Informações dos algoritmos
                self._desenhar_info_algoritmos()
                
                # Botões
                if hasattr(self, 'botao_comecar') and hasattr(self, 'botao_sair'):
                    comecar_ativo = self.labirinto_selecionado is not None
                    self._desenhar_botao(self.botao_comecar, "🚀 Começar Jogo", 
                                       self.cores['botao'], self.cores['botao_hover'],
                                       self.botao_hover == 'comecar', comecar_ativo)
                    
                    self._desenhar_botao(self.botao_sair, "❌ Sair",
                                       self.cores['botao_sair'], self.cores['botao_sair_hover'],
                                       self.botao_hover == 'sair')
                  # Instruções responsivas - posicionadas acima dos botões
                if not self.labirinto_selecionado:
                    instrucao = "Clique em um labirinto para selecioná-lo"
                    instrucao_surface = self.fonte_texto.render(instrucao, True, self.cores['texto_secundario'])
                    # Posicionar acima dos botões com espaçamento adequado
                    y_instrucao = self.botao_comecar.y - 30 if hasattr(self, 'botao_comecar') else self.altura - 120
                    instrucao_rect = instrucao_surface.get_rect(center=(self.largura // 2, y_instrucao))
                    self.tela.blit(instrucao_surface, instrucao_rect)
                
                # Controles rápidos - posicionados abaixo dos botões
                controles = "Teclas: 1-5 para seleção rápida | Enter=Começar | F11=Fullscreen | Esc=Sair"
                controles_surface = self.fonte_pequena.render(controles, True, self.cores['texto_secundario'])
                # Posicionar abaixo dos botões com margem segura
                y_controles = (self.botao_comecar.bottom + 15) if hasattr(self, 'botao_comecar') else self.altura - 20
                controles_rect = controles_surface.get_rect(center=(self.largura // 2, y_controles))
                self.tela.blit(controles_surface, controles_rect)
                
                pygame.display.flip()
                
            except Exception as e:
                print(f"❌ Erro ao desenhar: {e}")
                # Desenhar tela de erro básica
                self.tela.fill((50, 50, 50))
                error_text = self.fonte_texto.render(f"Erro: {str(e)}", True, (255, 255, 255))
                self.tela.blit(error_text, (50, 50))
                pygame.display.flip()
            
            try:
                self.clock.tick(60)
            except:
                pass
        
        return None
    
    def _alternar_fullscreen(self):
        """Alterna entre modo janela maximizada e fullscreen"""
        self._fullscreen_ativo = not self._fullscreen_ativo
        
        if self._fullscreen_ativo:
            # Ir para fullscreen
            self.tela = pygame.display.set_mode(self.resolucao_nativa, pygame.FULLSCREEN)
            print("🖥️ Modo fullscreen ativado")
        else:
            # Voltar para modo janela maximizada
            self.tela = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
            pygame.time.wait(50)
            
            # Maximizar novamente usando API do Windows
            try:
                hwnd = pygame.display.get_wm_info()["window"]
                SW_MAXIMIZE = 3
                ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
                pygame.time.wait(100)
                print("🖥️ Modo janela maximizada ativado")
            except Exception as e:
                print(f"⚠️ Erro ao maximizar: {e}")
                # Fallback para tamanho manual
                largura_maxima = int(self.resolucao_nativa[0] * 0.9)
                altura_maxima = int(self.resolucao_nativa[1] * 0.9)
                self.tela = pygame.display.set_mode((largura_maxima, altura_maxima), pygame.RESIZABLE)
        
        # Recalcular layout
        self.largura, self.altura = self.tela.get_size()
        self._configurar_fontes()
        self._calcular_layout()

    def _criar_labirinto_exemplo(self):
        """Cria um labirinto de exemplo se nenhum for encontrado"""
        print("🏗️ Criando labirinto de exemplo...")
        
        labirinto_exemplo = {
            'nome': 'Exemplo (Gerado)',
            'caminho': 'exemplo_interno',
            'dimensoes': '10x10',
            'altura': 10,
            'largura': 10,
            'total_celulas': 100,
            'paredes': 60,
            'caminhos': 40,
            'dificuldade': 'Fácil',
            'cor_dificuldade': (60, 180, 60),
            'densidade_paredes': 0.6
        }
        
        self.labirintos = [labirinto_exemplo]
        print("✅ Labirinto de exemplo criado")
