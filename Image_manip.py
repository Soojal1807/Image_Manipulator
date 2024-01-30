import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import numpy as np

class ImageManipulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Manipulator")  # Name of App
        self.root.geometry("720x720")  # Window Size

        # Image variables
        self.image_path = None
        self.image_original = None
        self.image_display = None

        # Brightness & contrast variables
        self.brightness_var = tk.DoubleVar()
        self.brightness_var.set(1.0)
        self.contrast_var = tk.DoubleVar()
        self.contrast_var.set(1.0)

        # GUI Parts
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        self.brightness_slider = tk.Scale(root, label="Brightness", from_=0.1, to=2.0, resolution=0.1,
                                          variable=self.brightness_var, orient=tk.HORIZONTAL, command=self.update_display)
        self.brightness_slider.pack(pady=10)

        self.contrast_slider = tk.Scale(root, label="Contrast", from_=0.1, to=2.0, resolution=0.1,
                                        variable=self.contrast_var, orient=tk.HORIZONTAL, command=self.update_display)
        self.contrast_slider.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.image_original = Image.open(file_path)  # Button To Load Image with selector to only select above formats.
            self.update_display()

    def update_display(self, *args):
        if self.image_original:
            # Apply brightness and contrast using NumPy
            enhanced_image = np.array(self.image_original)

            # Adjust brightness
            enhanced_image = np.clip(enhanced_image * self.brightness_var.get(), 0, 255)

            # Adjust contrast
            enhanced_image = np.clip((enhanced_image - 127.5) * self.contrast_var.get() + 127.5, 0, 255)

            enhanced_image = Image.fromarray(enhanced_image.astype('uint8'))

            # Resize image for display
            enhanced_image.thumbnail((720, 720))
            self.image_display = ImageTk.PhotoImage(enhanced_image)

            # Display the image
            if hasattr(self, "image_label"):
                self.image_label.configure(image=self.image_display)
            else:
                self.image_label = tk.Label(self.root, image=self.image_display)  # root is used to reference parent widget.
                self.image_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageManipulator(root)
    root.mainloop()
