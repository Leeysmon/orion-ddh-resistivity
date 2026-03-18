"""
Generate Doraemon app icon for Orion-DDH_v1
Run this script once to create the icon.png file
"""

from PIL import Image, ImageDraw

def create_doraemon_icon(size=512):
    """Create a Doraemon head icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size // 2, size // 2
    scale = size / 100
    
    # Blue head circle
    head_r = 45 * scale
    draw.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r], 
                 fill=(0, 153, 230, 255))
    
    # White face
    face_r = 38 * scale
    draw.ellipse([cx - face_r, cy - face_r + 5*scale, cx + face_r, cy + face_r + 5*scale], 
                 fill=(255, 255, 255, 255))
    
    # Eyes (white)
    eye_w, eye_h = 14 * scale, 18 * scale
    eye_y = cy - 8 * scale
    draw.ellipse([cx - 15*scale - eye_w/2, eye_y - eye_h/2, 
                  cx - 15*scale + eye_w/2, eye_y + eye_h/2], 
                 fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=int(1.5*scale))
    draw.ellipse([cx + 15*scale - eye_w/2, eye_y - eye_h/2, 
                  cx + 15*scale + eye_w/2, eye_y + eye_h/2], 
                 fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=int(1.5*scale))
    
    # Pupils
    pupil_r = 5 * scale
    pupil_y = eye_y + 2 * scale
    draw.ellipse([cx - 12*scale - pupil_r, pupil_y - pupil_r*1.3, 
                  cx - 12*scale + pupil_r, pupil_y + pupil_r*1.3], 
                 fill=(0, 0, 0, 255))
    draw.ellipse([cx + 12*scale - pupil_r, pupil_y - pupil_r*1.3, 
                  cx + 12*scale + pupil_r, pupil_y + pupil_r*1.3], 
                 fill=(0, 0, 0, 255))
    
    # Nose (red)
    nose_r = 8 * scale
    nose_y = cy + 5 * scale
    draw.ellipse([cx - nose_r, nose_y - nose_r, cx + nose_r, nose_y + nose_r], 
                 fill=(230, 50, 50, 255))
    
    # Nose line
    draw.line([cx, nose_y + nose_r, cx, cy + 28*scale], fill=(0, 0, 0, 255), width=int(2*scale))
    
    # Mouth (arc)
    mouth_y = cy + 18 * scale
    draw.arc([cx - 25*scale, mouth_y - 15*scale, cx + 25*scale, mouth_y + 15*scale],
             start=20, end=160, fill=(0, 0, 0, 255), width=int(2*scale))
    
    # Whiskers
    whisker_len = 22 * scale
    for i, offset in enumerate([-8, 0, 8]):
        wy = cy + 10*scale + offset*scale
        # Left whiskers
        draw.line([cx - 38*scale, wy - 3*scale*i/2, cx - 38*scale + whisker_len, wy], 
                  fill=(0, 0, 0, 255), width=int(1.5*scale))
        # Right whiskers
        draw.line([cx + 38*scale, wy - 3*scale*i/2, cx + 38*scale - whisker_len, wy], 
                  fill=(0, 0, 0, 255), width=int(1.5*scale))
    
    # Red collar
    collar_h = 8 * scale
    draw.ellipse([cx - 35*scale, cy + 38*scale, cx + 35*scale, cy + 38*scale + collar_h*2], 
                 fill=(230, 50, 50, 255))
    
    # Bell (yellow)
    bell_r = 10 * scale
    bell_y = cy + 42 * scale
    draw.ellipse([cx - bell_r, bell_y - bell_r, cx + bell_r, bell_y + bell_r], 
                 fill=(255, 220, 0, 255), outline=(0, 0, 0, 255), width=int(1*scale))
    
    return img

if __name__ == '__main__':
    # Create icons in different sizes
    icon = create_doraemon_icon(512)
    icon.save('assets/icon.png')
    print("Created assets/icon.png (512x512)")
    
    # Create smaller version for Android
    icon_192 = icon.resize((192, 192), Image.LANCZOS)
    icon_192.save('assets/icon-192.png')
    print("Created assets/icon-192.png (192x192)")
    
    print("\nIcon files created successfully!")
