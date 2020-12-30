from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets


class AddressForm(FlaskForm):
    address = TextField("Where are you now?", validators=[DataRequired()])
    number_of_locations = h5fields.IntegerField(
        "How many locations would you like to visit?",
        widget=h5widgets.NumberInput(min=2, max=20, step=1),
        validators=[DataRequired()],
    )
    quadrant = SelectMultipleField(
        f"What quadrants are you interested in?",
        choices=[
            (v, v)
            for v in [
                "calgary-nw",
                "calgary-ne",
                "calgary-sw",
                "calgary-se",
                "surroundings",
            ]
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Feeling Lucky")
