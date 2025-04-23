from PIL import Image, ImageDraw
import os

def create_pokeball_icon(size=256):
    # Crear una imagen con fondo transparente
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Dimensiones
    center = size // 2
    radius = size // 2 - 2
    band_height = size // 8
    
    # Dibujar la mitad superior (roja)
    draw.ellipse([(0, 0), (size-1, size-1)], fill=(228, 44, 44, 255))
    
    # Dibujar la mitad inferior (blanca)
    draw.rectangle([(0, center), (size-1, size-1)], fill=(255, 255, 255, 255))
    
    # Dibujar la banda negra del medio
    draw.rectangle([(0, center - band_height//2), 
                   (size-1, center + band_height//2)], 
                  fill=(0, 0, 0, 255))
    
    # Dibujar el círculo central
    outer_button_radius = size // 6
    inner_button_radius = size // 8
    draw.ellipse([(center - outer_button_radius, center - outer_button_radius),
                  (center + outer_button_radius, center + outer_button_radius)],
                 fill=(0, 0, 0, 255))
    draw.ellipse([(center - inner_button_radius, center - inner_button_radius),
                  (center + inner_button_radius, center + inner_button_radius)],
                 fill=(255, 255, 255, 255))
    
    return image

def save_icon_files():
    # Crear el directorio assets si no existe
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Crear iconos en diferentes tamaños
    sizes = [16, 32, 48, 64, 128, 256]
    icons = []
    
    for size in sizes:
        icon = create_pokeball_icon(size)
        icons.append(icon)
    
    # Guardar como .ico (Windows)
    icons[0].save('assets/icon.ico', format='ICO', sizes=[(s,s) for s in sizes], 
                 append_images=icons[1:])
    
    # Guardar también como PNG para otros usos
    icons[-1].save('assets/icon.png', format='PNG')

if __name__ == '__main__':
    save_icon_files() 