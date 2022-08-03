from my_app import db, login_manager
from my_app import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=40), nullable=False, unique=True)
    email=db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash=db.Column(db.String(length=60), nullable=False)
    target=db.Column(db.Integer(), nullable=False, default=0)          #one to many relationship
    trackers=db.relationship('Tracker',backref='owned_user', lazy=True)     #lazy=True it allows sqlalchemy to grab hold of all items in one shot
    log=db.relationship('Log')
    role=db.Column(db.String(), nullable=False, default='User')          #one to many relationship
    city=db.Column(db.String())
    phone_num=db.Column(db.Integer())
    social=db.Column(db.String())
    #add role ovwer here and can be assigned only in the backend 
    # one page which shows all the trackers and number of logs @app.route(/admin)
    @property
    def prettier_target(self):
        if len(str(self.target))>=4:
            return f'{str(self.target)[:-3]},{str(self.target)[-3:]} Cal'
        else:
            return f'{self.target} cal'

    @property
    def password(self):
        return self.password

    @password.setter
    def password (self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

class Tracker(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(length=40), nullable=False, unique=True)
    description=db.Column(db.String(length=1024))
    type=db.Column(db.String(length=40), nullable=False)
    owner=db.Column(db.Integer(), db.ForeignKey('user.id'))
    log=db.relationship('Log',cascade="all, delete")
    choices=db.Column(db.String()) #comma seperated values for the multiple choice 
    last_modified=db.Column(db.Integer())

    def __repr__(self):                     #used for debugging
        return f'Tracker : {self.name}'

class Log(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    value=db.Column(db.Integer())
    timestamp=db.Column(db.DateTime())
    note=db.Column(db.String())
    desc=db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.id',ondelete="CASCADE"))

