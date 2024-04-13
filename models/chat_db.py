
from app import db
import uuid
from datetime import datetime

class Chat_communication(db.Model):
    id = db.Column(db.String(120),default=lambda: str(uuid.uuid4()), primary_key=True)
    user_id = db.Column(db.String(120), db.ForeignKey('user_register.id'), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    chat_data = db.Column(db.TEXT, nullable=False)
    chat_index = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date_created = db.Column(db.Date, default=datetime.now().date())
    time_created = db.Column(db.Time, default=datetime.now().time())
    user = db.relationship('UserRegister', backref=db.backref('chats', lazy=True))
    
    def __repr__(self):
        return f"<Chat_communication {self.id}>"

    
class FileStore(db.Model):
    id = db.Column(db.String(120),default=lambda: str(uuid.uuid4()), primary_key=True)
    user_id = db.Column(db.String(120), db.ForeignKey('user_register.id'), nullable=False)
    collection_name=db.Column(db.String(255), nullable=False)
    collection_id=db.Column(db.String(150))
    document_name = db.Column(db.String(255), nullable=False)
    document_file_path = db.Column(db.String(255), nullable=False)
    user = db.relationship('UserRegister', backref=db.backref('file', lazy=True))
    
    def __repr__(self):
        return f"<FileStore {self.id}>"