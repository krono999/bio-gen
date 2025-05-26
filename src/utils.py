import numpy as np
from PIL import Image, ImageEnhance

def post_process_image(image_path):
    img = Image.open(image_path)
    
    img_array = np.array(img)
    img_array[:, :, 0] = np.sin(img_array[:, :, 0] * 0.1) * 255  
    img_array[:, :, 1] = np.log(img_array[:, :, 1] + 1) * 100     
    img_array[:, :, 2] = img_array[:, :, 2] ** 1.5                
    
    noise = np.random.normal(scale=0.2, size=img_array.shape)
    img_array = np.clip(img_array / 255 + noise * 0.3, 0, 1) * 255
    
    Image.fromarray(img_array.astype(np.uint8)).save(image_path)