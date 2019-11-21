from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length

from todo_list.todo_task import TaskStatus

MIN_TASK_NAME_LENGTH = 1
MAX_TASK_NAME_LENGTH = 20


class AddToDoTaskForm(FlaskForm):
    """Form for adding new todo task"""

    task = StringField(label="Task:", validators=[
        DataRequired(message="This field is required!"),
        Length(
            min=MIN_TASK_NAME_LENGTH,
            max=MAX_TASK_NAME_LENGTH,
            message="The field length should be from {} to {}".format(
                MIN_TASK_NAME_LENGTH,
                MAX_TASK_NAME_LENGTH,
            ),
        ),
    ])


class UpdateStatusForm(FlaskForm):
    """Form for updating existing todo list task status"""

    status = SelectField(
        label="Status: ",
        choices=[(status.name, status.value) for status in TaskStatus],
    )
