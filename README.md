# Book Recommender

This project provides users with a book recommendation. The program accepts two inputs from the user: a genre they are interested in and some other interesting topics they want to read. Given these inputs, this project utilizes the OpenLibrary Search API and conducts a search using the inputs. The results of the search are all added to a list, and a pandas DataFrame is created from that list of books. The book recommendation is a randomly chosen book stored within the DataFrame.

This project has undergone several iterations to enhance user experience and accessibility. It initially started as a command-line interface (CLI) application, allowing users to provide input and receive book recommendations directly in the terminal. To make this project more user-friendly, the project evolved into a graphical user interface (GUI) application using Tkinter.

Most recently, the latest version of the project has been developed into a web application using React. The React web app offers a dynamic and responsive interface, making it even more convenient for users to explore book recommendations based on their preferences.

## Version 3: Web (React App)

The latest version introduces a web-based user interface created using React. Users can input their preferences through the web interface, and the book recommendation is displayed on the screen. 

To run this version locally: 
1. Run the backend using this command: python app.py
2. Navigate to the src folder: cd frontend/src
3. Start development server: npm start


## Version 2: GUI Application

This version allows users to provide input and get their recommendations from a GUI application made using Tkinter.

To run this version use this command: 
python gui.py

## Version 1: CLI

In this versions users interact with the program by entering commands in the terminal. This is also where their recommendation is printed. 

To run this version use this command: 
python books.py