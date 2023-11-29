import os
import json
import base64
from pathlib import Path
from openai import OpenAI
from tqdm import tqdm

# Define directories
TRAIN_DIR = Path(__file__).parent.parent / "train"
ILLUSTRATIONS_DIR = TRAIN_DIR / "A"
PROMPT_FILE = TRAIN_DIR / "prompt.json"

PROMPT = """
Examine the provided illustration. Determine if it features a person and assertively identify their gender (man, woman).  
If they exist, note their hairstyle and any accessories like hats or glasses. 
If only a hand is shown, state "hand only." 

Should there be arrows, only specify their color (black, orange, blue, etc.). Ignore any other information about the arrows completely, including number, direction, and location. 
If the illustration is colored, describe the exact skin, hair, shirt, and eye colors, as well as the background color. 
Include any watermark text. Do not consider the hand or finger positions that are making sign language gestures, nor the number of people.

Respond with a valid JSON object with the key "caption" containing the direct caption of the illustration. 
For example: {"caption": "An illustration of a woman with long hair wearing glasses, with orange arrows."}
Note that the caption ends with punctuation, and the JSON object is wrapped in curly braces, and is outside a code block.
""".strip()

# Initialize OpenAI client
client = OpenAI()


# Function to encode image to base64
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



# Load already processed images if prompt.json exists
processed_images = set()
if PROMPT_FILE.exists():
    with open(PROMPT_FILE, 'r') as file:
        for line in file:
            data = json.loads(line)
            processed_images.add(Path(data["source"]).name)

# Iterate over images in ILLUSTRATIONS_DIR
for image_name in tqdm(os.listdir(ILLUSTRATIONS_DIR)):
    if image_name in processed_images:
        continue

    print("Processing", image_name)

    image_path = ILLUSTRATIONS_DIR / image_name
    base64_image = encode_image_to_base64(image_path)

    # Call OpenAI GPT-4 for image caption
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        # response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    {"type": "text", "text": PROMPT},
                ],
            }
        ],
        max_tokens=500
    )
    response_text = response.choices[0].message.content
    prompt = json.loads(response_text)["caption"]

    # Save output in prompt.json
    with open(PROMPT_FILE, 'a') as file:
        json.dump({"source": f"B/{image_name}", "target": f"A/{image_name}", "prompt": prompt}, file)
        file.write('\n')

