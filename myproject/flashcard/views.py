from .utils import Flashcard
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FlashcardList
from .serializers import ListSerializer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@api_view(['GET'])
def getLists(request):
    lists = FlashcardList.objects.all()
    if request.method == 'GET':
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def getListDetail(request, pk):

    if request.method == 'GET':
        try: #kiểm tra word đã từng được tạo trước đây chưa
            obj = FlashcardList.objects.get(name=pk)
            print(obj, pk)
            #print(Flashcard(f'{pk}').getList())
            return Response({
                "words" : Flashcard(f'{pk}').getList(),
                "name": pk
            })
        except ObjectDoesNotExist: 
            return Response("")