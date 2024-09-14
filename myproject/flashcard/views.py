from .utils import Flashcard, NonKanji
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FlashcardList, FlashcardWord
from .serializers import ListSerializer, WordSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status


# Create your views here.
@api_view(['GET'])
def getLists(request):
    lists = FlashcardList.objects.all().order_by('name')
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

@api_view(['POST'])
def createList(request):
    data = request.data
    name = data.get('name', '').strip()  # Lấy giá trị name từ request và loại bỏ khoảng trắng đầu và cuối
    
    # Kiểm tra xem tên đã tồn tại chưa
    existing_list = FlashcardList.objects.filter(name=name).first()
    
    if existing_list:
        # Nếu danh sách với tên đã tồn tại, trả về thông báo lỗi
        return Response({'error': 'Tên danh sách này đã tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Nếu danh sách chưa tồn tại, tạo mới và trả về thông tin danh sách mới
        new_list = FlashcardList.objects.create(name=name)
        serializer = ListSerializer(new_list)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def deleteList(request, pk):
    list = FlashcardList.objects.get(id=pk)
    list.delete()
    return Response('Word was deleted')

@api_view(['PUT'])
def updateList(request, pk):
    data = request.data
    print('request data: ', data)
    list = FlashcardList.objects.get(id=pk)
    serializer = ListSerializer(instance=list, data=data, partial=True)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        print('Data Saved Successfully')  # Thông báo khi lưu thành công
    else:
        print('Errors:', serializer.errors)  # In lỗi nếu dữ liệu không hợp lệ

    return Response(serializer.data)

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
def deleteWord(request):
    data = request.data
    wordId = data['wordId']
    listId = data['listId']
    
    try:
        word = FlashcardWord.objects.get(id=wordId)
        list = FlashcardList.objects.get(id=listId)

        # Xóa liên kết giữa từ và danh sách
        word.list.remove(list)

        # Kiểm tra nếu từ không còn liên kết với danh sách nào, thì xóa từ đó
        if word.list.count() == 0:
            word.delete()
            return Response({'success': 'Từ đã được xóa hoàn toàn.'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': 'Từ đã được xóa khỏi danh sách.'}, status=status.HTTP_200_OK)

    except FlashcardWord.DoesNotExist:
        return Response({'error': 'Từ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
    except FlashcardList.DoesNotExist:
        return Response({'error': 'Danh sách không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Có lỗi xảy ra: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def createWord(request):
    data = request.data
    print(data)
    try:
        list = FlashcardList.objects.get(id=data['listId'])
        existing_word = FlashcardWord.objects.filter(
            writing=data['w'],
            meaning=data['m'],
            furigana=data['p']
        ).first()

        print(existing_word)
        if existing_word:
            existing_word.list.add(list)
            serializer = WordSerializer(existing_word, many=False)
            return Response(serializer.data)
        else:
            print('case2')
            word = FlashcardWord.add(None, data['w'], data['m'], data['p'], list)
            Flashcard(f'{list.name}').findAndaddKanjiList(word)
            print('done')
            serializer = WordSerializer(word, many=False)
            return Response(serializer.data)
    except IntegrityError:
        # Trả về lỗi với mã lỗi và thông báo chi tiết
        return Response({'error': 'Từ mới đã tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        # Xử lý các lỗi khác
        return Response({'error': 'Có lỗi xảy ra khi thêm từ mới.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def addWord(request):
    try:
        data = request.data
        word_text = data['w']
        list_id = data['listId']
        
        word = NonKanji(word_text, 'javi', 'word')
        
        # Fetch the FlashcardList
        list = FlashcardList.objects.get(id=list_id)
        
        # Add word to Flashcard
        flashcard = Flashcard(f'{list.name}')
        flashcard.addNonKanji(word)
        
        return Response(status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)