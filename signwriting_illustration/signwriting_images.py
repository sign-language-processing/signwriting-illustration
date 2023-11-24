import os
import subprocess
import tempfile
from pathlib import Path
from typing import Union

from PIL import Image

TMPDIR = os.getenv('TMPDIR', '/tmp')
REPO_URL = 'https://github.com/sutton-signwriting/font-db.git'
REPO_DIR = os.path.join(TMPDIR, 'font-db')


def clone_repo_if_needed():
    if not os.path.exists(REPO_DIR):
        print(f"Cloning repository into {REPO_DIR}...")
        subprocess.run(["git", "clone", REPO_URL, REPO_DIR], check=True)

    # check if node_modules exists
    if not os.path.exists(os.path.join(REPO_DIR, 'node_modules')):
        print("Installing dependencies...")
        subprocess.run(["npm", "install"], cwd=REPO_DIR, check=True)


def signwriting_to_image(fsw: str, output: Union[str, Path], size=512):
    clone_repo_if_needed()

    temp_output = tempfile.NamedTemporaryFile(suffix='.png').name
    cmd = f'node {REPO_DIR}/fsw/fsw-sign-png "{fsw}" {temp_output}'
    subprocess.run(cmd, shell=True, check=True)

    output_im = Image.open(temp_output)  # this is RGBA

    # Create a 512x512 RGB image with a white background
    im = Image.new('RGB', (size, size), (255, 255, 255))

    # Calculate the position to paste the image so that it's centered
    x = (size - output_im.width) // 2
    y = (size - output_im.height) // 2

    # Paste the output_im image onto the white background
    im.paste(output_im, (x, y), output_im)

    im.save(output)
    return im


if __name__ == "__main__":
    fsw = 'AS10020S10028S22b04S22b00S22b04S22b10S22b14S22b10S2fb00M561x534S10028472x500S10020516x469S22b00530x502S22b04515x504S22b04545x504S22b14456x467S22b10472x467S22b10440x467S2fb00493x480'
    signwriting_to_image(fsw, 'test.png')
