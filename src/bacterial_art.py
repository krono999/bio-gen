import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
import random
import os
from datetime import datetime


def generate_cyanobacteria_frame(width, height, num_blobs, time):
 
    frame = np.zeros((height, width, 3), dtype=np.float32)

    for _ in range(num_blobs):
        angle = time * random.uniform(0.01, 0.05)
        radius = random.uniform(50, 200)
        cx = int(width / 2 + radius * np.cos(angle + random.random()))
        cy = int(height / 2 + radius * np.sin(angle + random.random()))

        blob_radius = random.randint(30, 80)
        color = np.array([
            random.uniform(0.2, 0.4),  
            random.uniform(0.6, 1.0),  
            random.uniform(0.6, 1.0)   
        ])

        yy, xx = np.mgrid[:height, :width]
        distance = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        mask = np.exp(-(distance ** 2) / (2 * (blob_radius ** 2)))

        frame += mask[:, :, np.newaxis] * color

    noise = np.random.normal(0, 0.02, (height, width, 3))
    frame += noise
    frame = np.clip(frame, 0, 1)

    return (frame * 255).astype(np.uint8)


def generate_cyanobacteria_gif(
    width=600,
    height=600,
    frames=30,
    blobs_per_frame=20,
    output_dir="gif_results"
):
    os.makedirs(output_dir, exist_ok=True)
    images = []

    for t in range(frames):
        array = generate_cyanobacteria_frame(width, height, blobs_per_frame, time=t)
        img = Image.fromarray(array)
        img = ImageEnhance.Contrast(img).enhance(1.2)
        images.append(img)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"cyanobacteria_{timestamp}.gif")
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=100, loop=0)

    print(f"result!!! jeje: {output_path}")


if __name__ == "__main__":
    generate_cyanobacteria_gif()
