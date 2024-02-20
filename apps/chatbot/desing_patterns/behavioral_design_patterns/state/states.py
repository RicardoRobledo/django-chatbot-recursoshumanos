from django.conf import settings
from string import Template

import pandas as pd

from .base_state import BaseState
from ...creational_patterns.singleton.openai_singleton import OpenAISingleton
from ....repositories.openai_repository import OpenAIRepository
from .template_requests.templates import user_request_template


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['InitialState']


class InitialState(BaseState):
    """
    This class define the first state like greet
    """


    def __new__(cls, *args, **kwargs):
        cls.send_initial_context()
        return super().__new__(cls)


    @classmethod
    def send_initial_context(self):
        """
        This method send the texts and urls to beggining the context of the conversation
        """
        
        '''
        # reading csv
        path = f'{settings.PATH_CSV_FILE}urls.csv'
        df = pd.read_csv(path)

        # adding text
        string = 
        ########## Esta es un tabla de tramites o servicios ########## 
        
        |Index|Texts|
        |---|---|
        

        openai_repository = OpenAIRepository()

        for index, content in df.iterrows():
            
            new_string = f"|{index}|{content['Texts']}|"
            
            if OpenAISingleton.is_string_below_limit_token(string+new_string):
                string+=f'{new_string}'
            else:
                openai_repository.post_user_message({
                    'role':'user',
                    'content':string
                })
                string = new_string
        
        openai_repository.post_user_message({
            'role':'user',
            'content':string
        })

        print(openai_repository.post_retrieve_message())'''


    def send_message(self, array_chat_json):

        '''
        text = Template(user_request_template).substitute(prompt=array_chat_json['content'].split('.')[0])

        openai_repository = OpenAIRepository()

        array_chat_json = {
            'role':'user',
            'content':text
        }
        
        openai_repository.post_user_message(array_chat_json)
        msg = openai_repository.post_retrieve_message()

        print(msg)

        #OpenAISingleton.destroy_conversation_thread()

        client = OpenAISingleton()
        thread = OpenAISingleton.get_conversation_thread()

        msg = OpenAISingleton.add_message(array_chat_json)
        OpenAISingleton.run_thread()
        s = OpenAISingleton.retrieve_message()
        
        print()

        print(array_chat_json['content'].split('.')[0])
        OpenAISingleton.destroy_conversation_thread()'''


    def transition(self):
        return self
