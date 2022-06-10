from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    task = StringField(label="Task", validators=[DataRequired()])
    description = StringField(label="Description")
    submit = SubmitField("Add New Task")
