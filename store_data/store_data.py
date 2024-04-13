from app  import db,app,socketio
from models.user_db import UserRegister
from models.chat_db import FileStore,Chat_communication
import os,uuid
from flask_bcrypt import Bcrypt 
from pg_embedding.create_embedding import create_retrieve_database

bcrypt = Bcrypt(app) 

def store_user_data(name,username,email,password):
    try:
        if UserRegister.query.filter_by(username=username).first() :
            return 'Username already exists. Please choose a different username.', 'error'
        if UserRegister.query.filter_by(email=email).first() : 
            return 'Email already exists. Please choose a different email.', 'error'
        new_user = UserRegister(
                        name=name, 
                        username=username, 
                        email=email, 
                        password=bcrypt.generate_password_hash(password).decode('utf-8')
                    )
        db.session.add(new_user)
        db.session.commit()
        return "Register successfully","info"
    except Exception as e:
        return str(e),"error"
    
def store_file_data(file,id,collection_name):
    try:
        if FileStore.query.filter_by(document_name=file.filename).first():
            return "File Already Uploaded","error"
        if FileStore.query.filter_by(collection_name=collection_name).first():
            return "Dataset already exists","error"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) 
        file.save(file_path)
        collection_id=str(uuid.uuid4())
        new_file=FileStore(user_id=id,collection_name=collection_name.capitalize(),collection_id=collection_id,document_name=file.filename,document_file_path=file_path)
        db.session.add(new_file)
        db.session.commit()
        create_retrieve_database(file_path,collection_id)
        return "File upload successfully","info"
    except Exception as e:
        return str(e),"error"
    
def store_chat_data(payload,id):
    try:
        for msg in payload:
            new_msg=Chat_communication(user_id=id,
                                    role=msg['role'],
                                    chat_data=msg['content'])
            db.session.add(new_msg)
            db.session.commit()
    except Exception as e:
        print(f"ChatError: {e}")
    