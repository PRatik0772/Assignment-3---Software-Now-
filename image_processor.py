import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.processed_image = None  

    def crop(self, img, crop_x, crop_y, crop_w, crop_h):
        """Crop image by selecting an area"""
        if img is not None and 0 <= crop_x < img.shape[1] and 0 <= crop_y < img.shape[0]:
            cropped = img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
            self.processed_image = cropped
            return cropped
        return img

    def resize(self, img, scale_percent):
        """Resize the image while maintaining the original dimensions for export"""
        if img is not None:
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
            self.processed_image = resized
            return resized
        return img
