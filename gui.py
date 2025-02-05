import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processor import ImageProcessor  # Ensure this file contains accurate cropping logic

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Cropping App")
        self.root.geometry("1000x600")
        self.root.configure(bg="#2C2F33")
        
        self.processor = ImageProcessor()
        
        # Main Frame Layout
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button Frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        self.load_button = ttk.Button(self.button_frame, text="Load Image", command=self.load_image, style="Custom.TButton")
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.crop_button = ttk.Button(self.button_frame, text="Crop Image", command=self.crop_image, style="Custom.TButton")
        self.crop_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(self.button_frame, text="Clear Selection", command=self.clear_crop_selection, style="Custom.TButton")
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Image Display Frame
        self.image_frame = ttk.Frame(self.main_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.image_frame, bg="#FFFFFF", width=400, height=400)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Cropped Image Frame
        self.cropped_frame = ttk.LabelFrame(self.image_frame, text="Cropped Image", labelanchor="n", padding=10)
        self.cropped_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.cropped_canvas = tk.Canvas(self.cropped_frame, bg="#DDDDDD", width=200, height=200)
        self.cropped_canvas.pack()
        
        self.dimensions_label = ttk.Label(self.cropped_frame, text="Dimensions: -", font=("Arial", 10, "bold"))
        self.dimensions_label.pack(pady=5)
        
        # Custom Button Styling
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", font=("Arial", 12, "bold"), padding=8, background="#FFD700", foreground="black")
        
        # Image variables
        self.image = None
        self.tk_image = None
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect_end_x = None
        self.rect_end_y = None
        self.rect = None
        self.cropped_image = None
        
        # Bind Mouse Events for Cropping
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image()
    
    def display_image(self):
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.pil_image = Image.fromarray(self.image_rgb)
        self.pil_image.thumbnail((400, 400))  # Resize for display
        self.tk_image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
    
    def on_mouse_press(self, event):
        self.rect_start_x = event.x
        self.rect_start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
    
    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect_end_x = event.x
        self.rect_end_y = event.y
        self.rect = self.canvas.create_rectangle(self.rect_start_x, self.rect_start_y,
                                                 self.rect_end_x, self.rect_end_y,
                                                 outline="red", width=2)
    
    def on_mouse_release(self, event):
        self.rect_end_x = event.x
        self.rect_end_y = event.y
    
    def crop_image(self):
        if None not in (self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y):
            x1, y1, x2, y2 = sorted([self.rect_start_x, self.rect_end_x]), sorted([self.rect_start_y, self.rect_end_y])
            cropped_image = self.image[y1[0]:y1[1], x1[0]:x1[1]]
            
            if cropped_image.size > 0:
                self.cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
                cropped_pil = Image.fromarray(self.cropped_image)
                cropped_pil.thumbnail((200, 200))  # Adjust size for display
                cropped_tk = ImageTk.PhotoImage(cropped_pil)
                
                self.cropped_canvas.create_image(0, 0, anchor="nw", image=cropped_tk)
                self.cropped_canvas.image = cropped_tk  # Keep reference
                self.dimensions_label.config(text=f"Dimensions: {x2[1]-x1[0]} x {y2[1]-y1[0]}")
    
    def clear_crop_selection(self):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
            self.rect_start_x = self.rect_start_y = self.rect_end_x = self.rect_end_y = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
