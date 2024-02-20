from django.conf import settings
import json
from asgiref.sync import sync_to_async

from rest_framework.response import Response
from rest_framework.decorators import api_view
from adrf.decorators import api_view as async_api_view

from ..repositories.openai_repository import OpenAIRepository
from ..desing_patterns.creational_patterns.singleton.openai_singleton import OpenAISingleton
from ...questions.design_patterns.creational_patterns.chroma_singleton import ChromaSingleton
from ...questions.utils.prompt_handlers.prompt_recursos_humanos import format_prompt


@async_api_view(['POST'])
async def post_message(request):
    """
    This view post a message
    """

    # getting request data
    query_dict = request.data
    array_chat_str = query_dict.get('array_chat', '')
    thread_id = query_dict.get('thread_id', '')

    # become in json
    # {
    #    'role': 'user',
    #    'content': 'abc...'
    # }
    array_chat_json = json.loads(array_chat_str)


    # getting chunks in vectorial database
    ChromaSingleton()
    #await ChromaSingleton.create()
    docs = await ChromaSingleton.search_similarity_procedure(array_chat_json['content'])
    context = ''
    for i, doc in enumerate(docs, start=1):
        context += f"{i} - {doc.metadata['pregunta']}: {doc.metadata['respuesta']}\n"

    openai_repository = OpenAIRepository()
    msg = format_prompt(context, array_chat_json['content'])
    msg = await openai_repository.post_user_message(msg, thread_id)

    return Response({'msg':msg})


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
