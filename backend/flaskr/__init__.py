import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add(
            "Access-Control-Allow-Credentials", "true"
        )
        return response
    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.all()
        formatted_categories = {
            category.id: category.type for category in categories}
        return (
            {
                'success': True,
                'categories': formatted_categories,
                'number_of_categories_available': len(categories)
            }
        )

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()
        categories = Category.query.all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': {
                    category.id: category.type for category in categories},
                'current_category': "All"
            }
        )
    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question:

            try:
                question.delete()
                questions = Question.query.all()
                current_questions = paginate_questions(request, questions)
                return jsonify(
                    {
                        "success": True,
                        "deleted": question_id,
                        # "questions": current_questions,
                        # "total_questions": len(questions),
                    }
                ), 200
            except BaseException:
                abort(400)
        abort(404)

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        question_answer = body.get("answer", None)
        question_category = body.get("category", None)
        question_difficulty = body.get("difficulty", None)

        if new_question and question_answer and question_category and question_difficulty is not None:
            try:
                question = Question(
                    question=new_question,
                    answer=question_answer,
                    category=question_category,
                    difficulty=question_difficulty)
                question.insert()

                return jsonify({
                    'response': question.id,
                    'success': True
                })
            except BaseException:
                abort(400)
        else:
            abort(404)
    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        if search_term is not None:
            try:
                questions = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search_term))
                ).all()
                searched_questions = [question.format()
                                      for question in questions]
                return jsonify({
                    'success': True,
                    'questions': searched_questions,
                    'current_category': "All",
                    'total_questions': len(questions)
                })
            except BaseException:
                abort(400)
        else:
            abort(404)
    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):

        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]
        if questions:
            try:
                current_category = Category.query.get(category_id).format()

                return jsonify({
                    "questions": formatted_questions,
                    "total_questions": len(questions),
                    "current_category": current_category['type'],


                })
            except BaseException:
                abort(400)
        else:
            abort(404)

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def get_question_for_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        if quiz_category is not None or previous_questions is not None:

            try:
                if quiz_category['id'] == 0:
                    questions = Question.query.all()
                else:
                    questions = Question.query.filter(
                        Question.category == quiz_category['id']).all()

                formatted_questions = [question.format()
                                       for question in questions]

                question = random.choice(formatted_questions)

                while len(previous_questions) < len(formatted_questions):
                    if question['id'] not in previous_questions:
                        return jsonify({
                            'success': True,
                            'question': question
                        })
                    else:
                        question = random.choice(formatted_questions)

                else:
                    return jsonify({
                        'success': False})
            except BaseException:
                abort(400)
        else:
            abort(404)

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"}),
        422,

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"}),
        400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app
