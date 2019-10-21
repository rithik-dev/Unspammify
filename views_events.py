from app import (app, db, render_template, request, session, flash, redirect)
from forms import AddEvent
from models import EventsModel, UserModel
from random import randint  # generating random id for events
from datetime import datetime

URL_PREFIX = '/events'


def generate_random_id(length=6):
    generated_id = "".join([str(randint(1, 9)) for x in range(length)])

    rs = db.session.query(EventsModel.ID).all()
    rs = tuple(x[0] for x in rs)

    while generated_id in rs:
        generated_id = generate_random_id()

    return generated_id


@app.route(URL_PREFIX + '/')
def display_events():
    if 'user' in session or 'admin' in session:  # accessible only if user or admin is logged in
        return render_template("events/homepage.html",
                               events=EventsModel.query.order_by(EventsModel.EventDate).all())
    else:
        flash("Not Logged In", 'danger')
        print("Not Logged In")
        return redirect('/login')


# add new event
@app.route(URL_PREFIX + '/add', methods=['GET', 'POST'])
def add_new_event():
    if 'admin' in session:  # can only add event if any admin is logged in
        form = AddEvent(request.form)
        if request.method == "POST" and form.validate():
            date = datetime.strptime(str(form.date.data), '%Y-%m-%d').strftime('%d/%m/%Y')
            time = str(form.time.data).strip().upper()
            venue = str(form.venue.data).strip().upper()
            heading = str(form.heading.data).strip()
            description = str(form.description.data).strip()

            random_id = generate_random_id()

            # add event to database
            e = EventsModel(random_id, heading, description, date, time, venue)
            db.session.add(e)
            db.session.commit()

            flash(f"Event Added Successfully With ID : '{random_id}'", 'success')
            print(f"Event Added Successfully With ID : '{random_id}'")
    else:
        flash("Admin Not Logged In", 'danger')
        print("Admin Not Logged In")
        return redirect('/login')
    return render_template("events/add-event.html", form=form)


@app.route(URL_PREFIX + '/modify/<string:event_id>', methods=['GET', 'POST'])
def modify_event(event_id):
    if 'admin' in session:
        event = EventsModel.query.filter_by(ID=event_id).first()
        if event is None:  # if event does not exist
            flash(f"Event With ID : '{event_id}' Does Not Exist", 'danger')
            print(f"Event With ID : '{event_id}' Does Not Exist")
            return redirect('/admin')
        else:
            field_values = {
                'date': datetime.strptime(event.EventDate, '%d/%m/%Y').date(),
                'time': event.EventTime,
                'venue': event.EventVenue,
                'heading': event.EventHeading,
                'description': event.EventDescription
            }
            form = AddEvent(request.form, **field_values)  # form is same for add and modify
            if request.method == "POST" and form.validate():
                event.EventDate = datetime.strptime(str(form.date.data), '%Y-%m-%d').strftime('%d/%m/%Y')
                event.EventTime = str(form.time.data).strip().upper()
                event.EventVenue = str(form.venue.data).strip().upper()
                event.EventHeading = str(form.heading.data).strip()
                event.EventDescription = str(form.description.data).strip()

                db.session.commit()

                flash(f"Event With ID : '{event_id}' Modified Successfully", 'success')
                print(f"Event With ID : '{event_id}' Modified Successfully")
                return redirect('/admin')
    else:
        flash("Admin Not Logged In", 'danger')
        print("Admin Not Logged In")
        return redirect('/login')
    return render_template("events/modify-event.html", form=form)


# delete event
@app.route(URL_PREFIX + '/delete/<string:event_id>')
def delete_event(event_id):
    if 'admin' in session:
        # delete event
        e = EventsModel.query.filter_by(ID=event_id).first()
        db.session.delete(e)

        # delete event from user's favourite events
        rs = UserModel.query.all()
        for user in rs:
            if event_id in user.InterestedActivities:
                fav_events = user.InterestedActivities.replace(event_id + ',', '')
                user.InterestedActivities = fav_events

        # commit changes
        db.session.commit()

        flash(f"Event With ID : '{event_id}' Deleted Successfully", 'success')
        print(f"Event With ID : '{event_id}' Deleted Successfully")
        return redirect('/admin')
    else:
        flash("Admin Not Logged In", 'danger')
        print("Admin Not Logged In")
        return redirect('/login')


@app.route(URL_PREFIX + '/add-to-fav/<string:event_id>')
def add_event_to_favourites(event_id):
    if 'user' in session:
        rs = UserModel.query.filter_by(ID=session['user']).first()
        if event_id in rs.InterestedActivities:
            flash(f"Event With ID : '{event_id}' Already In {rs.Name}'s Favourites", 'warning')
            print(f"Event With ID : '{event_id}' Already In {rs.Name}'s Favourites")
        else:
            rs.InterestedActivities = rs.InterestedActivities + event_id + ','
            db.session.commit()
            flash(f"Event With ID : '{event_id}' Added To {rs.Name}'s Favourites", 'success')
            print(f"Event With ID : '{event_id}' Added To {rs.Name}'s Favourites")
        return redirect('/events')
    else:
        flash("User Not Logged In", 'danger')
        print("User Not Logged In")
        return redirect('/login')


@app.route(URL_PREFIX + '/remove-from-fav/<string:event_id>')
def remove_event_from_favourites(event_id):
    if 'user' in session:
        rs = UserModel.query.filter_by(ID=session['user']).first()
        if event_id in rs.InterestedActivities:
            rs.InterestedActivities = str(rs.InterestedActivities).replace(event_id + ',', '')
            db.session.commit()
            flash(f"Event With ID : '{event_id}' Removed From {rs.Name}'s Favourites", 'success')
            print(f"Event With ID : '{event_id}' Removed From {rs.Name}'s Favourites")
        else:
            flash(f"Event With ID : '{event_id}' Not in {rs.Name}'s Favourites", 'danger')
            print(f"Event With ID : '{event_id}' Not in {rs.Name}'s Favourites")
        return redirect('/user/' + session['user'])
    else:
        flash("User Not Logged In", 'danger')
        print("User Not Logged In")
        return redirect('/login')
