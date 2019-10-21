from wtforms import Form, validators, StringField, PasswordField
from wtforms.fields.html5 import DateField


class LoginForm(Form):
    user_id = StringField(
        '', [validators.DataRequired()], render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.DataRequired()], render_kw={
                             'placeholder': 'Password'})


class RegisterForm(Form):
    first_name = StringField(
        '', [validators.DataRequired()], render_kw={'autofocus': True, 'placeholder': 'First Name'})
    last_name = StringField(
        '', [validators.DataRequired()], render_kw={'placeholder': 'Last Name'})
    user_id = StringField(
        '', [validators.DataRequired()], render_kw={'placeholder': 'University ID'})
    password = PasswordField('', [validators.DataRequired()], render_kw={'placeholder': 'Password'})


# class OTPForm(Form):
#     OTP = StringField('', [validators.DataRequired()], render_kw={'autofocus': True, 'placeholder': 'Enter OTP'})


class AddEvent(Form):
    date = DateField('', [validators.DataRequired()], render_kw={
            'autofocus': True, 'placeholder': 'Event Date ?'})
    venue = StringField('', [validators.DataRequired()], render_kw={
        'placeholder': 'Event Venue'})
    time = StringField('', [validators.DataRequired()],
                       render_kw={'placeholder': 'Event Time'})
    heading = StringField('', [validators.DataRequired()], render_kw={
        'placeholder': 'Event Heading'})
    description = StringField('', [validators.DataRequired()], render_kw={
            'placeholder': 'Event Description'})