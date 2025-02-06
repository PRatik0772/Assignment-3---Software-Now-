import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processor import ImageProcessor

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Processing App")
        self.root.geometry("1200x800")
        self.root.configure(bg="#222222")
        self.processor = ImageProcessor()

        # UI Elements with Styling
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10 )
        
        self.sidebar = tk.Frame(root, bg="#333333", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.container = tk.Frame(root, bg="#007bff")
        self.container.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.load_button = ttk.Button(self.sidebar, text="Load Image", command=self.load_image, style="TButton")
        self.load_button.pack(pady=10, padx=10, fill=tk.X)

        self.crop_button = ttk.Button(self.sidebar, text="Crop Image", command=self.crop_image, style="TButton")
        self.crop_button.pack(pady=10, padx=10, fill=tk.X)

        self.undo_button = ttk.Button(self.sidebar, text="Undo", command=self.undo, style="TButton")
        self.undo_button.pack(pady=10, padx=10, fill=tk.X)

        self.redo_button = ttk.Button(self.sidebar, text="Redo", command=self.redo, style="TButton")
        self.redo_button.pack(pady=10, padx=10, fill=tk.X)

        self.save_button = ttk.Button(self.sidebar, text="Save Image", command=self.save_image, style="TButton")
        self.save_button.pack(pady=10, padx=10, fill=tk.X)

        self.canvas = tk.Canvas(self.container, bg="#111111", bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.slider = ttk.Scale(self.sidebar, from_=10, to=200, orient="horizontal", command=self.resize_image)
        self.slider.set(100)
        self.slider.pack(pady=10, padx=10, fill=tk.X)

        # Image Variables
        self.image = None
        self.tk_image = None
        self.rect_start_x = self.rect_start_y = None
        self.rect_end_x = self.rect_end_y = None
        self.original_image = None
        self.resized_image = None
        self.cropped_image = None
        self.scale_factor = 1.0

        # Undo/Redo Stack
        self.undo_stack = []
        self.redo_stack = []

        # Mouse Bindings
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        # Keyboard Shortcuts
        root.bind("<Control-z>", self.undo)
        root.bind("<Control-y>", self.redo)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.original_image = Image.fromarray(self.image_rgb)
            self.resized_image = self.resize_to_container(self.original_image)
            self.display_image(self.resized_image)
            self.undo_stack.append(self.image_rgb.copy())

    def resize_to_container(self, img):
        container_width = self.container.winfo_width()
        container_height = self.container.winfo_height()
        if container_width == 1 or container_height == 1:
            container_width, container_height = 800, 600

        img_ratio = img.width / img.height
        container_ratio = container_width / container_height

        if img_ratio > container_ratio:
            new_width = container_width
            new_height = int(new_width / img_ratio)
        else:
            new_height = container_height
            new_width = int(new_height * img_ratio)
        
        self.scale_factor = img.width / new_width
        return img.resize((new_width, new_height), Image.LANCZOS)

    def display_image(self, img):
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, anchor="center", image=self.tk_image)
        self.canvas.config(width=img.width, height=img.height)

    def resize_image(self, scale):
        if self.original_image:
            scale_factor = float(scale) / 100
            new_size = (int(self.original_image.width * scale_factor), int(self.original_image.height * scale_factor))
            self.resized_image = self.original_image.resize(new_size, Image.LANCZOS)
            self.display_image(self.resized_image)

    def on_mouse_press(self, event):
        self.rect_start_x, self.rect_start_y = event.x, event.y

    def on_mouse_drag(self, event):
        self.rect_end_x, self.rect_end_y = event.x, event.y
        self.canvas.delete("crop_rect")
        self.canvas.create_rectangle(self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y, outline="red", width=2, tags="crop_rect")

    def on_mouse_release(self, event):
        self.rect_end_x, self.rect_end_y = event.x, event.y
        self.crop_image()

    def crop_image(self):
        if self.image is not None and self.rect_start_x and self.rect_start_y and self.rect_end_x and self.rect_end_y:
            x1 = int(min(self.rect_start_x, self.rect_end_x) * self.scale_factor)
            y1 = int(min(self.rect_start_y, self.rect_end_y) * self.scale_factor)
            x2 = int(max(self.rect_start_x, self.rect_end_x) * self.scale_factor)
            y2 = int(max(self.rect_start_y, self.rect_end_y) * self.scale_factor)
            
            self.image_rgb = self.image_rgb[y1:y2, x1:x2]
            self.display_image(Image.fromarray(self.image_rgb))
            self.undo_stack.append(self.image_rgb.copy())

    def save_image(self):
        if self.image_rgb is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(self.image_rgb, cv2.COLOR_RGB2BGR))

    def undo(self, event=None):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.image_rgb = self.undo_stack[-1]
            self.display_image(Image.fromarray(self.image_rgb))

    def redo(self, event=None):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.image_rgb = self.undo_stack[-1]
            self.display_image(Image.fromarray(self.image_rgb))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
