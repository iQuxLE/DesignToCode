import base64
from dataclasses import dataclass


@dataclass
class ImageEncoder:
    """
    A utility class for encoding images to Base64.
    """
    # image_path: str

    def encode_base64(self, image_path) -> str:
        """
        Encodes the image at the given path to a Base64 string.

        :return: A Base64 encoded string of the image.
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: The file {image_path} was not found.")
            return None
        except Exception as e:  # Added general exception handling
            print(f"Error: {e}")
            return None
