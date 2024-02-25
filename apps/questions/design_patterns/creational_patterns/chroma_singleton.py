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
        import os

        documents = os.listdir('datos')

        docs = []

        from langchain.docstore.document import Document

        for i in documents:

            with open(f'datos/{i}', encoding='utf-8') as file:
                docs.append(
                    Document(page_content=str.join('', file.readlines()), metadata={'file':i})
                )

        from langchain.text_splitter import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1800,
            chunk_overlap=300,
            length_function=len,
            is_separator_regex=False,
        )

        splitter_docs = text_splitter.split_documents(docs)
        Chroma.from_documents(splitter_docs, collection_name="recursos_humanos", persist_directory="chroma_db", embedding=cls.__embeddings)
    

    @classmethod
    async def multi_query_retriever(cls, multi_query):
        """
        this method use Multi-Query Retriever method
        
        :param multi_query: list of questions
        :return: a list with documents
        """

        docs = []

        for query in multi_query:
            print(docs)
            docs+=await cls.search_similarity_procedure(query)

        return docs


    @classmethod
    async def search_similarity_procedure(cls, text:str):
        """
        This method search the similarity in a text given inside Pinecone

        :param text: an string beging our text to query
        :return: a list with our documents 
        """

        docs = await cls.__client.asimilarity_search(text, k=1)
        
        return docs
