import os

def is_valid_image(file_path):
    """Check if the file is a valid image format"""
    return os.path.splitext(file_path)[-1].lower() in [".jpg", ".jpeg", ".png"]
