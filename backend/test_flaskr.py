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
        self.incomplete_question = {
            'question': '',
             'answer':'This is the answer',
             'category':3,
             'difficulty':3
             }
        self.search_term = {
            "searchTerm" : "title"
            }
        self.search_term2 = {
            "searchTerm" : "fresca"
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
    def test_get_all_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)

    def test_post_all_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method Not allowed')

    def test_get_paginated_page(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_get_non_existant_page(self):
        res = self.client().get('questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal server error')  

    
    """
    Make sure to change the id of the question in 'test_delete_question' before every test
    """
    def test_delete_question(self):
        res = self.client().delete("/questions/41")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
    def test_delete_non_existant_question(self):
        res = self.client().delete("/questions/100")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Internal server error")

    def test_post_new_question(self):    
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_incomplete_question(self):    
        res = self.client().post("/questions", json=self.incomplete_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Internal server error")

    def test_search_term(self):
        res = self.client().post("/questions", json=self.search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'], True)

    def test_non_existant_search_term(self):
        res = self.client().post("/questions", json=self.search_term2)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'], True)

    def test_get_questions_in_specific_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
    
    def test_get_questions_in_non_existant_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)  
        self.assertEqual(res.status_code,500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal server error')
    
    # def test_play_quiz(self):
    #     res = self.client().post("/quizzes", json={
    #         "previous_questions": [7],
    #         "quiz_category": 2
    #     })
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["question"])

    # def test_get_quiz_questions(self):
    #     res = self.client().get("/quizzes", json={
    #         "previous_questions": [7],
    #         "quiz_category": 2
    #     })
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 405)
    



    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()