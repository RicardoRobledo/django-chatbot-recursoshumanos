from django.conf import settings
import time

from openai import OpenAI
import tiktoken
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.pydantic_v1 import BaseModel, Field

from .....questions.design_patterns.creational_patterns.chroma_singleton import ChromaSingleton
from ....utils.prompt_handlers.prompt_loader import load_prompt_file


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
    async def query_information_user(cls, username):
        """
        Get all information of a user given

        :param user: username of a user
        :return: a string being the answer
        """

        db = SQLDatabase.from_uri(f"sqlite:///{settings.DATABASES['default']['NAME']}")

        llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
        #chain = create_sql_query_chain(llm, db)
        #response = chain.invoke({"question": f'Dame toda la informacion del usuario con nombre {username}'})

        from langchain_community.agent_toolkits import create_sql_agent
        agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
        
        resp = await agent_executor.ainvoke(
            f'Dime informacion del usuario con nombre {username}, con informacion legible, si tiene fechas en un formato conviertelo en entendible'
        )

        return resp


    @classmethod
    def create_multi_query_questions(cls, question):
        """
        Get all information of a user given

        :param user: username of a user
        :return: a tuple with the query result and the query
        """

        prompt = load_prompt_file('apps/chatbot/prompts/prompt_multi_query_questions.txt')

        from langchain_core.output_parsers import StrOutputParser

        parser = StrOutputParser()

        chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        from langchain.prompts import ChatPromptTemplate

        prompt = ChatPromptTemplate.from_template(
            template=prompt
        )

        from langchain_core.runnables import RunnablePassthrough

        response = prompt | chat_model | parser
        
        response = response.invoke({'question':question})

        return response.split('\n')


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

        :param thread: an int that contain our thread identifier
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
