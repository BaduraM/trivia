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
  
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_category(category_id):
    questions = Question.query.filter(Question.category==category_id)
    formatted_questions = [question.format() for question in questions]
    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': questions.count(),
      'current_category': category_id
    })

  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 9
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    categories = {}
    for qrow in Category.query.all():
      categories[qrow.id] = qrow.type
    return jsonify({
      'success': True,
      'total_questions': Question.query.count(),
      'questions': formatted_questions[start:end],
      'categories': categories,
      'current_category' : 1})

  @app.route('/categories')
  def get_categories():
    categories = {}
    for qrow in Category.query.all():
      categories[qrow.id] = qrow.type
    return jsonify({
      'success': True,
      'total_categories': Category.query.count(),
      'categories': categories
    })
  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    errnum = 0
    try:
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
          errnum = 404
        question.delete()
        return jsonify({
          'success': True,
          'deleted': question_id
        })
    except:
      if errnum > 0:
        abort(errnum)
      else:
        abort(400)
  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def search_questions():
    body = request.get_json()
    searchTerm = body.get('searchTerm', None)
    if searchTerm != None:
      if searchTerm == '':
        abort(400)
      questions = Question.query.filter(Question.question.like('%' + searchTerm + '%'))
      formatted_questions = [question.format() for question in questions]
      return jsonify({
        'success': True,
        'total_questions': questions.count(),
        'questions': formatted_questions,
        'current_category': 1
      })
    else:
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_difficulty = body.get('difficulty', None)
      new_category = body.get('category', None)

      try:
          question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
          question.insert()
          return jsonify({
            'success': True,
            'created': question.id
          })
      except:
        abort(422)


  '''
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/questions/<int:category_id>')
  def get_questions_by_category(category_id):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 9
    questions = Question.query.filter(Question.category==category_id)
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    return jsonify({
      'success': True,
      'current_category': category_id,
      'total_questions': questions.count(),
      'questions': formatted_questions[start:end],
      'categories': formatted_categories
    })

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz ():
    body = request.get_json()
    quiz_category = body.get('quiz_category', None)
    category_id = quiz_category.get('id', 1)
    previous = body.get('previous_questions', None)
    if previous == [] :
      questions = Question.query.filter(Question.category==category_id)
    else:
      questions = Question.query.filter(Question.category==category_id).filter(Question.id.notin_(previous))

    if questions.count() > 0 :
      sel = random.randint(0, questions.count() - 1)
      formatted_questions = questions[sel].format()
    else:
      formatted_questions = ''
    return jsonify({
      'success': True,
      'question': formatted_questions
    })
  
  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad request"
        }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method not allowed"
        }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable"
        }), 422

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal error"
        }), 500


  return app

    