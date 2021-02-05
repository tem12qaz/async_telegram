from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security

import requests
from .config import Configuration, RELOAD_REQUEST_PATH

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


#FLASK-ADMIN
from .models import Message, Answer, Block, Telegram_user, User, Role
from .views import HomeAdminView, AdminView, MessageView, AnswerView, BlockView, ReloadView, LogoutView

admin = Admin(app, 'Telegram Bot Admin', url='/', index_view=HomeAdminView(name='Documentation'))
admin.add_view(MessageView(Message, db.session))
admin.add_view(AnswerView(Answer, db.session))
admin.add_view(BlockView(Block, db.session))
admin.add_view(AdminView(Telegram_user, db.session))
admin.add_view(ReloadView(name='Reload Messages', endpoint='reload_messages'))
admin.add_view(LogoutView(name='Logout', endpoint='logout_redirect'))


#FLASK-SECURITY
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
