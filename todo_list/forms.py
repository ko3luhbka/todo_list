from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import (
    DataRequired,
    Length,
)

class AddToDoTaskForm(FlaskForm):
    item = StringField(
        label='Task:',
        validators=[
            DataRequired(message='This field is required!'),
            Length(
                min=1,
                max=20,
                message='The field length should be from 1 to 20'
            )
        ]
    )
    
