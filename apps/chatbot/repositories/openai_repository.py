import json

from ..desing_patterns.creational_patterns.singleton.openai_singleton import OpenAISingleton 
    

__author__ = 'Ricardo'
__version__ = '0.1'


class OpenAIRepository():
    """
    This class send the data to the client
    """

    async def post_user_message(self, text, thread):
        
        # sending message
        response = await OpenAISingleton.add_message(text, thread)

        return response


    def post_create_thread(self):

        return OpenAISingleton.create_conversation_thread()
