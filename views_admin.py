from app import (app, render_template, session, flash, redirect)
from models import EventsModel

URL_PREFIX = '/admin'


@app.route(URL_PREFIX + '/')
def admin_panel():
    if 'admin' in session:
        return render_template("panels/admin/homepage.html"
                               , events=EventsModel.query.order_by(EventsModel.EventDate).all())
    else:
        flash("Admin Not Logged In", 'danger')
        print("Admin Not Logged In")
        return redirect('/login')
