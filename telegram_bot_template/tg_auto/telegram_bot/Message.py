import copy
import logging
from .database import Database
from .functions import Function

class Message:
    all = {}
    #_txt_ Текст _img_ Картинка _vid_ видео _doc_ Файл
    def __init__(self, id, default=None, func=None, answers={}, message=[]):
        self.id = id
        self.default = default
        self.func = func
        self.answers = answers
        self.message = message
        Message.all[id] = self

    def __str__(self):
        return (f'Message id{self.id}')

    async def load_all_messages_from_db():
        rows = tuple(await Database.get_all_messages())
        for row in rows:
            loaded_message = Message(*row)

        logging.info('All messages loaded successfully')

    def clear():
        Message.all = []

    def reload_all_messages():
        clear()
        load_all_messages_from_db()

    def get_next_or_def(self, answer):
        index_answer = self.answers.get(answer)
        if index_answer == None:

            default = Message.all.get(self.default)
            if default == None:
                raise IndexError(f'default Message id{self.id} ссылается на несуществующее\
                                сообщение id{self.default}\nИли нет ни одного сообщения')
            else:
                return default

        index_next = index_answer.get('next_message_id')
        if index_next == None:
            raise IndexError(f'Не указан id следующего сообщения в Answer {index_answer} in Message id{self.id}')

        next_message = Message.all.get(index_next)
        if next_message == None:
            raise IndexError(f'Message id{self.id} ссылается на несуществующее сообщение с индексом {index_next}')

        else:
            return next_message

    def execute_func_and_get_new(self, message):
        if self.func:
            new_attr = getattr(Function, f'{self.func}')(message)

            new_message = copy.copy(self)

            for i in new_attr:
                setattr(new_message, i, new_attr[i])

            return(new_message)
        return(self)
