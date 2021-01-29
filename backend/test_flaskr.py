import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "trivia_test"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_name = "trivia"
        self.database_path = 'postgres://postgres:admin@localhost:5432/trivia'
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Q24',
            'answer': 'Q24',
            'category': 1,
            'difficulty': 1
        }
        self.wrong_category = {
            'question': 'Q24',
            'answer': 'Q24',
            'category': 0,
            'difficulty': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.     def test_get_paginated_questions(self):
    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    #Create an endpoint to handle GET requests for all available categories. 
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    #Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    #Create an endpoint to DELETE question using a question ID. 
    def test_delete_question(self):
        res = self.client().post('/questions', json=self.new_question)
        q = Question.query.filter(Question.question=='Q24').all()
        res = self.client().delete('/questions/' + str(q[0].id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], q[0].id)

    #Create a POST endpoint to get questions based on category. 
    def test_questions_by_category(self):
        res = self.client().get('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 1)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    #Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
    def test_questions_by_term(self):
        res = self.client().post('/questions', json={'searchTerm':'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    #Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
    def test_play_quiz(self):
        res = self.client().post('/questions', json={'quiz_categorry':[]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    #Create error handlers for all expected errors including 400, 404, 422 and 500
    def test_error_400_bad_request(self):
        res = self.client().post('/questions', json={'searchTerm':''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_error_404_not_found(self):
        res = self.client().delete('/questions/99')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_error_422_unprocessable(self):
        res = self.client().post('/questions', json=self.wrong_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_error_500_internal_error(self):
        res = self.client().post('/quizzes', json='{"previous_questions":"","quiz_category":"2"}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal error')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()