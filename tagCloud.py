import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from wordcloud import WordCloud
from collections import Counter
import tkinter as tk

def create_tag_cloud(num_top_tags):
    # Connect to the SQLite database
    conn = sqlite3.connect("image_notes.db")
    cursor = conn.cursor()

    try:
        # Retrieve all the tags from the database
        cursor.execute("SELECT tag FROM image_tags")
        tags = cursor.fetchall()

        if tags:
            # Convert the tags to a list
            tag_list = [tag[0] for tag in tags if tag[0]]

            # Count the frequency of each tag
            tag_counts = Counter(tag_list)

            # Get the top N most frequent tags
            top_tags = [tag for tag, _ in tag_counts.most_common(num_top_tags)]

            # Filter out the top N tags from the tag list
            filtered_tags = [tag for tag in tag_list if tag not in top_tags]

            if filtered_tags:
                # Convert the filtered tags to a string
                tag_string = ' '.join(filtered_tags)

                # Create a WordCloud object
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(tag_string)

                # Clear the previous plot
                plt.clf()

                # Display the tag cloud
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.tight_layout()

                # Redraw the canvas
                canvas.draw()
            else:
                print("No tags found after filtering the top {} tags.".format(num_top_tags))
        else:
            print("No tags found in the database.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close the database connection
        conn.close()

def update_filter():
    num_top_tags = int(filter_entry.get())
    create_tag_cloud(num_top_tags)

# Create the main window
window = tk.Tk()
window.title("Live Tag Cloud")

# Create a frame for the filter input
filter_frame = tk.Frame(window)
filter_frame.pack(pady=10)

filter_label = tk.Label(filter_frame, text="Number of top tags to filter:")
filter_label.pack(side=tk.LEFT)

filter_entry = tk.Entry(filter_frame, width=5)
filter_entry.insert(0, "3")  # Default value
filter_entry.pack(side=tk.LEFT, padx=5)

update_button = tk.Button(filter_frame, text="Update", command=update_filter)
update_button.pack(side=tk.LEFT)

# Create a figure and canvas for the plot
fig = plt.figure(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

# Run the initial tag cloud creation
create_tag_cloud(3)

# Start the Tkinter event loop
window.mainloop()