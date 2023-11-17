import cProfile
import pstats
from io import StringIO
from main import *  # Substitua isso pelo caminho real do seu módulo e método principal

# Crie um objeto cProfile
profiler = cProfile.Profile()

# Inicie o perfil
profiler.enable()

# Chame a função principal ou execute o bloco de código que você deseja perfilar
find_exit(l, posicao_inicial[0], posicao_inicial[1], [], correct_path, wrong_path)

# Pare o perfil
profiler.disable()

# Salve as estatísticas em um arquivo
stats = StringIO()
sortby = 'cumulative'
ps = pstats.Stats(profiler, stream=stats).sort_stats(sortby)
ps.print_stats()

with open('perfil_resultado.txt', 'w') as f:
    f.write(stats.getvalue())
