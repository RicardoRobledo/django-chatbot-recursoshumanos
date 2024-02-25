from django.conf import settings
import json
from asgiref.sync import sync_to_async

from rest_framework.response import Response
from rest_framework.decorators import api_view
from adrf.decorators import api_view as async_api_view

from ..repositories.openai_repository import OpenAIRepository
from ..desing_patterns.creational_patterns.singleton.openai_singleton import OpenAISingleton
from ...questions.design_patterns.creational_patterns.chroma_singleton import ChromaSingleton


@async_api_view(['POST'])
async def post_message(request):
    """
    This view post a message
    """

    # getting request data
    query_dict = request.data
    user = query_dict.get('user', '')
    array_chat_str = query_dict.get('array_chat', '')
    thread_id = query_dict.get('thread_id', '')

    # become in json
    # {
    #    'role': 'user',
    #    'content': 'abc...'
    # }
    array_chat_json = json.loads(array_chat_str)

    # ---------------------------------------------------

    import os

    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = f"rh"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = "ls__cfc30df65ce74784bc9421eff0797c1b"  # Update to your API key


    OpenAISingleton()
    ChromaSingleton()
    #await ChromaSingleton.create()

    docs = await ChromaSingleton.search_similarity_procedure(array_chat_json['content'])

    text = ''
    for i in docs:
        text+=f'\n\n{i.page_content}'
    
    print(text)

    sql_response = await OpenAISingleton.query_information_user(user)

    """# ---------------------------------------------------

    multi_query_questions = OpenAISingleton.create_multi_query_questions(array_chat_json['content'])
    multi_query_questions.append(array_chat_json['content'])

    docs = await ChromaSingleton.multi_query_retriever(multi_query_questions)

    from langchain_community.document_transformers import (
        LongContextReorder,
    )

    reordering = LongContextReorder()
    docs = reordering.transform_documents(docs)

    context_retrieved = []
    for i in docs:
        context_retrieved.append(f'\n\n{i.page_content}')

    unique_docs = set(context_retrieved)

    context = ''
    for i in unique_docs:
        context+=i"""

    from ..utils.prompt_handlers.prompt_loader import load_prompt_file

    prompt = load_prompt_file('apps/questions/prompts/prompt_recursos_humanos.txt')

    from langchain.prompts import PromptTemplate
    text = PromptTemplate.from_template(prompt).format(
        information=sql_response['input'],
        context=text,
        question=array_chat_json['content']
    )

    openairep=OpenAIRepository()

    text = await openairep.post_user_message(text, thread_id)

    return Response({'msg':text})


@api_view(['POST'])
def post_clean(request):
    """
    This view close our connection
    """

    OpenAISingleton.close_connection(request.data.get('thread_id'))

    return Response({})


@api_view(['POST'])
def post_create_thread(request):
    """
    This view create a thread
    """

    OpenAISingleton()
    thread = OpenAIRepository().post_create_thread()

    return Response({'thread_id':thread.id})
