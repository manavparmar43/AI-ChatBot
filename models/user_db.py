
from app import db
import uuid
from datetime import datetime

class UserRegister(db.Model):
    id = db.Column(db.String(120),default=lambda: str(uuid.uuid4()), primary_key=True)
    name=db.Column(db.String(120),  nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password=db.Column(db.String(250),  nullable=False)
    created_by=db.Column(db.String(120),  nullable=False,default=datetime.now())
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    

    def __repr__(self):
        return f"<User {self.username}>"
    
    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True  

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    