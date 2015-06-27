from server.models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    user_type = db.Column(db.SmallInteger)
    
    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)
        
    def __init__(self, name, password, email, user_type):
        self.name = name
        self.set_password(password)
        self.email = email
        self.user_type = user_type

