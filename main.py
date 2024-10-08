import qrcode
import random
import sys
from os import system, path, getcwd, makedirs
import os
from PIL import Image, ImageDraw


name = [*'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890']
qrcode_name = ''.join(random.choices(name, k = 10)) + '.png'


if len(sys.argv) > 1:
    input_data = sys.argv[1]
else:
    input_data = input('Url do qr code: ')


qr = qrcode.QRCode(
    version = 4,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 1
)
qr.add_data(input_data)
qr.make(fit = True)


img = qr.make_image(fill_color = 'black', back_color = 'white').convert('RGB')  # mudar cores do qr e do background se for necessário (funciona com rgb ou nomes de cores em string)

if input('Adicionar imagem dentro do qr code? (Caso queiras, responde com \'Y\'): ').strip().upper() == ('Y'):
    qr_width, qr_height = img.size
    
    blank_size = qr_width // 3
    blank_position = ((qr_width - blank_size) // 2, (qr_height - blank_size) // 2)
    
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        [blank_position, (blank_position[0] + blank_size, blank_position[1] + blank_size)],
        fill = 'white'  # trocar cor do background do icon inserido no meio do qr (deve ser igual à cor do background do qr)
    )
    while True:
        try:
            icon_path = input('Path da imagem para por dentro do QR (USAR PNG!!!): ').strip()
            
            icon_path = path.normpath(icon_path)

            if not path.isfile(icon_path):
                raise FileNotFoundError(f'O arquivo \'{icon_path}\' não foi encontrado. Verifique o caminho e tente novamente.')
            
            if not icon_path.lower().endswith('.png'):
                raise ValueError('A imagem deve estar no formato PNG.')
            
            icon = Image.open(icon_path).convert('RGBA')
            
            print(f'Imagem \'{icon_path}\' carregada com sucesso.')
            break

        except FileNotFoundError as e:
            print(f'Erro: {e}. Por favor, insira um caminho válido.')
        
        except ValueError as e:
            print(f'Erro: {e}. Por favor, escolha uma imagem no formato correto.')
        
        except OSError as e:
            print(f'Erro ao abrir a imagem: {e}. O arquivo pode estar corrompido ou não é uma imagem válida.')
    
    max_icon_size = qr_width // 4
    icon_ratio = min(max_icon_size / icon.width, max_icon_size / icon.height)
    icon_size = (int(icon.width * icon_ratio), int(icon.height * icon_ratio))
    icon = icon.resize(icon_size, Image.Resampling.LANCZOS)

    
    icon_position = (blank_position[0] + (blank_size - icon_size[0]) // 2, 
                     blank_position[1] + (blank_size - icon_size[1]) // 2)
    img.paste(icon, icon_position, mask=icon)


while True:
    save_path = input('Escolhe o diretório onde queres por o qr code (clica no Enter para usar o diretório atual): ').strip()
    
    if save_path == '':
        save_path = getcwd()

        save_path = path.normpath(save_path)

    else:
        if os.name == 'nt':
            if not (path.splitdrive(save_path)[0] or '').endswith(':'):
                print('Caminho inválido. Vê se o caminho começa com a letra da unidade, ex: \'C:\'.')

        else:
            if not save_path.startswith('/'):
                print('Caminho inválido. Certifique-se de que o caminho comece com '/'.')

        if not path.isdir(save_path):
            if input(f'O diretório \'{save_path}\' não existe. Queres criá-lo? (Y/N): ').strip().upper() == 'Y':
                try:
                    makedirs(save_path)
                    print(f'Diretório \'{save_path}\' criado com sucesso.')
                except OSError as e:
                    print(f'Erro ao criar o diretório: {e}.')


    qrcode_path = path.join(save_path, qrcode_name)
    break

img.save(qrcode_name)

print(f'QR Code salvo em {qrcode_path}')

system(qrcode_name)