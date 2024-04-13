from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from config.config_template import PGADMIN_URL

# from dotenv import load_dotenv
# from flask_mail import Mail

app = Flask(__name__)
app.secret_key="eMSk6t9FtLD64QSxGRDG"
app.config['SQLALCHEMY_DATABASE_URI'] = PGADMIN_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'files'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO()
socketio.init_app(app)
from models.user_db import UserRegister
from models.chat_db import Chat_communication,FileStore
from user.views import view_blueprint
app.register_blueprint(view_blueprint)


if __name__ == '__main__':
    socketio.run(app)





    