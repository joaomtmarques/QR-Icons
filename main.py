import qrcode
import random
import sys
from os import system, path, makedirs
import os
from PIL import Image, ImageDraw

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_downloads_dir():
    return path.join(os.path.expanduser('~'), 'Downloads')

def get_desktop_dir():
    return path.join(os.path.expanduser('~'), 'Desktop')
    
if len(sys.argv) > 1:
    input_data = sys.argv[1]
else:
    clear()
    input_data = input('Url do qr code: ')

qr = qrcode.QRCode(
    version = 4,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 1
)
qr.add_data(input_data)
qr.make(fit = True)

# muda as cores do qr e do background se for necessário (funciona com rgb ou nomes de cores em string)
img = qr.make_image(fill_color = 'black', back_color = 'white').convert('RGB')

clear()
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
            icon_path = input('Path do png: ').strip()
            clear()
            
            icon_path = path.normpath(icon_path)
            icon = Image.open(icon_path).convert('RGBA')
            
            print(f'Imagem \'{icon_path}\' carregada com sucesso.\n')
            break

        except FileNotFoundError as e:
            print(f'Erro: {e}. Por favor, insere um caminho válido.')
        
        except ValueError as e:
            print(f'Erro: {e}. Por favor, escolhe uma imagem no formato correto.')
        
        except OSError as e:
            print(f'Erro ao abrir a imagem: {e}. O arquivo pode estar corrompido ou o path pode estar mal escrito (não colocar entre aspas).')

    #tamanho da imagem
    max_icon_size = qr_width // 4
    icon_ratio = min(max_icon_size / icon.width, max_icon_size / icon.height)
    icon_size = (int(icon.width * icon_ratio), int(icon.height * icon_ratio))
    icon = icon.resize(icon_size, Image.Resampling.LANCZOS)

    #centrar a imagem
    icon_position = (blank_position[0] + (blank_size - icon_size[0]) // 2, 
                     blank_position[1] + (blank_size - icon_size[1]) // 2)
    
    img.paste(icon, icon_position, mask=icon)

while True:
    save_path = input(f'Escolhe o diretório onde queres por o qr code (predefinido é nos Downloads).\nGarante que escreves o path completo (Ex: \'C:\...\' ou \'~\...\'): ').strip()
    path_aceite = True

    if save_path.strip() == '':
        save_path = get_downloads_dir()

    else:
        if not path.isdir(save_path):
            if input(f'O diretório {get_desktop_dir()}\\{save_path} não existe. Queres criá-lo? (Y/N): ').strip().upper() == 'Y':
                clear()
                try:
                    makedirs(save_path)
                    print(f'Diretório {get_desktop_dir()}\\{save_path} criado com sucesso.')
                    path_aceite = True
                except OSError as e:
                    path_aceite = False
                    print(f'Erro ao criar o diretório: {e}.')
            else:
                path_aceite = False
                clear()
    
    if path_aceite == True:
        break

name = [*'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890']
qrcode_name = ''.join(random.choices(name, k = 10)) + '.png'

qrcode_path = path.join(save_path, qrcode_name)
img.save(qrcode_path)

print(f'QR Code foi guardado em {qrcode_path} !!')

system(qrcode_path)