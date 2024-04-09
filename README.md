# Image Tagging and Tag Cloud Visualization

This project is a Python script that processes images in a specified folder, extracts text from the images using optical character recognition (OCR), and generates tags based on the extracted text. The tags are then stored in a SQLite database. Additionally, the project provides a live tag cloud visualization that excludes the top N most frequent tags, where N is adjustable by the user.

## Features

- Recursively processes images in a specified folder and its subfolders
- Extracts text from images using the Tesseract OCR engine
- Generates tags based on the extracted text
- Stores the image paths, extracted text, and tags in a SQLite database
- Provides a live tag cloud visualization using the WordCloud library
- Allows the user to adjust the number of top tags to filter out from the tag cloud

## Requirements

- Python 3.x
- OpenCV (cv2)
- pytesseract
- Pillow (PIL)
- matplotlib
- wordcloud
- tkinter

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/image-tagging-project.git
   ```

2. Install the required dependencies:
   ```
   pip install opencv-python pytesseract Pillow matplotlib wordcloud
   ```

3. Install Tesseract OCR:
   - For Windows: Download the Tesseract OCR installer from the official website and install it.
   - For macOS: Install Tesseract OCR using Homebrew by running `brew install tesseract`.
   - For Linux: Install Tesseract OCR using your package manager, e.g., `sudo apt-get install tesseract-ocr`.

## Usage

1. Set the `folder_path` variable in the script to the path of the folder containing the images you want to process.

2. Run the script:
   ```
   python image_tagging.py
   ```

3. The script will process the images, extract text, generate tags, and store the information in the SQLite database.

4. A Tkinter window will open, displaying the live tag cloud visualization.

5. Use the entry field and update button to adjust the number of top tags to filter out from the tag cloud.

6. The tag cloud will be updated dynamically based on the user's input.

## Database Schema

The SQLite database used in this project has the following schema:

- `image_notes` table:
  - `id` (INTEGER): Primary key for the table
  - `image_path` (TEXT): Path of the processed image
  - `text` (TEXT): Extracted text from the image
  - `description` (TEXT): Description of the image (currently set to a default value)

- `image_tags` table:
  - `id` (INTEGER): Primary key for the table
  - `image_id` (INTEGER): Foreign key referencing the `id` column in the `image_notes` table
  - `tag` (TEXT): Generated tag for the image

## Customization

- You can modify the `process_image` function to customize the image processing and text extraction logic.
- The `create_tag_cloud` function can be adjusted to change the appearance and styling of the tag cloud visualization.
- The GUI layout and components can be customized in the Tkinter section of the script.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- The Tesseract OCR engine is developed by Google and used for text extraction in this project.
- The WordCloud library is used for generating the tag cloud visualization.

Feel free to contribute to this project by submitting pull requests or reporting issues on the GitHub repository.
Add to Conversation