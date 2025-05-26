import numpy as np
from PIL import Image, ImageEnhance
import random
import os
from datetime import datetime


def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return np.array([r + m, g + m, b + m])


class Bacteria:
    def __init__(self, width, height):
      
        self.cx = random.uniform(0, width)
        self.cy = random.uniform(0, height)

       
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

 
        self.radius_x = random.randint(20, 60)
        self.radius_y = random.randint(20, 60)

        h = random.uniform(0, 360)
        s = random.uniform(0.7, 1.0)
        v = random.uniform(0.7, 1.0)
        self.color = hsv_to_rgb(h, s, v)

        
        self.intensity = random.uniform(0.5, 1.0)
        self.sigma = random.uniform(0.8, 1.5)

        self.width = width
        self.height = height

    def update(self):
    
        self.cx += self.vx
        self.cy += self.vy

        if self.cx < 0:
            self.cx = 0
            self.vx *= -1
        elif self.cx > self.width:
            self.cx = self.width
            self.vx *= -1

        if self.cy < 0:
            self.cy = 0
            self.vy *= -1
        elif self.cy > self.height:
            self.cy = self.height
            self.vy *= -1

    def draw(self, frame):
        yy, xx = np.mgrid[:self.height, :self.width]

        
        distance = (((xx - self.cx) ** 2) / (self.radius_x ** 2) + ((yy - self.cy) ** 2) / (self.radius_y ** 2))
        mask = np.exp(-distance / (2 * self.sigma ** 2))

        frame += mask[:, :, np.newaxis] * self.color * self.intensity


def generate_cyanobacteria_frame(width, height, bacteria_list):
    frame = np.zeros((height, width, 3), dtype=np.float32)
    for b in bacteria_list:
        b.draw(frame)


    noise = np.random.normal(0, 0.02, (height, width, 3))
    frame += noise
    frame = np.clip(frame, 0, 1)
    return (frame * 255).astype(np.uint8)


def generate_cyanobacteria_gif(
    width=600,
    height=600,
    frames=80,            
    num_bacteria=50,      
    output_dir="gif_results"
):
    os.makedirs(output_dir, exist_ok=True)

    bacteria_list = [Bacteria(width, height) for _ in range(num_bacteria)]

    images = []
    for _ in range(frames):
        for b in bacteria_list:
            b.update()

        array = generate_cyanobacteria_frame(width, height, bacteria_list)
        img = Image.fromarray(array)
        img = ImageEnhance.Contrast(img).enhance(1.5)  
        images.append(img)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"cyanobacteria_{timestamp}.gif")
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=120, loop=0)

    print(f"¡Listo! Gif guardado en: {output_path}")


if __name__ == "__main__":
    generate_cyanobacteria_gif()
