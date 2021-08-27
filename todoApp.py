# Imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


# create the app and make the necessary configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/todoApp_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create an instance SQLAlchemy class to manage our DataBase 
db = SQLAlchemy(app)


# define the model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    # string representation of the class
    def __repr__(self) -> str:
        return f"Todo {self.id}: {self.description}"

# create all the models
db.create_all()


# handle the root page i.e. default view
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


# handle the create page
@app.route('/todos/create', methods= ['POST'])
def create_todo():
    # collect the value from the json object we get as the request
    value = request.get_json()['description']
    # create a new record using this form value and insert that record into our databse
    newTodoItem = Todo(description = value)
    db.session.add(newTodoItem)
    db.session.commit()

    # return a json response for processing AJAX request on client side
    return jsonify({
        'description': newTodoItem.description
    })