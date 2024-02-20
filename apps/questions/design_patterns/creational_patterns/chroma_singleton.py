from django.conf import settings
import time

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb


__author__ = 'Ricardo'
__version__ = '0.1'


class ChromaSingleton():


    __client = None
    __embeddings = None


    @classmethod
    def __get_connection(cls, embedding_function):
        """
        This method create our client
        """

        client = chromadb.PersistentClient(path="chroma_db")
        #if not 'recursos_humanos' in client.get_collections():
        #    client.create_collection("recursos_humanos")
        client = Chroma(client=client, collection_name="recursos_humanos", embedding_function=embedding_function)

        return client


    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:

            # making connection
            cls.__embeddings = OpenAIEmbeddings()
            cls.__client = cls.__get_connection(cls.__embeddings)

        return cls.__client
    

    @classmethod
    async def create(cls):
        import pandas as pd
        df = pd.read_csv("datos_recursos_humanos.csv")

        texts = df["Pregunta"].to_list()
        titles = df["Respuesta"].to_list()
        docs = []

        for i, j in zip(texts, titles):
            docs.append(Document(page_content=i, metadata={"pregunta":i, "respuesta":j}))

        Chroma.from_documents(docs, collection_name="recursos_humanos", persist_directory="chroma_db", embedding=cls.__embeddings)
    

    @classmethod
    async def search_similarity_procedure(cls, text:str):
        """
        This method search the similarity in a text given inside Pinecone

        :param text: an string beging our text to query
        :return: a list with our documents 
        """

        docs = await cls.__client.asimilarity_search(text, k=10)
        
        return docs