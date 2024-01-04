
import argparse
# import change_methods
import video_check
import os

# Create an argument parser
parser = argparse.ArgumentParser(description='Detecção de Mudanças')

# Add arguments for video path and autoreference
parser.add_argument('--video', type=str, help='Caminho para o arquivo de vídeo')
# parser.add_argument('--autoreference', type=str, help='Utilizar o primeiro video da pasta como referência?')
parser.add_argument('--tolerance', type=int, help='Tolerância para a diferença entre os quadros')
# parser.add_argument('--num_methods', type=int, help='Número de métodos a serem usados entre 1 e 4 (padrao 3)')

# Parse the command line arguments
args = parser.parse_args()

# Prompt the user for video path
args.video = input('Digite o caminho para o arquivo de vídeo: ')

# # Prompt the user for autoreference image path
# args.autoreference = input('Utilizar o primeiro video da pasta como referência?: (s/n) ')
# if args.autoreference == 'sim' or args.autoreference == 's' or args.autoreference == 'y' or args.autoreference == 'yes':
#     args.autoreference = True
#     reference_path = None
# else:
#     args.autoreference = False
#     referencia_path = input('Nome do video presente na pasta para ser utilizado como referencia: ')
#     reference_path = os.path.join(args.video, referencia_path)

# Prompt the user for tolerance
args.tolerance = int(input('Digite a tolerância para a diferença entre os quadros: (de 0 a 100 | padrao 6): '))

# Prompt the user for number of methods
# args.num_methods = int(input('Número de métodos a serem usados entre 1 e 4 (padrao 3): '))

# Call the check_videos function using the arguments
video_path = os.path.abspath(args.video)
# method = video_check.ChangeDetection(video_path, args.autoreference, args.tolerance, args.num_methods, reference_path)
method = video_check.ChangeDetection(video_path, args.tolerance)
method.check_videos()

