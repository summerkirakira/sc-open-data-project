import imageio
from PIL import Image
from pathlib import Path


def convert_dds_to_png(dds_path: Path, png_path: Path):
    image = imageio.imread(dds_path, format='dds')
    pil_image = Image.fromarray(image)
    pil_image.save(png_path, format='png')