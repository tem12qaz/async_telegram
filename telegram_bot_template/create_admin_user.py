from tg_auto.flask_admin_panel.app import db
from tg_auto.flask_admin_panel.app import user_datastore

email = input('email: ')
password = input('password: ')


user_datastore.create_user(email=email, password=password)
db.session.commit()
print('ok')
