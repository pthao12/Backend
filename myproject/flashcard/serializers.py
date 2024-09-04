from rest_framework.serializers import ModelSerializer
from .models import FlashcardList


class ListSerializer(ModelSerializer):
    class Meta:
        model = FlashcardList
        fields = '__all__'
