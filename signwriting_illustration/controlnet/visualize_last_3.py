from pathlib import Path
from PIL import Image

# Directory containing the image files
image_dir = Path("ControlNet/image_log/train")

# Check if the directory exists
if not image_dir.exists():
    raise FileNotFoundError(f"Directory {image_dir} not found.")

# Prefixes to search for
prefixes = ["conditioning", "control", "reconstruction", "samples"]

# Dictionary to hold the last three files of each type
file_dict = {prefix: [] for prefix in prefixes}

# Sorting and selecting files
for prefix in prefixes:
    files = sorted(image_dir.glob(f"{prefix}*.png"), reverse=True)[:3]
    file_dict[prefix] = files

# Check if there are 12 files in total
total_files = sum(len(files) for files in file_dict.values())
if total_files < 12:
    raise ValueError("Not enough files found to create the image grid. Only found {} files.".format(total_files))

print(file_dict)

# Creating the image grid
grid_width, grid_height = 3, 4
img_width, img_height = 2058, 516  # Set the size for each image in the grid
grid = Image.new('RGB', (grid_width * img_width, grid_height * img_height))

# Populating the grid with images
for i, (prefix, files) in enumerate(file_dict.items()):
    for j, file in enumerate(files):
        img = Image.open(file)
        img = img.resize((img_width, img_height))
        grid.paste(img, (j * img_width, i * img_height))

# Show the final grid image
grid.show()
