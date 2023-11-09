import os

import pdfplumber
from PIL import Image, ImageOps
from tqdm import tqdm

directory = 'illustrations'
pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
for filename in tqdm(sorted(pdf_files)):
    pdf_path = os.path.join(directory, filename)
    png_path = os.path.join(directory, filename[:-len(".pdf")] + ".png")

    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        image_objects = first_page.images
        assert len(image_objects) == 1
        for i, image in enumerate(image_objects):
            image_data = image['stream'].get_data()  # This should already decompress the data
            # If get_data() doesn't decompress, use zlib to decompress
            # image_data = zlib.decompress(image['stream'].read_rawdata())

            # Assuming image is RGB, each component is 8 bits, width and height are known
            width = image['stream']['Width']
            height = image['stream']['Height']
            try:
                img = Image.frombytes('RGB', (width, height), image_data)
            except Exception as e:
                if str(e) == "not enough image data":
                    img = Image.frombytes('L', (width, height), image_data)

            img = ImageOps.grayscale(img)
            img.save(png_path, 'PNG')

