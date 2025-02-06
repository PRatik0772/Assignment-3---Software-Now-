import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.processed_image = None  # Store the latest processed image

    def crop(self, img, crop_x, crop_y, crop_w, crop_h):
        """Crop image safely within bounds"""
        height, width, _ = img.shape
        crop_x = max(0, min(crop_x, width - 1))
        crop_y = max(0, min(crop_y, height - 1))
        crop_w = max(1, min(crop_w, width - crop_x))
        crop_h = max(1, min(crop_h, height - crop_y))

        cropped = img[crop_y:crop_y + crop_h, crop_x:crop_x + crop_w]
        self.processed_image = cropped
        return cropped

    def resize(self, img, scale_percent):
        """Resize image while maintaining aspect ratio"""
        if scale_percent <= 0:
            return img  # Return original if scale is invalid

        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        self.processed_image = resized
        return resized