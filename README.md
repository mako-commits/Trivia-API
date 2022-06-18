# API Development and Documentation Final Project

## Trivia App

This project is a Udacity full stack project for API Development and Documentation. The project is a trivia game that allows users do the following:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

### Frontend

#### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

3. **Run Frontend Server**
   The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`.

### Backend

#### Install Dependencies

1. **Python 3.7** - Install the latest version of python for your platform by following instructions in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - It is recommended to set up a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Setting up database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```
set FLASK_APP=flaskr
set FLASK_DEBUG=true
set FLASK_ENVIRONMENT=development
flask run
```

The `FLASK_ENVIRONMENT` flag will detect file changes and restart the server automatically.

## API Reference

[View the API_REFERENCE.md for the API documentation](./API_REFERENCE.md)

## Author

- Mubarak Mustapha

## Acknowledgement

- The Udacity team and mentors
