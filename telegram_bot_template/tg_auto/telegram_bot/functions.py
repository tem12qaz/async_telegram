

class Function:
    def get_tg_id(message):
        text = [f'_txt_{message.chat.id}']
        value = {'content': text}
        print(value)
        return(value)
