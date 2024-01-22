import imageio
from PIL import Image
from pathlib import Path
from loguru import logger
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def convert_dds_to_png(dds_path: Path, png_path: Path):
    try:
        image = imageio.imread(dds_path, format='dds')
        pil_image = Image.fromarray(image)
        pil_image.save(png_path, format='png')
    except Exception as e:
        logger.error(f"Failed to convert {dds_path} to {png_path}: {e}")