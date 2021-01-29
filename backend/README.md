# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/categories/<int:category_id>'
GET '/questions'
GET '/questions/<int:category_id>')
POST '/questions'
POST '/questions/search'
DELETE '/questions/<int:question_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Returns: A list of category objects, success value and total number of categories. 

{
"categories":[{"id":1,"type":"Science"},
              {"id":2,"type":"Art"},
              {"id":3,"type":"Geography"},
              {"id":4,"type":"History"},
              {"id":5,"type":"Entertainment"},{"id":6,"type":"Sports"}
             ],
"success":true,
"total_categories":6
}


GET '/categories/<int:category_id>'
- Fetches a list of questions for the given category
- Returns: A list of question objects, success value and total number of questions. 

{
"count":5,
"questions":[
            {"answer":"Escher","category":2,"difficulty":1,"id":16,        "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"},
            {"answer":"Mona Lisa","category":2,"difficulty":3,"id":17,"question":"La Giaconda is better known as what?"}]
"success":true}


GET '/questions'
GET '/questions/?page=2'
- Fetches a list of all questions
- Request Arguments: page
- Returns: A list of question objects, success value, total number of questions, a list of all categories
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1

{
    "categories":[
        {"id":1,"type":"Science"},
        {"id":2,"type":"Art"},
        {"id":3,"type":"Geography"}],
    "questions":[
        {"answer":"Agra","category":3,"difficulty":2,"id":15,"question":"The Taj Mahal is located in which Indian city?"},
        {"answer":"Escher","category":2,"difficulty":1,"id":16,"question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"},
        {"answer":"Mona Lisa","category":2,"difficulty":3,"id":17,"question":"La Giaconda is better known as what?"}],
    "success":true,
    "total_questions":100}


DELETE '/questions/<int:question_id>'
- Deletes the given question if it exists
- Returns: ID of deleted question and success value
{
    "deleted":43,
    "success":true
}
  

POST '/questions'
- Creates a new question using the submitted question, answer, difficulty and category
- Returns: ID of the created question and success value
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/questions -d "{\"question\":\"Question\",\"answer\":\"answer\",\"category\":\"1\",\"difficulty\":\"1\"}"

{
    "created":192,
    "success":true
}  


POST '/questions/search'
- Gets questions based on a search term
- Request Arguments: query
- Returns: A list of question objects, success value and total number of questions based on the search term

curl -X POST http://127.0.0.1:5000/questions/search?query=title

{
    "questions":[{
        "answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
        {"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"}],
    "success":true,
    "total_questions":2
}


GET '/questions/<int:category_id>'
- Fetches a list of questions for the given category
- Returns: A list of question objects, success value, total number of questions, list of all categories and current category

curl http://127.0.0.1:5000/questions/6

{
    "categories":[
        {"id":1,"type":"Science"},
        {"id":2,"type":"Art"},
        {"id":3,"type":"Geography"},
        ],
    "current_category":6,
    "questions":[
        {"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"},
        {"answer":"Uruguay","category":6,"difficulty":4,"id":11,"question":"Which country won the first ever soccer World Cup in 1930?"}],
    "success":true,
    "total_questions":2
}


GET '/questions/play'
- Takes category and previous question parameters and return a random questions within the given category if provided, and that is not one of the previous questions.
- Request Arguments: category, previous
- Returns: A random question objects, success value, total number of questions in the category, list of all categories, current category and ID of previous questions

curl "http://127.0.0.1:5000/questions/play?category=2&previous=21,22"

{
    "categories":[
        {"id":1,"type":"Science"},
        {"id":2,"type":"Art"},
        {"id":3,"type":"Geography"},
        ],
    "current_category":2,
    "previous_questions":"21,22",
    "question":
        {"answer":"Mona Lisa","category":2,"difficulty":3,"id":17,"question":"La Giaconda is better known as what?"},
    "success":true,
    "total_questions":5}


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```