from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length

from todo_list.todo_task import TaskStatus


class AddToDoTaskForm(FlaskForm):
    """Form for adding new todo task"""

    task = StringField(
        label="Task:",
        validators=[
            DataRequired(message="This field is required!"),
            Length(
                min=1,
                max=20,
                message="The field length should be from 1 to 20",
            )
        ]
    )


class UpdateStatusForm(FlaskForm):
    """Form for updating existing todo list task status"""

    status = SelectField(
        label="Status: ",
        choices=[
            (status.name, status.value) for status in TaskStatus
        ],
    )
