from flask import redirect, url_for, request
from flask_security import current_user

from flask_admin import BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from .config import RELOAD_REQUEST_PATH
import requests


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class HomeAdminView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin_home.html')

class AdminView(AdminMixin, ModelView):
    pass

class MessageView(AdminMixin, ModelView):
    column_list = ('id', 'type', 'content')
    form_columns = ('type', 'content')

class AnswerView(AdminMixin, ModelView):
    column_list = ('id', 'text', 'button', 'next_message_block')
    form_columns = ('text', 'button', 'next_message_block')

class BlockView(AdminMixin, ModelView):
    column_list = ('id', 'from_answer','messages','answers','default', 'function_name')
    pass

class ReloadView(AdminMixin, BaseView):
    @expose('/')
    def reload_messages(self):
        response = requests.get(RELOAD_REQUEST_PATH)
        return response.text

class LogoutView(AdminMixin, BaseView):
    @expose('/')
    def logout_button(self):
        return redirect(url_for('security.logout', next='/'))
