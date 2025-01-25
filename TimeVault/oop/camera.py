import pytesseract
from PIL import Image
import os

# Set up Tesseract path (update this path to the location of your Tesseract executable)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class CameraProcessor:
    @staticmethod
    def extract_text(image_path):
        """
        Extract text and numbers from an image using Tesseract OCR.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: Extracted text.
        """
        if not os.path.exists(image_path):
            return "Error: Image file not found."

        try:
            # Open the image
            image = Image.open(image_path)

            # Perform OCR on the image
            extracted_text = pytesseract.image_to_string(image)

            return extracted_text.strip()  # Return extracted text, remove extra spaces
        except Exception as e:
            return f"Error during text extraction: {str(e)}"
