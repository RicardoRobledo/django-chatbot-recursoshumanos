from django.conf import settings
import time

from openai import OpenAI
import tiktoken
from langchain.agents.openai_assistant import OpenAIAssistantRunnable


__author__ = 'Ricardo'
__version__ = '0.1'


class OpenAISingleton():


    __client = None
    __assistant = None


    @classmethod
    def __get_connection(self):
        """
        This method create our client
        """
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY,)

        return client


    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:

            # making connection
            cls.__client = cls.__get_connection()
            cls.__assistant = OpenAIAssistantRunnable(assistant_id=settings.ASSISTANT_ID, as_agent=True)
        
        return cls.__client


    @classmethod
    def create_conversation_thread(cls):
        """
        Make up a thread converation
        """

        return cls.__client.beta.threads.create()


    @classmethod
    def get_conversation_thread(cls, thread_id):
        """
        Get a thread converation

        :param thread: and int that contain our thread identifier
        """

        return cls.__client.beta.threads.messages.list(thread_id)


    @classmethod
    async def add_message(cls, text, thread_id):
        """
        Put a message in our conversation thread

        :param thread: and int that contain our thread identifier
        """

        msg = await cls.__assistant.ainvoke({
            "content": text,
            "thread_id": thread_id
        })

        return msg.return_values["output"]


    @classmethod
    def retrieve_message(cls, thread_id):
        """
        Put a message in our conversation thread

        :param thread: and int that contain our thread identifier
        :return: a string that is our response in json
        """

        messages = cls.__client.beta.threads.messages.list(thread_id)
        message = messages.data[0].content[0].text.value

        #return message[8:len(message)-3]
        return message


    @classmethod
    def run_thread(cls, thread_id):
        """
        Run our thread

        :param thread: and int that contain our thread identifier
        :return: an execution thread
        """

        # creation execution thread
        run = cls.__client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=settings.ASSISTANT_ID
        )
        
        # verifying status of execution thread
        while run.status == "queued" or run.status == "in_progress":

            run = cls.__client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )

            time.sleep(0.5)

        return run
    

    @classmethod
    def get_num_tokens_from_string(cls, string):
        """
        Returns the number of tokens in a text string.
        
        :param string: text to check out
        :return: a integer that is the number of tokens
        """
        encoding = tiktoken.encoding_for_model(settings.ASSISTANT_MODEL)
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(string))
        return num_tokens
    

    @classmethod
    def is_string_below_limit_token(cls, string):
        """
        Returns if a string is below the token limit
        
        :param string: text to check out
        :return: a boolean that tell us if the number of tokens is greater than the token limit
        """

        return cls.get_num_tokens_from_string(string)<settings.TOKEN_LIMIT


    @classmethod
    def close_connection(cls, thread_id):
        """
        This method close our client connection and our thread

        :param thread: and int that contain our thread identifier
        """

        cls.__client.beta.threads.delete(thread_id)
        cls.__client = None
