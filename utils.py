"""
Utilitários gerais para o projeto
"""
import os
import sys

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    try:
        import pygame
        print("✅ Pygame disponível")
        return True
    except ImportError:
        print("❌ Pygame não encontrado. Instale com: pip install pygame")
        return False

def obter_info_sistema():
    """Retorna informações do sistema"""
    return {
        'python_version': sys.version,
        'platform': sys.platform,
        'working_directory': os.getcwd()
    }

def criar_diretorio_se_nao_existir(caminho):
    """Cria um diretório se ele não existir"""
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print(f"📁 Diretório criado: {caminho}")

def listar_arquivos_por_extensao(diretorio, extensao):
    """Lista todos os arquivos com uma extensão específica em um diretório"""
    if not os.path.exists(diretorio):
        return []
    
    return [f for f in os.listdir(diretorio) if f.endswith(extensao)]

def debug_print(mensagem, ativo=True):
    """Print de debug que pode ser desabilitado"""
    if ativo:
        print(f"🔍 DEBUG: {mensagem}")
