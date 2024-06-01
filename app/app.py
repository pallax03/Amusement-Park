from os import environ
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from routes import routes
routes(app, db)

# from models import *
# from routes import *

# from . import create_app

# app = create_app()

# import routes

# from os import environ
# from flask import Flask, jsonify, make_response, request
# from flask_sqlalchemy import SQLAlchemy
# import pymysql

# # Initialize Flask application
# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
# app.config['SQLALCHEMY_ECHO'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# import models

# # db.create_all()

# # # Import routes (if any)
# # # import routes

# # @app.route('/test', methods=['GET'])
# # def test():
# #     return make_response(jsonify({'message': 'test visitor'}), 200)

# # @app.route('/visitors', methods=['POST'])
# # def create_visitor():
# #     try:
# #         data = request.get_json()
# #         visitor = Visitor(
# #             CodiceFiscale=data['CodiceFiscale'],
# #             Nome=data['Nome'],
# #             Cognome=data['Cognome'],
# #             DataDiNascita=data['DataDiNascita'],
# #             Altezza=data['Altezza'],
# #             Peso=data['Peso']
# #         )
# #         db.session.add(visitor)
# #         db.session.commit()
# #         return make_response(jsonify({'message': 'Visitor created'}), 201)
# #     except Exception as e:
# #         return make_response(jsonify({'error': str(e)}), 400)
    

# # @app.route('/visitors', methods=['GET'])
# # def get_visitors():
# #     try:
# #         visitors = Visitor.query.all()
# #         return make_response(jsonify([visitor.json() for visitor in visitors]), 200)
# #     except Exception as e:
# #         return make_response(jsonify({'error': str(e)}), 400)

# # @app.route('/visitors/<CodiceFiscale>', methods=['GET'])
# # def get_visitor(CodiceFiscale):
# #     try:
# #         visitor = Visitor.query.get(CodiceFiscale)
# #         if visitor:
# #             return make_response(jsonify(visitor.json()), 200)
# #         else:
# #             return make_response(jsonify({'message': 'Visitor not found'}), 404)
# #     except Exception as e:
# #         return make_response(jsonify({'error': str(e)}), 400)

# # @app.route('/visitors/<CodiceFiscale>', methods=['DELETE'])
# # def delete_visitor(CodiceFiscale):
# #     try:
# #         visitor = Visitor.query.get(CodiceFiscale)
# #         if visitor:
# #             db.session.delete(visitor)
# #             db.session.commit()
# #             return make_response(jsonify({'message': 'Visitor deleted'}), 200)
# #         else:
# #             return make_response(jsonify({'message': 'Visitor not found'}), 404)
# #     except Exception as e:
# #         return make_response(jsonify({'error': str(e)}), 400)


# @app.route('/')
# def index():
#     return str(db.session.execute('SELECT * FROM VISITATORI').fetchall())
#     # return render_template('index.html')

# # Add more routes as needed