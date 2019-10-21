from app import db


class UserModel(db.Model):
    __tablename__ = 'users'
    Name = db.Column(db.String(255), nullable=False)
    ID = db.Column(db.String(15), nullable=False, primary_key=True)
    Password = db.Column(db.String(100), nullable=False)
    InterestedActivities = db.Column(db.Text, nullable=False, default='')

    def __init__(self, Name, ID, Password, InterestedActivities):
        self.Name = Name
        self.ID = ID
        self.Password = Password
        self.InterestedActivities = InterestedActivities


class AdminModel(db.Model):
    __tablename__ = 'admins'
    ID = db.Column(db.String(255), nullable=False , primary_key=True)
    Password = db.Column(db.String(100), nullable=False)

    def __init__(self, AdminID, Password):
        self.ID = AdminID
        self.Password = Password


class EventsModel(db.Model):
    __tablename__ = 'events'
    ID = db.Column(db.String(8), nullable=False, primary_key=True)
    EventHeading = db.Column(db.String(255), nullable=False)
    EventDescription = db.Column(db.Text, nullable=False)
    EventDate = db.Column(db.String(20), nullable=False)
    EventTime = db.Column(db.String(255), nullable=False)
    EventVenue = db.Column(db.String(255), nullable=False)

    def __init__(self, ID, EventHeading, EventDescription, EventDate, EventTime, EventVenue):
        self.ID = ID
        self.EventHeading = EventHeading
        self.EventDescription = EventDescription
        self.EventDate = EventDate
        self.EventTime = EventTime
        self.EventVenue = EventVenue
