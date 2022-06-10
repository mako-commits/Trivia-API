import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('student','student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'question': 'This is a new question',
             'answer':'This is the answer',
             'category':3,
             'difficulty':3
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
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)

    # def test_add_category(self):
    #     res = self.client().post("/categories", json={"type": "Anime"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["added"])
    #     self.assertTrue(len(data["categories"]))
    def test_405_get_all_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method Not allowed')
        
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_get_page(self):
        res = self.client().get('questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')  

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_add_new_question(self):    
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        # self.assertTrue(data["created"])
        # self.assertTrue(len(data["questions"]))
    
    # def test_405_if_question_creation_not_allowed(self):
    #     res = self.client().post("/questions/23", json={})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["Error"], False)
    #     self.assertEqual(data["message"], "Method Not Allowed")
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()