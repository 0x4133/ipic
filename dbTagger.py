import sqlite3
import re


def extract_keywords(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())

    # Split the text into individual words
    words = text.split()

    # Remove common stop words (you can customize this list)
    stop_words = ['a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'in', 'on', 'at']
    keywords = [word for word in words if word not in stop_words]

    return keywords


def tag_images_with_keywords():
    # Connect to the SQLite database
    conn = sqlite3.connect("image_notes.db")
    cursor = conn.cursor()

    try:
        # Create a table to store the image tags
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id INTEGER,
                tag TEXT,
                FOREIGN KEY (image_id) REFERENCES image_notes (id)
            )
        """)

        # Retrieve all the image notes from the database
        cursor.execute("SELECT id, text, description FROM image_notes")
        image_notes = cursor.fetchall()

        # Check if any image notes exist
        if len(image_notes) == 0:
            print("No image notes found in the database.")
            return

        # Iterate over each image note
        for image_note in image_notes:
            image_id, text, description = image_note

            # Extract keywords from the text and description
            keywords = extract_keywords(text + ' ' + description)

            # Check if any keywords were extracted
            if len(keywords) == 0:
                print(f"No keywords extracted for image with ID: {image_id}")
                continue

            # Insert the keywords as tags for the image
            for keyword in keywords:
                cursor.execute("INSERT INTO image_tags (image_id, tag) VALUES (?, ?)", (image_id, keyword))

            print(f"Image with ID {image_id} tagged with keywords: {', '.join(keywords)}")

        # Commit the changes to the database
        conn.commit()

        print("Images tagged with keywords successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        conn.close()


# Run the script
tag_images_with_keywords()