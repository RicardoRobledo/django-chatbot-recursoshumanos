from .states import InitialState


__author__ = 'Ricardo'
__version__ = '0.1'


class ConversationFlow():
    """
    This class is define our conversation flow based in the behavioral design pattern 'state'
    """

    def __init__(self):
        self.__actual_state = InitialState()


    def send_message(self, array_chat_json):
        
        # send message
        msg = self.__actual_state.send_message(array_chat_json)
        
        # change state
        self.__actual_state = self.__actual_state.transition()
        
        return msg
