from .utils import Flashcard
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FlashcardList, FlashcardWord
from .serializers import ListSerializer, WordSerializer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@api_view(['GET'])
def getLists(request):
    lists = FlashcardList.objects.all()
    serializer = ListSerializer(lists, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def getListDetail(request, pk):
    try: #kiểm tra word đã từng được tạo trước đây chưa
        obj = FlashcardList.objects.get(id=pk)
        print(obj, pk)
        #print(Flashcard(f'{pk}').getList())
        return Response({
            "words" : Flashcard(f'{obj.name}').getList(),
            "name": obj.name
        })
    except ObjectDoesNotExist: 
        return Response("")

from django.views.decorators.csrf import csrf_exempt

@api_view(['PUT'])
def updateWord(request, pk):
    data = request.data
    print('request data: ', data)
    word = FlashcardWord.objects.get(id=pk)
    serializer = WordSerializer(instance=word, data=data, partial=True)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        print('Data Saved Successfully')  # Thông báo khi lưu thành công
    else:
        print('Errors:', serializer.errors)  # In lỗi nếu dữ liệu không hợp lệ

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteWord(request, pk):
    word = FlashcardWord.objects.get(id=pk)
    word.delete()
    return Response('Word was deleted')