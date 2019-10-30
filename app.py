from flask import (Flask, request, render_template, session, flash, redirect, url_for)

from flask_sqlalchemy import SQLAlchemy  # database
from passlib.hash import sha256_crypt  # password encryption
from datetime import timedelta
from flask_mail import Mail, Message  # to send email
from forms import (LoginForm, RegisterForm)  # , OTPForm)

app = Flask(__name__)
app.config.from_pyfile('app_config.py')
db = SQLAlchemy(app)

mail = Mail(app)


def get_session():
    return session


app.jinja_env.globals.update(get_session=get_session)


def sendMail(subject, message, recipients, message_on_true):
    try:
        with mail.connect() as conn:
            msg = Message(recipients=recipients,
                          body=message,
                          subject=subject)
            conn.send(msg)
        flash(message_on_true, 'success')
        return True
    except Exception as e:
        flash("Error Sending Email", 'danger')
        return False


# def addAdmin(id, password):
#     id = id.upper()
#     u = AdminModel(id,sha256_crypt.hash(password))
#     db.session.add(u)
#     db.session.commit()
#     print(f"Admin Added [ID : '{id}']")


@app.before_request
def make_session_permanent():
    # login session times out after 15 minutes of inactivity
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)


@app.route('/')
def index():  # landing page
    return render_template("layout.html")


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return redirect('/user/' + session['user'])
    elif 'admin' in session:
        return redirect('/admin')
    else:
        flash("Not Logged In", 'danger')
        print("Not Logged In")
        return redirect('/login')


@app.route('/user/<string:user_id>')
def logged_in_user(user_id):
    user_id = user_id.upper()
    if 'user' in session and session['user'] == user_id:
        rs = UserModel.query.filter_by(ID=user_id).first()

        favourite_events = str(rs.InterestedActivities).split(',')  # user's fav events
        favourite_events = favourite_events[:-1]  # as last event is always ''

        events = []
        for event in favourite_events:
            events.append(EventsModel.query.filter_by(ID=event).first())
        return render_template("panels/user/homepage.html", events=events)
    else:
        flash(f"User '{user_id}' Not Logged In", 'danger')
        print(f"User '{user_id}' Not Logged In")
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        id = str(form.user_id.data).strip().upper()
        password = str(form.password.data)

        if 'ADMIN' in id:  # admin login
            rs = AdminModel.query.filter_by(ID=id).first()  # rs is admin object

            if rs is not None:  # admin found

                if sha256_crypt.verify(password, rs.Password):  # password validate here
                    session.clear()

                    session['admin'] = id
                    session['name'] = rs.ID
                    flash(f"Successfully Logged In Admin '{rs.ID}'", 'success')
                    print(f"Successfully Logged In Admin '{rs.ID}'")
                    return redirect('/admin')
                else:
                    flash(f"Incorrect Password for '{rs.ID}'", 'danger')
                    print(f"Incorrect Password for '{rs.ID}'")

            else:
                flash(f"Admin '{id}' Not Found", 'danger')
                print(f"Admin '{id}' Not Found")

        else:  # user login
            rs = UserModel.query.filter_by(ID=id).first()  # rs is user object

            if rs is not None:  # user found

                if sha256_crypt.verify(password, rs.Password):  # password validate here
                    session.clear()

                    session['user'] = id
                    session['name'] = rs.Name
                    flash(f"Successfully Logged In User : {rs.Name}", 'success')
                    print(f"Successfully Logged In User : {rs.Name}")
                    return redirect('/user/' + id)
                else:
                    flash(f"Incorrect Password for '{rs.ID}'", 'danger')
                    print(f"Incorrect Password for '{rs.ID}'")
            else:
                flash(f"User with ID : '{id}' Not Found", 'danger')
                print(f"User with ID : '{id}' Not Found")
    return render_template("login-page.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        f_name = str(form.first_name.data).strip().title()
        l_name = str(form.last_name.data).strip().title()
        id = str(form.user_id.data).strip().upper()

        rs = db.session.query(UserModel.ID).all()
        rs = tuple(x[0] for x in rs)

        if id in rs:
            flash(f"User ID '{id}' is Already Registered", 'warning')
            print(f"User ID '{id}' is Already Registered")
        else:
            password = sha256_crypt.hash(str(form.password.data))

            u = UserModel(f"{f_name} {l_name}", id, password, '')
            db.session.add(u)
            db.session.commit()

            flash(f"Successfully Registered User '{f_name} {l_name}' [{id}]", 'success')
            print(f"Successfully Registered User '{f_name} {l_name}' [{id}]")
    return render_template("register-page.html", form=form)


@app.route('/logout')
def logout():
    if 'admin' in session:
        admin = session['name']
        session.clear()
        flash(f"Admin '{admin}' Logged Out Successfully", 'success')
        print(f"Admin '{admin}' Logged Out Successfully")
        del admin
    elif 'user' in session:
        user = session['name']
        session.clear()
        flash(f"User '{user}' Logged Out Successfully", 'success')
        print(f"User '{user}' Logged Out Successfully")
        del user
    else:
        flash("Not Logged In", 'warning')
        print("Not Logged In")
    return redirect('/login')


from views_events import *
from views_errors import *
from views_admin import *
from models import (UserModel, AdminModel, EventsModel)

if __name__ == '__main__':
    app.run()

# VERIFY USER EMAIL ID WITH OTP???
# otp = generate_otp()
#             email = id + '@bennett.edu.in'
#             values = {
#                 'subject': 'REGISTER NEW USER @UNSPAMMIFY',
#                 'message': 'Your OTP to register @unspammify is ' + otp,
#                 'message_on_true': f"An Email has been sent to '{email}' with an OTP",
#                 'recipients': [email]
#             }
#             if sendMail(**values):
#                 form_otp = OTPForm(request.form)
#                 if request.method == "POST" and form_otp.validate():
#                     user_entered_otp = str(form_otp.OTP.data).strip()
#                     print("userotp", user_entered_otp)
#                     if user_entered_otp == otp:
#                         # add user to database
#                         print("added to database")
#                         u = UserModel(f"{f_name} {l_name}", id, password, '')
#                         db.session.add(u)
#                         db.session.commit()
#
#                         flash(f"Successfully Registered User '{f_name} {l_name}' [{id}]", 'success')
#                         print(f"Successfully Registered User '{f_name} {l_name}' [{id}]")
#                     else:
#                         flash("Wrong OTP Entered !!", 'danger')
#                         print(f"Successfully Registered User '{f_name} {l_name}' [{id}]")
#                         return redirect('/register')
#
#                 return render_template("otp-verify.html", form=form_otp)
