from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/Onur/Desktop/Python/TodoApp/todo.db"
db = SQLAlchemy()
db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    complete = db.Column(db.Boolean, )

@app.route("/")
def index():
    todos = db.session.execute(db.select(Todo)).scalars()
    return render_template("index.html", todos = todos)


@app.route("/add", methods = ["POST"])
def addTodo():
    newTodo = Todo(title=request.form["title"], complete = False,)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/complete/<string:id>")
def complete(id):
    todo = db.session.execute(db.select(Todo).filter_by(id=id)).scalar_one()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def delete(id):
    deletetodo = db.session.execute(db.select(Todo).filter_by(id=id)).scalar_one()
    db.session.delete(deletetodo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)