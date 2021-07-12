from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flaskTodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# Routes
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    # if post req then add todo with form value
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # Add Todo
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    # Query to get all todo
    allTodo = Todo.query.all()

    # pass all Todos to index.html
    return render_template('index.html', allTodo=allTodo)

# Delete Todo


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Edit Todo


@app.route('/update/<int:sno>',  methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('edit.html', todo=todo)


# @app.route("/show")
# def show():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return "<p>Products Page</p>"


if __name__ == "__main__":
    app.run(debug=True)
