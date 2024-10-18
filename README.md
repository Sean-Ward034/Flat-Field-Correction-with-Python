
# Flat Field Correction Tool

## Overview
The **Flat Field Correction Tool** is a graphical user interface (GUI) application designed to correct raw images using flat-field correction. It helps improve image quality by compensating for variations in illumination and sensor artifacts. This application is particularly useful in scientific and industrial imaging where accuracy is paramount.

The tool allows you to:
- Load raw, dark field, and flat field images.
- Generate synthetic dark and flat field images from a raw image.
- Perform flat field correction on a raw image.
- Zoom in and out of images to inspect details.
- Save the corrected image.

The GUI is built using **Tkinter** (Python's standard GUI library) and relies on **PIL (Pillow)** and **NumPy** for image processing.

## Features
- **Load Images**: Load raw, dark field, and flat field images for processing.
- **Generate Synthetic Images**: Automatically generate dark and flat field images from the loaded raw image.
- **Flat Field Correction**: Perform flat field correction to reduce artifacts and enhance image quality.
- **Image Inspection**: Zoom in and out of raw and corrected images for a detailed view.
- **Save Corrected Image**: Save the processed image in PNG format.

## Prerequisites
Ensure you have the following installed:
- Python 3.6+
- **Tkinter** (included in most Python installations)
- **Pillow** (PIL fork for image handling)
- **NumPy**
- **SciPy** (for Gaussian filtering)

To install the required Python packages, run:

```sh
pip install Pillow numpy scipy
```

## How to Run the Application
1. Clone this repository or download the source code.
2. Open a terminal in the directory containing the code and run:

```sh
python flat_field_correction.py
```

3. The GUI window will open, allowing you to load images and perform corrections.

## Usage Guide
1. **Load Raw Image (R)**: Click the button to load a raw image (grayscale) from your computer.
2. **Load Dark Field Image (D)**: Optionally, load a dark field image.
3. **Load Flat Field Image (F)**: Optionally, load a flat field image.
4. **Generate D and F from R**: If dark and flat images are unavailable, click this button to generate synthetic versions from the raw image.
5. **Perform Flat Field Correction**: Once the required images are loaded or generated, click this button to apply the flat field correction.
6. **Save Corrected Image**: After correction, click this button to save the output image.
7. **Zoom Controls**: Use the Zoom In and Zoom Out buttons to inspect specific areas of the raw and corrected images.

## GUI Overview
- **Control Buttons**: Located at the top, these allow you to load images, perform corrections, and save results.
- **Image Panels**: Display the raw, dark field, flat field, and corrected images side by side.
- **Progress Bar**: Indicates the progress during long operations such as generating synthetic images.

## Flat Field Correction Algorithm
The flat field correction is performed as follows:
1. **Dark Field Subtraction**: Subtract the dark field image from the raw image.
2. **Flat Field Normalization**: Use the flat field image to normalize the illumination across the raw image.
3. **Gain Adjustment**: Calculate a gain matrix to correct uneven illumination.
4. **Final Correction**: Apply the calculated gain to the raw image to produce the corrected output.

The correction ensures that any variations in the sensor or lighting are minimized, resulting in a more accurate representation of the scene.

## Notes
- The images must have the same dimensions for the correction to be performed.
- Dark and flat field images are optional; if not provided, synthetic versions will be generated from the raw image.

## Example
1. Load your raw image by clicking **Load Raw Image (R)**.
2. If dark and flat field images are available, load them using their respective buttons. Otherwise, click **Generate D and F from R**.
3. Click **Perform Flat Field Correction** to process the image.
4. Save the corrected image by clicking **Save Corrected Image**.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create an issue or pull request.

## Contact
For any questions or feedback, please feel free to contact the project maintainer.

## Screenshots
Include screenshots here to give users an idea of how the application looks and functions.

## Acknowledgments
- **Pillow (PIL Fork)**: For easy image manipulation.
- **NumPy and SciPy**: For efficient image calculations and filtering.
