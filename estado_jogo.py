"""
Gerenciamento do estado do jogo
"""
from rato import *

class GerenciadorEstadoJogo:
    """Gerencia todo o estado do jogo"""
    
    def __init__(self, jogo):
        self.jogo = jogo
        self.resetar_estado_animacao()
    
    def resetar_estado_animacao(self):
        """Reseta todos os estados de animação"""
        self.jogo.mostrar_exploracao = True
        self.jogo.mostrar_caminho_final = False
        self.jogo.mover_player = False
        self.jogo.pausado = False
        self.jogo.indice_exploracao = 0
        self.jogo.indice_caminho = 0
        self.jogo.indice_player = 0
    
    def executar_busca(self, algoritmo="a_star"):
        """Executa uma busca com o algoritmo especificado"""
        print(f"🔍 Executando busca com algoritmo: {algoritmo.upper()}...")
        
        resultado = self.jogo.pathfinder.encontrar_caminho(
            self.jogo.labirinto, 
            self.jogo.posicao_inicial, 
            self.jogo.posicao_saida, 
            algoritmo
        )
        
        self.jogo.caminho_final, self.jogo.caminhos_explorados, self.jogo.estatisticas = resultado
        self.jogo.caminho_encontrado = len(self.jogo.caminho_final) > 0
        
        self.resetar_estado_animacao()
        self.jogo.player_manager.resetar()
        
        self._imprimir_estatisticas(algoritmo)
    
    def _imprimir_estatisticas(self, algoritmo):
        """Imprime estatísticas da busca"""
        if not self.jogo.estatisticas:
            print("⚠️ Nenhuma estatística disponível")
            return
        
        print(f"✅ Busca concluída em {self.jogo.estatisticas['tempo_execucao']:.4f}s")
        print(f"🧠 Algoritmo: {self.jogo.estatisticas.get('algoritmo', algoritmo)}")
        print(f"🎯 Nós visitados: {self.jogo.estatisticas['nos_visitados']}")
        
        if self.jogo.caminho_encontrado:
            print(f"🎉 Caminho encontrado! Tamanho: {len(self.jogo.caminho_final)} passos")
        else:
            print("❌ Nenhum caminho encontrado para o labirinto atual")
    
    def obter_estado_completo(self):
        """Retorna o estado completo do jogo para a interface"""
        return {
            # Estado da animação
            'mostrar_exploracao': self.jogo.mostrar_exploracao,
            'mostrar_caminho_final': self.jogo.mostrar_caminho_final,
            'mover_player': self.jogo.mover_player,
            'pausado': self.jogo.pausado,
            
            # Progresso
            'indice_exploracao': self.jogo.indice_exploracao,
            'indice_caminho': self.jogo.indice_caminho,
            'indice_player': self.jogo.indice_player,
            
            # Resultados
            'caminho_encontrado': self.jogo.caminho_encontrado,
            'caminho_final': self.jogo.caminho_final,
            'caminhos_explorados': self.jogo.caminhos_explorados,
            'estatisticas': self.jogo.estatisticas,
            
            # Player
            'player_finished': (hasattr(self.jogo.player_manager, 'player') and 
                              self.jogo.player_manager.player and 
                              self.jogo.player_manager.player.finished),
            
            # Dimensões
            'tamanho_celula': self.jogo.tamanho_celula,
            'offset_x': self.jogo.offset_x,
            'offset_y': self.jogo.offset_y,
            'largura_labirinto': self.jogo.largura_labirinto,
            'altura_labirinto': self.jogo.altura_labirinto
        }
    
    def _obter_status_player(self):
        """Retorna o status atual do player"""
        if not hasattr(self.jogo, 'player_manager') or not self.jogo.player_manager:
            return "Player não inicializado"
        
        if not self.jogo.player_manager.player:
            return "Player não criado"
        
        if self.jogo.player_manager.player.finished:
            return "Player chegou ao destino!"
        
        return "Player em movimento"
    
    def comparar_todos_algoritmos(self):
        """Executa comparação entre todos os algoritmos"""
        print("\n🔬 COMPARAÇÃO DE ALGORITMOS")
        print("=" * 50)
        
        resultados = self.jogo.pathfinder.comparar_algoritmos(
            self.jogo.labirinto,
            self.jogo.posicao_inicial,
            self.jogo.posicao_saida
        )
        
        for algoritmo, resultado in resultados.items():
            self._imprimir_resultado_comparacao(algoritmo, resultado)
        
        print("=" * 50)
    
    def _imprimir_resultado_comparacao(self, algoritmo, resultado):
        """Imprime resultado de um algoritmo na comparação"""
        if 'erro' in resultado:
            print(f"❌ {algoritmo.upper()}: {resultado['erro']}")
            return
        
        stats = resultado['estatisticas']
        caminho = resultado['caminho']
        
        print(f"✅ {algoritmo.upper()}:")
        print(f"   ⏱️  Tempo: {stats['tempo_execucao']:.4f}s")
        print(f"   🎯 Nós visitados: {stats['nos_visitados']}")
        print(f"   📏 Tamanho do caminho: {len(caminho) if caminho else 'N/A'}")
        print(f"   🎉 Sucesso: {'Sim' if stats.get('caminho_encontrado', False) else 'Não'}")
