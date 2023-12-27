from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import pandas as pd
from books import format_keywords

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

def create_rec(genre, keywords):
        """Makes API request and creates pandas dataframe from results."""
        books = []
        # construct the API URL with the genre and keywords parameters
        url = f"https://openlibrary.org/search.json?subject={genre}+{keywords}"
        # make API request
        response = requests.get(url)

        # check that response was successful
        if response.status_code == 200:
            # extract book information from the response
            book_info = response.json()

            for result in book_info['docs']:
                # exlcude low rated books and checks if number of pages is included with book info
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

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to My Book Recommender'})

@app.route('/recommend', methods=['POST'])
def recommend():
    # get genre and keywords
    data = request.json
    genre = data.get('genre')
    keywords = format_keywords(data.get('keywords'))

    # create rec if user provides input
    if genre and keywords:
        books_df = create_rec(genre, keywords)

        # check if df is empty
        if books_df.empty:
            return jsonify({'error': 'No such books exist, consider writing one :)'}), 404

        recommendation = books_df.sample(n=1).to_dict(orient='records')[0]
        response = jsonify(recommendation)
        response.headers.add('Access-Control-Allow-Origin', '*')  # Allow any origin
        return response

    return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__': 
    app.run(debug=True)