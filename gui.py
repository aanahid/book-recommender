"""book recommender gui"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests
from books import format_keywords

class BookRecommendationApp: 
    def __init__(self, root): 
        self.root = root
        self.root.geometry("630x530")
        self.root.title("Alondra's Book Recommender")
        self.root.configure(background="#F6E8EA")

        # styling
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Century Gothic", 10), foreground="#344966", background="#F6E8EA")
        self.style.configure("TButton", font=("Century Gothic", 10), foreground="#344966", background="#F6E8EA")
        self.style.configure("TEntry", font=("Century Gothic", 11), foreground="#344966")

        # create labels, entries, and buttons
        self.label_welcome = ttk.Label(root, text="Welcome to my book recommender!", font=("Century Gothic", 18, "bold"), foreground="#648767")
        self.label_prompt = ttk.Label(root, text="What genre are you interested in reading? ", style="TLabel")
        self.entry_genre = ttk.Entry(root, style="TEntry")
        self.label_prompt2 = ttk.Label(root, text="Enter keyword(s) that interest you (comma-separated): ", style="TLabel")
        self.entry_keywords = ttk.Entry(root, style="TEntry")
        self.button_recommend = ttk.Button(root, text="Get Recommendation", command=self.get_rec, style="TButton")
        self.button_clear = ttk.Button(root, text="Clear", command=self.clear_all, style="TButton")
        self.label_result = ttk.Label(root, text="", style="TLabel")
        self.label_title = ttk.Label(root, text="", style="TLabel")
        self.label_author = ttk.Label(root, text="", style="TLabel")
        self.label_pages = ttk.Label(root, text="", style="TLabel")
        self.label_subjects = ttk.Label(root, text="", style="TLabel")
        self.label_rating = ttk.Label(root, text="", style="TLabel")

        # configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # place everything in grid
        self.label_welcome.grid(row = 0, column = 0, columnspan = 2, padx=10, pady=10)
        self.label_prompt.grid(row = 1, column = 0, sticky="nsew", padx=10, pady=10)
        self.entry_genre.grid(row = 1, column = 1)
        self.label_prompt2.grid(row = 2, column = 0, sticky="nsew", padx=10, pady=10)
        self.entry_keywords.grid(row = 2, column = 1)
        self.button_recommend.grid(row = 3, column = 1, pady=15)
        self.button_clear.grid(row = 3, column = 0, pady=15)
        self.label_result.grid(row = 4, column = 0, columnspan = 2, padx=20)
        self.label_title.grid(row = 5, column = 0, columnspan = 2, padx=20)
        self.label_author.grid(row = 6, column = 0, columnspan = 2, padx=20)
        self.label_pages.grid(row = 7, column = 0, columnspan = 2, padx=20)
        self.label_subjects.grid(row = 8, column = 0, columnspan = 2, padx=20)
        self.label_rating.grid(row = 9, column = 0, columnspan = 2, padx=20)

    def get_rec(self):
        topic = self.entry_genre.get()
        keywords = format_keywords(self.entry_keywords.get())

        if topic and keywords:
            books_df = self.create_rec(topic, keywords)
            if books_df.empty: 
                self.clear_rec()
                self.label_result.config(text="No such books exists, consider writing one :)")
            else: 
                recommendation = books_df.sample(n=1)
                self.label_result.config(text="Here is your book recommendation: ")
                self.label_title.config(text=f"Title: {recommendation['title'].values[0]}")
                self.label_author.config(text=f"Author: {recommendation['author'].values[0]}")
                self.label_pages.config(text=f"Pages: {recommendation['pages'].values[0]}")
                self.label_subjects.config(text=f"Subjects: {recommendation['subjects'].values[0]}", wraplength = 575)
                rating = str(recommendation['rating'].values[0])
                self.label_rating.config(text=f"Rating: {rating} / 5.0")
        else:
            self.label_result.config(text="Please enter a genre and some keywords for your recommendation.")

    def create_rec(self, genre, keywords):
        books = []
        # construct the API URL with the genre and keywords parameters
        url = f"https://openlibrary.org/search.json?subject={genre}+{keywords}"
        # make API request
        response = requests.get(url)

        # check that response was successful
        if response.status_code == 200:
            # extract book information from the response
            book_info = response.json()

            # loop through results and add books to list
            for result in book_info['docs']:
                # exlcude low rated books and checks if number of pages is included
                if 'ratings_average' in result and result['ratings_average'] >= 2 and 'number_of_pages_median' in result:
                    subjects = ', '.join(result.get('subject', []))
                    book = {
                        'title': result['title'],
                        'author': result['author_name'][0],
                        'pages': result['number_of_pages_median'],
                        'subjects': subjects,
                        'rating': result['ratings_average']
                    }
                    books.append(book)   
        else: 
            print(f"Error: {response.status_code}")

        # creates and returns a pandas data frame from the list of books
        return pd.DataFrame(books)
    
    # clears entry lines and recommendation in labels
    def clear_all(self):
        self.entry_genre.delete(0, tk.END)
        self.entry_keywords.delete(0, tk.END)
        self.label_result.config(text="")
        self.label_title.config(text="")
        self.label_author.config(text="")
        self.label_pages.config(text="")
        self.label_subjects.config(text="")
        self.label_rating.config(text="")

    # clears recommendation in labels
    def clear_rec(self):
        self.label_result.config(text="")
        self.label_title.config(text="")
        self.label_author.config(text="")
        self.label_pages.config(text="")
        self.label_subjects.config(text="")
        self.label_rating.config(text="")


if __name__  == "__main__":
    root = tk.Tk()
    app = BookRecommendationApp(root)
    root.mainloop()