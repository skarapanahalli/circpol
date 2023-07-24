import glob
import os
from enum import Enum
from PIL import Image, ImageEnhance


class FilterType(Enum):
    DECREASE_BRIGHTNESS = 1
    INCREASE_CONTRAST = 2
    INCREASE_BOTH_BRIGHTNESS_AND_CONTRAST = 3

class ImageFilter:
    def __init__(self, image):
        self.image = image

    def increase_brightness(self):
        enhancer = ImageEnhance.Brightness(self.image)
        return enhancer.enhance(1.5)

    def decrease_brightness(self):
        enhancer = ImageEnhance.Brightness(self.image)
        return enhancer.enhance(0.5)

    def increase_contrast(self):
        enhancer = ImageEnhance.Contrast(self.image)
        return enhancer.enhance(1.5)


class ImageProcessor:
    def __init__(self, src_dir, out_dir):
        self.src_dir = src_dir
        self.out_dir = out_dir

    def modify_image(self, image, filter_type):
        image_filter = ImageFilter(image)

        if filter_type == FilterType.DECREASE_BRIGHTNESS:
            return image_filter.decrease_brightness()
        elif filter_type == FilterType.INCREASE_CONTRAST:
            return image_filter.increase_contrast()
        elif filter_type == FilterType.INCREASE_BOTH_BRIGHTNESS_AND_CONTRAST:
            temp_image_filter =  ImageFilter(image_filter.increase_brightness())
            return temp_image_filter.increase_contrast()
        else:
            raise ValueError("Invalid operation")

    def apply_filter(self, filter_type):
        # Get a list of all image file paths in the directory
        image_files = glob.glob(os.path.join(self.src_dir, "*.png"))

        is_exist = os.path.exists(self.out_dir)
        if not is_exist:
            os.makedirs(self.out_dir)

        # Process each image in the directory
        for image_path in image_files:
            # Open the image
            image = Image.open(image_path)
            modified_image = self.modify_image(image, filter_type)
            filename = os.path.basename(image_path)
            modified_path = os.path.join(self.out_dir, filename)
            modified_image.save(modified_path)
            print(f"Modified image saved as: {modified_path}")

if __name__ == "__main__":
    # Specify the directory containing the images that needs to be processed
    source = "D:\\temp\\"

    # Reduce Brightness
    destination = "D:\\temp\\out\\ReduceBrightness\\"
    processor = ImageProcessor(source, destination)
    processor.apply_filter(FilterType.DECREASE_BRIGHTNESS)

    # Increase Contrast
    destination = "D:\\temp\\out\\IncreaseContrast\\"
    processor = ImageProcessor(source, destination)
    processor.apply_filter(FilterType.INCREASE_CONTRAST)

    # Increase both Brightness and Contrast
    destination = "D:\\temp\\out\\IncreasedBothBrightnessAndContrast\\"
    processor = ImageProcessor(source, destination)
    processor.apply_filter(FilterType.INCREASE_BOTH_BRIGHTNESS_AND_CONTRAST)
