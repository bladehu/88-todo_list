from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os
from datetime import datetime as dt
from forms import AddTaskForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///todolist.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Bootstrap(app)


class ToDoDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(2000), unique=False, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(2000), nullable=True)


db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    form = AddTaskForm()
    if form.validate_on_submit():
        new_task = ToDoDB(
            task=form.task.data,
            active=True,
            date=dt.now().strftime("%Y.%m.%d. %H:%M"),
            description=form.description.data
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    tasks = ToDoDB.query.all()

    return render_template("index.html", tasks=tasks, form=form)


@app.route("/delete/<int:task_id>", methods=["GET", "POST"])
def delete_task(task_id):
    task_to_delete = ToDoDB.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/finish/<int:task_id>", methods=["GET", "POST"])
def finish_task(task_id):
    task_to_finish = ToDoDB.query.get(task_id)
    task_to_finish.active = False
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete-all", methods=["GET", "POST"])
def delete_all_finished_tasks():
    tasks_to_delete = ToDoDB.query.filter_by(active=0).all()
    for task in tasks_to_delete:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
