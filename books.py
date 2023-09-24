"""book recommender (from a lot of books) within the terminal"""

import pandas as pd
import requests

# global variables
user: str = ""
min_rating = 1.5
SMILEY: str = "\U0000263A"

# helper function definitions
def greet() -> None:
    """Greets player and gets user's name."""
    
    print("Welcome to my book recommender!")
    
    global user
    user = input("Before we start, what is your name? ")
    print(f"Nice to meet you, {user}. Let's get started! {SMILEY}")

def asking() -> tuple[str, str]: 
    """Asks the user about the type of book they are interested in."""
    
    genre = input(f"What genre are you interested in reading, {user}? ")
    keywords = input("Enter keyword(s) that interest you (comma-separated): ")

    # format keywords for api request if there is more than one
    keywords = format_keywords(keywords)
    return genre, keywords

def format_keywords(input: str) -> str:
    """Formats keywords for url search."""
    
    if "," in input: 
        words = input.split(",");
        formatted = "+".join(words)
        return formatted
    else: 
        return input

def create_df(genre: str, keywords: str) -> pd: 
    """Creates pandas data frame of books from url API call."""
    
    books = []

    # construct the API URL with the genre and keywords parameters and make API request
    url = f"https://openlibrary.org/search.json?subject={genre}+{keywords}"
    response = requests.get(url)
    
    # check that response was successful
    if response.status_code == 200:
        # extract book information from the response
        book_info = response.json()
    
        # loop through results and add books to list
        for result in book_info['docs']:
            # exlcude low rated books
            if 'ratings_average' in result and result['ratings_average'] >= min_rating:
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

    # Create a pandas data frame from the list of books
    books_df = pd.DataFrame(books)
    return books_df

def recommendation(books_df: pd) -> None: 
    """Prints info of random book from data frame"""
    
    random_book = books_df.sample(n=1)

    # Access the random book information
    title = random_book['title'].values[0]
    author = random_book['author'].values[0]
    pages = random_book['pages'].values[0]
    subjects = random_book['subjects'].values[0]
    rating = random_book['rating'].values[0]

    # Print the random book information
    print("Here is your recommendation...")
    print(title + " by " + author)
    print("Pages:", pages)
    print("Subjects:", subjects)
    print("Rating out of 5.0:", rating)    

# main function
def main() -> None: 
    """Entrypoint of program."""
    greet()
    genre, keywords = asking()

    books_df = create_df(genre, keywords)
    
    # checks if data frame is empty
    if books_df.empty: 
        print(f"No such books exists, consider writing one. {SMILEY}")
        return 
    
    # gets and prints recommendation
    recommendation(books_df)
    print(f"Hope you enjoy your recommendation, {user}. Have a nice day! {SMILEY}")

if __name__ == "__main__":
    main()