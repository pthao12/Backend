from rest_framework.serializers import ModelSerializer
from .models import FlashcardList, FlashcardWord


class ListSerializer(ModelSerializer):
    class Meta:
        model = FlashcardList
        fields = '__all__'

class WordSerializer(ModelSerializer):
    class Meta:
        model = FlashcardWord
        fields = ['meaning', 'furigana']