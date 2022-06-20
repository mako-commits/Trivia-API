## API Documentation

## Introduction

This API allows you manage a pool of questions and categories for a Trivia game. The API does not require authentication or API key

### Getting Started

    - Base URL: `http://127.0.0.1:5000`

### Errors

- Errors are returned as JSON

#### Status Codes

```
- 404 : "Resource not found"
- 422 : "Unprocessable entity"
- 400 : "Bad Request"
- 405 : "Method Not Allowed"
- 500 : "Internal server error"
```

#### Sample Response

```json
{
  "success": False,
  "error": 404,
  "message": "resource not found"
}
```

### Resource endpoint library

### `GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

#### Sample Response

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### `GET '/questions'`

- Fetches all questions from the database
- Request Argument: query parameter: `page=int` starting from 1
- Returns: a list of questions including pagination (every 10 questions), number of total questions, current category, categories and success status.

#### Sample Response

```json
{
    "categories": {
        "1": " Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "All",
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce then praise in the role of her beloved Lestat?"
        },
        ...
    ],
    "success": true,
    "total_questions": 21
}
```

### `GET '/categories/{category_id}/questions'`

- Get questions based on category
- Request Argument: path parameter: `category_id` of type int
- Returns: Current category, an array of questions within the specific category and the total number of questions within the category

#### Sample Response

```json
{
  "current_category": "Art",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism and a leading exponent of action painting?"
    }
  ],
  "total_questions": 4
}
```

### `DELETE '/questions/{question_id}'`

- DELETE question using a question ID
- Request Argument: Path parameter: `question_id` of type int
- Returns: Success status and id of deleted question if successful

#### Sample Response

```json
{
  "deleted": 5,
  "success": true
}
```

### `POST '/questions'`

- POST a new question, which will require the question and answer text,category, and difficulty score
- Request Argument: None
- Returns: Success status and id of added question

#### Request Body

```json
{
  "question": "What is Micheal Jackson signature move?",
  "answer": "Moon Walk",
  "category": 5,
  "difficulty": 4
}
```

#### Sample Response

```json
{
    "added": 1,
    "success": True
}
```

### `POST '/questions'`[SEARCH]

- Performs a search of questions from the database based on a search term
- Request Argument: None
- Returns: Current category of question,list of question related to search term, success status and total number of questions

#### Request Body

```json
{
  "searchTerm": "Tom"
}
```

#### Sample Response

```json
{
  "current_category": "All",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination in 1996?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### `POST '/quizzes'`

- Performs a search of questions from the database based on a search term
- Request Argument: None
- Returns: One question at a time randomly chosen from across all category or from a particular category.

#### Request Body

```json
{
  "previous_questions": [2],
  "quiz_category": { "type": "History", "id": "4" }
}
```

#### Sample Response

```json
{
  "question": {
    "answer": "Muhammad Ali",
    "category": 4,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
  },
  "success": true
}
```
