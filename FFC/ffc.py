import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance
import numpy as np
from scipy.ndimage import gaussian_filter

class FlatFieldCorrectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Flat Field Correction")
        master.geometry("1400x800")  # Set window size

        # Initialize images and zoom scale
        self.raw_image = None
        self.dark_image = None
        self.flat_image = None
        self.corrected_image = None
        self.zoom_scale = 1.0

        # Main frame to hold everything
        self.main_frame = tk.Frame(master, padx=10, pady=10)
        self.main_frame.pack(fill='both', expand=True)

        # Create frames for controls and images
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(side='top', fill='x', pady=10)

        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack(side='bottom', fill='both', expand=True)

        # Control Buttons
        # Load Raw Image Button
        self.load_raw_button = tk.Button(self.controls_frame, text="Load Raw Image (R)", command=self.load_raw_image)
        self.load_raw_button.grid(row=0, column=0, padx=5, pady=5)

        # Load Dark Field Image Button
        self.load_dark_button = tk.Button(self.controls_frame, text="Load Dark Field Image (D)", command=self.load_dark_image)
        self.load_dark_button.grid(row=0, column=1, padx=5, pady=5)

        # Load Flat Field Image Button
        self.load_flat_button = tk.Button(self.controls_frame, text="Load Flat Field Image (F)", command=self.load_flat_image)
        self.load_flat_button.grid(row=0, column=2, padx=5, pady=5)

        # Generate Dark and Flat Fields Button
        self.generate_button = tk.Button(self.controls_frame, text="Generate D and F from R", command=self.generate_dark_flat_fields)
        self.generate_button.grid(row=0, column=3, padx=5, pady=5)

        # Perform Flat Field Correction Button
        self.correct_button = tk.Button(self.controls_frame, text="Perform Flat Field Correction", command=self.perform_correction, state='disabled')
        self.correct_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Save Corrected Image Button
        self.save_button = tk.Button(self.controls_frame, text="Save Corrected Image", command=self.save_corrected_image, state='disabled')
        self.save_button.grid(row=1, column=2, columnspan=2, pady=10)

        # Zoom controls
        # Zoom In Button
        self.zoom_in_button = tk.Button(self.controls_frame, text="Zoom In (+)", command=lambda: self.zoom(1.2), state='disabled')
        self.zoom_out_button = tk.Button(self.controls_frame, text="Zoom Out (-)", command=lambda: self.zoom(0.8), state='disabled')
        self.zoom_in_button.grid(row=2, column=0, padx=5, pady=5)
        self.zoom_out_button.grid(row=2, column=1, padx=5, pady=5)

        # Progress bar for long operations
        self.progress = ttk.Progressbar(self.controls_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=2, column=2, columnspan=2, pady=10)

        # Canvas for images
        canvas_width = 300
        canvas_height = 300

        # Create Canvas for each image type
        self.canvas_R = tk.Canvas(self.image_frame, width=canvas_width, height=canvas_height, bg='white', bd=2, relief='sunken')
        self.canvas_D = tk.Canvas(self.image_frame, width=canvas_width, height=canvas_height, bg='white', bd=2, relief='sunken')
        self.canvas_F = tk.Canvas(self.image_frame, width=canvas_width, height=canvas_height, bg='white', bd=2, relief='sunken')
        self.canvas_C = tk.Canvas(self.image_frame, width=canvas_width, height=canvas_height, bg='white', bd=2, relief='sunken')

        # Arrange Canvases in the grid
        self.canvas_R.grid(row=0, column=0, padx=10, pady=10)
        self.canvas_D.grid(row=0, column=1, padx=10, pady=10)
        self.canvas_F.grid(row=0, column=2, padx=10, pady=10)
        self.canvas_C.grid(row=0, column=3, padx=10, pady=10)

        # Labels for images
        tk.Label(self.image_frame, text="Raw Image (R)").grid(row=1, column=0)
        tk.Label(self.image_frame, text="Dark Field (D)").grid(row=1, column=1)
        tk.Label(self.image_frame, text="Flat Field (F)").grid(row=1, column=2)
        tk.Label(self.image_frame, text="Corrected Image (C)").grid(row=1, column=3)

    def load_raw_image(self):
        # Load the raw image from the user's file system
        file_path = filedialog.askopenfilename(title="Select Raw Image (R)")
        if file_path:
            try:
                # Open the image and convert to floating-point format
                self.raw_image_original = Image.open(file_path).convert('F')
                self.raw_image = self.raw_image_original.copy()
                self.display_image(self.raw_image_original, self.canvas_R)
                messagebox.showinfo("Image Loaded", "Raw image loaded successfully.")
                # Enable buttons for further processing
                self.correct_button.config(state='normal')
                self.zoom_in_button.config(state='normal')
                self.zoom_out_button.config(state='normal')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load raw image:\n{e}")

    def load_dark_image(self):
        # Load the dark field image from the user's file system
        file_path = filedialog.askopenfilename(title="Select Dark Field Image (D)")
        if file_path:
            try:
                # Open the image and convert to floating-point format
                self.dark_image = Image.open(file_path).convert('F')
                self.display_image(self.dark_image, self.canvas_D)
                messagebox.showinfo("Image Loaded", "Dark field image loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dark field image:\n{e}")

    def load_flat_image(self):
        # Load the flat field image from the user's file system
        file_path = filedialog.askopenfilename(title="Select Flat Field Image (F)")
        if file_path:
            try:
                # Open the image and convert to floating-point format
                self.flat_image = Image.open(file_path).convert('F')
                self.display_image(self.flat_image, self.canvas_F)
                messagebox.showinfo("Image Loaded", "Flat field image loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load flat field image:\n{e}")

    def generate_dark_flat_fields(self):
        # Generate synthetic dark and flat field images from the raw image
        if self.raw_image_original is None:
            messagebox.showwarning("Missing Image", "Please load the raw image before generating D and F.")
            return

        try:
            self.progress.start()  # Start the progress bar

            # Generate Dark Field (D) by dimming the raw image
            raw_image_L = self.raw_image_original.convert('L')
            enhancer = ImageEnhance.Brightness(raw_image_L)
            dark_image_L = enhancer.enhance(0.25)  # Reduce brightness to simulate a dark field (reduced by 75%)
            self.dark_image = dark_image_L.convert('F')
            self.display_image(dark_image_L, self.canvas_D)

            # Generate Flat Field (F) by creating a uniform image with noise
            flat_brightness_value = 255  # Desired brightness level
            flat_array = np.full_like(np.array(self.raw_image_original), flat_brightness_value)
            noise = np.random.normal(0, 5, flat_array.shape)  # Add Gaussian noise
            flat_array = flat_array + noise
            flat_array = np.clip(flat_array, 0, 255)  # Clip values to valid range
            flat_array_smoothed = gaussian_filter(flat_array, sigma=5)  # Smooth with Gaussian filter

            self.flat_image = Image.fromarray(flat_array_smoothed.astype('float32'))
            self.display_image(self.flat_image, self.canvas_F)
            messagebox.showinfo("Generated", "Dark and Flat field images generated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate dark and flat fields:\n{e}")
        finally:
            self.progress.stop()  # Stop the progress bar

    def perform_correction(self):
        # Perform flat field correction using the loaded or generated images
        if self.raw_image_original is None:
            messagebox.showwarning("Missing Image", "Please load the raw image before performing correction.")
            return

        if self.dark_image is None or self.flat_image is None:
            messagebox.showwarning("Missing Images", "Please load or generate the dark and flat field images.")
            return

        try:
            # Convert images to numpy arrays for processing
            R = np.array(self.raw_image_original)
            D = np.array(self.dark_image)
            F = np.array(self.flat_image)

            # Ensure all images have the same dimensions
            if R.shape != D.shape or R.shape != F.shape:
                messagebox.showerror("Error", "All images must have the same dimensions.")
                return

            # Perform flat field correction calculation
            F_minus_D = F - D
            m = np.mean(F_minus_D)  # Mean of (F - D)
            denominator = F_minus_D.copy()
            denominator[denominator == 0] = np.nan  # Avoid division by zero by using NaN
            G = m / denominator  # Calculate gain
            R_minus_D = R - D  # Subtract dark field from raw image
            C = R_minus_D * G  # Apply gain to corrected image

            # Handle NaN and infinity values in the corrected image
            C = np.nan_to_num(C, nan=0.0, posinf=0.0, neginf=0.0)

            # Normalize corrected image to 8-bit format for display
            C = C - np.nanmin(C)
            if np.nanmax(C) != 0:
                C = C / np.nanmax(C)
            C = (C * 255).astype('uint8')

            # Convert corrected image to PIL format and display
            self.corrected_image = Image.fromarray(C)
            self.display_image(self.corrected_image, self.canvas_C)
            messagebox.showinfo("Correction Complete", "Flat field correction performed successfully.")
            self.save_button.config(state='normal')  # Enable save button
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during correction:\n{e}")

    def save_corrected_image(self):
        # Save the corrected image to the user's file system
        if self.corrected_image is None:
            messagebox.showwarning("No Corrected Image", "No corrected image to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", title="Save Corrected Image")
        if file_path:
            try:
                # Save the corrected image in grayscale format
                self.corrected_image.convert('L').save(file_path)
                messagebox.showinfo("Image Saved", "Corrected image saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save corrected image:\n{e}")

    def display_image(self, image, canvas):
        # Display an image on the given canvas
        canvas_width = int(canvas['width'])
        canvas_height = int(canvas['height'])
        image = image.copy()
        image.thumbnail((canvas_width, canvas_height))  # Resize to fit canvas while maintaining aspect ratio
        photo = ImageTk.PhotoImage(image.convert('L'))
        canvas.image = photo  # Keep reference to avoid garbage collection
        canvas.delete("all")  # Clear previous image
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=photo)  # Display the new image

    def zoom(self, factor):
        # Zoom in or out of the raw and corrected images
        self.zoom_scale *= factor
        if self.zoom_scale < 0.1:
            self.zoom_scale = 0.1  # Set minimum zoom limit
        elif self.zoom_scale > 10:
            self.zoom_scale = 10  # Set maximum zoom limit

        # Apply zoom to raw image if available
        if self.raw_image_original:
            raw_zoomed = self.raw_image_original.resize(
                (int(self.raw_image_original.width * self.zoom_scale),
                 int(self.raw_image_original.height * self.zoom_scale)),
                Image.LANCZOS)
            self.display_image(raw_zoomed, self.canvas_R)

        # Apply zoom to corrected image if available
        if self.corrected_image:
            corrected_zoomed = self.corrected_image.resize(
                (int(self.corrected_image.width * self.zoom_scale),
                 int(self.corrected_image.height * self.zoom_scale)),
                Image.LANCZOS)
            self.display_image(corrected_zoomed, self.canvas_C)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlatFieldCorrectionApp(root)
    root.mainloop()
