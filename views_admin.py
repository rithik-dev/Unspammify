from app import (app, render_template, session, flash, redirect, sort_events)
from models import EventsModel

URL_PREFIX = '/admin'


@app.route(URL_PREFIX + '/')
def admin_panel():
    if 'admin' in session:
        return render_template("panels/admin/homepage.html"
                               , events=sort_events(EventsModel.query.all()))
    else:
        flash("Admin Not Logged In", 'danger')
        print("Admin Not Logged In")
        return redirect('/login')
