# book-recommender

## Description
This project provides users with a book recommendation. The program accepts two inputs from the user: a genre they are interested in and some other interesting topics they want to read (comma-separated). Given these inputs, this project utilizes the OpenLibrary Search API and conducts a search using the inputs. The results of the search are all added to a list, and a pandas data frame is created from that list of books. The book recommendation is a randomly chosen book from this data frame. 

One version of this works directly in the terminal and asks users to provide their input within the terminal. The other version allows users to provide input and get their recommendations from a GUI application made using Tkinter. 
