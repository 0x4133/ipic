import cv2
import pytesseract
from PIL import Image
import os
import sqlite3

# Set the path to the Tesseract executable (macOS)
#pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

def process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to preprocess the image
    threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Extract text from the image using pytesseract
    text = pytesseract.image_to_string(threshold)

    # Provide a small description of the image
    description = "This image contains non-human objects or scenes."

    return text, description

def process_folder(folder_path, conn):
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Iterate over all the files and directories in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # If the item is a directory, recursively process it
        if os.path.isdir(item_path):
            process_folder(item_path, conn)
        # If the item is an image file, process it
        elif item.endswith(".jpg") or item.endswith(".png"):
            # Process the image
            text, description = process_image(item_path)

            # Insert the image notes into the database
            cursor.execute("INSERT INTO image_notes (image_path, text, description) VALUES (?, ?, ?)",
                           (item_path, text, description))

    # Commit the changes to the database
    conn.commit()

# Specify the folder path containing the non-human pictures
folder_path = "/Users/aaron/"

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect("image_notes.db")

# Create a table to store the image notes
conn.execute("""
    CREATE TABLE IF NOT EXISTS image_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        text TEXT,
        description TEXT
    )
""")

# Process the images in the folder recursively
process_folder(folder_path, conn)

# Close the database connection
conn.close()