from pathlib import Path
from typing import Union

from PIL import Image, UnidentifiedImageError
from signwriting.visualizer.visualize import signwriting_to_image

SIZE = 256

def signwriting_to_sized_image(fsw: str, output: Union[str, Path], size=256):
    try:
        output_im = signwriting_to_image(fsw)

    except UnidentifiedImageError:
        print(f"Error: {fsw} is not a valid FSW string")
        return None
    
    # resize to fit 256x256
    if output_im.width > size or output_im.height > size:
        scale = size / max(output_im.width, output_im.height)
        output_im = output_im.resize((int(output_im.width * scale), int(output_im.height * scale)), Image.NEAREST)

    # Create a 256x256 RGB image with a white background
    img = Image.new('RGB', (size, size), (255, 255, 255))

    # Calculate the position to paste the image so that it's centered
    x_offset = (size - output_im.width) // 2
    y_offset = (size - output_im.height) // 2
    offset = (x_offset, y_offset)

    # Paste the output_im image onto the white background
    img.paste(output_im, offset, output_im if output_im.mode == 'RGBA' else None)

    img.save(output)
    return img


if __name__ == "__main__":
    FSW = 'AS10020S10028S22b04S22b00S22b04S22b10S22b14S22b10S2fb00' + \
          'M561x534S10028472x500S10020516x469S22b00530x502S22b04515x504' + \
          'S22b04545x504S22b14456x467S22b10472x467S22b10440x467S2fb00493x480'
    signwriting_to_sized_image(FSW, 'test.png')
