from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.fields import IntegerField
from wtforms.widgets import NumberInput


class AddressForm(FlaskForm):
    address = StringField("Where are you now?", validators=[DataRequired()])
    number_of_locations = IntegerField(
        "How many locations would you like to visit?",
        widget=NumberInput(min=2, max=20, step=1),
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
