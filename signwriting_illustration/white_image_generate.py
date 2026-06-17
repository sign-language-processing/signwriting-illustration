"""
White image generator for conditioning in a ControlNet (Img2Img) pipeline.
"""

from PIL import Image

dimensions = (256, 256)
white_image = Image.new('RGB', dimensions, (255, 255, 255))

path_to_save = 'controlnet_huggingface/validation/white_image.png'
white_image.save(path_to_save)

print(f"Saved white image to: {path_to_save}")